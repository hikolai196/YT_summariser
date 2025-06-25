import os
import re
from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

from transcribe_tool import transcribe_youtube
from summarize_agent import summarize_transcript

# Tool Wrappers
@tool
def transcribe_tool(youtube_url: str) -> str:
    """Transcribes a YouTube video into text."""
    return transcribe_youtube.invoke(youtube_url)

@tool
def summarize_tool(transcript: str) -> str:
    """Summarizes a transcript into Markdown."""
    return summarize_transcript.invoke(transcript)

def define_tools():
    return [transcribe_tool, summarize_tool]


# AgentState
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# LLM setup
system_prompt = """
You are a helpful assistant.
- If the user provides a YouTube link, you should use the transcribe_tool and then summarize_tool.
- Otherwise, respond conversationally.
"""

llm = ChatOllama(model="llama3.2")
tools = define_tools()
tools_dict = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# Nodes definition
def call_llm(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=system_prompt)] + list(state['messages'])
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

def take_action(state: AgentState) -> AgentState:
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for call in tool_calls:
        tool_name = call['name']
        query = call['args'].get('youtube_url') or call['args'].get('transcript', '')

        print(f"Calling tool: {tool_name} with input: {query}")

        if tool_name not in tools_dict:
            print(f"Tool '{tool_name}' not found.")
            content = "Invalid tool call."
        else:
            content = tools_dict[tool_name].invoke(query)

        results.append(ToolMessage(tool_call_id=call['id'], name=tool_name, content=str(content)))

    return {'messages': results}

def should_continue(state: AgentState):
    last = state['messages'][-1]
    return hasattr(last, 'tool_calls') and len(last.tool_calls) > 0

# === Graph Setup ===
def build_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("llm", call_llm)
    graph.add_node("tool_use", take_action)
    
    graph.add_conditional_edges("llm", should_continue, {True: "tool_use", False: END})
    graph.add_edge("tool_use", "llm")
    graph.set_entry_point("llm")
    return graph.compile()


# Chat
def run_agent(agent):
    print("Chat Agent Ready. Type 'exit' to quit.")
    try:
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ["exit", "quit"]:
                break
            messages = [HumanMessage(content=query)]
            result = agent.invoke({"messages": messages})
            print("\n=== Agent ===")
            print(result['messages'][-1].content)
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    agent = build_agent_graph()
    run_agent(agent)
