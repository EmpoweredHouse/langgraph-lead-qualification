from dataclasses import dataclass, field
from typing import Annotated, Any, List, Optional
import operator

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


@dataclass(kw_only=True)
class InputState:
    """Input state defines the interface between the graph and the user (external API)."""

    icp: str
    "ICP provided by the user."

    company_webpage: str
    "Company website provided by the user."

    company_additional_data: dict[str, Any] = field(default_factory=dict)
    "Additional research company data, that can help to qualify the company."

    extraction_schema: dict[str, Any]
    "The json schema defines the information the agent is tasked with filling out."

    info: Optional[dict[str, Any]] = field(default=None)
    "The info state tracks the current extracted data for the given topic, conforming to the provided schema. This is primarily populated by the agent."



@dataclass(kw_only=True)
class OverallState:
    """Input state defines the interface between the graph and the user (external API)."""

    messages: Annotated[List[BaseMessage], add_messages] = field(default_factory=list)
    loop_step: Annotated[int, operator.add] = field(default=0)


@dataclass(kw_only=True)
class OutputState:
    """The response object for the end user."""

    info: dict[str, Any]
    """
    A dictionary containing the extracted and processed information
    based on the user's query and the graph's execution.
    This is the primary output of the enrichment process.
    """
