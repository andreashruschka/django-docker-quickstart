from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serlializers import PostSerializer, CommentSerializer
from rest_framework import serializers
from rest_framework import status


def index(request):
    return HttpResponse(Comment.objects.all().count())

@api_view(['GET'])
def delete_all(request):
    Comment.objects.all().delete()
    Post.objects.all().delete()
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["Get"])
def ApiOverview(request):
    api_urls = {
        # Posts
        'all Posts': '/post/all',
        'Search by Post id': 'post/?id=id',
        'Search by Post title': 'post/?title=title',
        'Add': 'post/create',
        'Update': 'post/update/pk',
        'Delete': 'post/pk/delete',
        # Comments
        'all Comments': '/comment/all',
        'Search by Comment id': '/comment/?id=id',
        'Search by Comment name': '/comment/?name=name',
        'Add Comment': '/comment/create',
        'Update Comment': '/comment/update/pk',
        'Delete Comment': '/comment/pk/delete'
    }
    return Response(api_urls)


@api_view(['POST'])
def add_post(request):
    post = PostSerializer(data=request.data)

    # validating for already existing data
    bob = request.data
    if Post.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if post.is_valid():
        post.save()
        return Response(post.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
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
def update_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    data = CommentSerializer(instance=comment, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
