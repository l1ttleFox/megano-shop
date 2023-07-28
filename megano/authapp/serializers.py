from rest_framework import serializers
from authapp.models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    """ Сериализатор модели аватара пользователя. """
    alt = serializers.ReadOnlyField(source="auto_alt")
    
    class Meta:
        model = Avatar
        fields = ["src", "alt"]
        
        
class ProfileSerializer(serializers.ModelSerializer):
    """ Сериализатор модели профиля пользователя. """
    
    email = serializers.SerializerMethodField()
    avatar = AvatarSerializer()
    
    class Meta:
        model = Profile
        fields = ["fullname", "email", "phone", "avatar"]
        
    def get_email(self, obj):
        """ Метод определения электронной почты пользователя вручную. """
        return obj.user.email
    
        