from dataclasses import dataclass, field
from typing import Annotated, Any, List, Optional
import operator

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

LEAD_QUALIFICATION_SIMPLE_SCHEMA = {
    "title": "LeadQualification",
    "description": "Basic lead qualification based on ICP and Buying Persona",
    "type": "object",
    "properties": {
        "lead_score": {
            "type": "integer",
            "description": "Numerical score assigned to the lead based on its fit with ICP and Buying Persona"
        },
        "score_reasoning": {
            "type": "string",
            "description": "Explanation of why the lead received this score, based on ICP and/or Buying Persona alignment"
        }
    },
    "required": ["lead_score", "score_reasoning"]
}



@dataclass(kw_only=True)
class InputState:
    """Input state defines the interface between the graph and the user (external API)."""

    company_research_data: dict[str, Any]
    "Additional research company data, that can help with the qualification process."

    icp: str
    "ICP (Ideal Customer Profile) provided by the user."

    buying_persona: Optional[str] = field(default=None)
    "The Buying Persona provided by the user."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: LEAD_QUALIFICATION_SIMPLE_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."


@dataclass(kw_only=True)
class OverallState:
    """Input state defines the interface between the graph and the user (external API)."""

    company_research_data: dict[str, Any]
    "Additional research company data, that can help with the qualification process."

    icp: str
    "ICP (Ideal Customer Profile) provided by the user."

    buying_persona: Optional[str] = field(default=None)
    "The Buying Persona provided by the user."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: LEAD_QUALIFICATION_SIMPLE_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."

    info: Optional[dict[str, Any]] = field(default=None)
    "The info state tracks the current extracted data for the given topic, conforming to the provided schema. This is primarily populated by the agent."

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
