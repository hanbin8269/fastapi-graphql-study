from graphene import String, ObjectType


class CourseType(ObjectType):
    id = String(required=True)
    title = String(required=True)
    instructor = String(required=True)
    published_date = String()
