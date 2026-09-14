from typing import TypedDict, Any, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    statement_id: str
    user_query: str
    messages: Annotated[list, add_messages]
    intent: str
    tool_results: list[Any]
    retrieved_context: list[str]
    requires_human: bool
    human_approval: bool
    final_answer: str