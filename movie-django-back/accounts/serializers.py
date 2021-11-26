from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'id')

class ProfileSerializer(serializers.ModelSerializer):
    def get_received(self, user):
        return user.followers.count()

    def get_sending(self, user):
        return user.hearts.count()

    hearts_received = serializers.SerializerMethodField("get_received")
    hearts_sending = serializers.SerializerMethodField("get_sending")
    
    class Meta:
        model = get_user_model()
        exclude = ('password',)

class IdentificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'id')
        

