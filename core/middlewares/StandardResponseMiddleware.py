import json
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import get_language
from rest_framework.response import Response

from ..response import api_response

class StandardResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only process API responses that are not already in our format
        if request.path.startswith('/api/') and not request.path.startswith('/api/docs/') and not request.path.startswith('/api/schema/'):
            # Check if the response is a DRF Response object that hasn't already been processed
            if isinstance(response, Response):
                # Check if the request is an authentication request
                if request.path.startswith('/api/auth/'):
                    # For auth requests, we still want to add the language header
                    if 'Content-Language' not in response:
                        response['Content-Language'] = get_language() or 'en'
                    return response  # Don't wrap the response data in the standard format for authentication requests

                response_data = response.data
                
                # Check if the response is already in our format
                if not (isinstance(response_data, dict) and all(key in response_data for key in ['data', 'error', 'code'])):
                    # Wrap the response data in our standard format
                    response.data = api_response(
                        data=response_data,
                        error=None,
                        code=response.status_code
                    )
                    
                    # Update the response content
                    response.content = json.dumps(response.data)
                
                # Add language header to indicate which language was used
                if 'Content-Language' not in response:
                    response['Content-Language'] = get_language() or 'en'
        
        return response