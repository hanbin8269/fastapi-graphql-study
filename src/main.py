import json
from fastapi import FastAPI
from graphene import ObjectType, List, String, Schema, Field

from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from src.schemas import CourseType


class Query(ObjectType):
    course_list = None
    get_course = Field(List(CourseType), id=String())

    async def resolve_get_course(self, info, id=None):
        with open("./courses.json") as courses:
            course_list = json.load(courses)
        if id:
            for course in course_list:
                if course["id"] == id:
                    return [course]
        return course_list


app = FastAPI()
app.add_route(
    "/graphql", GraphQLApp(schema=Schema(query=Query), executor_class=AsyncioExecutor)
)
