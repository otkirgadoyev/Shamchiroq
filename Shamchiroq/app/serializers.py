from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'voice')


class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        fields = ('name',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'end_date')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'price', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('id', 'user', 'text', 'link', 'is_file')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'username')

    def create(self, validated_data):
        user = User.objects.create(phone_number=validated_data['phone_number'],
                                   name=validated_data['name'],
                                   username=validated_data['username']
                                   )
        user.save()
        return user


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = ('verify_code', 'phone_number')


class CardNumberSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('card_number',)


class PaymentVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = ('verify_code',)


class SendChangePhoneNumberSerializer(serializers.ModelSerializer):
    voice = VoiceSerializer(many=True)

    def create(self, validated_data):
        voices = validated_data.pop('voice')
        verify = Verify.objects.create(**validated_data)
        for i in voices:
            Voice.objects.create(voice=verify, **voices)
            return verify

    class Meta:
        model = Verify
        fields = ('phone_number', 'verify_code', 'voice')
