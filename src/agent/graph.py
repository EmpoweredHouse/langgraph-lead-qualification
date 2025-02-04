
import json
from typing import Any, Dict, List, Literal, Optional, cast

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

from agent import prompts
from agent.configuration import Configuration
from agent.state import InputState, OverallState, OutputState
from agent.tools import scrape_website, search
from agent.utils import init_model

async def call_agent_model(
    state: OverallState, 
    *, 
    config: Optional[RunnableConfig] = None
) -> Dict[str, Any]:
    """Call the primary Language Model (LLM) to decide on the next research action.

    This asynchronous function performs the following steps:
    1. Initializes configuration and sets up the 'Info' tool, which is the user-defined extraction schema.
    2. Prepares the prompt and message history for the LLM.
    3. Initializes and configures the LLM with available tools.
    4. Invokes the LLM and processes its response.
    5. Handles the LLM's decision to either continue research or submit final info.
    """
    # Load configuration from the provided RunnableConfig
    configuration = Configuration.from_runnable_config(config)

    # Define the 'Info' tool, which is the user-defined extraction schema
    info_tool = {
        "name": "Info",
        "description": "Call this when you have gathered all the relevant info",
        "parameters": state.extraction_schema,
    }

    # Format the prompt defined in prompts.py with the extraction schema and params
    p = configuration.prompt.format(
        extraction_schema=json.dumps(state.extraction_schema, indent=2), 
        company_research_data=json.dumps(state.company_research_data, indent=2),
        icp=state.icp,
        buying_persona=state.buying_persona
    )

    # Create the messages list with the formatted prompt and the previous messages
    messages = [HumanMessage(content=p)] + state.messages

    # Initialize the raw model with the provided configuration and bind the tools
    raw_model = init_model(config)
    model = raw_model.bind_tools([scrape_website, search, info_tool], tool_choice="any")
    response = cast(AIMessage, await model.ainvoke(messages))

    # Initialize info to None
    info = None

    # Check if the response has tool calls
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "Info":
                info = tool_call["args"]
                break
    if info is not None:
        # The agent is submitting their answer;
        # ensure it isn't erroneously attempting to simultaneously perform research
        response.tool_calls = [
            next(tc for tc in response.tool_calls if tc["name"] == "Info")
        ]
    
    response_messages: List[BaseMessage] = [response]
    
    if not response.tool_calls:  # If LLM didn't respect the tool_choice
        response_messages.append(
            HumanMessage(content="Please respond by calling one of the provided tools.")
        )

    return {
        "messages": response_messages,
        "info": info,
        "loop_step": 1 # Add 1 to the step count
    }


class InfoIsSatisfactory(BaseModel):
    """Validate whether the current extracted info is satisfactory and complete."""

    reason: List[str] = Field(
        description="First, provide reasoning for why this is either good or bad as a final result. Must include at least 3 reasons."
    )
    is_satisfactory: bool = Field(
        description="After providing your reasoning, provide a value indicating whether the result is satisfactory. If not, you will continue researching."
    )
    improvement_instructions: Optional[str] = Field(
        description="If the result is not satisfactory, provide clear and specific instructions on what needs to be improved or added to make the information satisfactory."
        " This should include details on missing information, areas that need more depth, or specific aspects to focus on in further research.",
        default=None,
    )


async def reflect(
    state: OverallState, 
    *, 
    config: Optional[RunnableConfig] = None
) -> Dict[str, Any]:
    """Validate the quality of the data enrichment agent's output.

    This asynchronous function performs the following steps:
    1. Prepares the initial prompt using the main prompt template.
    2. Constructs a message history for the model.
    3. Prepares a checker prompt to evaluate the presumed info.
    4. Initializes and configures a language model with structured output.
    5. Invokes the model to assess the quality of the gathered information.
    6. Processes the model's response and determines if the info is satisfactory.
    """
    # Prepare the main prompt
    p = prompts.MAIN_PROMPT.format(
        extraction_schema=json.dumps(state.extraction_schema, indent=2), 
        company_research_data=json.dumps(state.company_research_data, indent=2),
        icp=state.icp,
        buying_persona=state.buying_persona
    )
    
    # Validate the last message
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"{reflect.__name__} expects the last message in the state to be an AI message with tool calls. "
            f"Got: {type(last_message)}"
        )
    
    # Construct the message history
    messages = [HumanMessage(content=p)] + state.messages[:-1]

    # Prepare the checker prompt
    presumed_info = state.info
    checker_prompt = (
        "I am thinking of calling the info tool with the info below. "
        "Is this good? Give your reasoning as well. "
        "You can encourage the Assistant to look at specific URLs if that seems relevant, or do more searches. "
        "If you don't think it is good, you should be very specific about what could be improved.\n\n"
        "{presumed_info}"
    )

    # Format the checker prompt with the presumed information
    formatted_checker_prompt = checker_prompt.format(presumed_info=json.dumps(presumed_info or {}, indent=2))
    messages.append(HumanMessage(content=formatted_checker_prompt))

    # Initialize and invoke the model
    raw_model = init_model(config)
    bound_model = raw_model.with_structured_output(InfoIsSatisfactory)
    response = cast(InfoIsSatisfactory, await bound_model.ainvoke(messages))

    # Construct ToolMessage with content
    tool_message_content = "\n".join(response.reason) if response.is_satisfactory and presumed_info else f"Unsatisfactory response:\n{response.improvement_instructions}"
    
    # Create ToolMessage with the required 'content' argument
    tool_message = ToolMessage(
        tool_call_id=last_message.tool_calls[0]["id"],
        content=tool_message_content,  # Added the 'content' argument here
        name="Info",
        additional_kwargs={"artifact": response.model_dump()},
    )

    if response.is_satisfactory and presumed_info:
        tool_message.status = "success"
        return {"info": presumed_info, "messages": [tool_message]}

    # If unsatisfactory, return improvement instructions
    tool_message.status = "error"
    return {"messages": [tool_message]}


