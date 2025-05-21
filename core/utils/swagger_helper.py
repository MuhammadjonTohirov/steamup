from drf_spectacular.utils import extend_schema, OpenApiExample
from functools import wraps

def api_schema(
    description = None, 
    request = None,  # For serializer
    request_data = None,  # For direct JSON schema
    request_examples = None,
    response_serializer = None,
    status_code = 200,
    success_data = None,
    tags = None
):
    """
    A universal decorator for standardized API responses.
    
    Args:
        description: API endpoint description
        request: Serializer class for request validation
        request_data: Dictionary defining JSON schema structure
        request_examples: List of dicts containing example request data
        response_serializer: Response serializer for success case
        status_code: Success status code (default 200)
        success_data: Example data to show in success response
        tags: List of tags for the endpoint
    """
    if request and request_data:
        raise ValueError("Cannot specify both 'request' and 'request_data'")

    # Default success data if none provided
    if success_data is None:
        success_data = {"message": "Operation successful"}
    
    # Create standard response example
    success_example = OpenApiExample(
        'Success Response',
        value={
            "data": success_data,
            "error": None,
            "code": status_code
        },
        response_only=True,
        status_codes=[str(status_code)]
    )
    
    # Create response mapping
    responses = {
        status_code: {
            "description": "Success response",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object"
                            },
                            "error": {
                                "type": "string",
                                "nullable": True
                            },
                            "code": {
                                "type": "integer",
                            }
                        },
                        "required": ["data", "code"]
                    }
                }
            }
        }
    }
    
    # Handle request schema
    request_schema = None
    request_examples_list = []

    if request_data:
        # Create schema from request_data
        request_schema = {
            "type": "object",
            "properties": {
                k: {"type": "string", "example": v} if isinstance(v, str) else v 
                for k, v in request_data.items()
            },
            "additionalProperties": False
        }
        
        # Add example from request_data
        request_examples_list.append(
            OpenApiExample(
                'Request Example',
                value=request_data,
                request_only=True
            )
        )
    elif request:
        request_schema = request

    # Add additional examples if provided
    if request_examples:
        for idx, example in enumerate(request_examples):
            request_examples_list.append(
                OpenApiExample(
                    f'Request Example {idx + 1}',
                    value=example,
                    request_only=True
                )
            )

    # Apply the decorator
    return extend_schema(
        description=description,
        request=request_schema,
        responses=responses,
        examples=[success_example] + request_examples_list,
        tags=tags
    )