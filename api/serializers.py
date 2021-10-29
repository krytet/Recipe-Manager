from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from collections import OrderedDict
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from rest_framework.generics import get_object_or_404


from api.models import Ingredient, Recipe, RecipeIngredient, Tag




User = get_user_model()


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        print(data)
        print(email, password)

        user = get_object_or_404(User, email=email)
        if user.check_password(password):
            data['user'] = user
            return data
        else:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')





class TagSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(read_only=True, required=False)
    #name = serializers.CharField(read_only=True, required=False)
    #color = serializers.CharField(read_only=True, required=False)
    #slug = serializers.CharField(read_only=True, required=False)

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



class ShortShowReciprSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    
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


