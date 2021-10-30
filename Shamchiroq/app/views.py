import uuid

from dj_rest_auth.app_settings import (
    JWTSerializer
)
from dj_rest_auth.utils import jwt_encode
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class Audiolist(APIView):

    def get(self, request):
        audio = Audio.objects.all()
        a = list(audio)
        audios = []
        if len(a) >= 5:
            for i in range(len(a) - 5, len(a)):
                audios.append(a[i])
        else:
            audios = a[::-1]
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)


class AudioDetail(APIView):

    def get_object(self, pk):

        try:
            return Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        audio = self.get_object(pk)
        serializer = AudioSerializer(audio)
        return Response(serializer.data)


class UserRegisterSerializerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.all()
        serializer = UserRegisterSerializer(user, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        request.data['username'] = str(uuid.uuid4().hex)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data['id']
            user_obj = User.objects.get(id=user_id)
            access_token, refresh_token = jwt_encode(user_obj)
            data = {
                'user': user_obj,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return Response(JWTSerializer(data, context=serializer).data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifySerializerView(APIView):
    @swagger_auto_schema(request_body=UserVerifySerializer)
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = UserVerifySerializer(data=request.data)
        if serializer.is_valid():
            user_verify = Verify.objects.filter(user__id=request.user.id).last()
            print(user_verify)
            if user_verify.verify_code == request.data['verify_code']:
                return Response({
                    "detail": "phone verification successfully completed"
                })
            else:
                return Response({
                    "detail": "Phone verification failed"
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceSendSerializerView(APIView):
    @swagger_auto_schema(request_body=PriceSerializer)
    def post(self, request, format=None):
        request.data['user'] = request.user.id
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendCardNumberSerializerView(APIView):
    @swagger_auto_schema(request_body=CardNumberSendSerializer)
    def post(self, request):
        try:
            card_number = request.data['card_number']
            request.user.card_number = card_number
            request.user.save()
            return Response({"detail": "success"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "error"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifySerializerView(APIView):
    def get(self, request):
        verify = Verify.objects.all()
        serializer = PaymentVerifySerializer(verify, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PaymentVerifySerializer)
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = PaymentVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = Verify.objects.filter(user__id=request.user.id).last()
            if user.verify_code == request.data['verify_code']:
                return Response({
                    'detail': 'Subscription has been successfully done'
                })
            else:
                return Response({
                    'detail': 'Subscription failed'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendChangePhoneNumberSerializerView(APIView):
    @swagger_auto_schema(request_body=SendChangePhoneNumberSerializer)
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = UserVerifySerializer(data=request.data)
        if serializer.is_valid():
            user_verify = Verify.objects.filter(user__id=request.user.id).last()

            if user_verify.verify_code == request.data['verify_code']:
                request.user.phone_number = request.data['phone_number']
                request.user.save()
                print(request.data['phone_number'])
                print(request.user.phone_number)
                return Response({
                    "detail": "Phone number successfully changed"
                })
            else:
                return Response({
                    "detail": "Phone number failed"
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
