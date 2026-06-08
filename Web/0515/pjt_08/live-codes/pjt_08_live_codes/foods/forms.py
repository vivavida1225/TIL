from django import forms
from .models import Recipe, Ingredient


# # 1
# class RecipeForm(forms.ModelForm):
#     # 식재료 정보 입력 필드
#     ingredients = forms.MultipleChoiceField(
#         choices=[
#             ('TMT', '토마토'),
#             ('OLV', '올리브'),
#             ('PAS', '파스타'),
#         ],
#         widget=forms.CheckboxSelectMultiple,
#         help_text='요리 재료를 선택하세요.',
#     )

#     class Meta:
#         model = Recipe
#         fields = '__all__'


# 2
class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'ingredients',
        ]
