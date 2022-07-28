from djoser.serializers import UserCreateSerializer as BaseCreateUserSerializer

class UserCreateSerializer(BaseCreateUserSerializer):
    class Meta(BaseCreateUserSerializer.Meta):
        fields = ['id', 'username', 'password','email','first_name','last_name']