def route_after_agent(
    state: OverallState,
) -> Literal["reflect", "tools", "call_agent_model", END]:
    """Schedule the next node after the agent's action.

    This function determines the next step in the research process based on the
    last message in the state. It handles three main scenarios:

    1. Error recovery: If the last message is unexpectedly not an AIMessage.
    2. Info submission: If the agent has called the "Info" tool to submit findings.
    3. Continued research: If the agent has called any other tool.
    """
    last_message = state.messages[-1]

    # "If for some reason the last message is not an AIMessage (due to a bug or unexpected behavior elsewhere in the code),
    # it ensures the system doesn't crash but instead tries to recover by calling the agent model again.
    if not isinstance(last_message, AIMessage):
        return "call_agent_model"
    # If the "Into" tool was called, then the model provided its extraction output. Reflect on the result
    if last_message.tool_calls and last_message.tool_calls[0]["name"] == "Info":
        return "reflect"
    # The last message is a tool call that is not "Info" (extraction output)
    else:
        return "tools"


def route_after_checker(
    state: OverallState, 
    config: RunnableConfig
) -> Literal[END, "call_agent_model"]:
    """Schedule the next node after the checker's evaluation.

    Determines whether to continue the research process or end it
    based on the checker's evaluation and the current state of the research.
    """
    configurable = Configuration.from_runnable_config(config)
    last_message = state.messages[-1]

    # Check if the loop has reached its maximum step
    if state.loop_step >= configurable.max_loops:
        return END

    # If no information is available, call the agent model
    if not state.info:
        return "call_agent_model"

    # Ensure the last message is a ToolMessage and check its status
    if not isinstance(last_message, ToolMessage):
        raise ValueError(
            f"{route_after_checker.__name__} expected a ToolMessage. "
            f"Received: {type(last_message)}."
        )
    
    # If the last message has an error, call the agent model again
    if last_message.status == "error":
        return "call_agent_model"

    # If no issues, end the research process
    return END


# Create the graph
workflow = StateGraph(
    OverallState,
    input=InputState,
    output=OutputState,
    config_schema=Configuration,
)

workflow.add_node(call_agent_model)
workflow.add_node(reflect)
workflow.add_node("tools", ToolNode([search, scrape_website]))
workflow.add_edge(START, "call_agent_model")
workflow.add_conditional_edges("call_agent_model", route_after_agent)
workflow.add_edge("tools", "call_agent_model")
workflow.add_conditional_edges("reflect", route_after_checker)

graph = workflow.compile()


# from typing import Any, Dict

# from langchain_core.runnables import RunnableConfig
# from langgraph.graph import StateGraph
# from langgraph.graph import START, END, StateGraph

# from agent.configuration import Configuration
# from agent.state import InputState, OverallState, OutputState


# async def scrape_website(
#     state: OverallState,
#     config: RunnableConfig,
# ) -> Dict[str, Any]:
#     """Each node does work."""
#     configuration = Configuration.from_runnable_config(config)
#     # configuration = Configuration.from_runnable_config(config)
#     # You can use runtime configuration to alter the behavior of your
#     # graph.
#     return {
#         "changeme": "output from my_node. "
#         f"Configured with {configuration.my_configurable_param}"
#     }


# # Define a new graph
# builder = StateGraph(
#     OverallState,
#     input=InputState,
#     output=OutputState,
#     config_schema=Configuration,
# )

# # Add the node to the graph
# builder.add_node("scrape_website", scrape_website)

# # Set the entrypoint as `call_model`
# builder.add_edge(START, "my_node")

# # Compile the workflow into an executable graph
# graph = builder.compile()
# graph.name = "Company Qualifier"
