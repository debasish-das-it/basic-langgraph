from dotenv import load_dotenv
import truststore


from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph,END

from nodes import run_agent_reasoning, tool_node

load_dotenv()
# Inject system trust store (replaces certifi-win32, supports Python 3.14+)
truststore.inject_into_ssl()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    """Determines whether the agent should continue reasoning or end the flow."""
    last_message = state["messages"][LAST]
    if not last_message.tool_calls:
        return END
    return ACT

flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)

flow.add_conditional_edges(AGENT_REASON, should_continue, {ACT: ACT, END: END})

flow.add_edge(ACT, AGENT_REASON)

app  = flow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="flow.png")

def main():
    print("Hello from tavilysearch-reactagent-langgraph!")
    res= app.invoke({"messages":[HumanMessage(content="What is the temperature in Pune? List it and triple it.")]} )
    print(res["messages"][LAST].content)


if __name__ == "__main__":
    main()
