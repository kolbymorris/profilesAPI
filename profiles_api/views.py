from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

import json

import six
from cloudinary import api  # Only required for creating upload presets on the fly
from cloudinary.forms import cl_init_js_callbacks
from django.http import HttpResponse
from django.shortcuts import render

from .forms import PhotoForm, PhotoDirectForm, PhotoUnsignedDirectForm
from .models import Photo


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, fromat=None):
        """returns a list of APIView features"""
        an_apiview = [
            ' Uses HTTP methods as function (get ,pist, patch, put, delete)',
            'Is similiar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields =('name', 'email',)

"""This is where the beginning of cloudinary code starts"""
    def filter_nones(d):
        return dict((k, v) for k, v in six.iteritems(d) if v is not None)


    def list(request):
        defaults = dict(format="jpg", height=150, width=150)
        defaults["class"] = "thumbnail inline"

        # The different transformations to present
        samples = [
            dict(crop="fill", radius=10),
            dict(crop="scale"),
            dict(crop="fit", format="png"),
            dict(crop="thumb", gravity="face"),
            dict(format="png", angle=20, height=None, width=None, transformation=[
                dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
            ]),
        ]
        samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
        return render(request, 'list.html', dict(photos=Photo.objects.all(), samples=samples))


    def upload(request):
        unsigned = request.GET.get("unsigned") == "true"

        if (unsigned):
            # For the sake of simplicity of the sample site, we generate the preset on the fly.
            # It only needs to be created once, in advance.
            try:
                api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
            except api.NotFound:
                api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True,
                                         folder="preset_folder")

        direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
        context = dict(
            # Form demonstrating backend upload
            backend_form=PhotoForm(),
            # Form demonstrating direct upload
            direct_form=direct_form,
            # Should the upload form be unsigned
            unsigned=unsigned,
        )
        # When using direct upload - the following call is necessary to update the
        # form's callback url
        cl_init_js_callbacks(context['direct_form'], request)

        if request.method == 'POST':
            # Only backend upload should be posting here
            form = PhotoForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                # Uploads image and creates a model instance for it
                form.save()

        return render(request, 'upload.html', context)


    def direct_upload_complete(request):
        form = PhotoDirectForm(request.POST)
        if form.is_valid():
            # Create a model instance for uploaded image using the provided data
            form.save()
            ret = dict(photo_id=form.instance.id)
        else:
            ret = dict(errors=form.errors)

        return HttpResponse(json.dumps(ret), content_type='application/json')
        """Cloudinary code ends"""

        
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)


    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
