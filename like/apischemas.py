from drf_yasg import openapi

like_action_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "post": openapi.Schema(type=openapi.TYPE_STRING, description='Post id'),
        }
    )
