from drf_yasg import openapi

create_post_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING, description='title (max 120 char)'),
            "body": openapi.Schema(type=openapi.TYPE_STRING, description='body'),
        }
    )
