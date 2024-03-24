from .models import Post, Comment
from .serlializers import PostSerializer, CommentSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=401)


@api_view(["Get"])
def api_overview(request):
    api_urls = {
        'generate-token': 'generate-token/',

        # Posts
        'all Posts': '/post/all/',
        'Search by Post id': 'post/all/?id=id',
        'Add': 'post/create/',
        'Update': 'post/update/pk/',
        'Delete': 'post/pk/delete/',
        # Comments
        'all Comments': '/comment/all/',
        'Search by Comment id': '/comment/all/?id=id',
        'Add Comment': '/comment/create/',
        'Update Comment': '/comment/update/pk/',
        'Delete Comment': '/comment/pk/delete/'
    }
    return Response(api_urls)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
    post = PostSerializer(data=request.data)

    # validating for already existing data
    if Post.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if post.is_valid():
        post.save()
        return Response(post.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_post(request):
    # checking for the parameters from the URL
    if request.query_params:
        posts = Post.objects.filter(**request.query_params.dict())
    else:
        posts = Post.objects.all()

    # if there is something in posts else raise error
    if posts:
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    data = PostSerializer(instance=post, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request):
    comment = CommentSerializer(data=request.data)

    # validating for already existing data
    if Comment.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if comment.is_valid():
        comment.save()
        return Response(comment.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_comment(request):
    # checking for the parameters from the URL
    if request.query_params:
        comments = Comment.objects.filter(**request.query_params.dict())
    else:
        comments = Comment.objects.all()

    # if there is something in comments else raise error
    if comments:
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    data = CommentSerializer(instance=comment, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
