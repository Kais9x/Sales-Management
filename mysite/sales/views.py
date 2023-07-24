import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import User, LoginUser, Commodities
import datetime
from django.contrib.auth.hashers import make_password, check_password
from .controllers import ChangeJWT, Create_Token, UUIDEncoder, UserController, CommoditiesController



# Create your views here.


def home(request):
    conUser = UserController()
    conCom = CommoditiesController()
    token = ChangeJWT(997746)
    commodities = Commodities.objects.all().order_by('-id')[:20]
    data_com = [conCom.getCommoditiesInfo(c) for c in commodities]

    response = render(request, "sales/home.html", {"data_com": data_com})
    response.set_cookie(key="Breaker", value=token)
    return response


def test(request):
    datetime_str = '09/19/22 13:55:26'

    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    # User.objects.create(name='phong pham', address='t3k5', birthday=datetime_object, status=0, type_user='re',
    #                           phone='0985166472')
    return render(request, "sales/test.html")


def login(request):
    # del request.session["user"]
    # del request.session["password"]
    token = 'abc'
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if data['status'] == 'login':
            user = LoginUser.objects.filter(account=data['user']).first()
            if user:
                if check_password(data["password"] + "H^LQ2ui$#C@!4$", user.password):
                    request.session["user"] = data["user"]
                    request.session["password"] = data["password"]
                    return JsonResponse({"msg": "Success 201!!!"}, status=201)

            return JsonResponse({"msg": "Incorrect password or account!!!"}, status=401)
        if data['status'] == 'register':
            if data["user"] != '':
                request.session["user"] = data["user"]
            if data["password"] != '':
                request.session["password"] = data["password"]
            return JsonResponse({"msg": "Success 201!!!"}, status=201)

        return JsonResponse({"msg": "Information is not accurate!!!"}, status=403)
    if "user" not in request.session or "password" not in request.session:
        token = ChangeJWT(997746)
    else:
        user = LoginUser.objects.filter(account=request.session["user"]).first()
        if user:
            if check_password(request.session["password"] + "H^LQ2ui$#C@!4$", user.password):
                if user.status == "user_active":
                    return redirect('home')
    response = render(request, "sales/login.html")
    response.set_cookie(key="Breaker", value=token)
    return response


def warehouses(request):
    token = ChangeJWT(997746)
    conUser = UserController()
    if "user" not in request.session or "password" not in request.session:
        return redirect('login')

    user = conUser.getUserbyEmail(request.session["user"])
    userInfo = conUser.getUserInfo(user)
    response = render(request, "sales/warehouses.html", {"user": json.dumps(userInfo, cls=UUIDEncoder)})
    response.set_cookie(key="Breaker", value=token)
    return response
