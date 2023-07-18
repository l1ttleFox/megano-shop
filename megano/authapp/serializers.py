from rest_framework import serializers
from authapp.models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["src", "alt"]
        
        
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    avatar = AvatarSerializer()
    
    class Meta:
        model = Profile
        fields = ["fullname", "email", "phone", "avatar"]
        
    def get_email(self, obj):
        return obj.user.email
    
        