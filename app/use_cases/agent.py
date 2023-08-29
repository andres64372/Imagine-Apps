from fastapi.responses import JSONResponse

from fastapi.responses import Response
from request_objects.agent import CreateAgentRequest
from repository.sql import DatabaseRepository
from domain.agents import Agent, Agents
from models.models import Agent as AgentModel

class GetAgentUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self):
        users = Agents(data=[
            Agent.model_validate(user)
            for user in self.__database_repo.get_agents()
        ])
        return JSONResponse(
            users.model_dump()
        )

class CreateAgentUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, request: CreateAgentRequest):
        agent = AgentModel(**request.model_dump())
        self.__database_repo.create_agent(agent)
        return Response(status_code=201)