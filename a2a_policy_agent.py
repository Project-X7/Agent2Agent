from dotenv import load_dotenv
import os
import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from a2a.utils import new_agent_text_message
from policy_agent import PolicyAgent

class PolicyAgentExecutor(AgentExecutor):
    def __init__(self) -> None:
        self.agent = PolicyAgent()
    async def execute(self, context: RequestContext, event_queue: EventQueue,) -> None:
        prompt = context.get_user_input()
        response = self.agent.answer_query(prompt)
        message = new_agent_text_message(response)
        await event_queue.enqueue_event(message)
    async def cancel(self, context: RequestContext, event_queue: EventQueue,) -> None:
        pass
    def main() -> None:
        print(f"Running A2A Health Insurance Policy Agent")
        load_dotenv(override=True)
        PORT = int(os.getenv("PORT", 8000))
        HOST = os.environ.get("HOST", "localhost")

        skill = AgentSkill(
            id="",
            name="",
            description="Answer insurance policy related queries based on the provided documents",
            tags=[],
            examples=[],
        )
        agent_card = AgentCard(
        name="InsurancePolicyCoverageAgent",
        description="Provides information about insurance policy coverage options and details.",
        url=f"http://{HOST}:{PORT}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

        request_handler = DefaultRequestHandler(agent_executor = PolicyAgentExecutor(),
            task_store=InMemoryTaskStore(),)

        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler,)

        uvicorn.run(server.build(), host=HOST, port=PORT)
    
    if __name__ == '__main__':
        main()
        