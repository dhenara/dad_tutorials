# ruff: noqa: E501
from dhenara.agent.dsl import (
    PLACEHOLDER,
    AIModelNode,
    AIModelNodeSettings,
    EventType,
    FileOperationNode,
    FileOperationNodeSettings,
    FlowDefinition,
    FolderAnalyzerNode,
    FolderAnalyzerSettings,
)
from dhenara.agent.dsl.inbuilt.flow_nodes.defs.types import FolderAnalysisOperation

from dhenara.ai.types import (
    AIModelCallConfig,
    ObjectTemplate,
    Prompt,
)

from src.agents.autocoder.types import TaskImplementation


# Parent of the repo where we analyse the folders
global_data_directory = "$var{run_root}/global_data"

# Create a FlowDefinition
implementation_flow = FlowDefinition()


# 1. Dynamic Folder Analysis
implementation_flow.node(
    "dynamic_repo_analysis",
    FolderAnalyzerNode(
        pre_events=[EventType.node_input_required],
        settings=None,
    ),
)

# 2. Code Generation Node
implementation_flow.node(
    "code_generator",
    AIModelNode(
        pre_events=[EventType.node_input_required],
        settings=AIModelNodeSettings(
            models=["claude-3-7-sonnet","o4-mini", "gemini-2.0-flash"],
            system_instructions=[
                # Role and Purpose
                "You are a professional code implementation agent specialized in executing precise file operations.",
                "Your task is to generate the exact file operations necessary to implement requested code changes - nothing more, nothing less.",
                "Generate machine-executable operations that require zero human intervention.",
                # Supported Operations
                "ALLOWED OPERATIONS:",
                "- create_file(file_path, content)",
                "- delete_file(file_path)",
                "- create_directory(directory_path)",
                # Prohibited Operations
                "PROHIBITED OPERATIONS (do not use):",
                "- edit_file",
                "- list_directory",
                "- search_files",
                "- get_file_metadata",
                "- list_allowed_directories",
                # Best Practices
                "IMPLEMENTATION GUIDELINES:",
                "1. For complete file replacement, use delete_file followed by create_file instead of a single edit_file.",
                "2. Maintain the project's existing code style, indentation, and formatting conventions.",
            ],
            prompt=Prompt.with_dad_text(
                text=(
                    "## Task Description\n"
                    "$var{task_description}"
                    "## Repository Context\n"
                    "$expr{$hier{dynamic_repo_analysis}.outcome.results}\n\n"
                    "## Implementation Requirements\n"
                    "1. Generate precise file operations that can be executed programmatically\n"
                    "2. Strictly follow instructions\n"
                    "3. Consider the entire context when making implementation decisions\n"
                    "## Output Format\n"
                    "Return a TaskImplementation object\n"
                ),
            ),
            model_call_config=AIModelCallConfig(
                structured_output=TaskImplementation,
                test_mode=False,
                max_output_tokens=64000,
                max_reasoning_tokens=4000,
                reasoning=True,
                timeout=1800.0,  # 30 minutes
            ),
        ),
    ),
)

# 3. File Operation Node
implementation_flow.node(
    "code_generator_file_ops",
    FileOperationNode(
        settings=FileOperationNodeSettings(
            base_directory=global_data_directory,
            operations_template=ObjectTemplate(
                expression="$expr{ $hier{code_generator}.outcome.structured.file_operations }",
            ),
            stage=True,
            commit=True,
            commit_message="$var{run_id}: Auto generated.",
        ),
    ),
)
