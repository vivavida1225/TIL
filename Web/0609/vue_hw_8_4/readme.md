### backend에서 article.id 못 받아오던 문제 해결하기
```python
# serializers.py
class ArticleListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        # fields 에 'id' 추가
        fields = ('id', 'title', 'content')
```

### Create 함수 정의하기
```javascript
const createArticle = function () {
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/articles/',
    data: {
      title: title.value,
      content: content.value
    }
  })
  .then(() => {
    router.push({name: 'home'})
  })
  .catch(err => console.log(err))
}
```
