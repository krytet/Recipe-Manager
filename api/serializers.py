from rest_framework import serializers
from django.contrib.auth import get_user_model
from collections import OrderedDict

from api.models import Ingredient, Recipe, RecipeIngredient, Tag



User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, required=False)
    name = serializers.CharField(read_only=True, required=False)
    color = serializers.CharField(read_only=True, required=False)
    slug = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']



class Custom(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        #kwargs['read_only'] = True
        super().__init__(**kwargs)


    
class ShowRecipeSerelizer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingedients')
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(method_name='get_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(method_name='get_in_cart')

    class Meta:
        model = Recipe
        fields = '__all__'
    

    def get_favorited(self, obj):
        return True
    
    def get_in_cart(self, obj):
        return True



class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingedients')
    #author = serializers.SlugRelatedField(
    #    slug_field='username',
    #    read_only = True
    #tags = TagSerializer(many=True, read_only=True)
    #tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),many=True)
    #tags = serializers.ManyRelatedField( write_only=True, child_relation=TagSerializer)
    class Meta:
        fields = '__all__'
        model = Recipe
    
    def get_tags(self, obj):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(list(obj.tags.all()))
        tags = list(obj.tags.all())
        serializer = TagSerializer(tags, many=True)
        #print(serializer)
        print(serializer.data)
        return serializer.data



    def create(self, validated_data):
        print(validated_data)
        print(self.get_extra_kwargs())
        print(self.get_fields())
        print(self.get_validators())
        print(self.get_unique_together_validators())
        #Извличение ингридиетов и тегов из данных
        ingredients = validated_data.pop('recipe_ingedients')
        tags = validated_data.pop('tags')
        # Создание рецепта
        recipe = Recipe.objects.create(**validated_data)
        # Создание ингрединтов рецепта
        for ingredient in ingredients:
            print(dict(ingredient)['ingredient'])
            print(dict(ingredient)['amount'])
            currect_ingredient = Ingredient.objects.get(**(dict(ingredient)['ingredient']))
            print(currect_ingredient)
            RecipeIngredient.objects.create(
                ingredient=currect_ingredient,
                recipe = recipe,
                amount = dict(ingredient)['amount']
            )
        print(validated_data)
        # Указане тегов в рецепте
        for tag in tags:
            recipe.tags.add(tag)

        return recipe
        

    #def to_representation(self, recipe, instance):
    #    data = ShowRecipeSerelizer(data=recipe)
    #    print('!!!!!!!!!!!!!!!!!!!')
    #    print(data)
    #    serializer = ShowRecipeSerelizer(recipe, many=True)
    #    return serializer.data

    
    def to_representation(self, data):
        """
        Object data -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = ShowRecipeSerelizer(data)

        for field in fields:
            attribute = field.get_attribute(data)
            if attribute is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret
