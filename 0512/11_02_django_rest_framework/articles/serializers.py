from pyexpat import model

from rest_framework import serializers
from sqlparse.filters import SerializerUnicode
from .models import Article, Comment


# 단일 게시글 데이터(단일 인스턴스)를 직렬화 하는 도구
# 그러면 ArticleListSerializer를 단일 게시글에서는 못쓰나요? ==> NO
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


# 전체 게시글 데이터(쿼리셋)를 직렬화 하는 도구
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)

class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id', 'title',)
    
    # 기존 읽기전용 필드인 article 필드을 위 도구의 결과값으로 재정의
    # 기존 필드를 재정의 할때는 Meta 클래스에서 작성했던 read_only_fields 가 먹히지 않음
    # 다른 방법으로 읽기 전용 필드로 설정
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ('article',)