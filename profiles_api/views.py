from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API View"""

    def get(self, request, fromat=None):
        """returns a list of APIView features"""
        an_apiview = [
            ' Uses HTTP methods as function (get ,pist, patch, put, delete)',
            'Is similiar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
