import json
from django.http import Http404, HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Task, UserProfile
from .serializer import RegisterSerializer, LoginSerializer, LogoutSerializer, UpdateUserSerializer, PasswordSerializer, \
    TaskSerializer, CustomUserSerializer, AllTaskSerializer, UserProfileSerializer, GetUserProfileSerializer
from .pagination import CustomPageNumberPageination
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


def current_user(request):
    serializer = CustomUserSerializer(request.user)
    user = request.user
    user_id = user.id
    if user_id == serializer.data['id']:
        return user_id
    else:
        return None

class CustomUserView(APIView):        #class member details view here(Read Only.)
    parser_classes = [JSONParser]
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        _info = CustomUser.objects.order_by("name")
        serializer = CustomUserSerializer(_info, many=True)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

class PasswordView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordSerializer

class DeleteUserView(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

class Profile(viewsets.ModelViewSet):
    serializer_class = GetUserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        user_data = current_user(self.request)
        return self.queryset.filter(profile_id=user_data) #self.request.user

    def create(self, request, *args, **kwargs):
        user_data = current_user(request)
        if user_data:
            image = self.request.data
            p=UserProfile.objects.create(profile_id=user_data, avatar=image['avatar'])
            print(p)
            res= {
                "avatar": 'avatar',
                "Message":  "Created Succeessfully"
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response("errors please calm to check", status=status.HTTP_400_BAD_REQUEST)


class TaskListView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Add id of currently logged user
        user_data = current_user(request)
        if user_data:
            info = Task.objects.filter(user_id=user_data)
            print("89797h", info)
            serializer = AllTaskSerializer(info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_data = current_user(request)
        request.data["user"] = user_data
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res= {
                "Title": serializer.data['title'],
                "Description": serializer.data['description'],
                "Completed": serializer.data['completed']
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        # Returns an object instance that should
        # be used for detail views.
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_data = current_user(request)
        task = self.get_object(pk)
        valid_serializer = TaskSerializer(task)
        if user_data == valid_serializer.data['user']:
            serializer = AllTaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response("NO Task details please Give a Valid ID ", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user_data = current_user(request)
        request.data["user"] = user_data
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res= {
                "Title": serializer.data['title'],
                "Description": serializer.data['description'],
                "Completed": serializer.data['completed']
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CompletedTask(APIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            # Add id of currently logged user
            user_data = current_user(request)
            if user_data:
                info = Task.objects.filter(user_id=user_data, completed=True)
                print("completed=True", info)
                serializer = AllTaskSerializer(info, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Please check there is no task", status=status.HTTP_400_BAD_REQUEST)


class PaginatedTask(generics.ListAPIView):
    pagination_class = CustomPageNumberPageination
    permission_classes = (IsAuthenticated,)
    serializer_class = AllTaskSerializer

    def get_queryset(self):
        # Add id of currently logged user
        serializer = CustomUserSerializer(self.request.user)
        user = self.request.user
        if user.id == serializer.data['id']:
            task_data = Task.objects.filter(user_id=user.id)
            return task_data


