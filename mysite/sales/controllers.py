from copy import deepcopy
import hashlib, json
from re import I
from django.db.models.query import QuerySet
from .models import *
import jwt
from datetime import datetime, timedelta
from uuid import UUID

AUTHORIZATION_KEY = 'tuapo_api_v1_custom_key'  # TODO: change temp key


def User_Claims():
    """
        User information % Claims
    """
    # tạo mã token
    token = hashlib.sha256(AUTHORIZATION_KEY.encode('utf-8')).hexdigest()

    # Thời gian hết hạn của token
    expires_in = datetime.utcnow() + timedelta(hours=12)

    # Tạo các claims
    payload = [{
        "iss_id": 997746,  # ID của người tạo token
        "user_type": 'admin',  # Phân cấp token
        "email": 'phong02081995@gmail.com',  # Email của người tạo
        "token": token,
        "exp": expires_in
    }]
    return payload


def ChangeJWT(iss_id):
    payload = User_Claims()
    data = {}
    for item in payload:
        if item["iss_id"] == iss_id:
            data = item
    secret_key = "T9cHUXgnETdWmpLshT6suomkiPyHknbHnUS5nURJhgU3s3moiS"
    algorithm = "HS256"

    # Tạo JWT token
    jwt_token = jwt.encode(data, secret_key, algorithm=algorithm).decode("utf-8")

    # In ra JWT token
    return jwt_token


def Create_Token(iss_id, user_type, email):
    """
        User information % Claims
    """
    # tạo mã token
    token = hashlib.sha256(AUTHORIZATION_KEY.encode('utf-8')).hexdigest()

    # Thời gian hết hạn của token
    expires_in = datetime.utcnow() + timedelta(hours=12)

    # Tạo các claims
    payload = {
        "iss_id": iss_id,  # ID của người tạo token
        "user_type": user_type,  # Phân cấp token
        "email": email,  # Email của người tạo
        "token": token,
        "exp": expires_in
    }
    secret_key = "T9cHUXgnETdWmpLshT6suomkiPyHknbHnUS5nURJhgU3s3moiS"
    algorithm = "HS256"

    # Tạo JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm=algorithm).decode("utf-8")

    # In ra JWT token
    return jwt_token


def formatDate(date):
    if not date:
        return None
    return datetime.strftime(date, '%Y{0}%m{1}%d').format(*'--')


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class UserController:
    def getAllUsers(self):
        try:
            return User.objects.all()
        except Exception as e:
            print('Get User: ', e)
            return []

    def getUserbyEmail(self, email):
        try:
            return User.objects.filter(email=email).first()
        except Exception as e:
            print('Get user by email: ', e)
            return []

    def getUserInfo(self, user):
        try:
            if not user:
                raise ValueError('User not found')

            # parse info from model
            userInfo = deepcopy(user.__dict__)
            userInfo['email'] = user.email
            userInfo['name'] = user.name
            userInfo['user_id'] = user.user_id
            userInfo['birthday'] = formatDate(user.birthday)
            userInfo['address'] = user.address
            userInfo['status'] = user.status
            userInfo['type_user'] = user.type_user
            userInfo['phone'] = user.phone



            del userInfo['_state']
            del userInfo['created_at']
            del userInfo['updated_at']

            return userInfo

        except Exception as e:
            print('get user info: ', e)
            return []


class CommoditiesController:
    def getCommoditiesInfo(self, com):
        try:
            if not com:
                raise ValueError("Not commodities")
            com_info = deepcopy(com.__dict__)
            com_info["id"] = str(com.id).replace('-', '')
            com_info["commodity_name"] = com.commodity_name
            com_info["count"] = com.count
            com_info["price"] = com.price
            com_info["image_commodity"] = str(com.image_commodity)
            com_info["user_id"] = str(com.user_id).replace('-', '')
            com_info["remaining_amount"] = com.remaining_amount
            com_info["goods_type"] = com.goods_type
            com_info["trademark"] = com.trademark
            com_info["description"] = com.description

            del com_info["_state"]
            del com_info['created_at']
            del com_info['updated_at']

            return com_info
        except Exception as e:
            print('Get commodities info: ', str(e))
            return []