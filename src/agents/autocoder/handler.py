from dhenara.agent.dsl import (
    FlowNodeTypeEnum,
    NodeInputRequiredEvent,
)
from dhenara.agent.utils.helpers.terminal import async_input, get_ai_model_node_input, get_folder_analyzer_node_input

from .flows.implementation import global_data_directory

async def node_input_event_handler(event: NodeInputRequiredEvent):
    node_input = None

    if event.node_type == FlowNodeTypeEnum.ai_model_call:
        if event.node_id == "code_generator": # NOTE: This is the node ID
            node_input = await get_ai_model_node_input(
                node_def_settings=event.node_def_settings,
            )
            #task_description= await async_input("Enter your query: ")
            #node_input.prompt_variables = {"task_description": task_description}

        event.input = node_input
        event.handled = True

    elif event.node_type == FlowNodeTypeEnum.folder_analyzer:
        if event.node_id == "dynamic_repo_analysis":
            node_input = await get_folder_analyzer_node_input(
                node_def_settings=event.node_def_settings,
                base_directory=global_data_directory,
                predefined_exclusion_patterns=[],
            )

        event.input = node_input
        event.handled = True