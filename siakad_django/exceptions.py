from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    if response.status_code == 401:
        response.data = {
            "message": "Authentication failed.",
            "is_success": False,
            "errors": {
                "non_field_errors": [
                    "Authentication credentials were not provided."
                ]
            },
        }

    return response