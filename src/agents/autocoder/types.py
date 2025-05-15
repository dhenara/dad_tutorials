from dhenara.agent.dsl.inbuilt.flow_nodes.defs.types import FileOperation
from pydantic import BaseModel, Field

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
