from django.db import models


# Create your models here.

# 식재료 모델
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# # 레시피 모델
# # 1
# class Recipe(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     # 재료들 정보를 쉼표로 구분하여 저장
#     ingredients = models.CharField(
#         max_length=600,
#         blank=True,
#     )
#     def __str__(self):
#         return self.name


# 2
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
    )
    # Ingredient 클래스가 Recipe 클래스 이후에 정의 되었을 경우 다음과 같이 표기 가능
    # ingredients = models.ManyToManyField(
    #     'foods.Ingredient',
    #     related_name='recipes',
    # )

    def __str__(self):
        return self.name
