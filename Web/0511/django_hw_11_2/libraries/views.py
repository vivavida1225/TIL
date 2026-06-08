from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from .models import Book, Review
from .serializers import BookListSerializer, BookSerializer, ReviewSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
def book_detail(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        book.delete()
        data = {
            'delete': f'도서 고유 번호 {book.isbn}번의 {book.title}을 삭제하였습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def review_list(request):
    # 1. GET 요청 시 리뷰 전체 조회
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def review_create(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(book=book)
        data = {
            'message': f'''Your review data of [content: {serializer.data["content"]}, score: {serializer.data["score"]}] was successfully saved.'''
        }
        return Response(data, status=status.HTTP_201_CREATED)
    