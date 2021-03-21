import json
from fastapi import FastAPI
from graphene import ObjectType, List, String, Schema, Field, Mutation

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


class CreateCourse(Mutation):
    course = Field(CourseType)

    class Arguments:
        id = String(required=True)
        title = String(required=True)
        instructor = String(required=True)

    async def mutate(self, info, id, title, instructor):
        with open("./courses.json", "r+") as courses:
            course_list = json.load(courses)
            course_list.append()
            courses.seek(0)
            json.dump(course_list, courses, indent=2)
        return CreateCourse(course=course_list[-1])


class Mutation(ObjectType):
    create_course = CreateCourse.Field()


app.add_route(
    "/graphql",
    GraphQLApp(
        schema=Schema(query=Query, mutation=Mutation), executor_class=AsyncioExecutor
    ),
)
