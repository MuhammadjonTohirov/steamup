from rest_framework.response import Response
from rest_framework import status

def api_response(data=None, error=None, code=None):
    """
    Create a standardized API response.
    
    Args:
        data: The data to return in the response
        error: Error message, if any
        code: HTTP status code
        
    Returns:
        A response object with the standardized structure
    """
    result = {
        "data": data,
        "error": error,
        "code": code or status.HTTP_200_OK
    }
    
    return result

class APIResponse(Response):
    """
    Custom Response class that wraps the response data in our standard format.
    """
    def __init__(self, data=None, error=None, code=None, **kwargs):
        if code is None:
            code = status.HTTP_200_OK
            
        response_data = api_response(data, error, code)
        super().__init__(data=response_data, status=code, **kwargs)