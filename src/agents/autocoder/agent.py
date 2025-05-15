from dhenara.agent.dsl import AgentDefinition

from .flows.implementation import implementation_flow

agent = AgentDefinition()
agent.flow(
    "main_flow",
    implementation_flow,
)
