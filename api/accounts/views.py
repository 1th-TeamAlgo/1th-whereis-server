from django.shortcuts import render, redirect
import requests
import json
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter


def index(request):
    print("##### Func -> index #####")
    return render(request, 'index.html', {})


def oauth(request):
    print("##### Func -> oauth #####")
    access_token = request.META['HTTP_KAKAO_ACCESS_TOKEN']
    # code -> authorize_code
    print('code = ' + str(access_token))

    print("##### 사용자 정보 얻어 보기 #####")
    user_profile_info_uri = "https://kapi.kakao.com/v2/user/me"
    print(user_profile_info_uri)

    print("##### 사용자 정보 얻기 위햇 POST 날려봄 #####")
    user_profile_info_uri_data = requests.post(user_profile_info_uri,
                                               headers={'Authorization': f"Bearer ${access_token}"})
    user_json_data = user_profile_info_uri_data.json()


    kakao_account = user_json_data['kakao_account']
    nickname = kakao_account['profile']['nickname']
    email = kakao_account['email']
    birthday = kakao_account['birthday']

    data = {
        "nickname" : nickname,
        'email' : email,
        'birthday' : birthday
    }
    print(data)
    user_jwt = make_jwt(data)

    print(user_jwt)
    return redirect('https://www.naver.com/')

def make_jwt(data):
    return None

def kakao_login(request):
    print("##### Func -> kakao_login #####")
    # GET /oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code HTTP/1.1
    # Host: kauth.kakao.com

    host = "https://kauth.kakao.com"
    login_request_uri = host + "/oauth/authorize?"

    client_id = 'be8d497f71f0e2427a73ffe6a8b93b9d'
    redirect_uri = 'http://127.0.0.1:8000/oauth'

    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'

    print("##### login_request_uri #####")
    print(login_request_uri)
    return redirect(login_request_uri)


def kakao_logout(reuqest):
    return redirect("https://naver.com")
