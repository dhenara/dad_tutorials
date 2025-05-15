from dhenara.agent.dsl.inbuilt.flow_nodes.defs.types import (
    FileOperation,
    FileSystemAnalysisOperation,
    FolderAnalysisOperation,
)
from pydantic import BaseModel, Field


class TaskSpec(BaseModel):
    """
    Specification for a logical development task with its required context.
    Each task is a discrete unit of work in the overall plan.
    Represents a logical task of implementation with its required context and description.
    """

    order: int = Field(
        ...,
        description="Execution order of this task in the overall plan",
    )
    task_id: str = Field(
        ...,
        description="Unique identifier for this task using only lowercase letters, numbers, and underscores [a-z0-9_]",
        pattern="^[a-z0-9_]+$",
    )
    description: str = Field(
        ...,
        description=(
            "Precise and detailed description of what this task accomplishes in markdown format. "
            "This is send to an LLM as along with the context read with `required_context`, "
            "so this should be detailed enough for the LLM to do the task"
        ),
    )
    required_context: list[FileSystemAnalysisOperation] = Field(
        default_factory=list,
        description=(
            "List of specific file-system analysis operations needed to provide context for implementing this task."
        ),
    )


class TaskSpecWithFolderAnalysisOps(TaskSpec):
    """Task spec with FolderAnalysisOperation in required_context for more option in analysis"""

    required_context: list[FolderAnalysisOperation] = Field(
        default_factory=list,
        description=(
            "List of specific file-system analysis operations needed to provide context for implementing this task."
        ),
    )


class TaskImplementation(BaseModel):
    """
    Contains the concrete file operations to implement a specific task of the plan.
    This is the output generated after analyzing the context specified in the TaskSpec.
    """

    task_id: str | None = Field(
        default=None,
        description=("ID of the corresponding TaskSpec that this implements if it was given in the inputs"),
    )
    file_operations: list[FileOperation] | None = Field(
        default_factory=list,
        description="Ordered list of file operations to execute for this implementation task",
    )
    execution_commands: list[dict] | None = Field(
        None,
        description="Optional shell commands to run after file operations (e.g., for build or setup)",
    )
    verification_commands: list[dict] | None = Field(
        None,
        description="Optional commands to verify the changes work as expected",
    )
