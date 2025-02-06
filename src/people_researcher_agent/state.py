from dataclasses import dataclass, field
from typing import Any, Optional, Annotated
import operator

from pydantic import BaseModel

DEFAULT_EXTRACTION_SCHEMA = {
  "type": "object",
  "required": [
    "years_experience",
    "current_company",
    "role",
    "prior_companies",
    "internet_presence",
    "social_activity",
    "company_type",
    "company_arr"
  ],
  "properties": {
    "role": {
      "type": "string",
      "description": "Current role of the person."
    },
    "years_experience": {
      "type": "number",
      "description": "How many years of full-time work experience (excluding internships) this person has."
    },
    "current_company": {
      "type": "string",
      "description": "The name of the current company the person works at."
    },
    "prior_companies": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of previous companies where the person has worked."
    },
    "internet_presence": {
      "type": "string",
      "enum": ["high", "medium", "low", "uncertain"],
      "description": "A qualitative measure of the person's internet presence. 'High' means the person is well-documented online (e.g., multiple verified sources such as LinkedIn, company pages, articles). 'Medium' indicates moderate presence (e.g., LinkedIn but little else). 'Low' means minimal presence (e.g., a single email with no linked profiles). 'Uncertain' means there is not enough data to determine presence."
    },
    "social_activity": {
      "type": "string",
      "enum": ["active", "moderate", "inactive", "unknown"],
      "description": "Indicates how active the person is on professional or industry-related social media (LinkedIn, X, Bluesky). 'Active' means they post regularly, 'moderate' means they engage but post infrequently, 'inactive' means their profile exists but lacks activity, 'unknown' means no social media presence was found."
    },
    "company_type": {
      "type": "string",
      "enum": ["saas", "marketplace", "other", "unknown"],
      "description": "Classifies the current company as 'SaaS', 'Marketplace', or 'Other'. If the company type is unclear, it will be marked as 'Unknown'."
    },
    "company_arr": {
      "type": "string",
      "description": "Estimated Annual Recurring Revenue (ARR) of the company in USD. If no data is found, this field is empty."
    }
  },
  "description": "Person information",
  "title": "Person"
}

class Person(BaseModel):
    """A class representing a person to research."""

    name: Optional[str] = None
    """The name of the person."""
    company: Optional[str] = None
    """The current company of the person."""
    linkedin: Optional[str] = None
    """The Linkedin URL of the person."""
    email: Optional[str] = None
    """The email of the person."""
    role: Optional[str] = None
    """The current title of the person."""


@dataclass(kw_only=True)
class InputState:
    """Input state defines the interface between the graph and the user (external API)."""

    person: Person
    "Person to research."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."

    user_notes: Optional[dict[str, Any]] = field(default=None)
    "Any notes from the user to start the research process."


@dataclass(kw_only=True)
class OverallState:
    """Input state defines the interface between the graph and the user (external API)."""

    person: Person
    "Person to research provided by the user."

    extraction_schema: dict[str, Any] = field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA
    )
    "The json schema defines the information the agent is tasked with filling out."

    user_notes: str = field(default=None)
    "Any notes from the user to start the research process."

    search_queries: list[str] = field(default=None)
    "List of generated search queries to find relevant information"

    # Add default values for required fields
    completed_notes: Annotated[list, operator.add] = field(default_factory=list)
    "Notes from completed research related to the schema"

    info: dict[str, Any] = field(default=None)
    """
    A dictionary containing the extracted and processed information
    based on the user's query and the graph's execution.
    This is the primary output of the enrichment process.
    """

    is_satisfactory: bool = field(default=None)
    "True if all required fields are well populated, False otherwise"

    reflection_steps_taken: int = field(default=0)
    "Number of times the reflection node has been executed"


@dataclass(kw_only=True)
class OutputState:
    """The response object for the end user.

    This class defines the structure of the output that will be provided
    to the user after the graph's execution is complete.
    """

    info: dict[str, Any]
    """
    A dictionary containing the extracted and processed information
    based on the user's query and the graph's execution.
    This is the primary output of the enrichment process.
    """
