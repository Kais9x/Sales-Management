import hashlib
from django.urls import re_path
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .controllers import *
from .serializer import *
from .models import *
from .utils import err_msgs
from django.contrib.auth.hashers import make_password
from .controllers import User_Claims
import jwt

AUTHORIZATION_KEY = 'tuapo_api_v1_custom_key'  # TODO: change temp key


class EntityActions(generics.GenericAPIView):
    """
        CRUD actions for entities in this app.
    """
    api_view = ['GET', 'POST', 'PATCH', 'DELETE']

    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            # Comment check token
            if token is None:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            token = token.split('Bearer ')[1]
            decoded = self.CheckPermissions(token)
            payload = User_Claims()
            check = False
            self.CheckDeadline(decoded["exp"])
            for item in payload:
                if item["iss_id"] == decoded["iss_id"] and item["email"] == decoded["email"] and item["user_type"] == decoded[
                    "user_type"] and item["token"] == decoded["token"]:
                    check = True
            if check == False:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)

            params = request.get_full_path()
            index = params.find("?")
            queryset = self.get_queryset()
            if index > -1:
                params = params[index + 1:len(params)]
                params = params.split("&")
                for item in params:
                    if item.find("=") > -1:
                        filter_kwargs = item.split("=")
                        search_key = filter_kwargs[0]
                        search_value = filter_kwargs[1]
                        filter_kwargs = {
                            "{}".format(search_key): search_value
                        }
                        queryset = queryset.filter(**filter_kwargs).all()
            queryset = queryset.all()
            data = self.serializer_class(queryset, many=True).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            # Comment check token
            if token is None:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            token = token.split('Bearer ')[1]
            decoded = self.CheckPermissions(token)
            payload = User_Claims()
            check = False
            self.CheckDeadline(decoded["exp"])
            for item in payload:
                if item["iss_id"] == decoded["iss_id"] and item["email"] == decoded["email"] and item["user_type"] == \
                        decoded[
                            "user_type"] and item["token"] == decoded["token"]:
                    check = True
            if check == False:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            data = request.data
            if type(data) is list:
                for item in data:
                    data = self.transformData(item)
                    serializer = self.serializer_class(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                return Response("Post List: Success 201!!!", status=status.HTTP_201_CREATED)
            if type(data) is not dict:
                data = data.dict()
            data = self.transformData(data)
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            print(token)
            if token is None or hashlib.sha256(AUTHORIZATION_KEY.encode('utf-8')).hexdigest() != token.split('Bearer ')[
                1]:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            data = request.data
            if type(data) is list:
                for item in data:
                    target = self.search_multi(item)
                    if not target:
                        return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
                    data = self.transformData(item)
                    serializer = self.serializer_class(target, data=data, parital=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                return Response("Patch list: Success 200!!!", status=status.HTTP_200_OK)
            target = self.search(request)
            if not target:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            if type(data) is not dict:
                data = data.dict()

            # Custom data transformation for ForeignKey fields
            data = self.transformData(data)
            serializer = self.serializer_class(target, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if token is None or hashlib.sha256(AUTHORIZATION_KEY.encode('utf-8')).hexdigest() != token.split('Bearer ')[
                1]:
                return Response(err_msgs.INVALID_CRED, status=status.HTTP_400_BAD_REQUEST)
            data = request.data
            if type(data) is list:
                for item in data:
                    target = self.search_multi(item)
                    if not target:
                        return Response(err_msgs.OBJECT_NOT_EXISTS, status=status.HTTP_400_BAD_REQUEST)
                    target.delete()
                return Response("Delete List: Success 200!!!", status=status.HTTP_200_OK)

            target = self.search(request)
            if not target:
                return Response(err_msgs.OBJECT_NOT_EXISTS, status=status.HTTP_400_BAD_REQUEST)
            target.delete()
            return Response(err_msgs.OK, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def search(self, request):
        search_key = request.GET.get('search_key', None)
        if search_key is None:
            search_key = request.POST.get('search_key', None)
        if search_key is None:
            raise Exception(err_msgs.SEARCH_KEY_NOT_EXISTS)
        search_value = request.POST.get('search_value', None)
        if search_value is None:
            search_value = request.POST.get('search_value', None)
        if search_value is None:
            raise Exception(err_msgs.SEARCH_VALUE_NOT_EXISTS)
        filter_kwargs = {
            "{}".format(search_key): search_value
        }
        filter_kwargs = self.transformData(filter_kwargs)
        target = self.get_queryset().filter(**filter_kwargs).first()
        return target

    def search_multi(self, item):
        search_value = ""
        if "search_key" in item:
            search_key = item["search_key"]
            search_value = item["search_value"]
            filter_kwargs = {
                "{}".format(search_key): search_value
            }
            filter_kwargs = self.transformData(filter_kwargs)
            target = self.get_queryset().filter(**filter_kwargs).first()
            return target
        else:
            return False

    def transformData(self, data):
        if 'password' in data:
            data['password'] = make_password(data['password'] + "H^LQ2ui$#C@!4$")
        if 'user' in data:
            user_id = LoginUser.objects.filter(account=data["user"]).first()
            if not user_id:
                raise ValueError("User not exit!")
            data["user"] = user_id.id
        if "commodity_name_id" in data:
            commodity_name_id = Commodities.objects.filter(id=data["commodity_name_id"])
            if not commodity_name_id:
                raise ValueError("Commodities not exit!")
        return data

    def CheckPermissions(self, token):
        try:
            secret = 'T9cHUXgnETdWmpLshT6suomkiPyHknbHnUS5nURJhgU3s3moiS'

            algorithm = "HS256"
            decoded = jwt.decode(token, secret, algorithms=[algorithm])
            return decoded
        except Exception as e:
            print('Raise Error check permissions', str(e))

    def CheckDeadline(self, time):
        dt_object = datetime.datetime.fromtimestamp(time)
        time_now = datetime.datetime.now()
        if dt_object > time_now:
            return True
        return False


class UserActions(EntityActions):
    queryset = User.objects
    serializer_class = UserSerializer


class LoginUserActions(EntityActions):
    queryset = LoginUser.objects
    serializer_class = LoginUserSerializer


class PaysActions(EntityActions):
    queryset = Pays.objects
    serializer_class = PaysSerializer


class ShoppingCartActions(EntityActions):
    queryset = ShoppingCart.objects
    serializer_class = ShoppingCartSerializer


class CommoditiesActions(EntityActions):
    queryset = Commodities.objects
    serializer_class = CommoditiesSerializer


urlpatterns = [
    re_path(r"^account?$", LoginUserActions.as_view(), name="login_user"),
    re_path(r"^users?$", UserActions.as_view(), name="users"),
    re_path(r"^shopping?$", ShoppingCartActions.as_view(), name="shopping_cart"),
    re_path(r"^pays?$", PaysActions.as_view(), name="pays"),
    re_path(r"^commodities?$", CommoditiesActions.as_view(), name="commodities"),
]
