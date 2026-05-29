from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer, ArticleListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# 4. DRF의 view 함수는 @api_view 데코레이터가 **필수!**
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # 1. 전체 게시글 조회(DB)
        articles = Article.objects.all()
        # 그런데 articles 는 장고에서만 쓰는 QuerySet Type ->
        # -> 직렬화를 거쳐 유연한 타입으로 변환

        # 2. 직렬화
        # 원물 데이터가 단일 데이터가 아닌 형식이면 many 옵션을 True로
        serializer = ArticleListSerializer(articles, many=True)

        # 3. 직렬화된 데이터 덩어리에서 게시글 데이터만 추출해서 응답
        return Response(serializer.data)
    # 데이터 생성 관련 처리
    elif request.method == 'POST':
        # 1. 사용자가 보낸 데이터를 직렬화
        # 과거에는 request.POST 에서 추출했지만 DRF에서는 request.data 에서 추출
        serializer = ArticleSerializer(data=request.data)
        # 2. 유효성 검사
        if serializer.is_valid():
            # 3. 저장
            serializer.save()
            # 4. 저장 후 201 상태 코드를 응답
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 5. 실패 시에는 400 응답
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def article_detail(request, article_id):
    article = Article.objects.get(pk = article_id)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)