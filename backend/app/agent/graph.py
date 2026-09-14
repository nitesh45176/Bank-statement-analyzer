from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

from app.agent.state import AgentState
from app.agent.tools import (
    get_account_details,
    get_transactions,
    calculate_spending,
    calculate_income,
    get_category_summary,
    get_monthly_summary,
    search_statement,
)


tools = [
    get_account_details,
    get_transactions,
    calculate_spending,
    calculate_income,
    get_category_summary,
    get_monthly_summary,
    search_statement,
]


load_dotenv()


llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=700
)

llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState):
    messages = state.get("messages", [])

    system_message = SystemMessage(
    content="""
You are Cashora AI, a financial intelligence assistant for Indian bank statements.

You have access to deterministic tools and a statement search tool.

Rules:

1. ALWAYS use a tool for financial calculations.
2. NEVER calculate totals yourself.
3. ALWAYS use the provided statement_id when calling tools.
4. NEVER invent, guess, or fabricate financial information or transactions.
5. Use INR (₹) for monetary values.
6. For total spending, total income, monthly totals, and category
   summaries, use the appropriate calculation/summary tool.
7. Use search_statement ONLY when the user asks about a specific
   transaction, merchant, narration, reference, or other statement
   detail that requires semantic search.
8. Keep responses concise and factual.
9. Return only the information needed to answer the user's question.
10. Do not repeat large transaction lists unless explicitly requested.

Zero-Result Handling (CRITICAL):
11. When a tool returns `found: false` or an empty list `[]`, this is a VALID
    result — NOT an error. Gracefully explain that no matching transactions
    were found. Example: "I couldn't find any Zomato transactions in this
    statement." or "There are no Netflix transactions recorded here."
12. NEVER treat an empty search result as an application error or system failure.
13. NEVER suggest the user try again or that something went wrong when a
    merchant or category simply has zero transactions in the statement.
14. If asked about spending for a merchant with zero matches, clearly state
    the spending was ₹0 (not found) rather than making up any amount.
"""
)

    recent_messages = messages[-6:]

    response = llm_with_tools.invoke(
        [system_message] + recent_messages
    )

    return {"messages": [response]}


tool_node = ToolNode(tools)


graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
)

graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()