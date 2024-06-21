import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .filters import GetProfileWithSubIdFilterSet
from .permissons import Cheak, IsOwner
from .serializers import RegistrationSerializer, VerificationSerializer, ProfileSerializer, \
    LoginSerializer, ImageSerializer, VideoSerializer, FavoriteSerializer, UserSerializer, \
    GetProfileImagesAndFeedbackImagesSerializer
from .models import PhoneVerification, User, ProfileModel, ProfileVideoModel, ProfileImageModel, \
    FavoriteModel
from .utils import send_sms
from rest_framework.viewsets import ModelViewSet


class RegisterView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verification = PhoneVerification.objects.create(phone=phone)
            verification.generate_code()
            # send_sms(phone, f"Your verification code is {verification.code}")
            request.session['phone'] = phone
            request.session['lan'] = serializer.validated_data['lan']
            request.session['lat'] = serializer.validated_data['lat']
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            if get_user_model().objects.filter(phone=phone).exists():
                verification = PhoneVerification.objects.create(phone=phone)
                verification.generate_code()
                return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You have to register first'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                otp = PhoneVerification.objects.get(phone=phone, code=code, is_active=True)
                if otp.created_at >= timezone.now() - timedelta(minutes=2):
                    otp.is_active = False
                    otp.save()
                    lat = request.session.get('lat')
                    lan = request.session.get('lan')
                    try:
                        user = User.objects.create_user(phone=phone, lan=lan, lat=lat)
                    except:
                        return Response(data={"msg": "Already checked"}, status=status.HTTP_400_BAD_REQUEST)

                    refresh = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'Registration successful!'
                    }, status=status.HTTP_200_OK)
                else:
                    otp.is_active = False
                    otp.save()
                    return Response(data={"msg": "This code was used or invalid"})
            except PhoneVerification.DoesNotExist:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneTokenObtainView(CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                otp = PhoneVerification.objects.get(phone=phone, code=code, is_active=True)
                if otp.created_at >= timezone.now() - timedelta(minutes=2):
                    otp.is_active = False
                    otp.save()
                    user = User.objects.get(phone=phone)

                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    otp.is_active = False
                    otp.save()
                    return Response(data={"msg": "This code was used or invalid"})
            except (PhoneVerification.DoesNotExist, User.DoesNotExist):
                return Response({'error': 'Invalid phone number or verification code'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [Cheak, ]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        if ProfileModel.objects.filter(user_id=request.user).exists():
            return Response(data={'msg': 'You are already registered'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetMyProfileView(ListAPIView):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user_id=request.user.id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetProfileWithSubId(ListAPIView):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GetProfileWithSubIdFilterSet


class ImageViewSet(ModelViewSet):
    queryset = ProfileImageModel.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.filter_queryset(self.get_queryset().filter(user_id=request.user.id))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class VideoViewSet(ModelViewSet):
    queryset = ProfileVideoModel.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.filter_queryset(self.get_queryset().filter(user_id=request.user.id))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class FavoriteViewSet(ModelViewSet):
    queryset = FavoriteModel.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        if request.data.get('profile_id') == request.user.id:
            return Response(data={'msg': "error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner_id=ProfileModel.objects.get(id=self.request.user.id))


class GetProfileImagesAndFeedbackImagesView(RetrieveAPIView):
    queryset = ProfileModel.objects.all()
    serializer_class = GetProfileImagesAndFeedbackImagesSerializer


@swagger_auto_schema(tags=['Update admin'], method='patch')
@api_view(['PATCH'])
def update_user(request, pk):
    try:
        if request.user.is_superuser:
            try:
                user = get_user_model().objects.get(pk=pk)
            except:
                return Response(data={"msg": "User was not found"}, status=status.HTTP_404_NOT_FOUND)
            user.is_staff = not user.is_staff
            user.save()
            serializer = UserSerializer(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": "You don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(data={"msg": "International server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
