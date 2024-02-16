import time
import requests
import json
import string
import random
import cv2
import os
import math
import pymysql
import boto3
import uuid
import inspect
from django.db.models import Count
from collections import Counter
from .forms import *
from .models import *
from PIL import Image
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict
from datetime import datetime, timedelta, date, timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from bson import json_util
from dateutil.relativedelta import relativedelta
# from django.fcm.models import FCMDevice
# from firebase_admin.messaging import Message, Notification
from pyfcm import FCMNotification
from twilio.rest import Client

serverURL = ""
bucketName = ""
s3PATH = ""



def print_line_number():
    frame = inspect.currentframe()
    line_number = frame.f_lineno
    print("Current line number:", line_number)



@csrf_exempt
def index(request):
    try:
        # data = json.loads(request.body.decode("utf-8"))
        # loginUserPK = data['loginUserPK']
        loginUserPK = "1"
        videoinfo = Video.objects.all().order_by('?')
        videoinfoList = []
        for index, i in enumerate(videoinfo):
            userPK = i.userPK
            videoPK = i.id
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = i.videoPATH
            videoPATH = serverURL+"/static/video"+videoPATH
            contents = i.contents
            hashTag = i.hashTag
            viewable = i.viewable
            likeCount = 0
            comentCount = 0
            userLikeCheck = ""
            userComentCheck = ""

            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = str(like_video_infoCount)

            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"

            coment_infoCount = Coment.objects.filter(videoPK = videoPK).count()
            comentCount = str(coment_infoCount)

            coment_infoCount_user = Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if coment_infoCount_user == 0:
                userComentCheck = "0"
            else:
                userComentCheck = "1"
                
            dictinfo = {
                'videoPK':str(videoPK), 
                'userPK':userPK, 
                'username':username, 
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'viewable':viewable,
                'likeCount':likeCount,
                'comentCount':comentCount,
                'userLikeCheck':userLikeCheck,
                'userComentCheck':userComentCheck
            }
            videoinfoList.append(dictinfo)

        text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        # context = {'code':'1', 'videoinfoList':videoinfoList}
        # return HttpResponse(json.dumps(context))
        
        return render(request, 'index.html', {'videoinfo':videoinfoList})
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"index Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return render(request, 'index.html',context)
    
proxy_dict = {
	"http"  : ""
}
push_service = FCMNotification(api_key="", proxy_dict=proxy_dict)


# 배너 정보
@csrf_exempt
def mainBanner(request):
    try:

        banner_MnginfoCount = Banner_Mng.objects.filter(useYn = "Y").count()
        if banner_MnginfoCount == 0:
            text = "배너 정보 없음"
            ment = "\033[92m"+"mainBanner SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))     

        else:
            banner_Mnginfo = Banner_Mng.objects.filter(useYn = "Y")
            bannerList = []
            for index, i in enumerate(banner_Mnginfo):
                itemPK = i.id
                imgPath = i.imgPath
                content = i.content
                reward = i.reward

                dictinfo = {'itemPK':itemPK, 'imgPath':imgPath, 'content':content, 'reward':reward}
                bannerList.append(dictinfo)
            text = "배너 정보 호출"
            ment = "\033[92m"+"mainBanner SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'bannerList':bannerList}
            return HttpResponse(json.dumps(context))     

  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"mainBanner Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 앱 시작시 버전 체크
@csrf_exempt
def appVersionCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        platform = data['platform']
        versioninfo = Version.objects.get(id = 1)
        if platform == "Android":
            version = versioninfo.aos
            reviewVer_aos = versioninfo.aos_review
            text = "Android 버전 확인"
            ment = "\033[92m"+"appVersionCheck SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'version':version, 'reviewVer_aos':reviewVer_aos, 'reviewVer_ios':None}
            return HttpResponse(json.dumps(context))
        elif platform == "iOS":
            version = versioninfo.ios
            reviewVer_ios = versioninfo.ios_review
            text = "IOS 버전 확인"
            ment = "\033[92m"+"appVersionCheck SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'version':version, 'reviewVer_aos':None, 'reviewVer_ios':reviewVer_ios}
            return HttpResponse(json.dumps(context))
        else:
            version = versioninfo.aos
            reviewVer_aos = versioninfo.aos_review
            reviewVer_ios = versioninfo.ios_review
            text = "임시로 안드버전 체크"
            ment = "\033[92m"+"appVersionCheck SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'version':version, 'reviewVer_aos':reviewVer_aos, 'reviewVer_ios':reviewVer_ios}
            return HttpResponse(json.dumps(context))     

  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"signup_CIDICheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 메시지 전송
@csrf_exempt
def phoneAuthCode(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        phone = data['phone']
        # phone = request.POST.get('phone')
        print("phone >>", phone)


        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)

        authCode = str(random.randint(100000, 999999))
        
        message = client.messages.create(
            body="인증 코드 ["+authCode+"] 입니다.",
            from_='+16592185817',
            to=phone
        )


        text = "phone : " + phone + ", 회원가입 가능"
        ment = "\033[92m"+"phoneAuthCode SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'0', 'authCode':authCode}
        return HttpResponse(json.dumps(context))      

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"phoneAuthCode Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))

    





# 회원가입
@csrf_exempt
def signup(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios

        form = SignUpForms(data)
        print(form)
        if form.is_valid():
            username = data['username']
            print("username >>>", username)
            new_user = SignUp.objects.create_user(**form.cleaned_data)
            if new_user:
                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                userinfoCount = SignUp.objects.filter(inviteCode=inviteCode).count()
                check = False
                if userinfoCount == 0:
                    userinfo = SignUp.objects.get(username=username)
                    userinfo.inviteCode = inviteCode
                    userinfo.point = "10"
                    userinfo.save()
                else:
                    while check == False:
                        inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                        userinfoCount_check = SignUp.objects.filter(inviteCode=inviteCode).count()
                        if userinfoCount_check == 0:
                            check = True
                            break;

                    userinfo = SignUp.objects.get(username=username)
                    userinfo.inviteCode = inviteCode
                    userinfo.point = "10"
                    userinfo.save()

                pointHistorySubmit = PointHistory(
                    userPK_S = "64",
                    userPK_R = userinfo.id,
                    point = "10",
                    status = "2",
                    contentsStatus = "0",
                    createAt = datetime.now(),
                    createAt_timestamp = str(round(time.time()))
                )
                pointHistorySubmit.save()

                text = "\033[92m"+"signup SUCCESS -> "+username+" 유저 회원가입 완료"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "new_user 오류 발생"
                ment = "\033[91m"+"signup ERROR -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')         
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
        else:
            text = "form 양식이 유효하지 않음; 회원가입 실패"
            ment = "\033[93m"+"signup WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))
            


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"signup Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))














# 회원가입 CI, DI 체크
@csrf_exempt
def signup_CIDICheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        CI = data['CI']
        DI = data['DI']
        print("CI", CI)
        print("DI", DI)
        userinfoCount = SignUp.objects.filter(CI=CI, DI=DI).count()
        if userinfoCount == 0:
            text = "가입 가능한 회원"
            ment = "\033[92m"+"signup_CIDICheck SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))        
        else:
            text = "이미 가입한 회원"
            ment = "\033[93m"+"signup_CIDICheck WARNING -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))

  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"signup_CIDICheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 회원가입 이메일 체크
@csrf_exempt
def signup_usernameCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            username = data['username']
            userinfoCount = SignUp.objects.filter(username=username).count()
            if userinfoCount == 0:
                text = "사용 가능한 아이디"
                ment = "\033[92m"+"signup_usernameCheck SUCCESS -> " + username + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))        
            else:
                text = "이미 존재하는 아이디"
                ment = "\033[93m"+"signup_usernameCheck WARNING -> " + username + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
            
        else:

            username = data['username']
            userinfoCount = SignUp.objects.filter(username=username).count()
            if userinfoCount == 0:
                text = "사용 가능한 아이디"
                ment = "\033[92m"+"signup_usernameCheck SUCCESS -> " + username + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))        
            else:
                text = "이미 존재하는 아이디"
                ment = "\033[93m"+"signup_usernameCheck WARNING -> " + username + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"signup_usernameCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 회원가입 닉네임 체크
@csrf_exempt
def signup_nickNameCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            nickName = data['nickName']
            userinfoCount = SignUp.objects.filter(nickName=nickName).count()
            if userinfoCount == 0:
                text = "사용 가능한 닉네임"
                ment = "\033[92m"+"signup_nickNameCheck SUCCESS -> " + nickName + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))        
            else:
                text = "이미 존재하는 닉네임"
                ment = "\033[93m"+"signup_nickNameCheck WARNING -> " + nickName + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
        else:
            nickName = data['nickName']
            userinfoCount = SignUp.objects.filter(nickName=nickName).count()
            if userinfoCount == 0:
                text = "사용 가능한 닉네임"
                ment = "\033[92m"+"signup_nickNameCheck SUCCESS -> " + nickName + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))        
            else:
                text = "이미 존재하는 닉네임"
                ment = "\033[93m"+"signup_nickNameCheck WARNING -> " + nickName + " : " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"signup_nickNameCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    










# 아이디찾기 - 핸드폰번호로 존재 여부 체크
@csrf_exempt
def findusername_phoneCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        phone = data['phone']
        userinfoCount = SignUp.objects.filter(phone=phone).count()
        if userinfoCount == 0:
            text = "존재하지 않는 회원"
            ment = "\033[92m"+"findusername_phoneCheck WARNING -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))        
        else:
            text = "존재하는 회원"
            ment = "\033[93m"+"findusername_phoneCheck SUCCESS -> " + text + "\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

  
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"findusername_phoneCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 아이디찾기 - CI, DI 체크
@csrf_exempt
def findusername_CIDICheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            CI = data['CI']
            DI = data['DI']
            userinfoCount = SignUp.objects.filter(CI=CI, DI=DI).count()
            if userinfoCount == 0:
                text = "CI / DI 불일치"
                ment = "\033[92m"+"findusername_CIDICheck WARNING -> " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))        
            else:
                userinfo = SignUp.objects.get(CI=CI, DI=DI)
                username = userinfo.username
                text = "CI / DI 일치; 인증 완료"
                ment = "\033[93m"+"findusername_CIDICheck SUCCESS -> " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'1', 'username':username}
                return HttpResponse(json.dumps(context))
        else:
            CI = data['CI']
            DI = data['DI']
            userinfoCount = SignUp.objects.filter(CI=CI, DI=DI).count()
            if userinfoCount == 0:
                text = "CI / DI 불일치"
                ment = "\033[92m"+"findusername_CIDICheck WARNING -> " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))        
            else:
                userinfo = SignUp.objects.get(CI=CI, DI=DI)
                username = userinfo.username
                text = "CI / DI 일치; 인증 완료"
                ment = "\033[93m"+"findusername_CIDICheck SUCCESS -> " + text + "\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'1', 'username':username}
                return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"findusername_CIDICheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    





# 로그인
@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginForm = LoginForms(data)
        if loginForm.is_valid():
            username = data['username']
            password = data['password']

            usercount = SignUp.objects.filter(username = username).count()
            if usercount == 0:
                text = "존재하지 않는 ID"
                ment = "\033[93m"+"login WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'0', 'userinfo':None}
                return HttpResponse(json.dumps(context))
            else:
                userinfo = SignUp.objects.get(username = username)
                grade = userinfo.grade
                if grade == "9":
                    text = "탈퇴한 회원"
                    ment = "\033[93m"+"login WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                    context = {'code':'2', 'userinfo':None}
                    return HttpResponse(json.dumps(context))
                else: 
                    user = authenticate(username=username,password=password)
                    if user:
                        # getToken = data['getToken']
                        fcmToken = data['getToken']
                        auth_login(request, user)
                        userinfo = SignUp.objects.get(username=username)
                        # userinfo.fcmToken = getToken
                        userinfo.fcmToken = fcmToken
                        userinfo.save()
                        text = "\033[92m"+"login SUCCESS, >"+username+" 유저 로그인"+"\033[0m"
                        print("["+str(datetime.now())+"] " + text)
                        userinfo.date_joined = userinfo.date_joined.strftime('%Y-%m-%d-%H:%M:%S')
                        userinfo.last_login = userinfo.last_login.strftime('%Y-%m-%d-%H:%M:%S')
                        profileIMG_path = userinfo.profileIMG_path
                        if profileIMG_path:
                            profileIMG_path = s3_profileimgPATH+profileIMG_path
                        else:
                            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                        # userinfo.fcmToken = fcmToken
                        # userinfo.save()

                        userinfo.profileIMG_path = profileIMG_path

                        
                        userinfo = model_to_dict(userinfo)
                        context = {'code':'1', 'userinfo':userinfo}
                        return HttpResponse(json.dumps(context))
                    else:
                        text = "login user 오류 발생"
                        ment = "\033[91m"+"login ERROR -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')         
                        context = {'code':'9', 'userinfo':None}
                        return HttpResponse(json.dumps(context))

                        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"login Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99',}
        return HttpResponse(json.dumps(context))




# 유저정보 갱신
@csrf_exempt
def updateUserinfo(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']

        userinfoCount = SignUp.objects.filter(id=loginUserPK).count()
        if userinfoCount == 0:
            text = "user PK값 : " + str(loginUserPK) + ", 존재하지 않는 ID :: 여기로오면 뭔가 잘못됨"
            ment = "\033[93m"+"updateUserinfo WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2', 'userinfo':None}
            return HttpResponse(json.dumps(context))
        else:
            # getToken = data['getToken']
            userinfo = SignUp.objects.get(id=loginUserPK)
            # userinfo.fcmToken = getToken
            # userinfo.save()

            userinfo.date_joined = userinfo.date_joined.strftime('%Y-%m-%d-%H:%M:%S')
            userinfo.last_login = userinfo.last_login.strftime('%Y-%m-%d-%H:%M:%S')
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            userinfo.profileIMG_path = profileIMG_path
            userinfo = model_to_dict(userinfo)

            text = "user PK값 : " + str(loginUserPK) + ", 유저 존재"
            ment = "\033[92m"+"updateUserinfo SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

            context = {'code':'1', 'userinfo':userinfo}
            return HttpResponse(json.dumps(context))
        

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"updateUserinfo Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99',}
        return HttpResponse(json.dumps(context))



# 비밀번호 재설정 -> 이메일, 전화번호 체크
@csrf_exempt
def changePW_check(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            email = data['email']

            userinfoCount = SignUp.objects.filter(username = email).count()
            if userinfoCount == 0:
                text = "유저가 존재하지 않음"
                ment = "\033[93m"+"changePW_check WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            else:
                text = "유저 존재"
                ment = "\033[92m"+"changePW_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
        else:
            email = data['email']

            userinfoCount = SignUp.objects.filter(username = email).count()
            if userinfoCount == 0:
                text = "유저가 존재하지 않음"
                ment = "\033[93m"+"changePW_check WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            else:
                text = "유저 존재"
                ment = "\033[92m"+"changePW_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"changePW_check Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 비밀번호 재설정, 핸드폰 인증
@csrf_exempt
def changePW_phoneConfirm(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        CI = data['CI']
        DI = data['DI']

        userinfoCount = SignUp.objects.filter(CI = CI).count()
        if userinfoCount == 0:
            text = "유저가 존재하지 않음"
            ment = "\033[93m"+"changePW_phoneConfirm WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))
        else:
            userinfo = SignUp.objects.get(CI = CI)
            userPK = userinfo.id
            username = userinfo.username
            text = "유저 인증 완료"
            ment = "\033[92m"+"changePW_phoneConfirm SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'userPK':userPK}
            return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"changePW_phoneConfirm Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 인앱 item 리스트
@csrf_exempt
def purchaselist(request):
    try:
	purchaseItemListinfo = purchaseItemList.objects.all()
	purchaseItemListinfo = serializers.serialize('json', purchaseItemListinfo)
	text = "인앱 아이템리스트 호출 완료"
	ment = "\033[92m"+"purchaselist SUCCESS -> "+text+"\033[0m"
	print("["+str(datetime.now())+"] " + ment + '\033[0m')
	context = {'code':'1', 'purchaseItemListinfo':purchaseItemListinfo}
	return HttpResponse(json.dumps(context))

        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"purchaselist Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 인앱결제
@csrf_exempt
def inapppurchase(request):
    try:

	loginUserPK = data['loginUserPK']
	point = data['point']
	cash = data['cash']
	
	inapppurchaseSubmit = InapppurchaseList(userPK = loginUserPK, point = point, cash = cash, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
	inapppurchaseSubmit.save()
	
	userinfo = SignUp.objects.get(id = loginUserPK)
	userinfo.point = int(userinfo.point) + int(point)
	userinfo.save()
	
	text = "충전완료"
	ment = "\033[92m"+"inapppurchase SUCCESS -> "+text+"\033[0m"
	print("["+str(datetime.now())+"] " + ment + '\033[0m')
	context = {'code':'1'}
	return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"inapppurchase Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 메인 비디오 리스트
@csrf_exempt
def videoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page
        loginUserPK = data['loginUserPK']
        videoinfoCount = Video.objects.filter(viewable = "0", status = "1").count()
        if videoinfoCount == 0:
            text = "비디오 리스트 없음"
            ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'videoinfoList':None}
            return HttpResponse(json.dumps(context))
        else:        
            videoinfo = Video.objects.filter(viewable = "0", status = "1").order_by('?')
            videoinfoList = []
            for index, i in enumerate(videoinfo):
                userPK = i.userPK

                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    videoPK = i.id
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    # s3Check = S3Check.objects.get(id = 1)
                    # s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"


                    videoPATH = i.videoPATH
                    videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"


                    thumbnailPATH = i.thumbnailPATH
                    thumbnailPATH = s3PATH_previous + thumbnailPATH




                    contents = i.contents
                    hashTag = i.hashTag
                    viewable = i.viewable
                    size = i.size
                    
                    
                    userLikeCheck = ""
                    viewCountCheck = ""


                    like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    likeCount = like_video_infoCount
                    if like_video_infoCount == 0:
                        pass
                    else:
                        like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                        for index, j in enumerate(like_video_info):
                            userPK_like = j.userPK

                            userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            if userBlockListinfoCount_likevideo == 1:
                                likeCount -= 1



                    like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if like_video_infoCount_user == 0:
                        userLikeCheck = "0"
                    else:
                        like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                        status = like_video_info_user.status
                        if status == "0":
                            userLikeCheck = "0"
                        elif status == "1":
                            userLikeCheck = "1"




                    coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                    comentCount = coment_infoCount
                    if coment_infoCount == 0:
                        pass
                    else:
                        coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                        for index, k in enumerate(coment_info):
                            userPK_coment = k.userPK
                            userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                            if userBlockListinfoCount_coment == 1:
                                comentCount -= 1


                    viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if viewCount_infoCount == 0:
                        viewCountCheck = "0"
                    else:
                        viewCountCheck = "1"


                    # ====================================================================================================================
                    # 20230731 2차 추가
                    
                    followingCheck = ""
                    followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = userPK).count()
                    if followListinfoCount == 0:
                        followingCheck = "0"
                    else:
                        followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = userPK)
                        status = followListinfo.status
                        if status == "0":
                            followingCheck = "0"
                        else:
                            followingCheck = "1"

                    # ====================================================================================================================


                    dictinfo = {
                        'videoPK':int(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'videoPATH':videoPATH,
                        'thumbnailPATH':thumbnailPATH,
                        'size':size,
                        'viewable':viewable,
                        'likeCount':str(likeCount),
                        'comentCount':str(comentCount),
                        'userLikeCheck':userLikeCheck,
                        'viewCountCheck':viewCountCheck,
                        'followingCheck':followingCheck
                    }
                    videoinfoList.append(dictinfo)

            # ====================================================================================================================
            # 20230807 내가한 팔로우 count 체크 추가
            followingListinfoCount = FollowList.objects.filter(userPK = loginUserPK, status = "1").count()
            followingCountCheck = ""
            if followingListinfoCount == 0:
                followingCountCheck = "0"
            else:
                followingCountCheck = "1"

            # ====================================================================================================================

            videoinfoList = videoinfoList[pageStart:pageEnd]
            videoAllinfo = serializers.serialize('json', videoinfo)
            text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoAllinfo':videoAllinfo, 'videoinfoList':videoinfoList, 'followingCountCheck':followingCountCheck}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# 메인 비디오 리스트
@csrf_exempt
def videoListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page
        loginUserPK = data['loginUserPK']
        videoAllinfo = data['videoAllinfo']
        videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]

        videoinfoList = []
        for index, i in enumerate(videoAllinfo):

            userPK = i['fields']['userPK']
            # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
            # if userBlockListinfoCount == 0:
            videoPK = i['pk']
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path


            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = i['fields']['videoPATH']
            videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
            # s3VideoPATH = i['fields']['s3VideoPATH']

            thumbnailPATH = i['fields']['thumbnailPATH']
            thumbnailPATH = s3PATH + thumbnailPATH

            # if s3Status == "0":
            #     videoPATH = serverURL+"/static/video"+videoPATH
            # elif s3Status == "1":
            #     videoPATH = s3PATH+s3VideoPATH

            contents = i['fields']['contents']
            hashTag = i['fields']['hashTag']
            viewable = i['fields']['viewable']

            
            
            userLikeCheck = ""
            viewCountCheck = ""


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = like_video_infoCount
            if like_video_infoCount == 0:
                pass
            else:
                like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                for index, j in enumerate(like_video_info):
                    userPK_like = j.userPK

                    userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likevideo == 1:
                        likeCount -= 1



            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"




            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1


            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"

            # ====================================================================================================================
            # 20230731 2차 추가
            followingCheck = ""
            followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = userPK).count()
            if followListinfoCount == 0:
                followingCheck = "0"
            else:
                followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = userPK)
                status = followListinfo.status
                if status == "0":
                    followingCheck = "0"
                else:
                    followingCheck = "1"
            # ====================================================================================================================



            dictinfo = {
                'videoPK':int(videoPK), 
                'userPK':userPK, 
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'viewable':viewable,
                'likeCount':str(likeCount),
                'comentCount':str(comentCount),
                'userLikeCheck':userLikeCheck,
                'viewCountCheck':viewCountCheck,
                'followingCheck':followingCheck
            }
            videoinfoList.append(dictinfo)

        text = "\033[92m"+"videoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList}
        return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoListMove Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 일반영상 후원
@csrf_exempt
def donetion(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        sender_userPK = data['sender_userPK']
        receiver_userPK = data['receiver_userPK']
        videoPK = data['videoPK']
        amount = data['amount']

        userinfo = SignUp.objects.get(id = sender_userPK)
        senderUserPoint = userinfo.point
        if int(senderUserPoint) < int(amount):
            text = "잔고 부족"
            ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        
        else:
            donetionListSubmit = DonationList(sender_userPK = sender_userPK, receiver_userPK = receiver_userPK, videoPK = videoPK, amount = amount, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            donetionListSubmit.save()

            userinfo = SignUp.objects.get(id = sender_userPK)
            userinfo.point = int(userinfo.point) - int(amount)
            userinfo.save()

            userinfo = SignUp.objects.get(id = receiver_userPK)
            userinfo.point = int(userinfo.point) + int(amount)
            userinfo.save()

            pointHistorySubmit = PointHistory(
                userPK_S = sender_userPK,
                userPK_R = receiver_userPK,
                videoPK = videoPK,
                point = amount,
                status = "0",
                contentsStatus = "1",
                createAt = datetime.now(),
                createAt_timestamp = str(round(time.time()))
            )
            pointHistorySubmit.save()


            text = "후원 완료"
            ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))



    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"donetion Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






# 입출금내역
@csrf_exempt
def pointHistory(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        sortingStatus = data['sortingStatus']
        userinfo = SignUp.objects.get(id = loginUserPK)
        myPoint = userinfo.point


        if sortingStatus == "0":
            pointHistoryinfoCount = PointHistory.objects.filter(Q(userPK_S = loginUserPK) | Q(userPK_R = loginUserPK)).count()
            if pointHistoryinfoCount == 0:
                text = "전체 - 리스트 없음"
                ment = "\033[93m"+"pointHistory WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2', 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            else:
                pointHistoryinfo = PointHistory.objects.filter(Q(userPK_S = loginUserPK) | Q(userPK_R = loginUserPK)).order_by("-id")
                pointHistoryList = []

                for index, i in enumerate(pointHistoryinfo):
                    userPK_S = i.userPK_S
                    userPK_R = i.userPK_R
                    videoPK = i.videoPK
                    status = i.status
                    title = i.title
                    contentsStatus = i.contentsStatus
                    createAt = str(i.createAt)
                    nickName = ""
                    point = ""
                    pointContentStatusinfo = PointContentStatus.objects.get(status = contentsStatus)
                    content = pointContentStatusinfo.content


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')
                    
                    if contentsStatus == "0":
                        point = "+"+i.point
                        userinfo_R = SignUp.objects.get(id = userPK_R)
                        nickName = userinfo_R.nickName
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "1":
                        if userPK_S == loginUserPK:
                            point = "-"+i.point
                            userinfo_R = SignUp.objects.get(id = userPK_R)
                            nickName = userinfo_R.nickName
                            dictinfo = {
                                'userPK_S':userPK_S,
                                'userPK_R':userPK_R,
                                'videoPK':videoPK,
                                'nickName':nickName,
                                'title':title,
                                'point':point,
                                'status':status,
                                'content':content,
                                'date':c,
                            }

                            pointHistoryList.append(dictinfo)
                        else:
                            pass

                    elif contentsStatus == "2":
                        point = "+"+i.point
                        userinfo_S = SignUp.objects.get(id = userPK_S)
                        nickName = userinfo_S.nickName
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "3":
                        point = "+"+i.point
                        userinfo_S = SignUp.objects.get(id = userPK_S)
                        nickName = userinfo_S.nickName

                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "4" or contentsStatus == "5" or contentsStatus == "6" or contentsStatus == "7" or contentsStatus == "8" or contentsStatus == "9":
                        point = "+"+i.point
                        userinfo_S = SignUp.objects.get(id = userPK_S)
                        nickName = userinfo_S.nickName
                        print("nickName >>", nickName)
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)



                text = "전체 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'pointHistoryList':pointHistoryList, 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))

        elif sortingStatus == "1":
            pointHistoryinfoCount = PointHistory.objects.filter(Q(userPK_R = loginUserPK)).count()
            if pointHistoryinfoCount == 0:
                text = "입금내역 - 리스트 없음"
                ment = "\033[93m"+"pointHistory WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2', 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            else:
                pointHistoryinfo = PointHistory.objects.filter(Q(userPK_R = loginUserPK)).order_by('-id')
                pointHistoryList = []

                for index, i in enumerate(pointHistoryinfo):
                    userPK_S = i.userPK_S
                    userPK_R = i.userPK_R
                    videoPK = i.videoPK
                    point = "+"+i.point
                    title = i.title
                    userinfo_S = SignUp.objects.get(id = userPK_S)
                    nickName = userinfo_S.nickName


                    status = i.status                       # "0" == "일반영상", "1" == "오디션영상", "2" == "기타"
                    contentsStatus = i.contentsStatus
                    createAt = str(i.createAt)

                    pointContentStatusinfo = PointContentStatus.objects.get(status = contentsStatus)
                    content = pointContentStatusinfo.content


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    if contentsStatus == "1":
                        pass
                    else:
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                text = "입금 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'pointHistoryList':pointHistoryList, 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))            
        elif sortingStatus == "2":
            pointHistoryinfoCount = PointHistory.objects.filter(Q(userPK_S = loginUserPK)).count()
            if pointHistoryinfoCount == 0:
                text = "출금내역 - 리스트 없음"
                ment = "\033[93m"+"pointHistory WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2', 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            else:
                pointHistoryinfo = PointHistory.objects.filter(Q(userPK_S = loginUserPK)).order_by('-id')
                pointHistoryList = []

                for index, i in enumerate(pointHistoryinfo):
                    userPK_S = i.userPK_S
                    userPK_R = i.userPK_R
                    videoPK = i.videoPK
                    point = "-"+i.point
                    title = i.title
                    userinfo_R = SignUp.objects.get(id = userPK_R)
                    nickName = userinfo_R.nickName


                    status = i.status                       # "0" == "일반영상", "1" == "오디션영상", "2" == "기타"
                    contentsStatus = i.contentsStatus
                    createAt = str(i.createAt)

                    pointContentStatusinfo = PointContentStatus.objects.get(status = contentsStatus)
                    content = pointContentStatusinfo.content


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    dictinfo = {
                        'userPK_S':userPK_S,
                        'userPK_R':userPK_R,
                        'videoPK':videoPK,
                        'nickName':nickName,
                        'title':title,
                        'point':point,
                        'status':status,
                        'content':content,
                        'date':c,
                    }

                    pointHistoryList.append(dictinfo)

                text = "출금 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'pointHistoryList':pointHistoryList, 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            
        else:
            pointHistoryinfoCount = PointHistory.objects.filter(Q(userPK_S = loginUserPK) | Q(userPK_R = loginUserPK)).count()
            if pointHistoryinfoCount == 0:
                text = "전체 - 리스트 없음"
                ment = "\033[93m"+"pointHistory WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2', 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            else:
                pointHistoryinfo = PointHistory.objects.filter(Q(userPK_S = loginUserPK) | Q(userPK_R = loginUserPK)).order_by('-id')
                pointHistoryList = []

                for index, i in enumerate(pointHistoryinfo):
                    userPK_S = i.userPK_S
                    userPK_R = i.userPK_R
                    videoPK = i.videoPK
                    status = i.status
                    title = i.title
                    contentsStatus = i.contentsStatus
                    createAt = str(i.createAt)
                    nickName = ""
                    point = ""
                    pointContentStatusinfo = PointContentStatus.objects.get(status = contentsStatus)
                    content = pointContentStatusinfo.content


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')
                    
                    if contentsStatus == "0":
                        point = "+"+i.point
                        userinfo_R = SignUp.objects.get(id = userPK_R)
                        nickName = userinfo_R.nickName
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "1":
                        if userPK_S == loginUserPK:
                            point = "-"+i.point
                            userinfo_R = SignUp.objects.get(id = userPK_R)
                            nickName = userinfo_R.nickName
                            dictinfo = {
                                'userPK_S':userPK_S,
                                'userPK_R':userPK_R,
                                'videoPK':videoPK,
                                'nickName':nickName,
                                'title':title,
                                'point':point,
                                'status':status,
                                'content':content,
                                'date':c,
                            }

                            pointHistoryList.append(dictinfo)
                        else:
                            pass

                    elif contentsStatus == "2":
                        point = "+"+i.point
                        userinfo_S = SignUp.objects.get(id = userPK_S)
                        nickName = userinfo_S.nickName
                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "3":
                        point = "+"+i.point
                        userinfo_R = SignUp.objects.get(id = userPK_R)
                        nickName = userinfo_R.nickName

                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)

                    elif contentsStatus == "4":
                        point = "+"+i.point
                        userinfo_S = SignUp.objects.get(id = userPK_S)
                        nickName = userinfo_S.nickName

                        dictinfo = {
                            'userPK_S':userPK_S,
                            'userPK_R':userPK_R,
                            'videoPK':videoPK,
                            'nickName':nickName,
                            'title':title,
                            'point':point,
                            'status':status,
                            'content':content,
                            'date':c,
                        }

                        pointHistoryList.append(dictinfo)


                text = "전체 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'pointHistoryList':pointHistoryList, 'myPoint':myPoint}
                return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"pointHistory Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 일반영상 후원 리스트
@csrf_exempt
def donetionList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']

            donetionListinfoCount = DonationList.objects.filter(sender_userPK = loginUserPK).count()
            if donetionListinfoCount == 0:
                text = "후원한것 없음"
                ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            else:
                donetionListinfo = DonationList.objects.filter(sender_userPK = loginUserPK)
                donetionList = []
                for index, i in enumerate(donetionListinfo):
                    amount = i.amount
                    receiver_userPK = i.receiver_userPK
                    createAt = str(i.createAt)
                    receiver_userinfo = SignUp.objects.get(id = receiver_userPK)
                    receiver_nickName = receiver_userinfo.nickName
                    receiver_profileIMG_path = receiver_userinfo.profileIMG_path
                    if receiver_profileIMG_path:
                        receiver_profileIMG_path = s3_profileimgPATH+receiver_profileIMG_path
                    else:
                        receiver_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"    


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    dictinfo = {
                        'receiver_nickName':receiver_nickName, 
                        'receiver_profileIMG_path':receiver_profileIMG_path, 
                        'amount':amount
                    }

                    donetionList.append(dictinfo)

                text = "후원 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'donetionList':donetionList}
                return HttpResponse(json.dumps(context))
        else:
            loginUserPK = data['loginUserPK']

            donetionListinfoCount = DonationList.objects.filter(sender_userPK = loginUserPK).count()
            if donetionListinfoCount == 0:
                text = "후원한것 없음"
                ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            else:
                donetionListinfo = DonationList.objects.filter(sender_userPK = loginUserPK)
                donetionList = []
                for index, i in enumerate(donetionListinfo):
                    amount = i.amount
                    receiver_userPK = i.receiver_userPK
                    createAt = str(i.createAt)
                    receiver_userinfo = SignUp.objects.get(id = receiver_userPK)
                    receiver_nickName = receiver_userinfo.nickName
                    receiver_profileIMG_path = receiver_userinfo.profileIMG_path
                    if receiver_profileIMG_path:
                        receiver_profileIMG_path = s3PATH+receiver_profileIMG_path
                    else:
                        receiver_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"    


                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    dictinfo = {
                        'receiver_nickName':receiver_nickName, 
                        'receiver_profileIMG_path':receiver_profileIMG_path, 
                        'amount':amount
                    }

                    donetionList.append(dictinfo)

                text = "후원 리스트 추출 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'donetionList':donetionList}
                return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"donetion Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 영상 신고
@csrf_exempt
def videoDeclaration(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            declarationUserPK = data['declarationUserPK'] # 신고한 유저 PK
            videoPK = data['videoPK']
            comment = data['comment']

            videoDeclarationListSubmit = VideoDeclarationList(declarationUserPK = declarationUserPK, videoPK = videoPK, comment = comment, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            videoDeclarationListSubmit.save()


            text = "신고 완료"
            ment = "\033[92m"+"videoDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            declarationUserPK = data['declarationUserPK'] # 신고한 유저 PK
            videoPK = data['videoPK']
            comment = data['comment']

            videoDeclarationListSubmit = VideoDeclarationList(declarationUserPK = declarationUserPK, videoPK = videoPK, comment = comment, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            videoDeclarationListSubmit.save()


            text = "신고 완료"
            ment = "\033[92m"+"videoDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoDeclaration Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 조회수
@csrf_exempt
def videoViewCount(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCount_info = ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                viewCount_info.save()
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
                ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
                ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCount_info = ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                viewCount_info.save()
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
                ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
                ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoViewCount Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 영상 좋아요
@csrf_exempt
def videoLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']

        like_video_infoCount = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
        if like_video_infoCount == 0:
            like_video_info = Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
            like_video_info.save()

            videoinfo = Video.objects.get(id = videoPK)
            videoOwnerPK = videoinfo.userPK
            thumbnailPATH = videoinfo.thumbnailPATH

            reqData = {"loginUserPK":loginUserPK, "ownerPK":videoOwnerPK, "thumbnailPATH":thumbnailPATH, "typeNum":"1", "itemPK":videoPK}


            if str(videoOwnerPK) == str(loginUserPK):
                pass
            else:
                sendAlim(reqData)

            text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
            ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            like_video_info = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
            status = like_video_info.status
            if status == "0":
                like_video_info.status = "1"
                like_video_info.save()

                videoinfo = Video.objects.get(id = videoPK)
                videoOwnerPK = videoinfo.userPK
                thumbnailPATH = videoinfo.thumbnailPATH

                reqData = {"loginUserPK":loginUserPK, "ownerPK":videoOwnerPK, "thumbnailPATH":thumbnailPATH, "typeNum":"1", "itemPK":videoPK}



                if str(videoOwnerPK) == str(loginUserPK):
                    pass
                else:
                    sendAlim(reqData)



                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
                ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            elif status == "1":
                like_video_info.status = "0"
                like_video_info.save()
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
                ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 댓글 리스트
@csrf_exempt
def comentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        comentinfoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()

        Videoinfo = Video.objects.get(id = videoPK)
        videoOwner_userPK = Videoinfo.userPK

        if comentinfoCount == 0:
            text = "댓글 없음"
            ment = "\033[93m"+"comentList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'comentinfoList':None}
            return HttpResponse(json.dumps(context))
        else:
            comentinfo = Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
            comentinfoList = []
            for index, i in enumerate(comentinfo):
                now  = int(round(time.time()))
                userPK = i.userPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    comentPK = i.id


                    createAt = i.createAt
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    previous = ""
                    previous_date = ""
                    userComentLikeCheck = ""
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)

                    if me_time < 1 :
                        # previous = '방금전'
                        previous = 'B'
                        previous_date = "0"
                        
                    elif me_time < 60 :
                        # previous = str(me_time) + '분전'
                        previous = 'M'
                        previous_date = str(me_time)

                    elif me_timehour < 24 :
                        # previous = str(me_timehour) + '시간전'
                        previous = 'H'
                        previous_date = str(me_timehour)
                    
                    elif me_timeday < 365 :
                        # previous = str(me_timeday) + '일전'
                        previous = 'D'
                        previous_date = str(me_timeday)

                    elif me_timeyear >= 1 : 
                        # previous = str(me_timeyear) + '년전'
                        previous = 'Y'
                        previous_date = str(me_timeyear)


                    # like_coment_infoCount = Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
                    # likeCount =  str(like_coment_infoCount)

                    like_coment_infoCount = Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
                    likeCount = like_coment_infoCount
                    if like_coment_infoCount == 0:
                        pass
                    else:
                        like_coment_info = Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1")
                        for index, j in enumerate(like_coment_info):
                            userPK_like = j.userPK
                            userBlockListinfoCount_likecoment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            if userBlockListinfoCount_likecoment == 1:
                                likeCount -= 1



                    like_coment_infoCount_user = Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if like_coment_infoCount_user == 0:
                        userComentLikeCheck = "0"
                    else:
                        Like_coment_info_user = Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
                        status = Like_coment_info_user.status
                        if status == "0":
                            userComentLikeCheck = "0"
                        elif status == "1":
                            userComentLikeCheck = "1"

                    
    

                    comentOnComent_infoCount = ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
                    comentONcomentCount = comentOnComent_infoCount
                    if comentOnComent_infoCount == 0:
                        pass
                    else:
                        comentOnComent_info = ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0")
                        for index, k in enumerate(comentOnComent_info):
                            userPK_comentOnComent = k.userPK
                            userBlockListinfoCount_likecomentOnComent = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_comentOnComent, status = "1").count()
                            if userBlockListinfoCount_likecomentOnComent == 1:
                                comentONcomentCount -= 1

                            comentONcomentPK = k.id
                            audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(loginUserPK = loginUserPK, commentCommentPK = comentONcomentPK).count() # 오디션에 넣고 삭제 해야함
                            if audition_CommentCommentDeclarationinfoCount:
                                comentONcomentCount -= 1



                    comentDict = {
                        'videoOwner_userPK':videoOwner_userPK,
                        'comentPK':str(comentPK),
                        'videoPK':videoPK,
                        'userPK':userPK,
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'previous':previous,
                        'previous_date':previous_date,
                        'likeCount':str(likeCount),
                        'comentONcomentLen':str(comentONcomentCount),
                        'userComentLikeCheck':userComentLikeCheck

                    }
                    comentinfoList.append(comentDict)


            text = "\033[92m"+"comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'comentinfoList':comentinfoList}
            return HttpResponse(json.dumps(context))
            


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99', 'comentinfoList':None}
        return HttpResponse(json.dumps(context))


    

# 댓글 저장
@csrf_exempt
def comentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            contents = data['contents']
            # comentinfoCount = Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            # if comentinfoCount == 0:
            Videoinfo = Video.objects.get(id = videoPK)
            videoOwner_userPK = Videoinfo.userPK

            comentSubmit = Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            comentSubmit.save()
            comentPK = comentSubmit.id
            comentinfo = Coment.objects.get(id = comentPK)
            userPK = comentinfo.userPK
            videoPK = comentinfo.videoPK
            contents = comentinfo.contents
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            name = userinfo.name
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            previous = ""
            previous_date = ""
            userComentLikeCheck = ""
            userComentONComentCheck = ""
            now  = int(round(time.time()))
            createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
            me_time = math.floor(((now - createAt_timestamp) / 60))
            me_timehour = math.floor((me_time / 60))
            me_timeday = math.floor((me_timehour / 24))
            me_timeyear = math.floor(me_timeday / 365)

            # if me_time < 1 :
            #     previous = '방금전'
                
            # elif me_time < 60 :
            #     previous = str(me_time) + '분전'

            # elif me_timehour < 24 :
            #     previous = str(me_timehour) + '시간전'
            
            # elif me_timeday < 365 :
            #     previous = str(me_timeday) + '일전'
            
            # elif me_timeyear >= 1 : 
            #     previous = str(me_timeyear) + '년전'
            if me_time < 1 :
                # previous = '방금전'
                previous = 'B'
                previous_date = "0"
                
            elif me_time < 60 :
                # previous = str(me_time) + '분전'
                previous = 'M'
                previous_date = str(me_time)

            elif me_timehour < 24 :
                # previous = str(me_timehour) + '시간전'
                previous = 'H'
                previous_date = str(me_timehour)
            
            elif me_timeday < 365 :
                # previous = str(me_timeday) + '일전'
                previous = 'D'
                previous_date = str(me_timeday)

            elif me_timeyear >= 1 : 
                # previous = str(me_timeyear) + '년전'
                previous = 'Y'
                previous_date = str(me_timeyear)

            # comentCount = Coment.objects.filter(videoPK = videoPK).count()

            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1


            coment_infoCount_user = Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            userComentCheck = ""
            if coment_infoCount_user == 0:
                userComentCheck = "0"
            else:
                userComentCheck = "1"

            comentinfo = {
                'videoOwner_userPK':videoOwner_userPK,
                'comentPK':str(comentPK),
                'videoPK':videoPK,
                'username':username,
                'nickName':nickName,
                'name':name,
                'profileIMG_path':profileIMG_path,
                'previous':previous,
                'previous_date':previous_date,
                'comentCount':str(comentCount),
                'userComentCheck':userComentCheck
            }

            text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
            ment = "\033[92m"+"comentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'comentinfo':comentinfo}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            contents = data['contents']
            # comentinfoCount = Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            # if comentinfoCount == 0:
            Videoinfo = Video.objects.get(id = videoPK)
            videoOwner_userPK = Videoinfo.userPK

            comentSubmit = Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            comentSubmit.save()
            comentPK = comentSubmit.id
            comentinfo = Coment.objects.get(id = comentPK)
            userPK = comentinfo.userPK
            videoPK = comentinfo.videoPK
            contents = comentinfo.contents
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            name = userinfo.name
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            previous = ""
            previous_date = ""
            userComentLikeCheck = ""
            userComentONComentCheck = ""
            now  = int(round(time.time()))
            createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
            me_time = math.floor(((now - createAt_timestamp) / 60))
            me_timehour = math.floor((me_time / 60))
            me_timeday = math.floor((me_timehour / 24))
            me_timeyear = math.floor(me_timeday / 365)

            # if me_time < 1 :
            #     previous = '방금전'
                
            # elif me_time < 60 :
            #     previous = str(me_time) + '분전'

            # elif me_timehour < 24 :
            #     previous = str(me_timehour) + '시간전'
            
            # elif me_timeday < 365 :
            #     previous = str(me_timeday) + '일전'
            
            # elif me_timeyear >= 1 : 
            #     previous = str(me_timeyear) + '년전'
            if me_time < 1 :
                # previous = '방금전'
                previous = 'B'
                previous_date = "0"
                
            elif me_time < 60 :
                # previous = str(me_time) + '분전'
                previous = 'M'
                previous_date = str(me_time)

            elif me_timehour < 24 :
                # previous = str(me_timehour) + '시간전'
                previous = 'H'
                previous_date = str(me_timehour)
            
            elif me_timeday < 365 :
                # previous = str(me_timeday) + '일전'
                previous = 'D'
                previous_date = str(me_timeday)

            elif me_timeyear >= 1 : 
                # previous = str(me_timeyear) + '년전'
                previous = 'Y'
                previous_date = str(me_timeyear)

            # comentCount = Coment.objects.filter(videoPK = videoPK).count()

            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1


            coment_infoCount_user = Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            userComentCheck = ""
            if coment_infoCount_user == 0:
                userComentCheck = "0"
            else:
                userComentCheck = "1"

            comentinfo = {
                'videoOwner_userPK':videoOwner_userPK,
                'comentPK':str(comentPK),
                'videoPK':videoPK,
                'username':username,
                'nickName':nickName,
                'name':name,
                'profileIMG_path':profileIMG_path,
                'previous':previous,
                'previous_date':previous_date,
                'comentCount':str(comentCount),
                'userComentCheck':userComentCheck
            }

            text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
            ment = "\033[92m"+"comentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'comentinfo':comentinfo}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentSubmit Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 영상주인이 댓글삭제 
@csrf_exempt
def videoOwner_comentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            comentPK = data['comentPK']
            loginUserPK = str(data['loginUserPK'])
            comentUserPK = str(data['comentUserPK'])
            videoPK = str(data['videoPK'])

            videoinfo = Video.objects.get(id = videoPK)
            videoinfo_userPK = videoinfo.userPK

            if loginUserPK == videoinfo_userPK:
                comentinfo = Coment.objects.get(id = int(comentPK), userPK = comentUserPK, videoPK = videoPK)
                comentinfo.status = "9"
                comentinfo.save()
                text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", videoinfo userPK값 : "+str(videoinfo_userPK)+", 댓글 삭제 완료"
                ment = "\033[92m"+"videoOwner_comentDel SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", videoinfo userPK값 : "+str(videoinfo_userPK)+", 영상 주인 PK 일치하지않음"
                ment = "\033[93m"+"videoOwner_comentDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            
        else:
            comentPK = data['comentPK']
            loginUserPK = str(data['loginUserPK'])
            comentUserPK = str(data['comentUserPK'])
            videoPK = str(data['videoPK'])

            videoinfo = Video.objects.get(id = videoPK)
            videoinfo_userPK = videoinfo.userPK

            if loginUserPK == videoinfo_userPK:
                comentinfo = Coment.objects.get(id = int(comentPK), userPK = comentUserPK, videoPK = videoPK)
                comentinfo.status = "9"
                comentinfo.save()
                text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", videoinfo userPK값 : "+str(videoinfo_userPK)+", 댓글 삭제 완료"
                ment = "\033[92m"+"videoOwner_comentDel SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", videoinfo userPK값 : "+str(videoinfo_userPK)+", 영상 주인 PK 일치하지않음"
                ment = "\033[93m"+"videoOwner_comentDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoOwner_comentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 댓글 삭제
@csrf_exempt
def comentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            comentPK = data['comentPK']
            loginUserPK = str(data['loginUserPK'])      # 현재 로그인한 유저 ( front에서 본인 게시글에서만 삭제 버튼이 보여지게되있어서 따로 뭘 할필요 없음)
            videoPK = str(data['videoPK'])

            comentinfo = Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK)
            comentinfo.status = "9"
            comentinfo.save()
            text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", 댓글 삭제 완료"
            ment = "\033[92m"+"comentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            comentPK = data['comentPK']
            loginUserPK = str(data['loginUserPK'])      # 현재 로그인한 유저 ( front에서 본인 게시글에서만 삭제 버튼이 보여지게되있어서 따로 뭘 할필요 없음)
            videoPK = str(data['videoPK'])

            comentinfo = Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK)
            comentinfo.status = "9"
            comentinfo.save()
            text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", 댓글 삭제 완료"
            ment = "\033[92m"+"comentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 댓글 좋아요
@csrf_exempt
def comentLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            like_coment_infoCount = Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
            if like_coment_infoCount == 0:
                like_coment_info = Like_coment(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1", comentPK = comentPK)
                like_coment_info.save()
                text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
                ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                like_coment_info = Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
                status = like_coment_info.status
                if status == "0":
                    like_coment_info.status = "1"
                    like_coment_info.save()
                    text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
                    ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    like_coment_info.status = "0"
                    like_coment_info.save()
                    text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
                    ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
        else:
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            like_coment_infoCount = Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
            if like_coment_infoCount == 0:
                like_coment_info = Like_coment(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1", comentPK = comentPK)
                like_coment_info.save()
                text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
                ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                like_coment_info = Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
                status = like_coment_info.status
                if status == "0":
                    like_coment_info.status = "1"
                    like_coment_info.save()
                    text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
                    ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    like_coment_info.status = "0"
                    like_coment_info.save()
                    text = "coment PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
                    ment = "\033[92m"+"comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    





# 대댓글 리스트
@csrf_exempt
def comentONcomentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        comentPK = data['comentPK']
        videoPK = data['videoPK']

        Videoinfo = Video.objects.get(id = videoPK)
        videoOwner_userPK = Videoinfo.userPK

        comentOnComentinfoCount = ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
        if comentOnComentinfoCount == 0:
            text = "대댓글 없음"
            ment = "\033[93m"+"comentONcomentList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'comentONcomentList':None}
            return HttpResponse(json.dumps(context))
        else:
            comentOnComentinfo = ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").order_by('-id')
            comentONcomentList = []
            for index, i in enumerate(comentOnComentinfo):
                comentONcomentPK = i.id

                now  = int(round(time.time()))
                userPK = i.userPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    previous = ""
                    previous_date = ""
                    userComentONComentLikeCheck = ""
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)



                    if me_time < 1 :
                        # previous = '방금전'
                        previous = 'B'
                        previous_date = "0"
                        
                    elif me_time < 60 :
                        # previous = str(me_time) + '분전'
                        previous = 'M'
                        previous_date = str(me_time)

                    elif me_timehour < 24 :
                        # previous = str(me_timehour) + '시간전'
                        previous = 'H'
                        previous_date = str(me_timehour)
                    
                    elif me_timeday < 365 :
                        # previous = str(me_timeday) + '일전'
                        previous = 'D'
                        previous_date = str(me_timeday)

                    elif me_timeyear >= 1 : 
                        # previous = str(me_timeyear) + '년전'
                        previous = 'Y'
                        previous_date = str(me_timeyear)


                    like_comentONcoment_infoCount = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
                    likeCount = like_comentONcoment_infoCount
                    if like_comentONcoment_infoCount == 0:
                        pass
                    else:
                        like_comentONcoment_info = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK)
                        for index, j in enumerate(like_comentONcoment_info):
                            userPK_like = j.userPK
                            userBlockListinfoCount_likecoment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            if userBlockListinfoCount_likecoment == 1:
                                likeCount -= 1


                    like_comentONcoment_infoCount_user = Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
                    if like_comentONcoment_infoCount_user == 0:
                        userComentONComentLikeCheck = "0"
                    else:
                        like_comentONcoment_info_user = Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                        status = like_comentONcoment_info_user.status
                        if status == "0":
                            userComentONComentLikeCheck = "0"
                        elif status == "1":
                            userComentONComentLikeCheck = "1"




                    comentOnComentinfoDict = {
                        'videoOwner_userPK':videoOwner_userPK,
                        'comentONcomentPK':comentONcomentPK,
                        'comentPK':comentPK,
                        'videoPK':videoPK,
                        'userPK':userPK,
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'previous':previous,
                        'previous_date':previous_date,
                        'likeCount':str(likeCount),
                        'userComentONComentLikeCheck':userComentONComentLikeCheck,
                    }
                    comentONcomentList.append(comentOnComentinfoDict)

            text = "\033[92m"+"comentONcomentList SUCCESS -> 대댓글 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'comentONcomentList':comentONcomentList}
            return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))

        

# 대댓글 저장
@csrf_exempt
def comentONcomentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            comentPK = data['comentPK']
            videoPK = data['videoPK']
            contents = data['contents']

            Videoinfo = Video.objects.get(id = videoPK)
            videoOwner_userPK = Videoinfo.userPK
            # comentOnComentinfoCount = ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
            # if comentOnComentinfoCount == 0:
            comentOnComentSubmit = ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            comentOnComentSubmit.save()

            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            comentOnComentinfo = ComentOnComent.objects.get(id = int(comentOnComentSubmit.id))
            comentONcomentPK = comentOnComentinfo.id
            createAt_timestamp = int(round(float(comentOnComentinfo.createAt_timestamp)))
            contents = comentOnComentinfo.contents
            previous = ""
            previous_date = ""
            userComentONComentLikeCheck = ""
            now  = int(round(time.time()))

            me_time = math.floor(((now - createAt_timestamp) / 60))
            me_timehour = math.floor((me_time / 60))
            me_timeday = math.floor((me_timehour / 24))
            me_timeyear = math.floor(me_timeday / 365)

            # if me_time < 1 :
            #     previous = '방금전'
                
            # elif me_time < 60 :
            #     previous = str(me_time) + '분전'

            # elif me_timehour < 24 :
            #     previous = str(me_timehour) + '시간전'
            
            # elif me_timeday < 365 :
            #     previous = str(me_timeday) + '일전'
            
            # elif me_timeyear >= 1 : 
            #     previous = str(me_timeyear) + '년전'
            if me_time < 1 :
                # previous = '방금전'
                previous = 'B'
                previous_date = "0"
                
            elif me_time < 60 :
                # previous = str(me_time) + '분전'
                previous = 'M'
                previous_date = str(me_time)

            elif me_timehour < 24 :
                # previous = str(me_timehour) + '시간전'
                previous = 'H'
                previous_date = str(me_timehour)
            
            elif me_timeday < 365 :
                # previous = str(me_timeday) + '일전'
                previous = 'D'
                previous_date = str(me_timeday)

            elif me_timeyear >= 1 : 
                # previous = str(me_timeyear) + '년전'
                previous = 'Y'
                previous_date = str(me_timeyear)



            # like_comentONcoment_infoCount = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
            # likeCount = str(like_comentONcoment_infoCount)

            like_comentONcoment_infoCount = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
            likeCount = like_comentONcoment_infoCount
            if like_comentONcoment_infoCount == 0:
                pass
            else:
                like_comentONcoment_info = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK)
                for index, j in enumerate(like_comentONcoment_info):
                    userPK_like = j.userPK
                    userBlockListinfoCount_likecoment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likecoment == 1:
                        likeCount -= 1        


            like_comentONcoment_infoCount_user = Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if like_comentONcoment_infoCount_user == 0:
                userComentONComentLikeCheck = "0"
            else:
                like_comentONcoment_info_user = Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = like_comentONcoment_info_user.status
                if status == "0":
                    userComentONComentLikeCheck = "0"
                elif status == "1":
                    userComentONComentLikeCheck = "1"



            comentOnComentinfo = {
                'videoOwner_userPK':videoOwner_userPK,
                'comentONcomentPK':comentONcomentPK,
                'comentPK':comentPK,
                'videoPK':videoPK,
                'userPK':loginUserPK,
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'previous':previous,
                'previous_date':previous_date,
                'likeCount':str(likeCount),
                'userComentONComentLikeCheck':userComentONComentLikeCheck,
            }


            text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
            ment = "\033[92m"+"comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'comentOnComentinfo':comentOnComentinfo}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            comentPK = data['comentPK']
            videoPK = data['videoPK']
            contents = data['contents']

            Videoinfo = Video.objects.get(id = videoPK)
            videoOwner_userPK = Videoinfo.userPK
            # comentOnComentinfoCount = ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
            # if comentOnComentinfoCount == 0:
            comentOnComentSubmit = ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            comentOnComentSubmit.save()

            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            comentOnComentinfo = ComentOnComent.objects.get(id = int(comentOnComentSubmit.id))
            comentONcomentPK = comentOnComentinfo.id
            createAt_timestamp = int(round(float(comentOnComentinfo.createAt_timestamp)))
            contents = comentOnComentinfo.contents
            previous = ""
            previous_date = ""
            userComentONComentLikeCheck = ""
            now  = int(round(time.time()))

            me_time = math.floor(((now - createAt_timestamp) / 60))
            me_timehour = math.floor((me_time / 60))
            me_timeday = math.floor((me_timehour / 24))
            me_timeyear = math.floor(me_timeday / 365)

            # if me_time < 1 :
            #     previous = '방금전'
                
            # elif me_time < 60 :
            #     previous = str(me_time) + '분전'

            # elif me_timehour < 24 :
            #     previous = str(me_timehour) + '시간전'
            
            # elif me_timeday < 365 :
            #     previous = str(me_timeday) + '일전'
            
            # elif me_timeyear >= 1 : 
            #     previous = str(me_timeyear) + '년전'
            if me_time < 1 :
                # previous = '방금전'
                previous = 'B'
                previous_date = "0"
                
            elif me_time < 60 :
                # previous = str(me_time) + '분전'
                previous = 'M'
                previous_date = str(me_time)

            elif me_timehour < 24 :
                # previous = str(me_timehour) + '시간전'
                previous = 'H'
                previous_date = str(me_timehour)
            
            elif me_timeday < 365 :
                # previous = str(me_timeday) + '일전'
                previous = 'D'
                previous_date = str(me_timeday)

            elif me_timeyear >= 1 : 
                # previous = str(me_timeyear) + '년전'
                previous = 'Y'
                previous_date = str(me_timeyear)



            # like_comentONcoment_infoCount = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
            # likeCount = str(like_comentONcoment_infoCount)

            like_comentONcoment_infoCount = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
            likeCount = like_comentONcoment_infoCount
            if like_comentONcoment_infoCount == 0:
                pass
            else:
                like_comentONcoment_info = Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK)
                for index, j in enumerate(like_comentONcoment_info):
                    userPK_like = j.userPK
                    userBlockListinfoCount_likecoment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likecoment == 1:
                        likeCount -= 1        


            like_comentONcoment_infoCount_user = Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if like_comentONcoment_infoCount_user == 0:
                userComentONComentLikeCheck = "0"
            else:
                like_comentONcoment_info_user = Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = like_comentONcoment_info_user.status
                if status == "0":
                    userComentONComentLikeCheck = "0"
                elif status == "1":
                    userComentONComentLikeCheck = "1"



            comentOnComentinfo = {
                'videoOwner_userPK':videoOwner_userPK,
                'comentONcomentPK':comentONcomentPK,
                'comentPK':comentPK,
                'videoPK':videoPK,
                'userPK':loginUserPK,
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'previous':previous,
                'previous_date':previous_date,
                'likeCount':str(likeCount),
                'userComentONComentLikeCheck':userComentONComentLikeCheck,
            }


            text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
            ment = "\033[92m"+"comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'comentOnComentinfo':comentOnComentinfo}
            return HttpResponse(json.dumps(context))

        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentSubmit Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 영상주인이 대댓글 삭제
@csrf_exempt
def videoOwner_comentONcomentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            comentONcomentPK = data['comentONcomentPK']
            comentONcomentUserPK = str(data['comentONcomentUserPK'])
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            videoinfo = Video.objects.get(id = videoPK)
            videoOwnerPK = videoinfo.userPK


            comentONcomentinfo = ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = comentONcomentUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + comentONcomentUserPK + ", 영상주인이 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            comentONcomentPK = data['comentONcomentPK']
            comentONcomentUserPK = str(data['comentONcomentUserPK'])
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            videoinfo = Video.objects.get(id = videoPK)
            videoOwnerPK = videoinfo.userPK


            comentONcomentinfo = ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = comentONcomentUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + comentONcomentUserPK + ", 영상주인이 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 대댓글 삭제
@csrf_exempt
def comentONcomentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            comentONcomentPK = data['comentONcomentPK']
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            comentONcomentinfo = ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            comentONcomentPK = data['comentONcomentPK']
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            comentONcomentinfo = ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 대댓글 좋아요
@csrf_exempt
def comentONcomentLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = str(data['loginUserPK'])
            comentONcomentPK = str(data['comentONcomentPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            like_comentONcomentinfoCount = Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if like_comentONcomentinfoCount == 0:
                Like_comentONcomentinfo = Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                Like_comentONcomentinfo.save()
                text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
                ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                like_comentONcomentinfo = Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = like_comentONcomentinfo.status
                if status == "0":
                    like_comentONcomentinfo.status = "1"
                    like_comentONcomentinfo.save()
                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    like_comentONcomentinfo.status = "0"
                    like_comentONcomentinfo.save()

                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
        else:
            loginUserPK = str(data['loginUserPK'])
            comentONcomentPK = str(data['comentONcomentPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])


            like_comentONcomentinfoCount = Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if like_comentONcomentinfoCount == 0:
                Like_comentONcomentinfo = Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                Like_comentONcomentinfo.save()
                text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
                ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                like_comentONcomentinfo = Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = like_comentONcomentinfo.status
                if status == "0":
                    like_comentONcomentinfo.status = "1"
                    like_comentONcomentinfo.save()
                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    like_comentONcomentinfo.status = "0"
                    like_comentONcomentinfo.save()

                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    
    







# 검색 페이지 비디오 리스트
# status == "0" : 검색 페이지 진입 시 
# status == "1" : 검색 했을때
# status == "2" : 이전 검색이나 , 추천검색 터치시
@csrf_exempt
def contentsSearch(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = str(data['loginUserPK'])
        searchContents = str(data['searchContents'])
        status = data['status']
        page = int(data['page'])
        pageStart = (page - 1) * 21
        pageEnd = 21 * page

        if status == "0":
            videoinfoCount = Video.objects.filter(viewable = "0", status = "1").count()
            if videoinfoCount == 0:
                text = "status :: "+status+" :: 영상 없음"
                ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0', 'videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                videoinfoCount = Video.objects.filter(viewable = "0", status = "1")[pageStart:pageEnd].count()
                if videoinfoCount == 0:
                    text = "status :: "+status+" :: 페이지 영상 없음"
                    ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2', 'videoinfoList':None}
                    return HttpResponse(json.dumps(context))
                else:

                    videoinfo = Video.objects.filter(viewable = "0", status = "1").order_by('?')
                    videoinfoList = []
                    for index, i in enumerate(videoinfo):
                        userPK = i.userPK
                        size = i.size
                        blockinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                        if blockinfoCount == 0:
                            videoPK = i.id
                            
                            # if thumbnailPATH:
                            #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH


                            userinfo = SignUp.objects.get(id = userPK)
                            username = userinfo.username
                            nickName = userinfo.nickName
                            
                            profileIMG_path = userinfo.profileIMG_path
                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                            videoPATH = i.videoPATH
                            videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                            # s3VideoPATH = i.s3VideoPATH
                            thumbnailPATH = i.thumbnailPATH
                            # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                            thumbnailPATH = s3PATH + thumbnailPATH
                            # s3Check = S3Check.objects.get(id = 1)
                            # s3Status = s3Check.status
                            # if s3Status == "0":
                            #     videoPATH = serverURL+"/static/video"+videoPATH
                            #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                            # elif s3Status == "1":

                            
                            contents = i.contents
                            hashTag = i.hashTag
                            viewable = i.viewable
                            likeCount = ""
                            comentCount = ""
                            userLikeCheck = ""
                            viewCountCheck = ""

                            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            likeCount = str(like_video_infoCount)

                            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            if like_video_infoCount_user == 0:
                                userLikeCheck = "0"
                            else:
                                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                                status = like_video_info_user.status
                                if status == "0":
                                    userLikeCheck = "0"
                                elif status == "1":
                                    userLikeCheck = "1"

                            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                            comentCount = str(coment_infoCount)

                            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            if viewCount_infoCount == 0:
                                viewCountCheck = "0"
                            else:
                                viewCountCheck = "1"


                            dictinfo = {
                                'videoPK':str(videoPK), 
                                'userPK':userPK, 
                                'username':username,
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'contents':contents,
                                'hashTag':hashTag,
                                'videoPATH':videoPATH,
                                'viewable':viewable,
                                'likeCount':likeCount,
                                'comentCount':comentCount,
                                'userLikeCheck':userLikeCheck,
                                'viewCountCheck':viewCountCheck,
                                'thumbnailPATH':thumbnailPATH,
                                'size':size
                            }
                            videoinfoList.append(dictinfo)

                    videoAllinfo = videoinfoList
                    videoinfoList = videoinfoList[pageStart:pageEnd]

                    # random.shuffle(videoinfoList)
                    text = "status :: "+status+" :: 영상 있음"
                    ment = "\033[92m"+"contentsSearch SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1', 'videoAllinfo':videoAllinfo, 'videoinfoList':videoinfoList}
                    return HttpResponse(json.dumps(context))
        else:
            if status == "1":
                # print("검색버튼 눌렀을때")

                videoinfoCount = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1").count()
                if videoinfoCount == 0:
                    text = "status :: "+status+" :: 영상 없음"
                    ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0', 'videoinfoList':None}
                    return HttpResponse(json.dumps(context))
                else:
                    searchListCount = SearchList.objects.filter(userPK = loginUserPK, searchContents = searchContents).count()
                    if searchListCount == 0:
                        searchListSubmit = SearchList(userPK = loginUserPK, searchContents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                        searchListSubmit.save()
                    else:
                        searchListinfo = SearchList.objects.get(userPK = loginUserPK, searchContents = searchContents)
                        searchListCount = int(searchListinfo.count)
                        searchListinfo.count = str(searchListCount + 1)
                        searchListinfo.status = "0"
                        searchListinfo.createAt = datetime.now()
                        searchListinfo.createAt_timestamp = str(round(time.time()))
                        searchListinfo.save()

                    featuredContentCount = FeaturedContent.objects.filter(contents = searchContents).count()
                    if featuredContentCount == 0:
                        featuredContentSubmit = FeaturedContent(contents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                        featuredContentSubmit.save()
                    else:
                        featuredContentinfo = FeaturedContent.objects.get(contents = searchContents)
                        count = int(featuredContentinfo.count)
                        featuredContentinfo.count = str(count + 1)
                        featuredContentinfo.createAt = datetime.now()
                        featuredContentinfo.createAt_timestamp = str(round(time.time()))
                        featuredContentinfo.save()
                        
                    videoinfoCount2 = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1")[pageStart:pageEnd].count()
                    if videoinfoCount2 == 0:
                        text = "status :: "+status+" :: 페이지 영상 없음"
                        ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'2', 'videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:
                        videoinfo = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1").order_by('?')
                        videoinfoList = []
                        for index, i in enumerate(videoinfo):
                            userPK = i.userPK
                            blockinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                            if blockinfoCount == 0:
                                videoPK = i.id
                                # thumbnailPATH = i.thumbnailPATH
                                # if thumbnailPATH:
                                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH

                                userinfo = SignUp.objects.get(id = userPK)
                                username = userinfo.username
                                nickName = userinfo.nickName
                                profileIMG_path = userinfo.profileIMG_path
                                if profileIMG_path:
                                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                                else:
                                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                                # videoPATH = i.videoPATH
                                # s3VideoPATH = i.s3VideoPATH
                                # thumbnailPATH = i.thumbnailPATH
                                # s3Check = S3Check.objects.get(id = 1)
                                # s3Status = s3Check.status
                                # if s3Status == "0":
                                #     videoPATH = serverURL+"/static/video"+videoPATH
                                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                                # elif s3Status == "1":
                                #     videoPATH = s3PATH+s3VideoPATH
                                #     thumbnailPATH = s3PATH+thumbnailPATH
                                videoPATH = i.videoPATH
                                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                                # videoPATH = s3PATH+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                                # s3VideoPATH = i.s3VideoPATH
                                thumbnailPATH = i.thumbnailPATH
                                # thumbnailPATH = s3PATH+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                                thumbnailPATH = s3PATH + thumbnailPATH

                                contents = i.contents
                                hashTag = i.hashTag
                                viewable = i.viewable
                                likeCount = ""
                                comentCount = ""
                                userLikeCheck = ""
                                viewCountCheck = ""
                                size = i.size

                                like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                                likeCount = str(like_video_infoCount)

                                like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                                if like_video_infoCount_user == 0:
                                    userLikeCheck = "0"
                                else:
                                    like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                                    status = like_video_info_user.status
                                    if status == "0":
                                        userLikeCheck = "0"
                                    elif status == "1":
                                        userLikeCheck = "1"

                                coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                                comentCount = str(coment_infoCount)

                                viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                                if viewCount_infoCount == 0:
                                    viewCountCheck = "0"
                                else:
                                    viewCountCheck = "1"


                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'username':username,
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'contents':contents,
                                    'hashTag':hashTag,
                                    'videoPATH':videoPATH,
                                    'viewable':viewable,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'userLikeCheck':userLikeCheck,
                                    'viewCountCheck':viewCountCheck,
                                    'thumbnailPATH':thumbnailPATH,
                                    'size':size
                                }
                                videoinfoList.append(dictinfo)

                        # videoAllinfo = serializers.serialize('json', videoinfo)
                        videoAllinfo = videoinfoList
                        videoinfoList = videoinfoList[pageStart:pageEnd]

                        # random.shuffle(videoinfoList)
                        text = "status :: "+status+" :: 영상 있음"
                        ment = "\033[92m"+"contentsSearch SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1', 'videoAllinfo':videoAllinfo, 'videoinfoList':videoinfoList}
                        return HttpResponse(json.dumps(context))

            elif status == "2":
                # print("이전검색이나 추천콘텐츠 터치시")
                videoinfoCount = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1").count()
                if videoinfoCount == 0:
                    text = "status :: "+status+" :: 영상 없음"
                    ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0', 'videoinfoList':None}
                    return HttpResponse(json.dumps(context))
                else:
                    videoinfoCount2 = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1")[pageStart:pageEnd].count()
                    if videoinfoCount2 == 0:
                        text = "status :: "+status+" :: 페이지 영상 없음"
                        ment = "\033[92m"+"contentsSearch WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'2', 'videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:
                        videoinfo = Video.objects.filter(contents__contains = searchContents, viewable = "0", status = "1").order_by('?')
                        videoinfoList = []
                        for index, i in enumerate(videoinfo):
                            userPK = i.userPK
                            blockinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                            if blockinfoCount == 0:
                                videoPK = i.id
                                # thumbnailPATH = i.thumbnailPATH
                                # if thumbnailPATH:
                                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                                userinfo = SignUp.objects.get(id = userPK)
                                username = userinfo.username
                                nickName = userinfo.nickName
                                profileIMG_path = userinfo.profileIMG_path
                                if profileIMG_path:
                                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                                else:
                                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                                # videoPATH = i.videoPATH
                                # s3VideoPATH = i.s3VideoPATH
                                # thumbnailPATH = i.thumbnailPATH
                                # s3Check = S3Check.objects.get(id = 1)
                                # s3Status = s3Check.status
                                # if s3Status == "0":
                                #     videoPATH = serverURL+"/static/video"+videoPATH
                                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                                # elif s3Status == "1":
                                #     videoPATH = s3PATH+s3VideoPATH
                                #     thumbnailPATH = s3PATH+thumbnailPATH

                                videoPATH = i.videoPATH
                                # videoPATH = s3PATH+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                                # s3VideoPATH = i.s3VideoPATH
                                thumbnailPATH = i.thumbnailPATH
                                # thumbnailPATH = s3PATH+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                                thumbnailPATH = s3PATH + thumbnailPATH

                                contents = i.contents
                                hashTag = i.hashTag
                                viewable = i.viewable
                                likeCount = ""
                                comentCount = ""
                                userLikeCheck = ""
                                viewCountCheck = ""
                                size = i.size

                                like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                                likeCount = str(like_video_infoCount)

                                like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                                if like_video_infoCount_user == 0:
                                    userLikeCheck = "0"
                                else:
                                    like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                                    status = like_video_info_user.status
                                    if status == "0":
                                        userLikeCheck = "0"
                                    elif status == "1":
                                        userLikeCheck = "1"

                                coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                                comentCount = str(coment_infoCount)

                                viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                                if viewCount_infoCount == 0:
                                    viewCountCheck = "0"
                                else:
                                    viewCountCheck = "1"


                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'username':username,
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'contents':contents,
                                    'hashTag':hashTag,
                                    'videoPATH':videoPATH,
                                    'viewable':viewable,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'userLikeCheck':userLikeCheck,
                                    'viewCountCheck':viewCountCheck,
                                    'thumbnailPATH':thumbnailPATH,
                                    'size':size
                                }
                                videoinfoList.append(dictinfo)

                        # videoAllinfo = serializers.serialize('json', videoinfo)
                        videoAllinfo = videoinfoList
                        videoinfoList = videoinfoList[pageStart:pageEnd]


                        # random.shuffle(videoinfoList)
                        text = "status :: "+status+" :: 영상 있음"
                        ment = "\033[92m"+"contentsSearch SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1', 'videoAllinfo':videoAllinfo, 'videoinfoList':videoinfoList}
                        return HttpResponse(json.dumps(context))



    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"contentsSearch Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))

            # videoinfo = Video.objects.all().order_by('?')[pageStart:pageEnd]
            # videoinfoList = []
            # for index, i in enumerate(videoinfo):
            #     userPK = i.userPK
            #     videoPK = i.id
            #     userinfo = SignUp.objects.get(id = userPK)
            #     username = userinfo.username
            #     nickName = userinfo.nickName
            #     profileIMG_path = userinfo.profileIMG_path
            #     if profileIMG_path:
            #         profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
            #     else:
            #         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
            #     videoPATH = i.videoPATH
            #     # videoPATH = s3_videoPATH+videoPATH
            #     videoPATH = serverURL+"/static/video"+videoPATH
            #     contents = i.contents
            #     hashTag = i.hashTag
            #     viewable = i.viewable
            #     likeCount = ""
            #     comentCount = ""
            #     userLikeCheck = ""
            #     viewCountCheck = ""

            #     like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            #     likeCount = str(like_video_infoCount)

            #     like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            #     if like_video_infoCount_user == 0:
            #         userLikeCheck = "0"
            #     else:
            #         like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
            #         status = like_video_info_user.status
            #         if status == "0":
            #             userLikeCheck = "0"
            #         elif status == "1":
            #             userLikeCheck = "1"

            #     coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            #     comentCount = str(coment_infoCount)

            #     viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            #     if viewCount_infoCount == 0:
            #         viewCountCheck = "0"
            #     else:
            #         viewCountCheck = "1"


            #     dictinfo = {
            #         'videoPK':str(videoPK), 
            #         'userPK':userPK, 
            #         'username':username,
            #         'nickName':nickName,
            #         'profileIMG_path':profileIMG_path,
            #         'contents':contents,
            #         'hashTag':hashTag,
            #         'videoPATH':videoPATH,
            #         'viewable':viewable,
            #         'likeCount':likeCount,
            #         'comentCount':comentCount,
            #         'userLikeCheck':userLikeCheck,
            #         'viewCountCheck':viewCountCheck
            #     }
            #     videoinfoList.append(dictinfo)


# 검색 페이지 비디오 리스트
# status == "0" : 검색 페이지 진입 시 
# status == "1" : 검색 했을때
# status == "2" : 이전 검색이나 , 추천검색 터치시
@csrf_exempt
def contentsSearchMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        page = int(data['page'])
        pageStart = (page - 1) * 21
        pageEnd = 21 * page
        loginUserPK = data['loginUserPK']
        videoAllinfo = data['videoAllinfo'][pageStart:pageEnd]
        videoAllinfoLen = len(videoAllinfo)
        # videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]
        if videoAllinfoLen == 0:
            text = " :: 페이지 영상 없음"
            ment = "\033[92m"+"contentsSearchMove WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2', 'videoinfoList':None}
            return HttpResponse(json.dumps(context))
        else:
            videoinfoList = []
            for index, i in enumerate(videoAllinfo):

                userPK = i['userPK']

                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']
                    thumbnailPATH = i['thumbnailPATH']


                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']

                    
                    
                    userLikeCheck = ""
                    viewCountCheck = ""


                    like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    likeCount = like_video_infoCount
                    if like_video_infoCount == 0:
                        pass
                    else:
                        like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                        for index, j in enumerate(like_video_info):
                            userPK_like = j.userPK

                            userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            if userBlockListinfoCount_likevideo == 1:
                                likeCount -= 1



                    like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if like_video_infoCount_user == 0:
                        userLikeCheck = "0"
                    else:
                        like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                        status = like_video_info_user.status
                        if status == "0":
                            userLikeCheck = "0"
                        elif status == "1":
                            userLikeCheck = "1"




                    coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                    comentCount = coment_infoCount
                    if coment_infoCount == 0:
                        pass
                    else:
                        coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                        for index, k in enumerate(coment_info):
                            userPK_coment = k.userPK
                            userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                            if userBlockListinfoCount_coment == 1:
                                comentCount -= 1


                    viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if viewCount_infoCount == 0:
                        viewCountCheck = "0"
                    else:
                        viewCountCheck = "1"


                    dictinfo = {
                        'videoPK':str(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'videoPATH':videoPATH,
                        'viewable':viewable,
                        'likeCount':likeCount,
                        'comentCount':comentCount,
                        'userLikeCheck':userLikeCheck,
                        'viewCountCheck':viewCountCheck,
                        'thumbnailPATH':thumbnailPATH
                    }
                    videoinfoList.append(dictinfo)

            text = "\033[92m"+"contentsSearchMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
                
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"contentsSearchMove Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# # 검색 상세 및 위아래 페이지 네이션
# @csrf_exempt
# def contentsSearchDetailListMove(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             videoAllinfo = data['videoAllinfo']
#             videoAllinfo = videoAllinfo[pageStart:pageEnd]
#             videoAllinfoLen = len(videoAllinfo)
#             if videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfoList = []
#                 for index, i in enumerate(videoAllinfo):

#                     userPK = i['userPK']

#                     userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
#                     if userBlockListinfoCount == 0:
#                         videoPK = i['videoPK']
#                         userinfo = SignUp.objects.get(id = userPK)
#                         username = userinfo.username
#                         nickName = userinfo.nickName
#                         profileIMG_path = userinfo.profileIMG_path
#                         s3Check = S3Check.objects.get(id = 1)
#                         s3Status = s3Check.status

#                         if profileIMG_path:
#                             profileIMG_path = s3_profileimgPATH+profileIMG_path
#                         else:
#                             profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                         videoPATH = i['videoPATH']
#                         # s3VideoPATH = i['s3VideoPATH']

#                         # if s3Status == "0":
#                         #     videoPATH = serverURL+"/static/video"+videoPATH
#                         # elif s3Status == "1":
#                         #     videoPATH = s3PATH+s3VideoPATH

#                         contents = i['contents']
#                         hashTag = i['hashTag']
#                         viewable = i['viewable']

                        
                        
#                         userLikeCheck = ""
#                         viewCountCheck = ""


#                         like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                         likeCount = like_video_infoCount
#                         if like_video_infoCount == 0:
#                             pass
#                         else:
#                             like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                             for index, j in enumerate(like_video_info):
#                                 userPK_like = j.userPK

#                                 userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                                 if userBlockListinfoCount_likevideo == 1:
#                                     likeCount -= 1



#                         like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                         if like_video_infoCount_user == 0:
#                             userLikeCheck = "0"
#                         else:
#                             like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                             status = like_video_info_user.status
#                             if status == "0":
#                                 userLikeCheck = "0"
#                             elif status == "1":
#                                 userLikeCheck = "1"




#                         coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                         comentCount = coment_infoCount
#                         if coment_infoCount == 0:
#                             pass
#                         else:
#                             coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                             for index, k in enumerate(coment_info):
#                                 userPK_coment = k.userPK
#                                 userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                                 if userBlockListinfoCount_coment == 1:
#                                     comentCount -= 1


#                         viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                         if viewCount_infoCount == 0:
#                             viewCountCheck = "0"
#                         else:
#                             viewCountCheck = "1"


#                         dictinfo = {
#                             'videoPK':int(videoPK), 
#                             'userPK':userPK, 
#                             'username':username,
#                             'nickName':nickName,
#                             'profileIMG_path':profileIMG_path,
#                             'contents':contents,
#                             'hashTag':hashTag,
#                             'videoPATH':videoPATH,
#                             'viewable':viewable,
#                             'likeCount':str(likeCount),
#                             'comentCount':str(comentCount),
#                             'userLikeCheck':userLikeCheck,
#                             'viewCountCheck':viewCountCheck
#                         }
#                         videoinfoList.append(dictinfo)

#                 text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             videoAllinfo = data['videoAllinfo']
#             videoAllinfo = videoAllinfo[pageStart:pageEnd]
#             videoAllinfoLen = len(videoAllinfo)
#             if videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfoList = []
#                 for index, i in enumerate(videoAllinfo):

#                     userPK = i['userPK']

#                     userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
#                     if userBlockListinfoCount == 0:
#                         videoPK = i['videoPK']
#                         userinfo = SignUp.objects.get(id = userPK)
#                         username = userinfo.username
#                         nickName = userinfo.nickName
#                         profileIMG_path = userinfo.profileIMG_path
#                         s3Check = S3Check.objects.get(id = 1)
#                         s3Status = s3Check.status

#                         if profileIMG_path:
#                             profileIMG_path = s3_profileimgPATH+profileIMG_path
#                         else:
#                             profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                         videoPATH = i['videoPATH']
#                         # s3VideoPATH = i['s3VideoPATH']

#                         # if s3Status == "0":
#                         #     videoPATH = serverURL+"/static/video"+videoPATH
#                         # elif s3Status == "1":
#                         #     videoPATH = s3PATH+s3VideoPATH

#                         contents = i['contents']
#                         hashTag = i['hashTag']
#                         viewable = i['viewable']

                        
                        
#                         userLikeCheck = ""
#                         viewCountCheck = ""


#                         like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                         likeCount = like_video_infoCount
#                         if like_video_infoCount == 0:
#                             pass
#                         else:
#                             like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                             for index, j in enumerate(like_video_info):
#                                 userPK_like = j.userPK

#                                 userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                                 if userBlockListinfoCount_likevideo == 1:
#                                     likeCount -= 1



#                         like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                         if like_video_infoCount_user == 0:
#                             userLikeCheck = "0"
#                         else:
#                             like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                             status = like_video_info_user.status
#                             if status == "0":
#                                 userLikeCheck = "0"
#                             elif status == "1":
#                                 userLikeCheck = "1"




#                         coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                         comentCount = coment_infoCount
#                         if coment_infoCount == 0:
#                             pass
#                         else:
#                             coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                             for index, k in enumerate(coment_info):
#                                 userPK_coment = k.userPK
#                                 userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                                 if userBlockListinfoCount_coment == 1:
#                                     comentCount -= 1


#                         viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                         if viewCount_infoCount == 0:
#                             viewCountCheck = "0"
#                         else:
#                             viewCountCheck = "1"


#                         dictinfo = {
#                             'videoPK':int(videoPK), 
#                             'userPK':userPK, 
#                             'username':username,
#                             'nickName':nickName,
#                             'profileIMG_path':profileIMG_path,
#                             'contents':contents,
#                             'hashTag':hashTag,
#                             'videoPATH':videoPATH,
#                             'viewable':viewable,
#                             'likeCount':str(likeCount),
#                             'comentCount':str(comentCount),
#                             'userLikeCheck':userLikeCheck,
#                             'viewCountCheck':viewCountCheck
#                         }
#                         videoinfoList.append(dictinfo)

#                 text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"videoList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# 검색 상세 및 위아래 페이지 네이션
@csrf_exempt
def contentsSearchDetailListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page
        loginUserPK = data['loginUserPK']
        videoAllinfo = data['videoAllinfo']
        videoAllinfo = videoAllinfo[pageStart:pageEnd]
        videoAllinfoLen = len(videoAllinfo)
        if videoAllinfoLen == 0:
            text = " :: 페이지 영상 없음"
            ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2', 'videoinfoList':None}
            return HttpResponse(json.dumps(context))
        else:
            videoinfoList = []
            for index, i in enumerate(videoAllinfo):
                userPK = i['userPK']

                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
 

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']
                    # s3VideoPATH = i['s3VideoPATH']

                    # if s3Status == "0":
                    #     videoPATH = serverURL+"/static/video"+videoPATH
                    # elif s3Status == "1":
                    #     videoPATH = s3PATH+s3VideoPATH

                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']
                    size = i['size']
                    
                    
                    userLikeCheck = ""
                    viewCountCheck = ""


                    like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    likeCount = like_video_infoCount
                    if like_video_infoCount == 0:
                        pass
                    else:
                        like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                        for index, j in enumerate(like_video_info):
                            userPK_like = j.userPK

                            userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            if userBlockListinfoCount_likevideo == 1:
                                likeCount -= 1



                    like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if like_video_infoCount_user == 0:
                        userLikeCheck = "0"
                    else:
                        like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                        status = like_video_info_user.status
                        if status == "0":
                            userLikeCheck = "0"
                        elif status == "1":
                            userLikeCheck = "1"




                    coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                    comentCount = coment_infoCount
                    if coment_infoCount == 0:
                        pass
                    else:
                        coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                        for index, k in enumerate(coment_info):
                            userPK_coment = k.userPK
                            userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                            if userBlockListinfoCount_coment == 1:
                                comentCount -= 1


                    viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if viewCount_infoCount == 0:
                        viewCountCheck = "0"
                    else:
                        viewCountCheck = "1"


                    dictinfo = {
                        'videoPK':int(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'videoPATH':videoPATH,
                        'viewable':viewable,
                        'likeCount':str(likeCount),
                        'comentCount':str(comentCount),
                        'userLikeCheck':userLikeCheck,
                        'viewCountCheck':viewCountCheck,
                        'size':size
                    }
                    videoinfoList.append(dictinfo)

            text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 검색 인풋 터치시 노출되는 리스트
@csrf_exempt
def searchHtml(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = str(data['loginUserPK'])

            now = date.today().isoformat()
            startDate = now + ' 00:00:00'
            startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            endDate = now + ' 23:59:59'
            endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')

    

            searchListinfoCount = SearchList.objects.filter(userPK = loginUserPK, status = "0").count()
            if searchListinfoCount == 0:
                featuredContentinfo = FeaturedContent.objects.filter(createAt__range=[startDate, endDate]).order_by('count')
                featuredContentinfoList = []
                for index, j in enumerate(featuredContentinfo):
                    contents = j.contents
                    featuredDictinfo = {'contents':contents}
                    featuredContentinfoList.append(featuredDictinfo)
                featuredContentinfoList = featuredContentinfoList[0:10]

                text = "최근 검색기록 없음"
                ment = "\033[92m"+"searchTest SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0', 'featuredContentinfoList':featuredContentinfoList}
                return HttpResponse(json.dumps(context))
            else:
                searchListinfo = SearchList.objects.filter(userPK = loginUserPK, status = "0").order_by('createAt')
                searchListinfoList = []
                for index, i in enumerate(searchListinfo):
                    searchListPK = i.id
                    searchContents = i.searchContents
                    dictinfo = {'searchListPK':str(searchListPK), 'searchContents':searchContents}
                    searchListinfoList.append(dictinfo)
                # searchListinfoList = searchListinfoList[0:10]
                searchListinfoList = searchListinfoList[-10:]

                featuredContentinfo = FeaturedContent.objects.filter(createAt__range=[startDate, endDate]).order_by('count')
                featuredContentinfoList = []
                for index, j in enumerate(featuredContentinfo):
                    contents = j.contents
                    featuredDictinfo = {'contents':contents}
                    featuredContentinfoList.append(featuredDictinfo)
                featuredContentinfoList = featuredContentinfoList[0:10]

            # searchListSubmit = SearchList(userPK = loginUserPK, searchContents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            # searchListSubmit.save()

            # featuredContentCount = FeaturedContent.objects.filter(contents = searchContents).count()
            # if featuredContentCount == 0:
            #     featuredContentSubmit = FeaturedContent(contents = searchContents, count = "0", createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            #     featuredContentSubmit.save()
            # else:
            #     featuredContentinfo = FeaturedContent.objects.get(contents = searchContents)
            #     count = int(featuredContentinfo.count)
            #     featuredContentinfo.count = str(count + 1)
            #     featuredContentinfo.save()

                text = "loginUser PK값 : " + loginUserPK
                ment = "\033[92m"+"searchHtml SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'searchListinfoList':searchListinfoList, 'featuredContentinfoList':featuredContentinfoList}

                return HttpResponse(json.dumps(context))
        else:
            loginUserPK = str(data['loginUserPK'])

            now = date.today().isoformat()
            startDate = now + ' 00:00:00'
            startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            endDate = now + ' 23:59:59'
            endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')

    

            searchListinfoCount = SearchList.objects.filter(userPK = loginUserPK, status = "0").count()
            if searchListinfoCount == 0:
                featuredContentinfo = FeaturedContent.objects.filter(createAt__range=[startDate, endDate]).order_by('count')
                featuredContentinfoList = []
                for index, j in enumerate(featuredContentinfo):
                    contents = j.contents
                    featuredDictinfo = {'contents':contents}
                    featuredContentinfoList.append(featuredDictinfo)
                featuredContentinfoList = featuredContentinfoList[0:10]

                text = "최근 검색기록 없음"
                ment = "\033[92m"+"searchTest SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0', 'featuredContentinfoList':featuredContentinfoList}
                return HttpResponse(json.dumps(context))
            else:
                searchListinfo = SearchList.objects.filter(userPK = loginUserPK, status = "0").order_by('createAt')
                searchListinfoList = []
                for index, i in enumerate(searchListinfo):
                    searchListPK = i.id
                    searchContents = i.searchContents
                    dictinfo = {'searchListPK':str(searchListPK), 'searchContents':searchContents}
                    searchListinfoList.append(dictinfo)
                # searchListinfoList = searchListinfoList[0:10]
                searchListinfoList = searchListinfoList[-10:]

                featuredContentinfo = FeaturedContent.objects.filter(createAt__range=[startDate, endDate]).order_by('count')
                featuredContentinfoList = []
                for index, j in enumerate(featuredContentinfo):
                    contents = j.contents
                    featuredDictinfo = {'contents':contents}
                    featuredContentinfoList.append(featuredDictinfo)
                featuredContentinfoList = featuredContentinfoList[0:10]

            # searchListSubmit = SearchList(userPK = loginUserPK, searchContents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            # searchListSubmit.save()

            # featuredContentCount = FeaturedContent.objects.filter(contents = searchContents).count()
            # if featuredContentCount == 0:
            #     featuredContentSubmit = FeaturedContent(contents = searchContents, count = "0", createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            #     featuredContentSubmit.save()
            # else:
            #     featuredContentinfo = FeaturedContent.objects.get(contents = searchContents)
            #     count = int(featuredContentinfo.count)
            #     featuredContentinfo.count = str(count + 1)
            #     featuredContentinfo.save()

                text = "loginUser PK값 : " + loginUserPK
                ment = "\033[92m"+"searchHtml SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'searchListinfoList':searchListinfoList, 'featuredContentinfoList':featuredContentinfoList}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"searchHtml Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





@csrf_exempt
def searchListDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            itemPK = data['itemPK']

            searchListinfo = SearchList.objects.get(id = itemPK)
            searchListinfo.status = "9"
            searchListinfo.save()            

            text = "itemPK값 : " + str(itemPK)
            ment = "\033[92m"+"searchListDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            itemPK = data['itemPK']

            searchListinfo = SearchList.objects.get(id = itemPK)
            searchListinfo.status = "9"
            searchListinfo.save()            

            text = "itemPK값 : " + str(itemPK)
            ment = "\033[92m"+"searchListDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"searchListDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))







# @csrf_exempt
# def contentsSearch(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         loginUserPK = str(data['loginUserPK'])
#         searchContents = str(data['searchContents'])
#         status = data['status']
#         if status == "0":
#             videoinfoCount = Video.objects.filter(viewable = "0").count()
#             if videoinfoCount == 0:
#                 text = "영상 없음 "
#                 ment = "\033[92m"+"searchTest WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfo = Video.objects.filter(viewable = "0").order_by('?')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     userPK = i.userPK
#                     videoPK = i.id
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     videoPATH = i.videoPATH
#                     # videoPATH = s3_videoPATH+videoPATH
#                     videoPATH = serverURL+"/static/video"+videoPATH
#                     contents = i.contents
#                     hashTag = i.hashTag
#                     viewable = i.viewable



#                     dictinfo = {
#                         'videoPK':str(videoPK), 
#                         'videoPATH':videoPATH,
#                     }
#                     videoinfoList.append(dictinfo)


#                 text = "영상 있음 "
#                 ment = "\033[92m"+"searchTest SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))
#         else:
#             if status == "1":
#                 # print("검색버튼 눌렀을때")

#                 videoinfoCount = Video.objects.filter(contents__contains = searchContents, viewable = "0").count()
#                 if videoinfoCount == 0:
#                     text = "comentONcoment PK값 : "
#                     ment = "\033[92m"+"searchTest WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2', 'videoinfoList':None}
#                     return HttpResponse(json.dumps(context))
#                 else:
#                     searchListCount = SearchList.objects.filter(userPK = loginUserPK, searchContents = searchContents).count()
#                     if searchListCount == 0:
#                         searchListSubmit = SearchList(userPK = loginUserPK, searchContents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                         searchListSubmit.save()
#                     else:
#                         searchListinfo = SearchList.objects.get(userPK = loginUserPK, searchContents = searchContents)
#                         searchListCount = int(searchListinfo.count)
#                         searchListinfo.count = str(searchListCount + 1)
#                         searchListinfo.status = "0"
#                         searchListinfo.createAt = datetime.now()
#                         searchListinfo.createAt_timestamp = str(round(time.time()))
#                         searchListinfo.save()

#                     featuredContentCount = FeaturedContent.objects.filter(contents = searchContents).count()
#                     if featuredContentCount == 0:
#                         featuredContentSubmit = FeaturedContent(contents = searchContents, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                         featuredContentSubmit.save()
#                     else:
#                         featuredContentinfo = FeaturedContent.objects.get(contents = searchContents)
#                         count = int(featuredContentinfo.count)
#                         featuredContentinfo.count = str(count + 1)
#                         featuredContentinfo.createAt = datetime.now()
#                         featuredContentinfo.createAt_timestamp = str(round(time.time()))
#                         featuredContentinfo.save()

#                     videoinfo = Video.objects.filter(contents__contains = searchContents, viewable = "0").order_by('?')
#                     videoinfoList = []
#                     for index, i in enumerate(videoinfo):
#                         userPK = i.userPK
#                         videoPK = i.id
#                         userinfo = SignUp.objects.get(id = userPK)
#                         username = userinfo.username
#                         nickName = userinfo.nickName
#                         profileIMG_path = userinfo.profileIMG_path
#                         if profileIMG_path:
#                             profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#                         else:
#                             profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                         videoPATH = i.videoPATH
#                         # videoPATH = s3_videoPATH+videoPATH
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         contents = i.contents
#                         hashTag = i.hashTag
#                         viewable = i.viewable



#                         dictinfo = {
#                             'videoPK':str(videoPK), 
#                             'videoPATH':videoPATH,
#                         }
#                         videoinfoList.append(dictinfo)            


#                     text = "comentONcoment PK값 : "
#                     ment = "\033[92m"+"searchTest SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1', 'videoinfoList':videoinfoList}
#                     return HttpResponse(json.dumps(context))
#             elif status == "2":
#                 # print("이전검색이나 추천콘텐츠 터치시")
#                 videoinfoCount = Video.objects.filter(contents__contains = searchContents, viewable = "0").count()
#                 if videoinfoCount == 0:
#                     text = "comentONcoment PK값 : "
#                     ment = "\033[92m"+"searchTest WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2', 'videoinfoList':None}
#                     return HttpResponse(json.dumps(context))
#                 else:
#                     videoinfo = Video.objects.filter(contents__contains = searchContents, viewable = "0").order_by('?')
#                     videoinfoList = []
#                     for index, i in enumerate(videoinfo):
#                         userPK = i.userPK
#                         videoPK = i.id
#                         userinfo = SignUp.objects.get(id = userPK)
#                         username = userinfo.username
#                         nickName = userinfo.nickName
#                         profileIMG_path = userinfo.profileIMG_path
#                         if profileIMG_path:
#                             profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#                         else:
#                             profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                         videoPATH = i.videoPATH
#                         # videoPATH = s3_videoPATH+videoPATH
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         contents = i.contents
#                         hashTag = i.hashTag
#                         viewable = i.viewable



#                         dictinfo = {
#                             'videoPK':str(videoPK), 
#                             'videoPATH':videoPATH,
#                         }
#                         videoinfoList.append(dictinfo)            


#                     text = "comentONcoment PK값 : "
#                     ment = "\033[92m"+"searchTest SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1', 'videoinfoList':videoinfoList}
#                     return HttpResponse(json.dumps(context))
                
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"searchTest Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))








@csrf_exempt
def featuredSearch(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            contents = data['contents']
            print("contents >>>>>>", contents)
            videoinfo = Video.objects.filter(contents__contains = contents, viewable = "0")
            # print(videoinfo)


            videoinfoList = []
            for index, i in enumerate(videoinfo):
                userPK = i.userPK
                videoPK = i.id
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # videoPATH = i.videoPATH
                # # videoPATH = s3_videoPATH+videoPATH
                # videoPATH = serverURL+"/static/video"+videoPATH
                videoPATH = i.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"


                contents = i.contents
                hashTag = i.hashTag
                viewable = i.viewable
                size = i.size



                dictinfo = {
                    'videoPK':str(videoPK), 
                    'videoPATH':videoPATH,
                    'size':size
                }
                videoinfoList.append(dictinfo)
            text = "contents  : " + contents
            ment = "\033[92m"+"featuredSearch SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
        else:
            contents = data['contents']
            print("contents >>>>>>", contents)
            videoinfo = Video.objects.filter(contents__contains = contents, viewable = "0")
            # print(videoinfo)


            videoinfoList = []
            for index, i in enumerate(videoinfo):
                userPK = i.userPK
                videoPK = i.id
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # videoPATH = i.videoPATH
                # # videoPATH = s3_videoPATH+videoPATH
                # videoPATH = serverURL+"/static/video"+videoPATH

                videoPATH = i.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"


                contents = i.contents
                hashTag = i.hashTag
                viewable = i.viewable
                size = i.size



                dictinfo = {
                    'videoPK':str(videoPK), 
                    'videoPATH':videoPATH,
                    'size':size
                }
                videoinfoList.append(dictinfo)
            text = "contents  : " + contents
            ment = "\033[92m"+"featuredSearch SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"featuredSearch Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 상대방 프로필 업로드한 비디오 리스트 TAb 분리
@csrf_exempt
def userProfile_videoListTab(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        userPK = data['userPK']
        userinfo = SignUp.objects.get(id = int(userPK))
        
        videoinfoCount = Video.objects.filter(userPK = userPK, status = "1").count()
        if videoinfoCount == 0:
            text = "등록한 영상 없음"
            ment = "\033[93m"+"userProfile WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'2', 'videoinfoCount':str(videoinfoCount), 'viewCountinfoCount':"0"}
            return HttpResponse(json.dumps(context))
        else:
            videoinfo = Video.objects.filter(userPK = userPK, status = "1").order_by('-id')
            videoinfoList = []
            for index, i in enumerate(videoinfo):
                videoPK = i.id
                viewCountinfoCount = ViewCount.objects.filter(userPK = userPK, videoPK = videoPK).count()



                videoPATH = i.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                # s3VideoPATH = i.s3VideoPATH
                thumbnailPATH = i.thumbnailPATH
                # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                thumbnailPATH = s3PATH + thumbnailPATH
                # thumbnailPATH = serverURL + "/static/" + thumbnailPATH
                size = i.size


                
                dictinfo = {'videoPK':videoPK, 'thumbnailPATH':thumbnailPATH, 'viewCountinfoCount':str(viewCountinfoCount), 'size':size}
                videoinfoList.append(dictinfo)
            

            text = "user PK값 : " + str(userPK) + ", 상대 유저정보 및 video정보 리스트 Response"
            ment = "\033[92m"+"userProfile SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'videoinfoList':videoinfoList, 'videoinfoCount':str(videoinfoCount)}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 상대방프로필에서 업로드한영상 상세
@csrf_exempt
def userProfile_videoDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        userPK = data['userPK']
    
        videoinfo = Video.objects.filter(Q(userPK = userPK, status = "1") | Q(userPK = userPK, status = "9")).order_by('-id')
        videoinfoList = []
        for index, i in enumerate(videoinfo):
            userPK = i.userPK
            videoPK = i.id
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            # s3Check = S3Check.objects.get(id = 1)
            # s3Status = s3Check.status

            # videoPATH = i.videoPATH
            # s3VideoPATH = i.s3VideoPATH
            # thumbnailPATH = i.thumbnailPATH
            
            # if s3Status == "0":
            #     videoPATH = serverURL+"/static/video"+videoPATH
            #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            # elif s3Status == "1":
            #     videoPATH = s3PATH+s3VideoPATH
            #     thumbnailPATH = s3PATH+thumbnailPATH


            videoPATH = i.videoPATH
            videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
            # s3VideoPATH = i.s3VideoPATH
            thumbnailPATH = i.thumbnailPATH
            # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
            thumbnailPATH = s3PATH + thumbnailPATH


            contents = i.contents
            hashTag = i.hashTag
            viewable = i.viewable
            userLikeCheck = ""
            viewCountCheck = ""
            size = i.size

            # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            # likeCount = str(like_video_infoCount)


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = like_video_infoCount
            if like_video_infoCount == 0:
                pass
            else:
                like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                for index, j in enumerate(like_video_info):
                    userPK_like = j.userPK
                    userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likevideo == 1:
                        likeCount -= 1


            like_video_infoCount_user = Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
            if like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                like_video_info_user = Like_video.objects.get(userPK = userPK, videoPK = videoPK)
                status = like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"

            # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            # comentCount = str(coment_infoCount)

            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1



            viewCount_infoCount = ViewCount.objects.filter(userPK = userPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"


            dictinfo = {
                'videoPK':str(videoPK), 
                'userPK':userPK, 
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'viewable':viewable,
                'likeCount':likeCount,
                'comentCount':comentCount,
                'userLikeCheck':userLikeCheck,
                'viewCountCheck':viewCountCheck,
                'size':size
            }
            videoinfoList.append(dictinfo)

        text = "\033[92m"+"userProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList}
        return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile_videoDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 상대방 프로필 업로드한 오디션 비디오 리스트
@csrf_exempt
def userProfile_auditionVideoTab(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userPK = data['userPK']

        auditionVideoinfoCount = Audition_video.objects.filter(userPK = userPK, status = "1").count()
        if auditionVideoinfoCount == 0:
            text = "user PK값 : " + str(userPK) + ", 등록한 영상 없음"
            ment = "\033[93m"+"userProfile_auditionVideoTab WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        else:
            auditionVideoinfo = Audition_video.objects.filter(userPK = userPK, status = "1").order_by('-id')
            auditionVideoinfoList = []
            for index, i in enumerate(auditionVideoinfo):
                videoPK = i.id
                auditionListPK = i.auditionListPK
                # thumbnailPATH = i.thumbnailPATH
                # thumbnailPATH = s3PATH+thumbnailPATH

                thumbnailPATH = i.thumbnailPATH
                # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                thumbnailPATH = s3PATH + thumbnailPATH



                audition_CountCount = Audition_Count.objects.filter(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK).count()
                viewcount = 0
                if audition_CountCount == 0:
                    viewcount = 0
                else:
                    audition_Count = Audition_Count.objects.filter(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK)
                    viewcount = audition_Count.viewcount


                dictinfo = {'videoPK':videoPK, 'thumbnailPATH':thumbnailPATH, 'viewcount':viewcount}
                auditionVideoinfoList.append(dictinfo)
            

            text = "user PK값 : " + str(userPK) + ", 유저정보 및 video정보 리스트 Response"
            ment = "\033[92m"+"userProfile_auditionVideoTab SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'auditionVideoinfoList':auditionVideoinfoList}
            return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile_auditionVideoTab Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 상대방프로필에서 -> 업로드한 오디션 영상 상세
@csrf_exempt
def userProfile_auditionVideoDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        userPK = data['userPK']
        videoPK = data['videoPK']
        auditionVideoinfo = Audition_video.objects.get(id = videoPK)
        ownerPK = auditionVideoinfo.userPK      # 여기선  userPK  이걸로 써도 되긴하지만 혹시몰라 video에서 가져옴
        userinfo = SignUp.objects.get(id = ownerPK)
        nickName = userinfo.nickName
        profileIMG_path = userinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3_profileimgPATH+profileIMG_path
        else:
            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

        auditionListPK = auditionVideoinfo.auditionListPK
        contents = auditionVideoinfo.contents
        hashTag = auditionVideoinfo.hashTag

        s3Check = S3Check.objects.get(id = 1)
        s3Status = s3Check.status

        videoPATH = auditionVideoinfo.videoPATH
        videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"



        

        auditionListinfoCount = Audition_List.objects.filter(id = auditionListPK).count()
        if auditionListinfoCount == 0:
            text = "\033[92m"+"userProfile_auditionVideoDetail SUCCESS -> 비디오 상세 -> 여기로오면 뭔가 잘못됨 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'auditionVideoDetail':auditionVideoDetail}
            return HttpResponse(json.dumps(context))
        else:
            auditionListinfo = Audition_List.objects.get(id = auditionListPK)
            auditionTitle = auditionListinfo.title

            audition_CountinfoCount = Audition_Count.objects.filter(ownerPK = userPK, videoPK = videoPK).count()
            likeCount = 0
            comentCount = 0
            if audition_CountinfoCount == 0:
                likeCount = 0
                comentCount = 0
            else:
                audition_Countinfo = Audition_Count.objects.filter(ownerPK = userPK, videoPK = videoPK)
                likeCount = 0
                comentCount = 0
                for index, i in enumerate(audition_Countinfo):
                    likeCount += int(i.like)
                    comentCount += int(i.coment)



            auditionVideoDetail = [{
                'videoPK':str(videoPK),
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'videoPATH':videoPATH,
                'contents':contents,
                'hashTag':hashTag,
                'auditionTitle':auditionTitle,
                'likeCount':likeCount,
                'comentCount':comentCount,
            }]
            

            text = "\033[92m"+"userProfile_auditionVideoDetail SUCCESS -> 비디오 상세 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'auditionVideoDetail':auditionVideoDetail}
            return HttpResponse(json.dumps(context))
        


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile_auditionVideoDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# # 상대방프로필에서 업로드한영상 상세
# @csrf_exempt
# def userProfile_videoDetail(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             userPK = data['userPK']
        
#             videoinfo = Video.objects.filter(Q(userPK = userPK, status = "1") | Q(userPK = userPK, status = "9")).order_by('-id')
#             videoinfoList = []
#             for index, i in enumerate(videoinfo):
#                 userPK = i.userPK
#                 videoPK = i.id
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 s3Check = S3Check.objects.get(id = 1)
#                 s3Status = s3Check.status

#                 videoPATH = i.videoPATH
#                 s3VideoPATH = i.s3VideoPATH
#                 thumbnailPATH = i.thumbnailPATH
                
#                 if s3Status == "0":
#                     videoPATH = serverURL+"/static/video"+videoPATH
#                     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                 elif s3Status == "1":
#                     videoPATH = s3PATH+s3VideoPATH
#                     thumbnailPATH = s3PATH+thumbnailPATH

#                 contents = i.contents
#                 hashTag = i.hashTag
#                 viewable = i.viewable
#                 userLikeCheck = ""
#                 viewCountCheck = ""

#                 # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 # likeCount = str(like_video_infoCount)


#                 like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 likeCount = like_video_infoCount
#                 if like_video_infoCount == 0:
#                     pass
#                 else:
#                     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     for index, j in enumerate(like_video_info):
#                         userPK_like = j.userPK
#                         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                         if userBlockListinfoCount_likevideo == 1:
#                             likeCount -= 1


#                 like_video_infoCount_user = Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                 if like_video_infoCount_user == 0:
#                     userLikeCheck = "0"
#                 else:
#                     like_video_info_user = Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                     status = like_video_info_user.status
#                     if status == "0":
#                         userLikeCheck = "0"
#                     elif status == "1":
#                         userLikeCheck = "1"

#                 # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = str(coment_infoCount)

#                 coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount
#                 if coment_infoCount == 0:
#                     pass
#                 else:
#                     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     for index, k in enumerate(coment_info):
#                         userPK_coment = k.userPK
#                         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                         if userBlockListinfoCount_coment == 1:
#                             comentCount -= 1



#                 viewCount_infoCount = ViewCount.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                 if viewCount_infoCount == 0:
#                     viewCountCheck = "0"
#                 else:
#                     viewCountCheck = "1"


#                 dictinfo = {
#                     'videoPK':str(videoPK), 
#                     'userPK':userPK, 
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'hashTag':hashTag,
#                     'videoPATH':videoPATH,
#                     'viewable':viewable,
#                     'likeCount':likeCount,
#                     'comentCount':comentCount,
#                     'userLikeCheck':userLikeCheck,
#                     'viewCountCheck':viewCountCheck
#                 }
#                 videoinfoList.append(dictinfo)

#             text = "\033[92m"+"userProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
#         else:
#             loginUserPK = data['loginUserPK']
#             userPK = data['userPK']
        
#             videoinfo = Video.objects.filter(Q(userPK = userPK, status = "1") | Q(userPK = userPK, status = "9")).order_by('-id')
#             videoinfoList = []
#             for index, i in enumerate(videoinfo):
#                 userPK = i.userPK
#                 videoPK = i.id
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 s3Check = S3Check.objects.get(id = 1)
#                 s3Status = s3Check.status

#                 videoPATH = i.videoPATH
#                 s3VideoPATH = i.s3VideoPATH
#                 thumbnailPATH = i.thumbnailPATH
                
#                 if s3Status == "0":
#                     videoPATH = serverURL+"/static/video"+videoPATH
#                     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                 elif s3Status == "1":
#                     videoPATH = s3PATH+s3VideoPATH
#                     thumbnailPATH = s3PATH+thumbnailPATH

#                 contents = i.contents
#                 hashTag = i.hashTag
#                 viewable = i.viewable
#                 userLikeCheck = ""
#                 viewCountCheck = ""

#                 # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 # likeCount = str(like_video_infoCount)


#                 like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 likeCount = like_video_infoCount
#                 if like_video_infoCount == 0:
#                     pass
#                 else:
#                     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     for index, j in enumerate(like_video_info):
#                         userPK_like = j.userPK
#                         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                         if userBlockListinfoCount_likevideo == 1:
#                             likeCount -= 1


#                 like_video_infoCount_user = Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                 if like_video_infoCount_user == 0:
#                     userLikeCheck = "0"
#                 else:
#                     like_video_info_user = Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                     status = like_video_info_user.status
#                     if status == "0":
#                         userLikeCheck = "0"
#                     elif status == "1":
#                         userLikeCheck = "1"

#                 # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = str(coment_infoCount)

#                 coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount
#                 if coment_infoCount == 0:
#                     pass
#                 else:
#                     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     for index, k in enumerate(coment_info):
#                         userPK_coment = k.userPK
#                         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                         if userBlockListinfoCount_coment == 1:
#                             comentCount -= 1



#                 viewCount_infoCount = ViewCount.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                 if viewCount_infoCount == 0:
#                     viewCountCheck = "0"
#                 else:
#                     viewCountCheck = "1"


#                 dictinfo = {
#                     'videoPK':str(videoPK), 
#                     'userPK':userPK, 
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'hashTag':hashTag,
#                     'videoPATH':videoPATH,
#                     'viewable':viewable,
#                     'likeCount':likeCount,
#                     'comentCount':comentCount,
#                     'userLikeCheck':userLikeCheck,
#                     'viewCountCheck':viewCountCheck
#                 }
#                 videoinfoList.append(dictinfo)

#             text = "\033[92m"+"userProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
        
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"userProfile_videoDetail Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))






# 유저 신고
@csrf_exempt
def userDeclaration(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            declarationkUserPK = data['declarationkUserPK']
            comment = data['comment']

            userDeclarationListSubmit = UserDeclarationList(loginUserPK = loginUserPK, declarationkUserPK = declarationkUserPK, comment = comment, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            userDeclarationListSubmit.save()

            text = str(loginUserPK) + " 유저가 -> " + str(declarationkUserPK) + " 유저 신고 -> 신고 사유 : " + comment
            ment = "\033[92m"+"userDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            loginUserPK = data['loginUserPK']
            declarationkUserPK = data['declarationkUserPK']
            comment = data['comment']

            userDeclarationListSubmit = UserDeclarationList(loginUserPK = loginUserPK, declarationkUserPK = declarationkUserPK, comment = comment, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            userDeclarationListSubmit.save()

            text = str(loginUserPK) + " 유저가 -> " + str(declarationkUserPK) + " 유저 신고 -> 신고 사유 : " + comment
            ment = "\033[92m"+"userDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userDeclaration Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# # 유저 차단
# @csrf_exempt
# def userBlock(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             blockUserPK = data['blockUserPK']

#             userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = blockUserPK).count()
#             if userBlockListinfoCount == 0:
#                 userBlockSubmit = UserBlockList(loginUserPK = loginUserPK, blockUserPK = blockUserPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 userBlockSubmit.save()

#                 text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#                 ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 userBlockListinfo = UserBlockList.objects.get(loginUserPK = loginUserPK, blockUserPK = blockUserPK)
#                 status = userBlockListinfo.status
#                 if status == "0":
#                     userBlockListinfo.createAt = datetime.now()
#                     userBlockListinfo.createAt_timestamp = str(round(time.time()))
#                     userBlockListinfo.status = "1"
#                     userBlockListinfo.save()

#                     text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#                     ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))

#                 elif status == "1":
#                     userBlockListinfo.status = "0"
#                     userBlockListinfo.save()

#                     text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단 해제"
#                     ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#         else:
#             loginUserPK = data['loginUserPK']
#             blockUserPK = data['blockUserPK']

#             userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = blockUserPK).count()
#             if userBlockListinfoCount == 0:
#                 userBlockSubmit = UserBlockList(loginUserPK = loginUserPK, blockUserPK = blockUserPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 userBlockSubmit.save()

#                 text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#                 ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 userBlockListinfo = UserBlockList.objects.get(loginUserPK = loginUserPK, blockUserPK = blockUserPK)
#                 status = userBlockListinfo.status
#                 if status == "0":
#                     userBlockListinfo.createAt = datetime.now()
#                     userBlockListinfo.createAt_timestamp = str(round(time.time()))
#                     userBlockListinfo.status = "1"
#                     userBlockListinfo.save()

#                     text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#                     ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))

#                 elif status == "1":
#                     userBlockListinfo.status = "0"
#                     userBlockListinfo.save()

#                     text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단 해제"
#                     ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"userBlock Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# # 유저 차단
# @csrf_exempt
# def userBlock(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         loginUserPK = data['loginUserPK']
#         blockUserPK = data['blockUserPK']

#         userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = blockUserPK).count()
#         print("userBlockListinfoCount >>>", userBlockListinfoCount)
#         if userBlockListinfoCount == 0:
#             userBlockSubmit = UserBlockList(loginUserPK = loginUserPK, blockUserPK = blockUserPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#             userBlockSubmit.save()

#             text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#             ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
#         else:
#             userBlockListinfo = UserBlockList.objects.get(loginUserPK = loginUserPK, blockUserPK = blockUserPK)
#             status = userBlockListinfo.status
#             if status == "0":
#                 userBlockListinfo.createAt = datetime.now()
#                 userBlockListinfo.createAt_timestamp = str(round(time.time()))
#                 userBlockListinfo.status = "1"
#                 userBlockListinfo.save()

#                 text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
#                 ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))

#             elif status == "1":
#                 userBlockListinfo.status = "0"
#                 userBlockListinfo.save()

#                 text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단 해제"
#                 ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"userBlock Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# # 유저 차단 리스트
# @csrf_exempt
# def userBlockList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']

#             userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK).count()
#             if userBlockListinfoCount == 0:
#                 text = "user PK값 : " + str(loginUserPK) + ", 차단한 유저 없음"
#                 ment = "\033[93m"+"userBlockList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))

#             else:
#                 userBlockListinfo = UserBlockList.objects.filter(loginUserPK = loginUserPK).order_by('-createAt')
#                 userBlockList = []
#                 for index, i in enumerate(userBlockListinfo):
#                     blockUserPK = i.blockUserPK
#                     createAt = str(i.createAt)
#                     blockuserinfo = SignUp.objects.get(id = blockUserPK)
#                     blockuserNickname = blockuserinfo.nickName
#                     profileIMG_path = blockuserinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {'blockUserPK':blockUserPK, 'blockuserNickname':blockuserNickname, 'profileIMG_path':profileIMG_path, 'blockDate':c}
#                     userBlockList.append(dictinfo)

#                 text = "user PK값 : " + str(loginUserPK) + ", 유저 차단 리스트"
#                 ment = "\033[92m"+"userBlockList SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1', 'userBlockList':userBlockList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             loginUserPK = data['loginUserPK']

#             userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK).count()
#             if userBlockListinfoCount == 0:
#                 text = "user PK값 : " + str(loginUserPK) + ", 차단한 유저 없음"
#                 ment = "\033[93m"+"userBlockList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))

#             else:
#                 userBlockListinfo = UserBlockList.objects.filter(loginUserPK = loginUserPK).order_by('-createAt')
#                 userBlockList = []
#                 for index, i in enumerate(userBlockListinfo):
#                     blockUserPK = i.blockUserPK
#                     createAt = str(i.createAt)
#                     blockuserinfo = SignUp.objects.get(id = blockUserPK)
#                     blockuserNickname = blockuserinfo.nickName
#                     profileIMG_path = blockuserinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {'blockUserPK':blockUserPK, 'blockuserNickname':blockuserNickname, 'profileIMG_path':profileIMG_path, 'blockDate':c}
#                     userBlockList.append(dictinfo)

#                 text = "user PK값 : " + str(loginUserPK) + ", 유저 차단 리스트"
#                 ment = "\033[92m"+"userBlockList SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1', 'userBlockList':userBlockList}
#                 return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"userBlockList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 유저 차단 리스트
@csrf_exempt
def userBlockList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']

        userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK).count()
        if userBlockListinfoCount == 0:
            text = "user PK값 : " + str(loginUserPK) + ", 차단한 유저 없음"
            ment = "\033[93m"+"userBlockList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))

        else:
            userBlockListinfo = UserBlockList.objects.filter(loginUserPK = loginUserPK).order_by('-createAt')
            userBlockList = []
            for index, i in enumerate(userBlockListinfo):
                blockUserPK = i.blockUserPK
                createAt = str(i.createAt)
                blockuserinfo = SignUp.objects.get(id = blockUserPK)
                blockuserNickname = blockuserinfo.nickName
                profileIMG_path = blockuserinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                b = datetime.fromtimestamp(float(timestamp))
                c = b.strftime('%Y-%m-%d %H:%M')

                dictinfo = {'blockUserPK':blockUserPK, 'blockuserNickname':blockuserNickname, 'profileIMG_path':profileIMG_path, 'blockDate':c}
                userBlockList.append(dictinfo)

            text = "user PK값 : " + str(loginUserPK) + ", 유저 차단 리스트"
            ment = "\033[92m"+"userBlockList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'userBlockList':userBlockList}
            return HttpResponse(json.dumps(context))
            


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userBlockList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# # 내 프로필 및 업로드한 비디오 리스트
# @csrf_exempt
# def myProfile(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:


#             loginUserPK = data['loginUserPK']
#             userinfo = SignUp.objects.get(id = int(loginUserPK))
#             username = userinfo.username
#             nickName = userinfo.nickName
#             point = userinfo.point
#             AboutMe = userinfo.AboutMe
#             if int(point) > 1000:
#                 point = str('{:,}'.format(int(point)))
#             profileIMG_path = userinfo.profileIMG_path
#             print("profileIMG_path >>", profileIMG_path)
#             if profileIMG_path:
#                 profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 # profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             link = userinfo.link

#             userinfoList = [{'username':username, 'nickName':nickName, 'profileIMG_path':profileIMG_path, 'point':point, 'AboutMe':AboutMe, 'link':link}]
#             videoinfoCount = Video.objects.filter(userPK = loginUserPK, status = "1").count()
#             if videoinfoCount == 0:
#                 text = "user PK값 : " + str(loginUserPK) + ", 등록한 영상 없음"
#                 ment = "\033[93m"+"myProfile WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')       
#                 context = {'code':'2', 'userinfoList':userinfoList, 'videoinfoCount':str(videoinfoCount), 'viewCountinfoCount':"0"}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfo = Video.objects.filter(userPK = loginUserPK, status = "1").order_by('-id')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     videoPK = i.id
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status
#                     videoPATH = i.videoPATH
#                     s3VideoPATH = i.s3VideoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     if s3Status == "0":
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     elif s3Status == "1":
#                         videoPATH = s3PATH+s3VideoPATH
#                         thumbnailPATH = s3PATH+thumbnailPATH

                    
                    


#                     viewCountinfoCount = ViewCount.objects.filter(videoPK = videoPK).count()


#                     dictinfo = {'thumbnailPATH':thumbnailPATH, 'videoPATH':videoPATH, 'viewCountinfoCount':str(viewCountinfoCount)}
#                     videoinfoList.append(dictinfo)
                

#                 text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
#                 ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1', 'userinfoList':userinfoList, 'videoinfoList':videoinfoList, 'videoinfoCount':str(videoinfoCount)}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             loginUserPK = data['loginUserPK']
#             userinfo = SignUp.objects.get(id = int(loginUserPK))
#             username = userinfo.username
#             nickName = userinfo.nickName
#             point = userinfo.point
#             AboutMe = userinfo.AboutMe
#             if int(point) > 1000:
#                 point = str('{:,}'.format(int(point)))
#             profileIMG_path = userinfo.profileIMG_path
#             print("profileIMG_path >>", profileIMG_path)
#             if profileIMG_path:
#                 profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 # profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             link = userinfo.link

#             userinfoList = [{'username':username, 'nickName':nickName, 'profileIMG_path':profileIMG_path, 'point':point, 'AboutMe':AboutMe, 'link':link}]
#             videoinfoCount = Video.objects.filter(userPK = loginUserPK, status = "1").count()
#             if videoinfoCount == 0:
#                 text = "user PK값 : " + str(loginUserPK) + ", 등록한 영상 없음"
#                 ment = "\033[93m"+"myProfile WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')       
#                 context = {'code':'2', 'userinfoList':userinfoList, 'videoinfoCount':str(videoinfoCount), 'viewCountinfoCount':"0"}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfo = Video.objects.filter(userPK = loginUserPK, status = "1").order_by('-id')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     videoPK = i.id
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status
#                     videoPATH = i.videoPATH
#                     s3VideoPATH = i.s3VideoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     if s3Status == "0":
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     elif s3Status == "1":
#                         videoPATH = s3PATH+s3VideoPATH
#                         thumbnailPATH = s3PATH+thumbnailPATH

                    
                    


#                     viewCountinfoCount = ViewCount.objects.filter(videoPK = videoPK).count()


#                     dictinfo = {'thumbnailPATH':thumbnailPATH, 'videoPATH':videoPATH, 'viewCountinfoCount':str(viewCountinfoCount)}
#                     videoinfoList.append(dictinfo)
                

#                 text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
#                 ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1', 'userinfoList':userinfoList, 'videoinfoList':videoinfoList, 'videoinfoCount':str(videoinfoCount)}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    


# # 내 프로필
# @csrf_exempt
# def myProfile(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         loginUserPK = data['loginUserPK']
#         userinfo = SignUp.objects.get(id = int(loginUserPK))
#         username = userinfo.username
#         nickName = userinfo.nickName
#         point = userinfo.point
#         AboutMe = userinfo.AboutMe
#         if int(point) > 1000:
#             point = str('{:,}'.format(int(point)))
#         profileIMG_path = userinfo.profileIMG_path
#         if profileIMG_path:
#             profileIMG_path = s3_profileimgPATH+profileIMG_path
#             # profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#         else:
#             profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#         link = userinfo.link

#         videoinfoCount = Video.objects.filter(userPK = loginUserPK, status = "1").count()
#         audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, status = "1").count()
        
#         allVideoCount = videoinfoCount + audition_videoinfoCount

#         userinfoList = [{'username':username, 'nickName':nickName, 'profileIMG_path':profileIMG_path, 'point':point, 'AboutMe':AboutMe, 'link':link, 'allVideoCount':allVideoCount}]


#         text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
#         ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'1', 'userinfoList':userinfoList}
#         return HttpResponse(json.dumps(context))
            

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))





# 내 프로필 업로드한 비디오 리스트 tab
@csrf_exempt
def myProfile_videoListTab(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        userinfo = SignUp.objects.get(id = int(loginUserPK))

        videoinfoCount = Video.objects.filter(userPK = loginUserPK, status = "1").count()
        if videoinfoCount == 0:
            text = "user PK값 : " + str(loginUserPK) + ", 등록한 영상 없음"
            ment = "\033[93m"+"myProfile WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'2', 'videoinfoCount':str(videoinfoCount), 'viewCountinfoCount':"0"}
            return HttpResponse(json.dumps(context))
        else:
            videoinfo = Video.objects.filter(userPK = loginUserPK, status = "1").order_by('-id')
            videoinfoList = []
            for index, i in enumerate(videoinfo):
                videoPK = i.id
                # s3Check = S3Check.objects.get(id = 1)
                # s3Status = s3Check.status
                # videoPATH = i.videoPATH
                # s3VideoPATH = i.s3VideoPATH
                # thumbnailPATH = i.thumbnailPATH
                # if s3Status == "0":
                #     videoPATH = serverURL+"/static/video"+videoPATH
                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                # elif s3Status == "1":
                #     videoPATH = s3PATH+s3VideoPATH
                #     thumbnailPATH = s3PATH+thumbnailPATH

                videoPATH = i.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                # s3VideoPATH = i.s3VideoPATH
                thumbnailPATH = i.thumbnailPATH
                # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                thumbnailPATH = s3PATH + thumbnailPATH
                # thumbnailPATH = serverURL + "/static/" + thumbnailPATH
                size = i.size


                viewCountinfoCount = ViewCount.objects.filter(videoPK = videoPK).count()


                dictinfo = {'videoPK':videoPK, 'thumbnailPATH':thumbnailPATH, 'viewCountinfoCount':str(viewCountinfoCount), 'size':size}
                videoinfoList.append(dictinfo)
            

            text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
            ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'videoinfoList':videoinfoList, 'videoinfoCount':str(videoinfoCount)}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# # 내프로필에서 업로드한영상 상세
# @csrf_exempt
# def myProfile_videoDetail(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
        
#             videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('-id')
#             videoinfoList = []
#             for index, i in enumerate(videoinfo):
#                 userPK = i.userPK
#                 videoPK = i.id
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 s3Check = S3Check.objects.get(id = 1)
#                 s3Status = s3Check.status

#                 videoPATH = i.videoPATH
#                 s3VideoPATH = i.s3VideoPATH
#                 thumbnailPATH = i.thumbnailPATH
                
#                 if s3Status == "0":
#                     videoPATH = serverURL+"/static/video"+videoPATH
#                     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                 elif s3Status == "1":
#                     videoPATH = s3PATH+s3VideoPATH
#                     thumbnailPATH = s3PATH+thumbnailPATH

#                 contents = i.contents
#                 hashTag = i.hashTag
#                 viewable = i.viewable
#                 likeCount = ""
#                 comentCount = ""
#                 userLikeCheck = ""
#                 viewCountCheck = ""

#                 # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 # likeCount = str(like_video_infoCount)


#                 like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 likeCount = like_video_infoCount
#                 if like_video_infoCount == 0:
#                     pass
#                 else:
#                     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     for index, j in enumerate(like_video_info):
#                         userPK_like = j.userPK
#                         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                         if userBlockListinfoCount_likevideo == 1:
#                             likeCount -= 1


#                 like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 if like_video_infoCount_user == 0:
#                     userLikeCheck = "0"
#                 else:
#                     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     status = like_video_info_user.status
#                     if status == "0":
#                         userLikeCheck = "0"
#                     elif status == "1":
#                         userLikeCheck = "1"

#                 # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = str(coment_infoCount)


#                 coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount
#                 if coment_infoCount == 0:
#                     pass
#                 else:
#                     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     for index, k in enumerate(coment_info):
#                         userPK_coment = k.userPK
#                         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                         if userBlockListinfoCount_coment == 1:
#                             comentCount -= 1


#                 viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 if viewCount_infoCount == 0:
#                     viewCountCheck = "0"
#                 else:
#                     viewCountCheck = "1"


#                 dictinfo = {
#                     'videoPK':str(videoPK), 
#                     'userPK':userPK, 
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'hashTag':hashTag,
#                     'videoPATH':videoPATH,
#                     'viewable':viewable,
#                     'likeCount':likeCount,
#                     'comentCount':comentCount,
#                     'userLikeCheck':userLikeCheck,
#                     'viewCountCheck':viewCountCheck
#                 }
#                 videoinfoList.append(dictinfo)

#             text = "\033[92m"+"myProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             loginUserPK = data['loginUserPK']
        
#             videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('-id')
#             videoinfoList = []
#             for index, i in enumerate(videoinfo):
#                 userPK = i.userPK
#                 videoPK = i.id
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3_profileimgPATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 s3Check = S3Check.objects.get(id = 1)
#                 s3Status = s3Check.status

#                 videoPATH = i.videoPATH
#                 s3VideoPATH = i.s3VideoPATH
#                 thumbnailPATH = i.thumbnailPATH
                
#                 if s3Status == "0":
#                     videoPATH = serverURL+"/static/video"+videoPATH
#                     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                 elif s3Status == "1":
#                     videoPATH = s3PATH+s3VideoPATH
#                     thumbnailPATH = s3PATH+thumbnailPATH

#                 contents = i.contents
#                 hashTag = i.hashTag
#                 viewable = i.viewable
#                 likeCount = ""
#                 comentCount = ""
#                 userLikeCheck = ""
#                 viewCountCheck = ""

#                 # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 # likeCount = str(like_video_infoCount)


#                 like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 likeCount = like_video_infoCount
#                 if like_video_infoCount == 0:
#                     pass
#                 else:
#                     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     for index, j in enumerate(like_video_info):
#                         userPK_like = j.userPK
#                         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                         if userBlockListinfoCount_likevideo == 1:
#                             likeCount -= 1


#                 like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 if like_video_infoCount_user == 0:
#                     userLikeCheck = "0"
#                 else:
#                     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     status = like_video_info_user.status
#                     if status == "0":
#                         userLikeCheck = "0"
#                     elif status == "1":
#                         userLikeCheck = "1"

#                 # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = str(coment_infoCount)


#                 coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount
#                 if coment_infoCount == 0:
#                     pass
#                 else:
#                     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     for index, k in enumerate(coment_info):
#                         userPK_coment = k.userPK
#                         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                         if userBlockListinfoCount_coment == 1:
#                             comentCount -= 1


#                 viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 if viewCount_infoCount == 0:
#                     viewCountCheck = "0"
#                 else:
#                     viewCountCheck = "1"


#                 dictinfo = {
#                     'videoPK':str(videoPK), 
#                     'userPK':userPK, 
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'hashTag':hashTag,
#                     'videoPATH':videoPATH,
#                     'viewable':viewable,
#                     'likeCount':likeCount,
#                     'comentCount':comentCount,
#                     'userLikeCheck':userLikeCheck,
#                     'viewCountCheck':viewCountCheck
#                 }
#                 videoinfoList.append(dictinfo)

#             text = "\033[92m"+"myProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"myProfile_videoDetail Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 내프로필에서 업로드한영상 상세
@csrf_exempt
def myProfile_videoDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
    
        videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('-id')
        videoinfoList = []
        for index, i in enumerate(videoinfo):
            userPK = i.userPK
            videoPK = i.id
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            # s3Check = S3Check.objects.get(id = 1)
            # s3Status = s3Check.status

            # videoPATH = i.videoPATH
            # s3VideoPATH = i.s3VideoPATH
            # thumbnailPATH = i.thumbnailPATH
            
            # if s3Status == "0":
            #     videoPATH = serverURL+"/static/video"+videoPATH
            #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            # elif s3Status == "1":
            #     videoPATH = s3PATH+s3VideoPATH
            #     thumbnailPATH = s3PATH+thumbnailPATH


            videoPATH = i.videoPATH
            videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
            # s3VideoPATH = i.s3VideoPATH
            thumbnailPATH = i.thumbnailPATH
            # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
            thumbnailPATH = s3PATH + thumbnailPATH


            contents = i.contents
            hashTag = i.hashTag
            viewable = i.viewable
            likeCount = ""
            comentCount = ""
            userLikeCheck = ""
            viewCountCheck = ""

            size = i.size

            # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            # likeCount = str(like_video_infoCount)


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = like_video_infoCount
            if like_video_infoCount == 0:
                pass
            else:
                like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                for index, j in enumerate(like_video_info):
                    userPK_like = j.userPK
                    userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likevideo == 1:
                        likeCount -= 1


            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"

            # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            # comentCount = str(coment_infoCount)


            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1


            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"


            dictinfo = {
                'videoPK':str(videoPK), 
                'userPK':userPK, 
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'viewable':viewable,
                'likeCount':likeCount,
                'comentCount':comentCount,
                'userLikeCheck':userLikeCheck,
                'viewCountCheck':viewCountCheck,
                'size':size
            }
            videoinfoList.append(dictinfo)

        text = "\033[92m"+"myProfile_videoDetail SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList}
        return HttpResponse(json.dumps(context))
        

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_videoDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 내 프로필 업로드한 오디션 비디오 리스트
@csrf_exempt
def myProfile_auditionVideoTab(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']

        auditionVideoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, status = "1").count()
        if auditionVideoinfoCount == 0:
            text = "user PK값 : " + str(loginUserPK) + ", 등록한 영상 없음"
            ment = "\033[93m"+"myProfile_auditionVideoTab WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        else:
            auditionVideoinfo = Audition_video.objects.filter(userPK = loginUserPK, status = "1").order_by('-id')
            auditionVideoinfoList = []
            for index, i in enumerate(auditionVideoinfo):
                videoPK = i.id
                auditionListPK = i.auditionListPK
                thumbnailPATH = i.thumbnailPATH
                # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                thumbnailPATH = s3PATH + thumbnailPATH
                


                audition_CountCount = Audition_Count.objects.filter(ownerPK = loginUserPK, auditionListPK = auditionListPK, videoPK = videoPK).count()
                viewcount = 0
                if audition_CountCount == 0:
                    viewcount = 0
                else:
                    audition_Count = Audition_Count.objects.get(ownerPK = loginUserPK, auditionListPK = auditionListPK, videoPK = videoPK)
                    viewcount = audition_Count.viewcount


                dictinfo = {'videoPK':videoPK, 'thumbnailPATH':thumbnailPATH, 'viewcount':viewcount}
                auditionVideoinfoList.append(dictinfo)
            

            text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
            ment = "\033[92m"+"myProfile_auditionVideoTab SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'auditionVideoinfoList':auditionVideoinfoList}
            return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_auditionVideoTab Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    





# 내프로필에서 -> 업로드한 오디션 영상 상세
@csrf_exempt
def myProfile_auditionVideoDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        auditionVideoinfo = Audition_video.objects.get(id = videoPK)
        ownerPK = auditionVideoinfo.userPK      # 여기선  loginUserPK  이걸로 써도 되긴하지만 혹시몰라 video에서 가져옴
        userinfo = SignUp.objects.get(id = ownerPK)
        nickName = userinfo.nickName
        profileIMG_path = userinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3_profileimgPATH+profileIMG_path
        else:
            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

        auditionListPK = auditionVideoinfo.auditionListPK
        contents = auditionVideoinfo.contents
        hashTag = auditionVideoinfo.hashTag

        s3Check = S3Check.objects.get(id = 1)
        s3Status = s3Check.status

        videoPATH = auditionVideoinfo.videoPATH
        videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"

        
        auditionListinfoCount = Audition_List.objects.filter(id = auditionListPK).count()
        if auditionListinfoCount == 0:
            text = "\033[92m"+"myProfile_auditionVideoDetail SUCCESS -> 비디오 상세 -> 여기로오면 뭔가 잘못됨 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'auditionVideoDetail':auditionVideoDetail}
            return HttpResponse(json.dumps(context))
        else:
            auditionListinfo = Audition_List.objects.get(id = auditionListPK)
            auditionTitle = auditionListinfo.title

            audition_CountinfoCount = Audition_Count.objects.filter(ownerPK = loginUserPK, videoPK = videoPK).count()
            likeCount = 0
            comentCount = 0
            if audition_CountinfoCount == 0:
                likeCount = 0
                comentCount = 0
            else:
                audition_Countinfo = Audition_Count.objects.filter(ownerPK = loginUserPK, videoPK = videoPK)
                likeCount = 0
                comentCount = 0
                for index, i in enumerate(audition_Countinfo):
                    likeCount += int(i.like)
                    comentCount += int(i.coment)



            auditionVideoDetail = [{
                'videoPK':str(videoPK),
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'videoPATH':videoPATH,
                'contents':contents,
                'hashTag':hashTag,
                'auditionTitle':auditionTitle,
                'likeCount':likeCount,
                'comentCount':comentCount,
            }]
            

            text = "\033[92m"+"myProfile_auditionVideoDetail SUCCESS -> 비디오 상세 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'auditionVideoDetail':auditionVideoDetail}
            return HttpResponse(json.dumps(context))
        


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_auditionVideoDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))































# 내 프로필 편집 페이지
@csrf_exempt
def myProfile_modifyinfo(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            
            loginUserPK = data['loginUserPK']
            # loginUserPK = "1"
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName
            name = userinfo.name
            link = userinfo.link
            aboutMe = userinfo.AboutMe
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                # profileIMG_path = s3_profileimgPATH+profileIMG_path
                profileIMG_path = s3_profileimgPATH+profileIMG_path

            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            userinfoList = [{'username':username, 'nickName':nickName, 'name':name, 'profileIMG_path':profileIMG_path, 'aboutMe':aboutMe, 'link':link}]

            text = "user PK값 : " + str(loginUserPK) + ", 유저정보 Response"
            ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'userinfoList':userinfoList}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            # loginUserPK = "1"
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName
            name = userinfo.name
            link = userinfo.link
            aboutMe = userinfo.AboutMe
            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                # profileIMG_path = s3_profileimgPATH+profileIMG_path
                profileIMG_path = s3_profileimgPATH+profileIMG_path

            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            userinfoList = [{'username':username, 'nickName':nickName, 'name':name, 'profileIMG_path':profileIMG_path, 'aboutMe':aboutMe, 'link':link}]

            text = "user PK값 : " + str(loginUserPK) + ", 유저정보 Response"
            ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'userinfoList':userinfoList}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 프로필 이미지 변경
# @csrf_exempt
# def modify_profileIMG(request):
#     try:
#         if request.method == 'POST':
#             loginUserPK = request.POST.get('loginUserPK')
#             reqFile = request.FILES
#             if len(reqFile['file']) != 0:
#                 file = request.FILES['file']
#                 s3_client = boto3.client(
#                     's3',
#                     aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",
#                     aws_secret_access_key = "hscX1K4FxEvJHceqpbGqyfRoJSnKKEITqMptb6x7"
#                 )
#                 imgPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                 userinfoinfoCount = SignUp.objects.filter(profileIMG_path=imgPATH).count()
#                 check = False
#                 if userinfoinfoCount == 0:
#                     url = 'profileIMG/'+imgPATH
#                     s3_client.upload_fileobj(
#                         file, 
#                         "showplus", 
#                         url, 
#                         ExtraArgs={
#                             "ContentType": file.content_type
#                         }
#                     )
#                     userinfo = SignUp.objects.get(id = loginUserPK)
#                     userinfo.profileIMG_path = imgPATH
#                     userinfo.save()

#                 else:
#                     while check == False:
#                         imgPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                         userinfoinfoCount_check = SignUp.objects.filter(profileIMG_path=imgPATH).count()
#                         if userinfoinfoCount_check == 0:
#                             check = True
#                             url = 'profileIMG/'+imgPATH
#                             s3_client.upload_fileobj(
#                                 file, 
#                                 "showplus", 
#                                 url, 
#                                 ExtraArgs={
#                                     "ContentType": file.content_type
#                                 }
#                             )
#                             break;
#                     userinfo = SignUp.objects.get(id = loginUserPK)
#                     userinfo.profileIMG_path = imgPATH
#                     userinfo.save()
#                 text = "user PK값 : " + str(loginUserPK) + ", 프로필 이미지 저장 완료"
#                 ment = "\033[92m"+"modify_profileIMG SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#             else:
#                 text = "user PK값 : " + str(loginUserPK) + ", 이미지 파일이 안넘어옴"
#                 ment = "\033[93m"+"modify_profileIMG WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"modify_profileIMG Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    
    


# # 프로필 이미지 임시 저장
@csrf_exempt
def modify_profileIMG_tmp(request):
    try:
        if request.method == 'POST':
            loginUserPK = request.POST.get('loginUserPK')
            reqFile = request.FILES
            print("reqFile >>", reqFile)
            print("reqFile >>", reqFile['file'])
            if len(reqFile['file']) != 0:
                img = request.FILES['file']
                splitdata = str(img).split('.')
                splitdata = splitdata[-1]
                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                inviteCode = inviteCode + '.' + splitdata

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)



                path = '/mnt/project/app/static/profileIMG/tmp/'+year+'/'+month+'/'+day+'/'+loginUserPK+'/'
                savePATH = 'profileIMG/profileIMG/tmp/' +year+'/'+month+'/'+day+'/'+loginUserPK+'/' + inviteCode

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = ""      # showplus
                )

                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(inviteCode)):
                    os.remove(path +str(inviteCode))
                with open(path +str(inviteCode), 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                imgPATH = path + inviteCode
                with open(imgPATH, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        savePATH, 
                        # ExtraArgs={
                        #     "ContentType": image_file.content_type
                        # }
                    )



                userinfo = SignUp.objects.get(id = loginUserPK)
                userinfo.profileIMG_path_tmp = savePATH
                userinfo.save()

                profileIMG_path_tmp = userinfo.profileIMG_path_tmp

                text = "user PK값 : " + str(loginUserPK) + ", 프로필 이미지 저장 완료"
                ment = "\033[92m"+"modify_profileIMG_tmp SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1', 'profileIMG_path_tmp':profileIMG_path_tmp}
                return HttpResponse(json.dumps(context, default=json_util.default))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 이미지 파일이 안넘어옴"
                ment = "\033[93m"+"modify_profileIMG_tmp WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_profileIMG_tmp Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 프로필 이미지 임시 저장 삭제
@csrf_exempt
def modify_profileIMG_tmpDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userinfo = SignUp.objects.get(id = loginUserPK)
        userinfo.profileIMG_path_tmp = None
        userinfo.save()

        text = "user PK값 : " + str(loginUserPK) + ", 임시 프로필 이미지 제거 완료"
        ment = "\033[92m"+"modify_profileIMG_tmpDel SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1'}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_profileIMG_tmpDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# # 프로필 이미지 변경
@csrf_exempt
def modify_profileIMG(request):
    try:
        if request.method == 'POST':
            loginUserPK = request.POST.get('loginUserPK')
            reqFile = request.FILES
            if len(reqFile['file']) != 0:
                img = request.FILES['file']
                splitdata = str(img).split('.')
                splitdata = splitdata[-1]
                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                inviteCode = inviteCode + '.' + splitdata

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)




                path = '/mnt/project/app/static/profileIMG/'+year+'/'+month+'/'+day+'/'+loginUserPK+'/'
                savePATH = 'profileIMG/profileIMG/' +year+'/'+month+'/'+day+'/'+loginUserPK+'/' + inviteCode

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = ""      # showplus
                )





                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(inviteCode)):
                    os.remove(path +str(inviteCode))
                with open(path +str(inviteCode), 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                imgPATH = path + inviteCode
                with open(imgPATH, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        savePATH, 
                        # ExtraArgs={
                        #     "ContentType": image_file.content_type
                        # }
                    )



                userinfo = SignUp.objects.get(id = loginUserPK)
                userinfo.profileIMG_path = savePATH
                userinfo.save()

                text = "user PK값 : " + str(loginUserPK) + ", 프로필 이미지 저장 완료"
                ment = "\033[92m"+"modify_profileIMG SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context, default=json_util.default))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 이미지 파일이 안넘어옴"
                ment = "\033[93m"+"modify_profileIMG WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_profileIMG Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 이름 변경 가능 여부 체크
@csrf_exempt
def modify_name_check(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousName = userinfo.name

            modiNameinfoCount = Modify_name.objects.filter(userPK = loginUserPK).count()
            if modiNameinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 이름 변경 가능"
                ment = "\033[92m"+"modify_name_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiNameinfo = Modify_name.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiNameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                previous_date = ""
                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'


                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 불가"
                    ment = "\033[93m"+"modify_name_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 가능"
                    ment = "\033[92m"+"modify_name_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousName = userinfo.name

            modiNameinfoCount = Modify_name.objects.filter(userPK = loginUserPK).count()
            if modiNameinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 이름 변경 가능"
                ment = "\033[92m"+"modify_name_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiNameinfo = Modify_name.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiNameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                previous_date = ""
                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'


                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 불가"
                    ment = "\033[93m"+"modify_name_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 가능"
                    ment = "\033[92m"+"modify_name_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_name_check Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 이름 변경
@csrf_exempt
def modify_name(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            newName = data['newName']
            userinfo = SignUp.objects.get(id = int(loginUserPK))
            previousName = userinfo.name

            modiNameinfoCount = Modify_name.objects.filter(userPK = loginUserPK).count()
            if modiNameinfoCount == 0:
                modiNameinfoSubmit = Modify_name(userPK = loginUserPK, previousName = previousName, newName = newName, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                modiNameinfoSubmit.save()
                userinfo.name = newName
                userinfo.save()
                text = "user PK값 : " + str(loginUserPK) + ", 최초 이름 변경 완료"
                ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiNameinfo = Modify_name.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiNameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 불가"
                    ment = "\033[93m"+"modify_name WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 가능"
                    ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    modiNameinfo.previousName = previousName
                    modiNameinfo.newName = newName
                    modiNameinfo.createAt = datetime.now()
                    modiNameinfo.createAt_timestamp = str(round(time.time()))
                    modiNameinfo.save()
                    userinfo.name = newName
                    userinfo.save()

                    text = "user PK값 : " + str(loginUserPK) + ", 이름 변경 완료"
                    ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
        else:
            loginUserPK = data['loginUserPK']
            newName = data['newName']
            userinfo = SignUp.objects.get(id = int(loginUserPK))
            previousName = userinfo.name

            modiNameinfoCount = Modify_name.objects.filter(userPK = loginUserPK).count()
            if modiNameinfoCount == 0:
                modiNameinfoSubmit = Modify_name(userPK = loginUserPK, previousName = previousName, newName = newName, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                modiNameinfoSubmit.save()
                userinfo.name = newName
                userinfo.save()
                text = "user PK값 : " + str(loginUserPK) + ", 최초 이름 변경 완료"
                ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiNameinfo = Modify_name.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiNameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 불가"
                    ment = "\033[93m"+"modify_name WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 이름 변경 가능"
                    ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    modiNameinfo.previousName = previousName
                    modiNameinfo.newName = newName
                    modiNameinfo.createAt = datetime.now()
                    modiNameinfo.createAt_timestamp = str(round(time.time()))
                    modiNameinfo.save()
                    userinfo.name = newName
                    userinfo.save()

                    text = "user PK값 : " + str(loginUserPK) + ", 이름 변경 완료"
                    ment = "\033[92m"+"modify_name SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_name Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 아이디 변경 가능 여부 체크
@csrf_exempt
def modify_username_check(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUsername = userinfo.username

            modiUsernameinfoCount = Modify_username.objects.filter(userPK = loginUserPK).count()
            if modiUsernameinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 가능"
                ment = "\033[92m"+"modify_username_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiUsernameinfo = Modify_username.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiUsernameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 30:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 불가"
                    ment = "\033[93m"+"modify_username_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 30:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 가능"
                    ment = "\033[92m"+"modify_username_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUsername = userinfo.username

            modiUsernameinfoCount = Modify_username.objects.filter(userPK = loginUserPK).count()
            if modiUsernameinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 가능"
                ment = "\033[92m"+"modify_username_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiUsernameinfo = Modify_username.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiUsernameinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 30:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 불가"
                    ment = "\033[93m"+"modify_username_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 30:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 가능"
                    ment = "\033[92m"+"modify_username_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_username_check Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 아이디 변경
@csrf_exempt
def modify_username(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            newUsername = data['newUsername']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUsername = userinfo.username

            userinfoCount = SignUp.objects.filter(username = newUsername).count()
            if userinfoCount == 0:
                modiUsernameinfoCount = Modify_username.objects.filter(userPK = loginUserPK).count()
                if modiUsernameinfoCount == 0:
                    modiUsernameinfoSubmit = Modify_username(userPK = loginUserPK, previousUsername = previousUsername, newUsername = newUsername, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                    modiUsernameinfoSubmit.save()
                    userinfo.username = newUsername
                    userinfo.save()
                    text = "user PK값 : " + str(loginUserPK) + ", 최초 아이디 변경 완료"
                    ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    modiUsernameinfo = Modify_username.objects.get(userPK = loginUserPK)
                    createAt_timestamp = int(modiUsernameinfo.createAt_timestamp)
                    now  = int(round(time.time()))
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)
                    previous = ""
                    if me_time < 1 :
                        previous = '방금전'
                        
                    elif me_time < 60 :
                        previous = str(me_time) + '분전'

                    elif me_timehour < 24 :
                        previous = str(me_timehour) + '시간전'
                    
                    elif me_timeday < 365 :
                        previous = str(me_timeday) + '일전'
                    
                    elif me_timeyear >= 1 : 
                        previous = str(me_timeyear) + '년전'

                    if me_timeday < 30:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 불가"
                        ment = "\033[93m"+"Modify_username WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'0'}
                        return HttpResponse(json.dumps(context))
                    elif me_timeday > 30:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 가능"
                        ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')

                        modiUsernameinfo.previousUsername = previousUsername
                        modiUsernameinfo.newUsername = newUsername
                        modiUsernameinfo.createAt = datetime.now()
                        modiUsernameinfo.createAt_timestamp = str(round(time.time()))
                        modiUsernameinfo.save()
                        userinfo.username = newUsername
                        userinfo.save()

                        text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 완료"
                        ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1'}
                        return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 중복된 아이디 있음; 아이디 변경 불가"
                ment = "\033[93m"+"Modify_username WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))    
            
        else:
            loginUserPK = data['loginUserPK']
            newUsername = data['newUsername']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUsername = userinfo.username

            userinfoCount = SignUp.objects.filter(username = newUsername).count()
            if userinfoCount == 0:
                modiUsernameinfoCount = Modify_username.objects.filter(userPK = loginUserPK).count()
                if modiUsernameinfoCount == 0:
                    modiUsernameinfoSubmit = Modify_username(userPK = loginUserPK, previousUsername = previousUsername, newUsername = newUsername, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                    modiUsernameinfoSubmit.save()
                    userinfo.username = newUsername
                    userinfo.save()
                    text = "user PK값 : " + str(loginUserPK) + ", 최초 아이디 변경 완료"
                    ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    modiUsernameinfo = Modify_username.objects.get(userPK = loginUserPK)
                    createAt_timestamp = int(modiUsernameinfo.createAt_timestamp)
                    now  = int(round(time.time()))
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)
                    previous = ""
                    if me_time < 1 :
                        previous = '방금전'
                        
                    elif me_time < 60 :
                        previous = str(me_time) + '분전'

                    elif me_timehour < 24 :
                        previous = str(me_timehour) + '시간전'
                    
                    elif me_timeday < 365 :
                        previous = str(me_timeday) + '일전'
                    
                    elif me_timeyear >= 1 : 
                        previous = str(me_timeyear) + '년전'

                    if me_timeday < 30:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 불가"
                        ment = "\033[93m"+"Modify_username WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'0'}
                        return HttpResponse(json.dumps(context))
                    elif me_timeday > 30:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 아이디 변경 가능"
                        ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')

                        modiUsernameinfo.previousUsername = previousUsername
                        modiUsernameinfo.newUsername = newUsername
                        modiUsernameinfo.createAt = datetime.now()
                        modiUsernameinfo.createAt_timestamp = str(round(time.time()))
                        modiUsernameinfo.save()
                        userinfo.username = newUsername
                        userinfo.save()

                        text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 완료"
                        ment = "\033[92m"+"Modify_username SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1'}
                        return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 중복된 아이디 있음; 아이디 변경 불가"
                ment = "\033[93m"+"Modify_username WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))     
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"Modify_username Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 닉네임 변경 가능 여부 체크
@csrf_exempt
def modify_userNick_check(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)

            modiUserNickinfoCount = Modify_userNick.objects.filter(userPK = loginUserPK).count()
            if modiUserNickinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 닉네임 변경 가능"
                ment = "\033[92m"+"modify_userNick_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiUserNickinfo = Modify_userNick.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiUserNickinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 불가"
                    ment = "\033[93m"+"modify_userNick_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 가능"
                    ment = "\033[92m"+"modify_userNick_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = data['loginUserPK']
            userinfo = SignUp.objects.get(id = loginUserPK)

            modiUserNickinfoCount = Modify_userNick.objects.filter(userPK = loginUserPK).count()
            if modiUserNickinfoCount == 0:
                text = "user PK값 : " + str(loginUserPK) + ", 닉네임 변경 가능"
                ment = "\033[92m"+"modify_userNick_check SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                modiUserNickinfo = Modify_userNick.objects.get(userPK = loginUserPK)
                createAt_timestamp = int(modiUserNickinfo.createAt_timestamp)
                now  = int(round(time.time()))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)
                previous = ""
                if me_time < 1 :
                    previous = '방금전'
                    
                elif me_time < 60 :
                    previous = str(me_time) + '분전'

                elif me_timehour < 24 :
                    previous = str(me_timehour) + '시간전'
                
                elif me_timeday < 365 :
                    previous = str(me_timeday) + '일전'
                
                elif me_timeyear >= 1 : 
                    previous = str(me_timeyear) + '년전'

                if me_timeday < 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 불가"
                    ment = "\033[93m"+"modify_userNick_check WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                elif me_timeday > 7:
                    text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 가능"
                    ment = "\033[92m"+"modify_userNick_check SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_userNick_check Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 닉네임 변경
@csrf_exempt
def modify_userNick(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            newUserNick = data['newUserNick']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUserNick = userinfo.nickName
            
            userinfoCount = SignUp.objects.filter(nickName = newUserNick).count()
            if userinfoCount == 0:
                modiUserNickinfoCount = Modify_userNick.objects.filter(userPK = loginUserPK).count()
                if modiUserNickinfoCount == 0:
                    modiUsernameinfoSubmit = Modify_userNick(userPK = loginUserPK, previousUserNick = previousUserNick, newUserNick = newUserNick, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                    modiUsernameinfoSubmit.save()
                    userinfo.nickName = newUserNick
                    userinfo.save()
                    text = "user PK값 : " + str(loginUserPK) + ", 최초 닉네임 변경 완료"
                    ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else: 
                    modiUserNickinfo = Modify_userNick.objects.get(userPK = loginUserPK)
                    createAt_timestamp = int(modiUserNickinfo.createAt_timestamp)
                    now  = int(round(time.time()))
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)
                    previous = ""
                    if me_time < 1 :
                        previous = '방금전'
                        
                    elif me_time < 60 :
                        previous = str(me_time) + '분전'

                    elif me_timehour < 24 :
                        previous = str(me_timehour) + '시간전'
                    
                    elif me_timeday < 365 :
                        previous = str(me_timeday) + '일전'
                    
                    elif me_timeyear >= 1 : 
                        previous = str(me_timeyear) + '년전'

                    if me_timeday < 7:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 불가"
                        ment = "\033[93m"+"modify_userNick WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'0'}
                        return HttpResponse(json.dumps(context))
                    elif me_timeday > 7:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 가능"
                        ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        modiUserNickinfo.previousUserNick = previousUserNick
                        modiUserNickinfo.newUserNick = newUserNick
                        modiUserNickinfo.createAt = datetime.now()
                        modiUserNickinfo.createAt_timestamp = str(round(time.time()))
                        modiUserNickinfo.save()
                        userinfo.nickName = newUserNick
                        userinfo.save()

                        text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 완료"
                        ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1'}
                        return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 중복된 닉네임 있음; 아이디 변경 불가"
                ment = "\033[93m"+"modify_userNick WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            newUserNick = data['newUserNick']
            userinfo = SignUp.objects.get(id = loginUserPK)
            previousUserNick = userinfo.nickName
            
            userinfoCount = SignUp.objects.filter(nickName = newUserNick).count()
            if userinfoCount == 0:
                modiUserNickinfoCount = Modify_userNick.objects.filter(userPK = loginUserPK).count()
                if modiUserNickinfoCount == 0:
                    modiUsernameinfoSubmit = Modify_userNick(userPK = loginUserPK, previousUserNick = previousUserNick, newUserNick = newUserNick, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                    modiUsernameinfoSubmit.save()
                    userinfo.nickName = newUserNick
                    userinfo.save()
                    text = "user PK값 : " + str(loginUserPK) + ", 최초 닉네임 변경 완료"
                    ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else: 
                    modiUserNickinfo = Modify_userNick.objects.get(userPK = loginUserPK)
                    createAt_timestamp = int(modiUserNickinfo.createAt_timestamp)
                    now  = int(round(time.time()))
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)
                    previous = ""
                    if me_time < 1 :
                        previous = '방금전'
                        
                    elif me_time < 60 :
                        previous = str(me_time) + '분전'

                    elif me_timehour < 24 :
                        previous = str(me_timehour) + '시간전'
                    
                    elif me_timeday < 365 :
                        previous = str(me_timeday) + '일전'
                    
                    elif me_timeyear >= 1 : 
                        previous = str(me_timeyear) + '년전'

                    if me_timeday < 7:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 불가"
                        ment = "\033[93m"+"modify_userNick WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'0'}
                        return HttpResponse(json.dumps(context))
                    elif me_timeday > 7:
                        text = "user PK값 : " + str(loginUserPK) + ", 변경한지 "+previous+"; 닉네임 변경 가능"
                        ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        modiUserNickinfo.previousUserNick = previousUserNick
                        modiUserNickinfo.newUserNick = newUserNick
                        modiUserNickinfo.createAt = datetime.now()
                        modiUserNickinfo.createAt_timestamp = str(round(time.time()))
                        modiUserNickinfo.save()
                        userinfo.nickName = newUserNick
                        userinfo.save()

                        text = "user PK값 : " + str(loginUserPK) + ", 아이디 변경 완료"
                        ment = "\033[92m"+"modify_userNick SUCCESS -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')
                        context = {'code':'1'}
                        return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 중복된 닉네임 있음; 아이디 변경 불가"
                ment = "\033[93m"+"modify_userNick WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_userNick Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 자기소개 변경
@csrf_exempt
def modify_AboutMe(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            aboutMe = data['aboutMe']
            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.AboutMe = aboutMe
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 자기소개 변경 완료"
            ment = "\033[92m"+"modify_AboutMe SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            aboutMe = data['aboutMe']
            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.AboutMe = aboutMe
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 자기소개 변경 완료"
            ment = "\033[92m"+"modify_AboutMe SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_AboutMe Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 링크 변경
@csrf_exempt
def modify_link(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            link = data['link']
            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.link = link
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 링크 변경 완료"
            ment = "\033[92m"+"modify_link SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            link = data['link']
            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.link = link
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 링크 변경 완료"
            ment = "\033[92m"+"modify_link SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"modify_link Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    





# # 내가등록한 영상리스트 현황 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 )
# @csrf_exempt
# def myVideoList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             # page = int(data['page'])
#             # pageStart = (page - 1) * 10
#             # pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             videoinfoCount = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
#             if videoinfoCount == 0:
#                 text = "내가 업로드한 비디오 리스트 없음"
#                 ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:        
#                 # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
#                 videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     userPK = i.userPK
#                     videoPK = i.id
#                     status = i.status
#                     createAt = str(i.createAt)
#                     comment = i.comment
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         # profileIMG_path = s3_profileimgPATH+profileIMG_path
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path

#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     # videoPATH = i.videoPATH
#                     # s3VideoPATH = i.s3VideoPATH
#                     # thumbnailPATH = i.thumbnailPATH
#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+s3VideoPATH
#                     #     thumbnailPATH = s3PATH+thumbnailPATH

#                     videoPATH = i.videoPATH
#                     videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
#                     # s3VideoPATH = i.s3VideoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"

#                     print("thumbnailPATH >>>>", thumbnailPATH)


#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {
#                         'videoPK':str(videoPK),
#                         'thumbnailPATH':thumbnailPATH,
#                         'dateTime':c,
#                         'status':status,
#                         'comment':comment
#                     }
#                     videoinfoList.append(dictinfo)

#                     # contents = i.contents
#                     # hashTag = i.hashTag
#                     # viewable = i.viewable
#                     # likeCount = ""
#                     # comentCount = ""
#                     # userLikeCheck = ""
#                     # viewCountCheck = ""

#                     # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     # likeCount = str(like_video_infoCount)

#                     # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if like_video_infoCount_user == 0:
#                     #     userLikeCheck = "0"
#                     # else:
#                     #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     #     status = like_video_info_user.status
#                     #     if status == "0":
#                     #         userLikeCheck = "0"
#                     #     elif status == "1":
#                     #         userLikeCheck = "1"

#                     # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                     # comentCount = str(coment_infoCount)

#                     # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if viewCount_infoCount == 0:
#                     #     viewCountCheck = "0"
#                     # else:
#                     #     viewCountCheck = "1"


#                     # dictinfo = {
#                     #     'videoPK':str(videoPK), 
#                     #     'userPK':userPK, 
#                     #     'username':username,
#                     #     'nickName':nickName,
#                     #     'profileIMG_path':profileIMG_path,
#                     #     'contents':contents,
#                     #     'hashTag':hashTag,
#                     #     'videoPATH':videoPATH,
#                     #     'viewable':viewable,
#                     #     'likeCount':likeCount,
#                     #     'comentCount':comentCount,
#                     #     'userLikeCheck':userLikeCheck,
#                     #     'viewCountCheck':viewCountCheck
#                     # }
#                     # videoinfoList.append(dictinfo)
                    
#                 text = "\033[92m"+"myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))

#         else:
#             # page = int(data['page'])
#             # pageStart = (page - 1) * 10
#             # pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             videoinfoCount = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
#             if videoinfoCount == 0:
#                 text = "내가 업로드한 비디오 리스트 없음"
#                 ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:        
#                 # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
#                 videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     userPK = i.userPK
#                     videoPK = i.id
#                     status = i.status
#                     createAt = str(i.createAt)
#                     comment = i.comment
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         # profileIMG_path = s3_profileimgPATH+profileIMG_path
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path

#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i.videoPATH
#                     s3VideoPATH = i.s3VideoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status
#                     if s3Status == "0":
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     elif s3Status == "1":
#                         videoPATH = s3PATH+s3VideoPATH
#                         thumbnailPATH = s3PATH+thumbnailPATH


#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {
#                         'videoPK':str(videoPK),
#                         'thumbnailPATH':thumbnailPATH,
#                         'dateTime':c,
#                         'status':status,
#                         'comment':comment
#                     }
#                     videoinfoList.append(dictinfo)

#                     # contents = i.contents
#                     # hashTag = i.hashTag
#                     # viewable = i.viewable
#                     # likeCount = ""
#                     # comentCount = ""
#                     # userLikeCheck = ""
#                     # viewCountCheck = ""

#                     # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     # likeCount = str(like_video_infoCount)

#                     # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if like_video_infoCount_user == 0:
#                     #     userLikeCheck = "0"
#                     # else:
#                     #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     #     status = like_video_info_user.status
#                     #     if status == "0":
#                     #         userLikeCheck = "0"
#                     #     elif status == "1":
#                     #         userLikeCheck = "1"

#                     # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                     # comentCount = str(coment_infoCount)

#                     # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if viewCount_infoCount == 0:
#                     #     viewCountCheck = "0"
#                     # else:
#                     #     viewCountCheck = "1"


#                     # dictinfo = {
#                     #     'videoPK':str(videoPK), 
#                     #     'userPK':userPK, 
#                     #     'username':username,
#                     #     'nickName':nickName,
#                     #     'profileIMG_path':profileIMG_path,
#                     #     'contents':contents,
#                     #     'hashTag':hashTag,
#                     #     'videoPATH':videoPATH,
#                     #     'viewable':viewable,
#                     #     'likeCount':likeCount,
#                     #     'comentCount':comentCount,
#                     #     'userLikeCheck':userLikeCheck,
#                     #     'viewCountCheck':viewCountCheck
#                     # }
#                     # videoinfoList.append(dictinfo)
                    
#                 text = "\033[92m"+"myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"myVideoList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))





# 내가등록한 영상리스트 현황 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 )
@csrf_exempt
def myVideoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # page = int(data['page'])
        # pageStart = (page - 1) * 10
        # pageEnd = 10 * page
        loginUserPK = data['loginUserPK']
        videoinfoCount = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
        if videoinfoCount == 0:
            text = "내가 업로드한 비디오 리스트 없음"
            ment = "\033[93m"+"videoList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'videoinfoList':None}
            return HttpResponse(json.dumps(context))
        else:        
            # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
            videoinfo = Video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
            videoinfoList = []
            for index, i in enumerate(videoinfo):
                userPK = i.userPK
                videoPK = i.id
                status = i.status
                createAt = str(i.createAt)
                comment = i.comment
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    # profileIMG_path = s3_profileimgPATH+profileIMG_path
                    profileIMG_path = s3_profileimgPATH+profileIMG_path

                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # videoPATH = i.videoPATH
                # s3VideoPATH = i.s3VideoPATH
                # thumbnailPATH = i.thumbnailPATH
                # s3Check = S3Check.objects.get(id = 1)
                # s3Status = s3Check.status
                # if s3Status == "0":
                #     videoPATH = serverURL+"/static/video"+videoPATH
                #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                # elif s3Status == "1":
                #     videoPATH = s3PATH+s3VideoPATH
                #     thumbnailPATH = s3PATH+thumbnailPATH

                videoPATH = i.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                # s3VideoPATH = i.s3VideoPATH
                thumbnailPATH = i.thumbnailPATH
                print("thumbnailPATH >>>", thumbnailPATH)
                # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
                thumbnailPATH = s3PATH + thumbnailPATH
                size = i.size
                print("thumbnailPATH >>>>", thumbnailPATH)


                timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                b = datetime.fromtimestamp(float(timestamp))
                c = b.strftime('%Y-%m-%d %H:%M')

                dictinfo = {
                    'videoPK':str(videoPK),
                    'videoPATH':videoPATH,
                    'thumbnailPATH':thumbnailPATH,
                    'dateTime':c,
                    'status':status,
                    'comment':comment,
                    'size':size
                }
                videoinfoList.append(dictinfo)

                # contents = i.contents
                # hashTag = i.hashTag
                # viewable = i.viewable
                # likeCount = ""
                # comentCount = ""
                # userLikeCheck = ""
                # viewCountCheck = ""

                # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                # likeCount = str(like_video_infoCount)

                # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                # if like_video_infoCount_user == 0:
                #     userLikeCheck = "0"
                # else:
                #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                #     status = like_video_info_user.status
                #     if status == "0":
                #         userLikeCheck = "0"
                #     elif status == "1":
                #         userLikeCheck = "1"

                # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                # comentCount = str(coment_infoCount)

                # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                # if viewCount_infoCount == 0:
                #     viewCountCheck = "0"
                # else:
                #     viewCountCheck = "1"


                # dictinfo = {
                #     'videoPK':str(videoPK), 
                #     'userPK':userPK, 
                #     'username':username,
                #     'nickName':nickName,
                #     'profileIMG_path':profileIMG_path,
                #     'contents':contents,
                #     'hashTag':hashTag,
                #     'videoPATH':videoPATH,
                #     'viewable':viewable,
                #     'likeCount':likeCount,
                #     'comentCount':comentCount,
                #     'userLikeCheck':userLikeCheck,
                #     'viewCountCheck':viewCountCheck
                # }
                # videoinfoList.append(dictinfo)
                
            text = "\033[92m"+"myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))




    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myVideoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# # 내가등록한 영상리스트 현황 디테일 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 -> 썸내일 터치 )
# @csrf_exempt
# def myVideoListDetail(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username
#             nickName = userinfo.nickName
#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3_profileimgPATH+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             videoPATH = videoinfo.videoPATH
#             videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"

#             thumbnailPATH = videoinfo.thumbnailPATH
#             thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
#             # s3Check = S3Check.objects.get(id = 1)
#             # s3Status = s3Check.status
#             # if s3Status == "0":
#             #     videoPATH = serverURL+"/static/video"+videoPATH
#             #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#             # elif s3Status == "1":
#             #     s3VideoPATH = videoinfo.s3VideoPATH
#             #     videoPATH = s3PATH+s3VideoPATH
#             #     thumbnailPATH = s3PATH+thumbnailPATH



            

            

#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag


#             like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#             likeCount = str(like_video_infoCount)


#             coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#             comentCount = str(coment_infoCount)

#             viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()



#             videoinfoList = [{
#                 'videoPK':videoPK,
#                 'nickName':nickName,
#                 'profileIMG_path':profileIMG_path,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'videoPATH':videoPATH,
#             }]
#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username
#             nickName = userinfo.nickName
#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3_profileimgPATH+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             videoPATH = videoinfo.videoPATH
#             thumbnailPATH = videoinfo.thumbnailPATH
#             s3Check = S3Check.objects.get(id = 1)
#             s3Status = s3Check.status
#             if s3Status == "0":
#                 videoPATH = serverURL+"/static/video"+videoPATH
#                 thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#             elif s3Status == "1":
#                 s3VideoPATH = videoinfo.s3VideoPATH
#                 videoPATH = s3PATH+s3VideoPATH
#                 thumbnailPATH = s3PATH+thumbnailPATH


#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag


#             like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#             likeCount = str(like_video_infoCount)


#             coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#             comentCount = str(coment_infoCount)

#             viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()



#             videoinfoList = [{
#                 'videoPK':videoPK,
#                 'nickName':nickName,
#                 'profileIMG_path':profileIMG_path,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'videoPATH':videoPATH,
#             }]
#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"myVideoListDetail Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))






# 내가등록한 영상리스트 현황 디테일 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 -> 썸내일 터치 )
@csrf_exempt
def myVideoListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
    
        videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
        
        videoPK = videoinfo.id
        status = videoinfo.status
        createAt = str(videoinfo.createAt)
        comment = videoinfo.comment
        userinfo = SignUp.objects.get(id = loginUserPK)
        username = userinfo.username
        nickName = userinfo.nickName
        profileIMG_path = userinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3_profileimgPATH+profileIMG_path
        else:
            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

        videoPATH = videoinfo.videoPATH
        videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
        
        thumbnailPATH = videoinfo.thumbnailPATH
        # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
        thumbnailPATH = s3PATH + thumbnailPATH
        # s3Check = S3Check.objects.get(id = 1)
        # s3Status = s3Check.status
        # if s3Status == "0":
        #     videoPATH = serverURL+"/static/video"+videoPATH
        #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
        # elif s3Status == "1":
        #     s3VideoPATH = videoinfo.s3VideoPATH
        #     videoPATH = s3PATH+s3VideoPATH
        #     thumbnailPATH = s3PATH+thumbnailPATH

        contents = videoinfo.contents
        hashTag = videoinfo.hashTag
        size = videoinfo.size


        like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
        likeCount = str(like_video_infoCount)


        coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
        comentCount = str(coment_infoCount)

        viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()



        videoinfoList = [{
            'videoPK':videoPK,
            'nickName':nickName,
            'profileIMG_path':profileIMG_path,
            'contents':contents,
            'hashTag':hashTag,
            'videoPATH':videoPATH,
            'size':size
        }]
        # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
            
        text = "\033[92m"+"myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList}
        return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myVideoListDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    








#  내가등록한 영상 삭제
@csrf_exempt
def myVideoDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfoCount = Video.objects.filter(id = videoPK, userPK = loginUserPK).count()
            if videoinfoCount == 0:
                text = "값이 잘못 넘어옴; 이러면 안되는데??"
                ment = "\033[93m"+"myVideoDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            else:
                videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
                videoinfo.status = "5"
                videoinfo.save()

                text = "\033[92m"+"myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfoCount = Video.objects.filter(id = videoPK, userPK = loginUserPK).count()
            if videoinfoCount == 0:
                text = "값이 잘못 넘어옴; 이러면 안되는데??"
                ment = "\033[93m"+"myVideoDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            else:
                videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
                videoinfo.status = "5"
                videoinfo.save()

                text = "\033[92m"+"myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myVideoDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# 설정 - 휴대폰번호 변경
@csrf_exempt
def settings_modiPhoneNum(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            phone = data['phone']
            CI = data['CI']
            DI = data['DI']

            userinfo = SignUp.objects.get(id = loginUserPK)
            previousCI = userinfo.CI
            previousDI = userinfo.DI

            if CI == previousCI and DI == previousDI:
                userinfo.phone = phone
                userinfo.save()
                text = "user PK값 : " + str(loginUserPK) + ", CI, DI 일치 -- 전화번호 업데이트 완료"
                ment = "\033[92m"+"settings_modiPhoneNum SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", CI, DI 불일치"
                ment = "\033[93m"+"settings_modiPhoneNum WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            phone = data['phone']
            CI = data['CI']
            DI = data['DI']

            userinfo = SignUp.objects.get(id = loginUserPK)
            previousCI = userinfo.CI
            previousDI = userinfo.DI

            if CI == previousCI and DI == previousDI:
                userinfo.phone = phone
                userinfo.save()
                text = "user PK값 : " + str(loginUserPK) + ", CI, DI 일치 -- 전화번호 업데이트 완료"
                ment = "\033[92m"+"settings_modiPhoneNum SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", CI, DI 불일치"
                ment = "\033[93m"+"settings_modiPhoneNum WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_modiPhoneNum Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 설정 - 이전 비밀번호 체크
@csrf_exempt
def settings_pwCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            pw = data['pw']
            userinfo = SignUp.objects.get(id = loginUserPK)
            password = userinfo.password
            checkPW = check_password(pw, password)
            if checkPW:
                text = "user PK값 : " + str(loginUserPK) + ", 이전 비밀번호 체크 완료"
                ment = "\033[92m"+"settings_pwCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 이전 비밀번호 불일치"
                ment = "\033[92m"+"settings_pwCheck WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            pw = data['pw']
            userinfo = SignUp.objects.get(id = loginUserPK)
            password = userinfo.password
            checkPW = check_password(pw, password)
            if checkPW:
                text = "user PK값 : " + str(loginUserPK) + ", 이전 비밀번호 체크 완료"
                ment = "\033[92m"+"settings_pwCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "user PK값 : " + str(loginUserPK) + ", 이전 비밀번호 불일치"
                ment = "\033[92m"+"settings_pwCheck WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_pwCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 설정 - 비밀번호 변경
@csrf_exempt
def settings_changePW(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            newPassword = data['newPassword']

            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.set_password(newPassword)
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 비밀번호 변경 완료"
            ment = "\033[92m"+"settings_changePW SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            newPassword = data['newPassword']

            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.set_password(newPassword)
            userinfo.save()

            text = "user PK값 : " + str(loginUserPK) + ", 비밀번호 변경 완료"
            ment = "\033[92m"+"settings_changePW SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_changePW Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 설정 - 스타회원 전환 신청
@csrf_exempt
def settings_changeMembership(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            grade = userinfo.grade
            if grade == "1" or grade == "2" or grade == "5" or grade == "9":
                if grade == "5":
                    membershipListinfo = MembershipList.objects.get(userPK = loginUserPK)
                    endDate = str(membershipListinfo.endDate)
                    timestamp = time.mktime(datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')
                    text = "user PK값 : " + str(loginUserPK) + ", " + c + " 이후 가능;"
                    ment = "\033[93m"+"settings_changeMembership WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'5', 'endDate':c}
                    return HttpResponse(json.dumps(context))
                else:
                    text = "loginUserPK PK값 : " + str(loginUserPK) + " 이미 스타회원 전환 신청했거나, 스타회원인 유저"
                    ment = "\033[92m"+"settings_changeMembership WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
            else:
                userinfo.grade = "1"
                userinfo.save()
                text = "loginUserPK PK값 : " + str(loginUserPK) + " 스타회원 전환 신청"
                ment = "\033[92m"+"settings_changeMembership SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            grade = userinfo.grade
            if grade == "1" or grade == "2" or grade == "5" or grade == "9":
                if grade == "5":
                    membershipListinfo = MembershipList.objects.get(userPK = loginUserPK)
                    endDate = str(membershipListinfo.endDate)
                    timestamp = time.mktime(datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')
                    text = "user PK값 : " + str(loginUserPK) + ", " + c + " 이후 가능;"
                    ment = "\033[93m"+"settings_changeMembership WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'5', 'endDate':c}
                    return HttpResponse(json.dumps(context))
                else:
                    text = "loginUserPK PK값 : " + str(loginUserPK) + " 이미 스타회원 전환 신청했거나, 스타회원인 유저"
                    ment = "\033[92m"+"settings_changeMembership WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
            else:
                userinfo.grade = "1"
                userinfo.save()
                text = "loginUserPK PK값 : " + str(loginUserPK) + " 스타회원 전환 신청"
                ment = "\033[92m"+"settings_changeMembership SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 설정 - 유저 탈퇴전 보유 STAR 체크
@csrf_exempt
def settings_userSignOut_starCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            point = userinfo.point

            if int(point) > 10:
                text = "user PK값 : " + str(loginUserPK) + ", 보유스타 10이상; 탈퇴불가"
                ment = "\033[92m"+"settings_userSignOut_starCheck WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            elif int(point) <= 10:
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", 보유스타 10이하; 탈퇴가능"
                ment = "\033[92m"+"settings_userSignOut_starCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            point = userinfo.point

            if int(point) > 10:
                text = "user PK값 : " + str(loginUserPK) + ", 보유스타 10이상; 탈퇴불가"
                ment = "\033[92m"+"settings_userSignOut_starCheck WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            elif int(point) <= 10:
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", 보유스타 10이하; 탈퇴가능"
                ment = "\033[92m"+"settings_userSignOut_starCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context)) 


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_userSignOut_starCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 설정 - 유저 탈퇴
@csrf_exempt
def settings_userSignOut(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.grade = "9"
            userinfo.CI = None
            userinfo.DI = None
            userinfo.save()


            text = "loginUserPK PK값 : " + str(loginUserPK) + " 탈퇴"
            ment = "\033[92m"+"settings_userSignOut SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']

            userinfo = SignUp.objects.get(id = loginUserPK)
            userinfo.grade = "9"
            userinfo.CI = None
            userinfo.DI = None
            userinfo.save()


            text = "loginUserPK PK값 : " + str(loginUserPK) + " 탈퇴"
            ment = "\033[92m"+"settings_userSignOut SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_userSignOut Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# # tournament
# @csrf_exempt
# def testAAAAA(request):
#     try:
#         auditionListinfoCount = Audition_List.objects.all().count()
#         if auditionListinfoCount == 0:
#             print("DB에 저장된 정보 없음 ( 토너먼트 없음 )")
#         else:
#             auditionListinfo_progressCheck = Audition_List.objects.filter(progressStatus = "1").count()
#             if auditionListinfo_progressCheck == 0:
#                 print("진행중인 토너먼트 없음")
#                 auditionListinfo = Audition_List.objects.filter(progressStatus = "0")
#                 for index, i in enumerate(auditionListinfo):
#                     now  = datetime.now()
#                     startDate = i.startAt
#                     if startDate <= now:
#                         print("진행해야할 토너먼트 있음")
#                         i.progressStatus = "1"
#                         i.save()
#                     else:
#                         print("진행해야할 토너먼트 없음")
#             else:
#                 print("진행중인 토너먼트 있음")
#                 auditionListinfo = Audition_List.objects.get(progressStatus = "1")
#                 now  = datetime.now()
#                 endDate = auditionListinfo.endAt
#                 if endDate <= now:
#                     print("종료될 토너먼트 있음")
#                     auditionListinfo.progressStatus = "9"
#                     auditionListinfo.save()
#                 else:
#                     categoryListinfo = CategoryList.objects.filter()
#                     for index, n in enumerate(categoryListinfo):
#                         categoryPK = n.id
#                         auditionListinfoPK = auditionListinfo.id
#                         auditionDetailListinfo_category_count = Audition_DetailList.objects.filter(auditionListPK = auditionListinfoPK, category = categoryPK).count()
#                         if auditionDetailListinfo_category_count == 0:
#                             print("오디션 카테고리 없음")
#                         else:
#                             print("오디션 카테고리 있음")
#                             auditionDetailListinfo_category = Audition_DetailList.objects.filter(auditionListPK = auditionListinfoPK, category = categoryPK)
#                             for index, j in enumerate(auditionDetailListinfo_category):
#                                 now  = datetime.now()
#                                 progressStatus = j.progressStatus
#                                 startDate = j.startDate
#                                 endDate = j.endDate
#                                 tournamentStatus = j.tournamentStatus
#                                 if startDate <= now:
#                                     if endDate >= now:
#                                         if progressStatus == "0":
#                                             print("오디션 시작할게 있음")
#                                             j.progressStatus = "1"
#                                             j.save()
#                                             if int(tournamentStatus) >= 2:
#                                                 sum = int(tournamentStatus) - 1
#                                                 updateCheck = Audition_DetailList.objects.get(auditionListPK = auditionListinfoPK, category = categoryPK, tournamentStatus = str(sum))
#                                                 updateCheck.progressStatus = "3"
#                                                 updateCheck.save()
#                                         elif progressStatus == "1":
#                                             print("오디션 정상 진행 중")
#                                         else:
#                                             print("몰?루")
#                                     else:
#                                         if progressStatus == "1":
#                                             j.progressStatus = "2"
#                                             j.save()

#                                             audition_videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListinfoPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus).count()
#                                             if audition_videoinfoCount == 0:
#                                                 print("토너먼트영상이 없음")
#                                             else:
#                                                 print("토너먼트 분배 짜야함")
#                                                 audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListinfoPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                                                 allCountList = []
                                                
#                                                 for index, n in enumerate(audition_videoinfo):
#                                                     userPK = n.userPK
#                                                     videoPK = n.id
#                                                     audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                                                     audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                                                     audition_viewcount_infoCount = Audition_ViewCount.objects.filter(videoPK = videoPK).count()
#                                                     sum = audition_like_video_infoCount + audition_coment_infoCount + audition_viewcount_infoCount
#                                                     dictinfo = {"userPK":userPK, "LC":audition_like_video_infoCount, "CC":audition_coment_infoCount, "VC":audition_viewcount_infoCount, "AC":sum}
#                                                     allCountList.append(dictinfo)

#                                                 slicingCount = 0
#                                                 if tournamentStatus == "1":
#                                                     slicingCount = 32
#                                                 elif tournamentStatus == "2":
#                                                     slicingCount = 16
#                                                 elif tournamentStatus == "3":
#                                                     slicingCount = 8
#                                                 elif tournamentStatus == "4":
#                                                     slicingCount = 4
#                                                 elif tournamentStatus == "5":
#                                                     slicingCount = 2
#                                                 elif tournamentStatus == "6":
#                                                     slicingCount = 1
                                                
#                                                 allCountList = sorted(allCountList, key=lambda x: x['AC'], reverse=True)[0:slicingCount]
#                                                 # print(allCountList)
#                                                 allCountListLen = len(allCountList)
#                                                 while allCountListLen != 0:
#                                                     samplelist_L = random.sample(allCountList, 1)
#                                                     samplelist_L0 = samplelist_L[0]
#                                                     userPK_left = samplelist_L0['userPK']
#                                                     versusListinfo = VersusList(userPK_left = userPK_left, auditionListPK = auditionListinfoPK, categoryPK = categoryPK, tournamentStatus = int(tournamentStatus) + 1)
#                                                     versusListinfo.save()
#                                                     allCountList.remove(samplelist_L0)

#                                                     samplelist_R = random.sample(allCountList, 1)
#                                                     samplelist_R0 = samplelist_R[0]
#                                                     userPK_right = samplelist_R0['userPK']
#                                                     versusListinfo = VersusList.objects.get(id = versusListinfo.id)
#                                                     versusListinfo.userPK_right = userPK_right
#                                                     versusListinfo.save()
#                                                     allCountList.remove(samplelist_R0)
#                                                     if len(allCountList) == 0:
#                                                         break

#         text = "테스트"
#         ment = "\033[92m"+"testAAAAA SUCCESS -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'1'}
#         return HttpResponse(json.dumps(context))
            
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"testAAAAA Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    






@csrf_exempt
def auditionHtml(request):
    try:
        return render(request, 'audition.html', {})
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"auditionHtml Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return render(request, 'auditionHtml.html',context)



# # 오디션 동영상 업로드
# @csrf_exempt
# def audition_fileupload(request):
#     try:
#         if request.method == 'POST':
#             userPK = str(request.POST.get('userPK'))
#             category = request.POST.get('category')
#             viewable = request.POST.get('viewable')
#             reqFile = request.FILES
#             newimgpath = ""
#             if len(reqFile['file']) != 0:
#                 audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#                 audition_ListPK = str(audition_List_info.id)
#                 file = request.FILES['file']
#                 s3_client = boto3.client(
#                     's3',
#                     # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
#                     # aws_secret_access_key = "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"        # ygbs
#                     aws_access_key_id     = "AKIATCKASMRTO26B7DGI",                         # showplus
#                     aws_secret_access_key = "SH9TxcPqhIvxNuo9oTMtDS8qVvuCOCk2APaw2xgo"      # showplus
#                 )
#                 videoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                 videoinfoCount = Audition_video.objects.filter(videoPATH=videoPATH).count()
#                 check = False
#                 if videoinfoCount == 0:
#                     url = 'auditionVideos/'+videoPATH
#                     s3_client.upload_fileobj(
#                         file, 
#                         "showplus", 
#                         url, 
#                         ExtraArgs={
#                             "ContentType": file.content_type
#                         }
#                     )
#                     AuditionVideoSubmit = Audition_video(userPK = userPK, auditionListPK = audition_ListPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), videoPATH = videoPATH, viewable = viewable)
#                     AuditionVideoSubmit.save()

#                 else:
#                     while check == False:
#                         videoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                         videoinfoCount_check = Audition_video.objects.filter(videoPATH=videoPATH).count()
#                         if videoinfoCount_check == 0:
#                             check = True
#                             url = 'auditionVideos/'+videoPATH
#                             s3_client.upload_fileobj(
#                                 file, 
#                                 "showplus", 
#                                 url, 
#                                 ExtraArgs={
#                                     "ContentType": file.content_type
#                                 }
#                             )
#                             break;
#                     AuditionVideoSubmit = Audition_video(userPK = userPK, auditionListPK = audition_ListPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), videoPATH = videoPATH, viewable = viewable)
#                     AuditionVideoSubmit.save()

#                 text = "user PK값 : " + userPK + ", 동영상 저장 완료"
#                 ment = "\033[92m"+"fileupload SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#             else:
#                 text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
#                 ment = "\033[93m"+"fileupload WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'9'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"fileupload Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# 나를 팔로우 한 유저 리스트
@csrf_exempt
def audition_uploadCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']

            audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK).count()
            if audition_videoinfoCount == 0:
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
                ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            else:
                audition_videoinfoDelCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK, status = "5").count()
                if audition_videoinfoCount == audition_videoinfoDelCount:
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
                    ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                else:                
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 불가"
                    ment = "\033[93m"+"audition_uploadCheck WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']

            audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK).count()
            if audition_videoinfoCount == 0:
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
                ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))
            else:
                audition_videoinfoDelCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK, status = "5").count()
                if audition_videoinfoCount == audition_videoinfoDelCount:
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
                    ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'0'}
                    return HttpResponse(json.dumps(context))
                else:                
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 불가"
                    ment = "\033[93m"+"audition_uploadCheck WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_uploadCheck Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 오디션 동영상 업로드
@csrf_exempt
def audition_fileupload(request):
    try:
        if request.method == 'POST':
            userPK = str(request.POST.get('loginUserPK'))
            contents = request.POST.get('contents')
            hashTag = request.POST.get('hashTag')
            location = request.POST.get('location')
            viewable = request.POST.get('viewable')
            categoryPK = request.POST.get('categoryPK')
            tournamentStatus = request.POST.get('tournamentStatus')
            auditionListPK = request.POST.get('auditionListPK')
            rewardRate = request.POST.get('rewardRate')
            reqFile = request.FILES
            print("reqFile >>", reqFile)
            if len(reqFile['file']) != 0:
                img = request.FILES['file']
                print("img >>>", img)


                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                inviteCode = inviteCode + ".jpg"
                userinfoCount = Audition_video.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                check = False
                if userinfoCount == 0:
                    pass
                else:
                    while check == False:
                        inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                        inviteCode = inviteCode + ".jpg"
                        userinfoCount_check = SignUp.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                        if userinfoCount_check == 0:
                            check = True
                            break;

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'



                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = ""      # showplus
                )
                s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))



                videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + s3VideoPATH

                s3_client.upload_fileobj(
                    img, 
                    bucketName, 
                    videoURL, 
                    ExtraArgs={
                        "ContentType": img.content_type
                    }
                )
                
                # -----------------------------------------------------------

                count = 1
                test = 1
                train = 1
                vidcap = cv2.VideoCapture(s3PATH+videoURL)
                thumbnailPath = '/mnt/project/app/static/auditions/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
                if not os.path.exists(thumbnailPath):
                    os.makedirs(thumbnailPath)
                
                thumbnail_savePATH = ""
                
                while(vidcap.isOpened()):
                    ret, image = vidcap.read()
                    if(ret==False):
                        break
                    if(int(vidcap.get(1)) % 5 == 0):
                        num=count % 10
                        thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                        print("thumbnail_savePATH >>", thumbnail_savePATH)
                        cv2.imwrite(thumbnailPath + inviteCode, image)
                        break;
                vidcap.release()



                thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH
                thumbnailimg = thumbnailPath + inviteCode
                with open(thumbnailimg, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        thumbnailURL, 
                        # ExtraArgs={
                        #     "ContentType": image_file.content_type
                        # }
                    )


                savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

                if hashTag == "":
                    hashTag = None

                videoSubmit = Audition_video(
                    userPK = userPK, 
                    createAt = datetime.now(), 
                    createAt_timestamp = str(round(time.time())), 
                    thumbnailPATH = thumbnailURL, 
                    videoPATH = videoURL, 
                    # s3VideoPATH = videoURL,
                    contents = contents, 
                    hashTag = hashTag,
                    location = location,
                    viewable = viewable,
                    categoryPK = categoryPK,
                    tournamentStatus = tournamentStatus,
                    auditionListPK = auditionListPK,
                    rewardRate = str(rewardRate)
                )
                videoSubmit.save()
                
                videoPK = videoSubmit.id
                Audition_CountSubmit = Audition_Count(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK)
                Audition_CountSubmit.save()

                text = "user PK값 : " + userPK + ", 동영상 저장 완료"
                ment = "\033[92m"+"fileupload SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context, default=json_util.default))

            else:
                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"fileupload WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"fileupload Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# # 오디션 동영상 업로드
# @csrf_exempt
# def audition_fileupload(request):
#     try:
#         if request.method == 'POST':
#             userPK = str(request.POST.get('userPK'))
#             category = request.POST.get('category')
#             viewable = request.POST.get('viewable')

#             reqFile = request.FILES
#             newimgpath = ""
#             if len(reqFile['file']) != 0:
                
#                 audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#                 audition_ListPK = str(audition_List_info.id)

#                 img = request.FILES['file']
#                 splitdata = str(img).split('.')

#                 now = datetime.now()
#                 year = str(now.year)
#                 month = str(now.month)
#                 day = str(now.day)

#                 path = '/mnt/project/app/static/audition_video/'+year+'/'+month+'/'+day+'/'+userPK+'/'

#                 if not os.path.exists(path):
#                     os.makedirs(path)
#                 if os.path.isfile(path +str(img)):
#                     os.remove(path +str(img))
#                 with open(path +str(img), 'wb+') as destination:
#                     for chunk in img.chunks():
#                         destination.write(chunk)
#                 savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)
#                 AuditionVideoSubmit = Audition_video(userPK = userPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), videoPATH = savePATH, viewable = viewable)
#                 AuditionVideoSubmit.save()

#                 text = "user PK값 : " + userPK + ", 동영상 저장 완료"
#                 ment = "\033[92m"+"audition_fileupload SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#             else:
#                 text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
#                 ment = "\033[93m"+"audition_fileupload WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'9'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_fileupload Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    


@csrf_exempt
def auditionMainHtml(request):
    try:
        return render(request, 'auditionMain.html', {})
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"auditionMain Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return render(request, 'auditionMain.html',context)
    


# 오디션 카테고리 리스트 ( 오디션 첫 페이지 )
@csrf_exempt
def audition_categoryList(request):
    try:
        categoryListinfoCount = CategoryList.objects.filter(status = "0").count()
        if categoryListinfoCount == 0:
            text = "카테고리 없음"
            ment = "\033[93m"+"audition_categoryList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2', 'categoryList':None}
            return HttpResponse(json.dumps(context))        
        else:
            categoryListinfo = CategoryList.objects.filter(status = "0")
            categoryList = []
            for index, i in enumerate(categoryListinfo):
                categoryPK = i.id
                categoryName = i.category
                categoryImgPATH = i.categoryImgPATH
                if categoryImgPATH:
                    categoryImgPATH = serverURL+"/static/categoryIMG"+categoryImgPATH


                dictinfo = {'categoryPK':categoryPK, 'categoryName':categoryName, 'categoryImgPATH':categoryImgPATH}
                categoryList.append(dictinfo)



            text = "\033[92m"+"audition_categoryList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'categoryList':categoryList}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_categoryList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 오디션 카테고리2 리스트 
@csrf_exempt
def audition_auditionList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            categoryPK = data['categoryPK']
            categoryName = data['categoryName']


            auditionListinfoCount = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9").count()

            if auditionListinfoCount == 0:
                text = "오디션 없음"
                ment = "\033[93m"+"audition_auditionList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'auditionList':None}
                return HttpResponse(json.dumps(context))        
            else:
                auditionListinfo = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9")
                auditionList = []
                for index, i in enumerate(auditionListinfo):
                    auditionListPK = i.id
                    tournamentStatusPK = i.tournamentStatusPK
                    TournamentStatusListinfo = TournamentStatusList.objects.get(status = tournamentStatusPK)
                    tournamentStatus = TournamentStatusListinfo.status
                    progressStatus = i.progressStatus
                    title = i.title
                    auditionImgPATH = i.auditionImgPATH
                    if auditionImgPATH:
                        auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH


                    dictinfo = {'auditionListPK':auditionListPK, 'tournamentStatusPK':tournamentStatusPK, 'tournamentStatus':tournamentStatus, 'progressStatus':progressStatus, 'title':title, 'auditionImgPATH':auditionImgPATH}
                    auditionList.append(dictinfo)



                text = "\033[92m"+"audition_auditionList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'categoryName':categoryName, 'auditionList':auditionList}
                return HttpResponse(json.dumps(context))

        else:
            categoryPK = data['categoryPK']
            categoryName = data['categoryName']


            auditionListinfoCount = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9").count()

            if auditionListinfoCount == 0:
                text = "오디션 없음"
                ment = "\033[93m"+"audition_auditionList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'auditionList':None}
                return HttpResponse(json.dumps(context))        
            else:
                auditionListinfo = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9")
                auditionList = []
                for index, i in enumerate(auditionListinfo):
                    auditionListPK = i.id
                    tournamentStatusPK = i.tournamentStatusPK
                    TournamentStatusListinfo = TournamentStatusList.objects.get(status = tournamentStatusPK)
                    tournamentStatus = TournamentStatusListinfo.status
                    progressStatus = i.progressStatus
                    title = i.title
                    auditionImgPATH = i.auditionImgPATH
                    if auditionImgPATH:
                        auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH


                    dictinfo = {'auditionListPK':auditionListPK, 'tournamentStatusPK':tournamentStatusPK, 'tournamentStatus':tournamentStatus, 'progressStatus':progressStatus, 'title':title, 'auditionImgPATH':auditionImgPATH}
                    auditionList.append(dictinfo)



                text = "\033[92m"+"audition_auditionList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'categoryName':categoryName, 'auditionList':auditionList}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_auditionList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# # 오디션 비디오 리스트
# @csrf_exempt
# def audition_videoList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         page = int(data['page'])
#         pageStart = (page - 1) * 10
#         pageEnd = 10 * page
#         loginUserPK = data['loginUserPK']
#         auditionListPK = data['auditionListPK']
#         categoryListPK = data['categoryListPK']
#         tournamentPK = data['tournamentPK']

#         # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")

#         videoinfoCount = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1", status = "1").count()
#         if videoinfoCount == 0:
#             text = "비디오 리스트 없음"
#             ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#             context = {'code':'0', 'videoinfoList':None}
#             return HttpResponse(json.dumps(context))
#         else:        
#             # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
#             audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1", status = "1").order_by('?')
#             audition_videoinfoList = []
#             for index, i in enumerate(audition_videoinfo):
#                 userPK = i.userPK
#                 videoPK = i.id
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path

#                 videoPATH = i.videoPATH
#                 # videoPATH = s3_audition_videoPATH+videoPATH
#                 videoPATH = serverURL+"/static/audition_video"+videoPATH
#                 contents = i.contents
#                 hashTag = i.hashTag
#                 viewable = i.viewable
#                 likeCount = ""
#                 comentCount = ""
#                 userLikeCheck = ""

#                 audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                 likeCount = str(audition_like_video_infoCount)

#                 audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 if audition_like_video_infoCount_user == 0:
#                     userLikeCheck = "0"
#                 else:
#                     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     status = audition_like_video_info_user.status
#                     if status == "0":
#                         userLikeCheck = "0"
#                     elif status == "1":
#                         userLikeCheck = "1"

#                 audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                 comentCount = str(audition_coment_infoCount)

#                 # audition_coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 # if audition_coment_infoCount_user == 0:
#                 #     userComentCheck = "0"
#                 # else:
#                 #     userComentCheck = "1"
                    


#                 dictinfo = {
#                     'videoPK':str(videoPK), 
#                     'userPK':userPK, 
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'hashTag':hashTag,
#                     'videoPATH':videoPATH,
#                     'viewable':viewable,
#                     'likeCount':likeCount,
#                     'comentCount':comentCount,
#                     'userLikeCheck':userLikeCheck,
#                 }
#                 audition_videoinfoList.append(dictinfo)
#             text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'audition_videoinfoList':audition_videoinfoList}
#             return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_videoList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    

# 오디션 비디오 리스트
@csrf_exempt
def audition_videoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            page = int(data['page'])
            pageStart = (page - 1) * 21
            pageEnd = 21 * page
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']
            categoryPK = data['categoryPK']

            # loginUserPK = data['loginUserPK']
            # auditionListPK = data['auditionListPK']
            # categoryListPK = data['categoryListPK']
            # tournamentPK = data['tournamentPK']

            # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
            if progressStatus == "2":
                pass
            else:
                if tournamentStatus == "1":
                    videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
                    if videoinfoCount == 0:
                        text = "비디오 리스트 없음"
                        ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                        context = {'code':'0', 'audition_videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:        
                        # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
                        audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").order_by('?')
                        audition_videoinfoList = []
                        winnerPoint = 0
                        for index, i in enumerate(audition_videoinfo):
                            userPK = i.userPK
                            videoPK = i.id
                            userinfo = SignUp.objects.get(id = userPK)
                            username = userinfo.username
                            nickName = userinfo.nickName
                            profileIMG_path = userinfo.profileIMG_path
                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                            thumbnailPATH = i.thumbnailPATH
                            thumbnailPATH = s3PATH+thumbnailPATH

                            videoPATH = i.videoPATH
                            s3Check = S3Check.objects.get(id = 1)
                            s3Status = s3Check.status
                            if s3Status == "0":
                                videoPATH = serverURL+"/static/video"+videoPATH
                            elif s3Status == "1":
                                videoPATH = s3PATH+videoPATH

                            
                            contents = i.contents
                            hashTag = i.hashTag
                            viewable = i.viewable
                            # likeCount = ""
                            # comentCount = ""
                            # userLikeCheck = ""

                            # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            # likeCount = str(audition_like_video_infoCount)

                            # audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
                            # if audition_like_video_infoCount_user == 0:
                            #     userLikeCheck = "0"
                            # else:
                            #     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
                            #     status = audition_like_video_info_user.status
                            #     if status == "0":
                            #         userLikeCheck = "0"
                            #     elif status == "1":
                            #         userLikeCheck = "1"

                            # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                            # comentCount = str(audition_coment_infoCount)

                            # audition_coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            # if audition_coment_infoCount_user == 0:
                            #     userComentCheck = "0"
                            # else:
                            #     userComentCheck = "1"
                                
                            audition_Count = Audition_Count.objects.get(videoPK = videoPK)
                            winnerPoint += int(audition_Count.donation)

                            dictinfo = {
                                'videoPK':str(videoPK), 
                                'userPK':userPK, 
                                'username':username,
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'contents':contents,
                                'hashTag':hashTag,
                                'thumbnailPATH':thumbnailPATH,
                                'videoPATH':videoPATH,
                                'viewable':viewable,
                                # 'likeCount':likeCount,
                                # 'comentCount':comentCount,
                                # 'userLikeCheck':userLikeCheck,
                                'auditionListPK':auditionListPK,
                                'tournamentStatus':tournamentStatus,
                                'categoryPK':categoryPK
                            }
                            audition_videoinfoList.append(dictinfo)
                        # random.shuffle(audition_videoinfoList)
                        audition_videoAllinfo = audition_videoinfoList
                        audition_videoinfoList = audition_videoinfoList[pageStart:pageEnd]

                        text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                        print("["+str(datetime.now())+"] " + text)
                        context = {'code':'1', 'audition_videoAllinfo':audition_videoAllinfo, 'audition_videoinfoList':audition_videoinfoList, 'winnerPoint':winnerPoint}
                        return HttpResponse(json.dumps(context))
        else:
            page = int(data['page'])
            pageStart = (page - 1) * 21
            pageEnd = 21 * page
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']
            categoryPK = data['categoryPK']

            # loginUserPK = data['loginUserPK']
            # auditionListPK = data['auditionListPK']
            # categoryListPK = data['categoryListPK']
            # tournamentPK = data['tournamentPK']

            # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
            if progressStatus == "2":
                pass
            else:
                if tournamentStatus == "1":
                    videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
                    if videoinfoCount == 0:
                        text = "비디오 리스트 없음"
                        ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                        context = {'code':'0', 'audition_videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:        
                        # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
                        audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").order_by('?')
                        audition_videoinfoList = []
                        winnerPoint = 0
                        for index, i in enumerate(audition_videoinfo):
                            userPK = i.userPK
                            videoPK = i.id
                            userinfo = SignUp.objects.get(id = userPK)
                            username = userinfo.username
                            nickName = userinfo.nickName
                            profileIMG_path = userinfo.profileIMG_path
                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                            thumbnailPATH = i.thumbnailPATH
                            thumbnailPATH = s3PATH+thumbnailPATH

                            videoPATH = i.videoPATH
                            s3Check = S3Check.objects.get(id = 1)
                            s3Status = s3Check.status
                            if s3Status == "0":
                                videoPATH = serverURL+"/static/video"+videoPATH
                            elif s3Status == "1":
                                videoPATH = s3PATH+videoPATH

                            
                            contents = i.contents
                            hashTag = i.hashTag
                            viewable = i.viewable
                            # likeCount = ""
                            # comentCount = ""
                            # userLikeCheck = ""

                            # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            # likeCount = str(audition_like_video_infoCount)

                            # audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
                            # if audition_like_video_infoCount_user == 0:
                            #     userLikeCheck = "0"
                            # else:
                            #     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
                            #     status = audition_like_video_info_user.status
                            #     if status == "0":
                            #         userLikeCheck = "0"
                            #     elif status == "1":
                            #         userLikeCheck = "1"

                            # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                            # comentCount = str(audition_coment_infoCount)

                            # audition_coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            # if audition_coment_infoCount_user == 0:
                            #     userComentCheck = "0"
                            # else:
                            #     userComentCheck = "1"
                                
                            audition_Count = Audition_Count.objects.get(videoPK = videoPK)
                            winnerPoint += int(audition_Count.donation)

                            dictinfo = {
                                'videoPK':str(videoPK), 
                                'userPK':userPK, 
                                'username':username,
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'contents':contents,
                                'hashTag':hashTag,
                                'thumbnailPATH':thumbnailPATH,
                                'videoPATH':videoPATH,
                                'viewable':viewable,
                                # 'likeCount':likeCount,
                                # 'comentCount':comentCount,
                                # 'userLikeCheck':userLikeCheck,
                                'auditionListPK':auditionListPK,
                                'tournamentStatus':tournamentStatus,
                                'categoryPK':categoryPK
                            }
                            audition_videoinfoList.append(dictinfo)
                        # random.shuffle(audition_videoinfoList)
                        audition_videoAllinfo = audition_videoinfoList
                        audition_videoinfoList = audition_videoinfoList[pageStart:pageEnd]

                        text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                        print("["+str(datetime.now())+"] " + text)
                        context = {'code':'1', 'audition_videoAllinfo':audition_videoAllinfo, 'audition_videoinfoList':audition_videoinfoList, 'winnerPoint':winnerPoint}
                        return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_videoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# # 오디션별 현재 상금
# @csrf_exempt
# def audition_winnerPoint(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             auditionListPK = data['auditionListPK']

#             audition_Countinfo = Audition_Count.objects.filter(auditionListPK = auditionListPK)
#             winnerPoint = 0
#             for index, i in enumerate(audition_Countinfo):
#                 winnerPoint += int(i.donation)

#             text = "\033[92m"+"audition_winnerPoint SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'winnerPoint':winnerPoint}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             auditionListPK = data['auditionListPK']

#             audition_Countinfo = Audition_Count.objects.filter(auditionListPK = auditionListPK)
#             winnerPoint = 0
#             for index, i in enumerate(audition_Countinfo):
#                 winnerPoint += int(i.donation)

#             text = "\033[92m"+"audition_winnerPoint SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'winnerPoint':winnerPoint}
#             return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_winnerPoint Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# # 오디션별 현재 상금
# @csrf_exempt
# def audition_winnerPoint(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         auditionListPK = data['auditionListPK']

        # audition_Countinfo = Audition_Count.objects.filter(auditionListPK = auditionListPK)
        # winnerPoint = 0
        # for index, i in enumerate(audition_Countinfo):
        #     winnerPoint += int(i.donation)

#         print("winnerPoint >>-----------------", winnerPoint)

#         text = "\033[92m"+"audition_winnerPoint SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#         print("["+str(datetime.now())+"] " + text)
#         context = {'code':'1', 'winnerPoint':winnerPoint}
#         return HttpResponse(json.dumps(context))
        


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_winnerPoint Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# # 오디션 비디오 리스트 페이지네이션
# @csrf_exempt
# def audition_videoListMove(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             page = int(data['page'])
#             pageStart = (page - 1) * 21
#             pageEnd = 21 * page
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']
#             categoryPK = data['categoryPK']
#             audition_videoAllinfo = data['audition_videoAllinfo'][pageStart:pageEnd]
#             videoAllinfoLen = len(audition_videoAllinfo)
#             # videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]
#             if videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"audition_videoListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'audition_videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_videoinfoList = []
#                 for index, i in enumerate(audition_videoAllinfo):

#                     userPK = i['userPK']

#                     # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
#                     # if userBlockListinfoCount == 0:
#                     videoPK = i['videoPK']
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status

#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']
#                     # videoPATH = s3PATH+videoPATH
#                     # s3VideoPATH = i['s3VideoPATH']
#                     thumbnailPATH = i['thumbnailPATH']
                    
#                     # thumbnailPATH = s3PATH+thumbnailPATH
                                    
#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+videoPATH
#                     #     thumbnailPATH = s3PATH+thumbnailPATH

#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+s3VideoPATH
#                     #     thumbnailPATH = s3PATH+thumbnailPATH

#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']

                    
                    
#                     # userLikeCheck = ""
#                     # viewCountCheck = ""


#                     # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     # likeCount = like_video_infoCount
#                     # if like_video_infoCount == 0:
#                     #     pass
#                     # else:
#                     #     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     #     for index, j in enumerate(like_video_info):
#                     #         userPK_like = j.userPK

#                     #         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                     #         if userBlockListinfoCount_likevideo == 1:
#                     #             likeCount -= 1



#                     # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if like_video_infoCount_user == 0:
#                     #     userLikeCheck = "0"
#                     # else:
#                     #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     #     status = like_video_info_user.status
#                     #     if status == "0":
#                     #         userLikeCheck = "0"
#                     #     elif status == "1":
#                     #         userLikeCheck = "1"




#                     # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                     # comentCount = coment_infoCount
#                     # if coment_infoCount == 0:
#                     #     pass
#                     # else:
#                     #     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     #     for index, k in enumerate(coment_info):
#                     #         userPK_coment = k.userPK
#                     #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                     #         if userBlockListinfoCount_coment == 1:
#                     #             comentCount -= 1


#                     # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if viewCount_infoCount == 0:
#                     #     viewCountCheck = "0"
#                     # else:
#                     #     viewCountCheck = "1"


#                     dictinfo = {
#                         'videoPK':str(videoPK), 
#                         'userPK':userPK, 
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'hashTag':hashTag,
#                         'thumbnailPATH':thumbnailPATH,
#                         'videoPATH':videoPATH,
#                         'viewable':viewable,
#                         # 'likeCount':likeCount,
#                         # 'comentCount':comentCount,
#                         # 'userLikeCheck':userLikeCheck,
#                         # 'viewCountCheck':viewCountCheck,
#                         'auditionListPK':auditionListPK,
#                         'tournamentStatus':tournamentStatus,
#                         'categoryPK':categoryPK
#                     }
#                     audition_videoinfoList.append(dictinfo)

#                 # print("audition_videoinfoList >>", audition_videoinfoList)
#                 text = "\033[92m"+"audition_videoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_videoinfoList':audition_videoinfoList}
#                 return HttpResponse(json.dumps(context))
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 21
#             pageEnd = 21 * page
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']
#             categoryPK = data['categoryPK']
#             audition_videoAllinfo = data['audition_videoAllinfo'][pageStart:pageEnd]
#             videoAllinfoLen = len(audition_videoAllinfo)
#             # videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]
#             if videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"audition_videoListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'audition_videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_videoinfoList = []
#                 for index, i in enumerate(audition_videoAllinfo):

#                     userPK = i['userPK']

#                     # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
#                     # if userBlockListinfoCount == 0:
#                     videoPK = i['videoPK']
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status

#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']
#                     # videoPATH = s3PATH+videoPATH
#                     # s3VideoPATH = i['s3VideoPATH']
#                     thumbnailPATH = i['thumbnailPATH']
                    
#                     # thumbnailPATH = s3PATH+thumbnailPATH
                                    
#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+videoPATH
#                     #     thumbnailPATH = s3PATH+thumbnailPATH

#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     #     thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+s3VideoPATH
#                     #     thumbnailPATH = s3PATH+thumbnailPATH

#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']

                    
                    
#                     # userLikeCheck = ""
#                     # viewCountCheck = ""


#                     # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     # likeCount = like_video_infoCount
#                     # if like_video_infoCount == 0:
#                     #     pass
#                     # else:
#                     #     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
#                     #     for index, j in enumerate(like_video_info):
#                     #         userPK_like = j.userPK

#                     #         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
#                     #         if userBlockListinfoCount_likevideo == 1:
#                     #             likeCount -= 1



#                     # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if like_video_infoCount_user == 0:
#                     #     userLikeCheck = "0"
#                     # else:
#                     #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                     #     status = like_video_info_user.status
#                     #     if status == "0":
#                     #         userLikeCheck = "0"
#                     #     elif status == "1":
#                     #         userLikeCheck = "1"




#                     # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                     # comentCount = coment_infoCount
#                     # if coment_infoCount == 0:
#                     #     pass
#                     # else:
#                     #     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
#                     #     for index, k in enumerate(coment_info):
#                     #         userPK_coment = k.userPK
#                     #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                     #         if userBlockListinfoCount_coment == 1:
#                     #             comentCount -= 1


#                     # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     # if viewCount_infoCount == 0:
#                     #     viewCountCheck = "0"
#                     # else:
#                     #     viewCountCheck = "1"


#                     dictinfo = {
#                         'videoPK':str(videoPK), 
#                         'userPK':userPK, 
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'hashTag':hashTag,
#                         'thumbnailPATH':thumbnailPATH,
#                         'videoPATH':videoPATH,
#                         'viewable':viewable,
#                         # 'likeCount':likeCount,
#                         # 'comentCount':comentCount,
#                         # 'userLikeCheck':userLikeCheck,
#                         # 'viewCountCheck':viewCountCheck,
#                         'auditionListPK':auditionListPK,
#                         'tournamentStatus':tournamentStatus,
#                         'categoryPK':categoryPK
#                     }
#                     audition_videoinfoList.append(dictinfo)

#                 # print("audition_videoinfoList >>", audition_videoinfoList)
#                 text = "\033[92m"+"audition_videoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_videoinfoList':audition_videoinfoList}
#                 return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_videoListMove Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    

# 오디션 비디오 리스트 페이지네이션
@csrf_exempt
def audition_videoListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            page = int(data['page'])
            pageStart = (page - 1) * 21
            pageEnd = 21 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']
            categoryPK = data['categoryPK']
            audition_videoAllinfo = data['audition_videoAllinfo'][pageStart:pageEnd]
            videoAllinfoLen = len(audition_videoAllinfo)
            # videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]
            if videoAllinfoLen == 0:
                text = " :: 페이지 영상 없음"
                ment = "\033[92m"+"audition_videoListMove WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'audition_videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                audition_videoinfoList = []
                for index, i in enumerate(audition_videoAllinfo):

                    userPK = i['userPK']


                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']

                    thumbnailPATH = i['thumbnailPATH']
                    

                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']




                    dictinfo = {
                        'videoPK':str(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'thumbnailPATH':thumbnailPATH,
                        'videoPATH':videoPATH,
                        'viewable':viewable,

                        'auditionListPK':auditionListPK,
                        'tournamentStatus':tournamentStatus,
                        'categoryPK':categoryPK
                    }
                    audition_videoinfoList.append(dictinfo)

                # print("audition_videoinfoList >>", audition_videoinfoList)
                text = "\033[92m"+"audition_videoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'audition_videoinfoList':audition_videoinfoList}
                return HttpResponse(json.dumps(context))
        else:
            page = int(data['page'])
            pageStart = (page - 1) * 21
            pageEnd = 21 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']
            categoryPK = data['categoryPK']
            audition_videoAllinfo = data['audition_videoAllinfo'][pageStart:pageEnd]
            videoAllinfoLen = len(audition_videoAllinfo)
            # videoAllinfo = json.loads(videoAllinfo)[pageStart:pageEnd]
            if videoAllinfoLen == 0:
                text = " :: 페이지 영상 없음"
                ment = "\033[92m"+"audition_videoListMove WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'audition_videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                audition_videoinfoList = []
                for index, i in enumerate(audition_videoAllinfo):

                    userPK = i['userPK']


                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']

                    thumbnailPATH = i['thumbnailPATH']
                    
                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']


                    dictinfo = {
                        'videoPK':str(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'thumbnailPATH':thumbnailPATH,
                        'videoPATH':videoPATH,
                        'viewable':viewable,
                        'auditionListPK':auditionListPK,
                        'tournamentStatus':tournamentStatus,
                        'categoryPK':categoryPK
                    }
                    audition_videoinfoList.append(dictinfo)

                # print("audition_videoinfoList >>", audition_videoinfoList)
                text = "\033[92m"+"audition_videoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'audition_videoinfoList':audition_videoinfoList}
                return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_videoListMove Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 오디션 영상 후원
@csrf_exempt
def audition_donetion(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            sender_userPK = data['sender_userPK']
            receiver_userPK = data['receiver_userPK']
            videoPK = data['videoPK']
            amount = data['amount']

            userinfo = SignUp.objects.get(id = sender_userPK)
            senderUserPoint = userinfo.point
            if int(senderUserPoint) < int(amount):
                text = "잔고 부족"
                ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            
            else:
                donetionListSubmit = Audition_DonationList(sender_userPK = sender_userPK, receiver_userPK = receiver_userPK, videoPK = videoPK, amount = amount, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                donetionListSubmit.save()

                userinfo = SignUp.objects.get(id = sender_userPK)
                userinfo.point = int(userinfo.point) - int(amount)
                userinfo.save()

                audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                audition_Countinfo.donation = int(audition_Countinfo.donation) + int(amount)
                audition_Countinfo.save()

                text = "후원 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            
        else:
            sender_userPK = data['sender_userPK']
            receiver_userPK = data['receiver_userPK']
            videoPK = data['videoPK']
            amount = data['amount']

            userinfo = SignUp.objects.get(id = sender_userPK)
            senderUserPoint = userinfo.point
            if int(senderUserPoint) < int(amount):
                text = "잔고 부족"
                ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            
            else:
                donetionListSubmit = Audition_DonationList(sender_userPK = sender_userPK, receiver_userPK = receiver_userPK, videoPK = videoPK, amount = amount, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                donetionListSubmit.save()

                userinfo = SignUp.objects.get(id = sender_userPK)
                userinfo.point = int(userinfo.point) - int(amount)
                userinfo.save()

                audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                audition_Countinfo.donation = int(audition_Countinfo.donation) + int(amount)
                audition_Countinfo.save()

                text = "후원 완료"
                ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"donetion Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 오디션 예전선 상세 및 위아래 페이지 네이션
@csrf_exempt
def audition_DetailListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            audition_videoAllinfo = data['audition_videoAllinfo']
            audition_videoAllinfo = audition_videoAllinfo[pageStart:pageEnd]
            audition_videoAllinfoLen = len(audition_videoAllinfo)
            if audition_videoAllinfoLen == 0:
                text = " :: 페이지 영상 없음"
                ment = "\033[92m"+"audition_DetailListMove WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                videoinfoList = []
                for index, i in enumerate(audition_videoAllinfo):

                    userPK = i['userPK']

                    # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                    # if userBlockListinfoCount == 0:
                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']
                    # videoPATH = s3PATH+videoPATH

                    # s3Check = S3Check.objects.get(id = 1)
                    # s3Status = s3Check.status
                    # if s3Status == "0":
                    #     videoPATH = serverURL+"/static/video"+videoPATH
                    # elif s3Status == "1":
                    #     videoPATH = s3PATH+videoPATH
                    # s3VideoPATH = i['s3VideoPATH']

                    # if s3Status == "0":
                    #     videoPATH = serverURL+"/static/video"+videoPATH
                    # elif s3Status == "1":
                    #     videoPATH = s3PATH+s3VideoPATH

                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']

                    
                    
                    userLikeCheck = ""
                    viewCountCheck = ""


                    # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    # likeCount = like_video_infoCount
                    # if like_video_infoCount == 0:
                    #     pass
                    # else:
                    #     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                    #     for index, j in enumerate(like_video_info):
                    #         userPK_like = j.userPK

                    #         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    #         if userBlockListinfoCount_likevideo == 1:
                    #             likeCount -= 1


                    # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    # if like_video_infoCount_user == 0:
                    #     userLikeCheck = "0"
                    # else:
                    #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                    #     status = like_video_info_user.status
                    #     if status == "0":
                    #         userLikeCheck = "0"
                    #     elif status == "1":
                    #         userLikeCheck = "1"


                    audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    likeCount = str(audition_like_video_infoCount)

                    audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
                    if audition_like_video_infoCount_user == 0:
                        userLikeCheck = "0"
                    else:
                        audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
                        status = audition_like_video_info_user.status
                        if status == "0":
                            userLikeCheck = "0"
                        elif status == "1":
                            userLikeCheck = "1"







                    audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                    comentCount = str(audition_coment_infoCount)

                    # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                    # comentCount = coment_infoCount
                    # if coment_infoCount == 0:
                    #     pass
                    # else:
                    #     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                    #     for index, k in enumerate(coment_info):
                    #         userPK_coment = k.userPK
                    #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    #         if userBlockListinfoCount_coment == 1:
                    #             comentCount -= 1


                    viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if viewCount_infoCount == 0:
                        viewCountCheck = "0"
                    else:
                        viewCountCheck = "1"


                    dictinfo = {
                        'videoPK':int(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'videoPATH':videoPATH,
                        'viewable':viewable,
                        'likeCount':str(likeCount),
                        'comentCount':str(comentCount),
                        'userLikeCheck':userLikeCheck,
                        'viewCountCheck':viewCountCheck
                    }
                    videoinfoList.append(dictinfo)


                # print("videoinfoList >>", videoinfoList)
                text = "\033[92m"+"audition_DetailListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'videoinfoList':videoinfoList}
                return HttpResponse(json.dumps(context))
            
        else:
            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            audition_videoAllinfo = data['audition_videoAllinfo']
            audition_videoAllinfo = audition_videoAllinfo[pageStart:pageEnd]
            audition_videoAllinfoLen = len(audition_videoAllinfo)
            if audition_videoAllinfoLen == 0:
                text = " :: 페이지 영상 없음"
                ment = "\033[92m"+"audition_DetailListMove WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2', 'videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                videoinfoList = []
                for index, i in enumerate(audition_videoAllinfo):

                    userPK = i['userPK']

                    # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                    # if userBlockListinfoCount == 0:
                    videoPK = i['videoPK']
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status

                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i['videoPATH']
                    # videoPATH = s3PATH+videoPATH

                    # s3Check = S3Check.objects.get(id = 1)
                    # s3Status = s3Check.status
                    # if s3Status == "0":
                    #     videoPATH = serverURL+"/static/video"+videoPATH
                    # elif s3Status == "1":
                    #     videoPATH = s3PATH+videoPATH
                    # s3VideoPATH = i['s3VideoPATH']

                    # if s3Status == "0":
                    #     videoPATH = serverURL+"/static/video"+videoPATH
                    # elif s3Status == "1":
                    #     videoPATH = s3PATH+s3VideoPATH

                    contents = i['contents']
                    hashTag = i['hashTag']
                    viewable = i['viewable']

                    
                    
                    userLikeCheck = ""
                    viewCountCheck = ""


                    # like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    # likeCount = like_video_infoCount
                    # if like_video_infoCount == 0:
                    #     pass
                    # else:
                    #     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                    #     for index, j in enumerate(like_video_info):
                    #         userPK_like = j.userPK

                    #         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    #         if userBlockListinfoCount_likevideo == 1:
                    #             likeCount -= 1


                    # like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    # if like_video_infoCount_user == 0:
                    #     userLikeCheck = "0"
                    # else:
                    #     like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                    #     status = like_video_info_user.status
                    #     if status == "0":
                    #         userLikeCheck = "0"
                    #     elif status == "1":
                    #         userLikeCheck = "1"


                    audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                    likeCount = str(audition_like_video_infoCount)

                    audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
                    if audition_like_video_infoCount_user == 0:
                        userLikeCheck = "0"
                    else:
                        audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
                        status = audition_like_video_info_user.status
                        if status == "0":
                            userLikeCheck = "0"
                        elif status == "1":
                            userLikeCheck = "1"







                    audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                    comentCount = str(audition_coment_infoCount)

                    # coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                    # comentCount = coment_infoCount
                    # if coment_infoCount == 0:
                    #     pass
                    # else:
                    #     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                    #     for index, k in enumerate(coment_info):
                    #         userPK_coment = k.userPK
                    #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    #         if userBlockListinfoCount_coment == 1:
                    #             comentCount -= 1


                    viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                    if viewCount_infoCount == 0:
                        viewCountCheck = "0"
                    else:
                        viewCountCheck = "1"


                    dictinfo = {
                        'videoPK':int(videoPK), 
                        'userPK':userPK, 
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'hashTag':hashTag,
                        'videoPATH':videoPATH,
                        'viewable':viewable,
                        'likeCount':str(likeCount),
                        'comentCount':str(comentCount),
                        'userLikeCheck':userLikeCheck,
                        'viewCountCheck':viewCountCheck
                    }
                    videoinfoList.append(dictinfo)


                # print("videoinfoList >>", videoinfoList)
                text = "\033[92m"+"audition_DetailListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'videoinfoList':videoinfoList}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_DetailListMove Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))







# 오디션 예선 집계중 페이지
@csrf_exempt
def audition_aggregatingList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            # page = int(data['page'])
            # pageStart = (page - 1) * 21
            # pageEnd = 21 * page
            # loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']


            # loginUserPK = data['loginUserPK']
            # auditionListPK = data['auditionListPK']
            # categoryListPK = data['categoryListPK']
            # tournamentPK = data['tournamentPK']

            # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
            if progressStatus == "2":
                pass
            else:
                if tournamentStatus == "1":
                    # videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd].count()
                    videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
                    if videoinfoCount == 0:
                        text = "비디오 리스트 없음"
                        ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                        context = {'code':'0', 'audition_videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:        
                        # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
                        # audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd]
                        audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")
                        aggregatingList = []
                        for index, i in enumerate(audition_videoinfo):
                            userPK = i.userPK
                            videoPK = i.id
                            userinfo = SignUp.objects.get(id = userPK)
                            nickName = userinfo.nickName
                            profileIMG_path = userinfo.profileIMG_path
                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                            userLikeCheck = ""

                            donation = 0
                            likeCount = 0
                            comentCount = 0
                            viewCount = 0

                            Audition_Countinfo_count = Audition_Count.objects.filter(videoPK = videoPK).count()
                            if Audition_Countinfo_count == 0:
                                Audition_CountSubmit = Audition_Count(ownerPK = userPK, videoPK = videoPK)
                                Audition_CountSubmit.save()
                            else:
                                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                                donation = int(Audition_Countinfo.donation)
                                donationSum = donation * 50
                                likeCount = int(Audition_Countinfo.like)
                                likeSum = likeCount * 25
                                comentCount = int(Audition_Countinfo.coment)
                                comentSum = comentCount * 10
                                viewCount = int(Audition_Countinfo.viewcount)
                                viewCountSum = viewCount * 15



                            # likeCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            # comentCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                            # comentinfo = Audition_Coment.objects.filter(videoPK = videoPK)




                            # viewCount = Audition_ViewCount.objects.filter(videoPK = videoPK).count()
                            allSum = donationSum + likeSum + comentSum + viewCountSum
                            
                            dictinfo = {
                                'videoPK':str(videoPK), 
                                'userPK':userPK, 
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'donation':donation,
                                'likeCount':likeCount,
                                'comentCount':comentCount,
                                'viewCount':viewCount,
                                'allSum':allSum,
                            }
                            aggregatingList.append(dictinfo)

                        aggregatingList = sorted(aggregatingList, key=lambda x: x['allSum'], reverse=True)
                        aggregatingList2 = []
                        rank = 0
                        for index, j in enumerate(aggregatingList):
                            if index == 0:

                                videoPK = j['videoPK']
                                userPK = j['userPK']
                                nickName = j['nickName']
                                profileIMG_path = j['profileIMG_path']
                                donation = j['donation']
                                likeCount = j['likeCount']
                                comentCount = j['comentCount']
                                viewCount = j['viewCount']
                                allSum = j['allSum']

                                rank += 1

                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'donation':donation,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'viewCount':viewCount,
                                    'allSum':allSum,
                                    'rank': int(rank),
                                }
                                aggregatingList2.append(dictinfo)
                            else:

                                checkIdx = index - 1
                                previous = aggregatingList2[checkIdx]
                                previous_allSum = previous['allSum']
                                previous_rank = previous['rank']

                                videoPK = j['videoPK']
                                userPK = j['userPK']
                                nickName = j['nickName']
                                profileIMG_path = j['profileIMG_path']
                                donation = j['donation']
                                likeCount = j['likeCount']
                                comentCount = j['comentCount']
                                viewCount = j['viewCount']
                                allSum = j['allSum']


                                if int(allSum) == int(previous_allSum):
                                    rank = int(previous_rank)
                                else:
                                    rankCount = len(aggregatingList2)
                                    rank = rankCount + 1

                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'donation':donation,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'viewCount':viewCount,
                                    'allSum':allSum,
                                    'rank': int(rank),
                                }
                                aggregatingList2.append(dictinfo)


                        aggregatingList2 = sorted(aggregatingList2, key=lambda x: x['rank'], reverse=True)




                        text = "\033[92m"+"aggregatingList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                        print("["+str(datetime.now())+"] " + text)
                        context = {'code':'1', 'aggregatingList':aggregatingList2}
                        return HttpResponse(json.dumps(context))
                    

        else:
            # page = int(data['page'])
            # pageStart = (page - 1) * 21
            # pageEnd = 21 * page
            # loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            progressStatus = data['progressStatus']


            # loginUserPK = data['loginUserPK']
            # auditionListPK = data['auditionListPK']
            # categoryListPK = data['categoryListPK']
            # tournamentPK = data['tournamentPK']

            # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
            if progressStatus == "2":
                pass
            else:
                if tournamentStatus == "1":
                    # videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd].count()
                    videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
                    if videoinfoCount == 0:
                        text = "비디오 리스트 없음"
                        ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
                        print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                        context = {'code':'0', 'audition_videoinfoList':None}
                        return HttpResponse(json.dumps(context))
                    else:        
                        # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
                        # audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd]
                        audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")
                        aggregatingList = []
                        for index, i in enumerate(audition_videoinfo):
                            userPK = i.userPK
                            videoPK = i.id
                            userinfo = SignUp.objects.get(id = userPK)
                            nickName = userinfo.nickName
                            profileIMG_path = userinfo.profileIMG_path
                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                            userLikeCheck = ""

                            donation = 0
                            likeCount = 0
                            comentCount = 0
                            viewCount = 0

                            Audition_Countinfo_count = Audition_Count.objects.filter(videoPK = videoPK).count()
                            if Audition_Countinfo_count == 0:
                                Audition_CountSubmit = Audition_Count(ownerPK = userPK, videoPK = videoPK)
                                Audition_CountSubmit.save()
                            else:
                                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                                donation = int(Audition_Countinfo.donation)
                                donationSum = donation * 50
                                likeCount = int(Audition_Countinfo.like)
                                likeSum = likeCount * 25
                                comentCount = int(Audition_Countinfo.coment)
                                comentSum = comentCount * 10
                                viewCount = int(Audition_Countinfo.viewcount)
                                viewCountSum = viewCount * 15



                            # likeCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            # comentCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                            # comentinfo = Audition_Coment.objects.filter(videoPK = videoPK)




                            # viewCount = Audition_ViewCount.objects.filter(videoPK = videoPK).count()
                            allSum = donationSum + likeSum + comentSum + viewCountSum
                            
                            dictinfo = {
                                'videoPK':str(videoPK), 
                                'userPK':userPK, 
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'donation':donation,
                                'likeCount':likeCount,
                                'comentCount':comentCount,
                                'viewCount':viewCount,
                                'allSum':allSum,
                            }
                            aggregatingList.append(dictinfo)

                        aggregatingList = sorted(aggregatingList, key=lambda x: x['allSum'], reverse=True)
                        aggregatingList2 = []
                        rank = 0
                        for index, j in enumerate(aggregatingList):
                            if index == 0:

                                videoPK = j['videoPK']
                                userPK = j['userPK']
                                nickName = j['nickName']
                                profileIMG_path = j['profileIMG_path']
                                donation = j['donation']
                                likeCount = j['likeCount']
                                comentCount = j['comentCount']
                                viewCount = j['viewCount']
                                allSum = j['allSum']

                                rank += 1

                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'donation':donation,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'viewCount':viewCount,
                                    'allSum':allSum,
                                    'rank': int(rank),
                                }
                                aggregatingList2.append(dictinfo)
                            else:

                                checkIdx = index - 1
                                previous = aggregatingList2[checkIdx]
                                previous_allSum = previous['allSum']
                                previous_rank = previous['rank']

                                videoPK = j['videoPK']
                                userPK = j['userPK']
                                nickName = j['nickName']
                                profileIMG_path = j['profileIMG_path']
                                donation = j['donation']
                                likeCount = j['likeCount']
                                comentCount = j['comentCount']
                                viewCount = j['viewCount']
                                allSum = j['allSum']


                                if int(allSum) == int(previous_allSum):
                                    rank = int(previous_rank)
                                else:
                                    rankCount = len(aggregatingList2)
                                    rank = rankCount + 1

                                dictinfo = {
                                    'videoPK':str(videoPK), 
                                    'userPK':userPK, 
                                    'nickName':nickName,
                                    'profileIMG_path':profileIMG_path,
                                    'donation':donation,
                                    'likeCount':likeCount,
                                    'comentCount':comentCount,
                                    'viewCount':viewCount,
                                    'allSum':allSum,
                                    'rank': int(rank),
                                }
                                aggregatingList2.append(dictinfo)


                        aggregatingList2 = sorted(aggregatingList2, key=lambda x: x['rank'], reverse=True)




                        text = "\033[92m"+"aggregatingList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                        print("["+str(datetime.now())+"] " + text)
                        context = {'code':'1', 'aggregatingList':aggregatingList2}
                        return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"aggregatingList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 32강부터는 여기서
@csrf_exempt
def audition_matchesList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            categoryListPK = data['categoryListPK']
            tournamentStatus = data['tournamentStatus']

            versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
            if versusListinfoCount == 0:
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
                versusListinfoList = []
                
                for index, i in enumerate(versusListinfo):
                    userPK_left = i.userPK_left
                    userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                    userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                    userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                    userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                    userPK_left_userNick = userPK_left_userinfo.nickName
                    userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                    if userPK_left_profileIMG_path:
                        userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                    else:
                        userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    LLS = i.LLS
                    LVS = i.LVS
                    LDS = i.LDS
                    LCS = i.LCS
                    LAS = i.LAS


                    
                    userPK_right = i.userPK_right
                    userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                    userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                    userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                    userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                    userPK_right_userNick = userPK_right_userinfo.nickName
                    userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                    if userPK_right_profileIMG_path:
                        userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                    else:
                        userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    RLS = i.RLS
                    RCS = i.RCS
                    RVS = i.RVS
                    RDS = i.RDS
                    RAS = i.RAS

                    # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
                    # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

                    # 작업완료되면 위에걸로 다시 바꿔야함 gogo
                    audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "26")
                    audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "26")

                    videoPK_left = str(audition_videoinfo_left.id)
                    videoPK_right = str(audition_videoinfo_right.id)
                    thumbnailPATH_left = ""
                    thumbnailPATH_right = ""
                    if tournamentStatus == "6":
                        
                        thumbnailPATH_left = audition_videoinfo_left.thumbnailPATH
                        thumbnailPATH_left = s3PATH+thumbnailPATH_left

                        
                        thumbnailPATH_right = audition_videoinfo_right.thumbnailPATH
                        thumbnailPATH_right = s3PATH+thumbnailPATH_right

                    dictinfo = {
                        'left': {
                            'userPK_left':userPK_left,
                            'videoPK_left':videoPK_left,
                            'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                            'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                            'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
                            'userPK_left_userNick':userPK_left_userNick,
                            'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
                            'thumbnailPATH_left':thumbnailPATH_left,
                            'LLS': LLS,
                            'LVS': LVS,
                            'LDS': LDS,
                            'LCS': LCS,
                            'LAS': LAS
                        },
                        'right': {
                            'userPK_right':userPK_right,
                            'videoPK_right':videoPK_right,
                            'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                            'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                            'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
                            'userPK_right_userNick':userPK_right_userNick,
                            'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
                            'thumbnailPATH_right':thumbnailPATH_right,
                            'RLS': RLS,
                            'RCS': RCS,
                            'RVS': RVS,
                            'RDS': RDS,
                            'RAS': RAS
                        },
                        'sum': int(LAS) + int(RAS)
                    }
                    versusListinfoList.append(dictinfo)
                # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)
                text = "\033[92m"+"audition_matchesList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'versusListinfoList':versusListinfoList}
                return HttpResponse(json.dumps(context))
            
        else:
            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            categoryListPK = data['categoryListPK']
            tournamentStatus = data['tournamentStatus']

            versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
            if versusListinfoCount == 0:
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
                versusListinfoList = []
                
                for index, i in enumerate(versusListinfo):
                    userPK_left = i.userPK_left
                    userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                    userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                    userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                    userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                    userPK_left_userNick = userPK_left_userinfo.nickName
                    userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                    if userPK_left_profileIMG_path:
                        userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                    else:
                        userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    LLS = i.LLS
                    LVS = i.LVS
                    LDS = i.LDS
                    LCS = i.LCS
                    LAS = i.LAS


                    
                    userPK_right = i.userPK_right
                    userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                    userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                    userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                    userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                    userPK_right_userNick = userPK_right_userinfo.nickName
                    userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                    if userPK_right_profileIMG_path:
                        userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                    else:
                        userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    RLS = i.RLS
                    RCS = i.RCS
                    RVS = i.RVS
                    RDS = i.RDS
                    RAS = i.RAS

                    # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
                    # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

                    # 작업완료되면 위에걸로 다시 바꿔야함 gogo
                    audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "20")
                    audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "20")

                    videoPK_left = str(audition_videoinfo_left.id)
                    videoPK_right = str(audition_videoinfo_right.id)
                    thumbnailPATH_left = ""
                    thumbnailPATH_right = ""
                    if tournamentStatus == "6":
                        
                        thumbnailPATH_left = audition_videoinfo_left.thumbnailPATH
                        thumbnailPATH_left = s3PATH+thumbnailPATH_left

                        
                        thumbnailPATH_right = audition_videoinfo_right.thumbnailPATH
                        thumbnailPATH_right = s3PATH+thumbnailPATH_right

                    dictinfo = {
                        'left': {
                            'userPK_left':userPK_left,
                            'videoPK_left':videoPK_left,
                            'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                            'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                            'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
                            'userPK_left_userNick':userPK_left_userNick,
                            'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
                            'thumbnailPATH_left':thumbnailPATH_left,
                            'LLS': LLS,
                            'LVS': LVS,
                            'LDS': LDS,
                            'LCS': LCS,
                            'LAS': LAS
                        },
                        'right': {
                            'userPK_right':userPK_right,
                            'videoPK_right':videoPK_right,
                            'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                            'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                            'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
                            'userPK_right_userNick':userPK_right_userNick,
                            'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
                            'thumbnailPATH_right':thumbnailPATH_right,
                            'RLS': RLS,
                            'RCS': RCS,
                            'RVS': RVS,
                            'RDS': RDS,
                            'RAS': RAS
                        },
                        'sum': int(LAS) + int(RAS)
                    }
                    versusListinfoList.append(dictinfo)
                # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)
                text = "\033[92m"+"audition_matchesList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'versusListinfoList':versusListinfoList}
                return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_matchesList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))











# 매치 리스트 영상 상세보기 
@csrf_exempt
def audition_matchesListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK)
            ownerPK = videoinfo.userPK
            videoPK = videoinfo.id
            status = videoinfo.status
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = ownerPK)
            username = userinfo.username
            nickName = userinfo.nickName

            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = videoinfo.videoPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status


            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
            
            # 작업완료되면 위에걸로 다시 바꿔야함 gogo
            # videoPATH = serverURL+"/static/audition_video"+videoPATH

            contents = videoinfo.contents
            hashTag = videoinfo.hashTag


            audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = str(audition_like_video_infoCount)

            audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = ownerPK, videoPK = videoPK).count()
            if audition_like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                audition_like_video_info_user = Audition_Like_video.objects.get(userPK = ownerPK, videoPK = videoPK)
                status = audition_like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"




            audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
            comentCount = str(audition_coment_infoCount)


            videoinfo = {
                'ownerPK':ownerPK,
                'videoPK':videoPK,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'userLikeCheck':userLikeCheck,
                'likeCount':likeCount,
                'comentCount':comentCount
            }

            # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
            text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfo':videoinfo}
            return HttpResponse(json.dumps(context))


        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK)
            ownerPK = videoinfo.userPK
            videoPK = videoinfo.id
            status = videoinfo.status
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = ownerPK)
            username = userinfo.username
            nickName = userinfo.nickName

            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = videoinfo.videoPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status


            # if s3Status == "0":
            #     videoPATH = serverURL+"/static/video"+videoPATH
            # elif s3Status == "1":
            #     videoPATH = s3PATH+videoPATH
            
            # 작업완료되면 위에걸로 다시 바꿔야함 gogo
            videoPATH = serverURL+"/static/audition_video"+videoPATH

            contents = videoinfo.contents
            hashTag = videoinfo.hashTag


            audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = str(audition_like_video_infoCount)

            audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = ownerPK, videoPK = videoPK).count()
            if audition_like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                audition_like_video_info_user = Audition_Like_video.objects.get(userPK = ownerPK, videoPK = videoPK)
                status = audition_like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"




            audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
            comentCount = str(audition_coment_infoCount)


            videoinfo = {
                'ownerPK':ownerPK,
                'videoPK':videoPK,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'userLikeCheck':userLikeCheck,
                'likeCount':likeCount,
                'comentCount':comentCount
            }

            # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
            text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfo':videoinfo}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_matchesListDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))

























# 이전 대진 내역
@csrf_exempt
def audition_previousMatcheslist(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            categoryListPK = data['categoryListPK']
            tournamentStatus = data['tournamentStatus']

            versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
            if versusListinfoCount == 0:
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
                versusListinfoList = []
                
                for index, i in enumerate(versusListinfo):
                    userPK_left = i.userPK_left
                    userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                    userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                    userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                    userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                    userPK_left_userNick = userPK_left_userinfo.nickName
                    userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                    if userPK_left_profileIMG_path:
                        userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                    else:
                        userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    LLS = i.LLS
                    LVS = i.LVS
                    LDS = i.LDS
                    LCS = i.LCS
                    LAS = i.LAS
                    
                    userPK_right = i.userPK_right
                    userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                    userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                    userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                    userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                    userPK_right_userNick = userPK_right_userinfo.nickName
                    userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                    if userPK_right_profileIMG_path:
                        userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                    else:
                        userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    RLS = i.RLS
                    RCS = i.RCS
                    RVS = i.RVS
                    RDS = i.RDS
                    RAS = i.RAS


                    dictinfo = {
                        'left': {
                            'userPK_left':userPK_left,
                            'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                            'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                            'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
                            'userPK_left_userNick':userPK_left_userNick,
                            'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
                            'LLS': LLS,
                            'LVS': LVS,
                            'LDS': LDS,
                            'LCS': LCS,
                            'LAS': LAS
                        },
                        'right': {
                            'userPK_right':userPK_right,
                            'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                            'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                            'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
                            'userPK_right_userNick':userPK_right_userNick,
                            'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
                            'RLS': RLS,
                            'RCS': RCS,
                            'RVS': RVS,
                            'RDS': RDS,
                            'RAS': RAS
                        },
                        'sum': int(LAS) + int(RAS)
                    }
                    versusListinfoList.append(dictinfo)          
                # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)

                text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'versusListinfoList':versusListinfoList}
                return HttpResponse(json.dumps(context))
            
        else:
            page = int(data['page'])
            pageStart = (page - 1) * 10
            pageEnd = 10 * page
            loginUserPK = data['loginUserPK']
            auditionListPK = data['auditionListPK']
            categoryListPK = data['categoryListPK']
            tournamentStatus = data['tournamentStatus']

            versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
            if versusListinfoCount == 0:
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
                versusListinfoList = []
                
                for index, i in enumerate(versusListinfo):
                    userPK_left = i.userPK_left
                    userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                    userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                    userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                    userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                    userPK_left_userNick = userPK_left_userinfo.nickName
                    userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                    if userPK_left_profileIMG_path:
                        userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                    else:
                        userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    LLS = i.LLS
                    LVS = i.LVS
                    LDS = i.LDS
                    LCS = i.LCS
                    LAS = i.LAS
                    
                    userPK_right = i.userPK_right
                    userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                    userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                    userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                    userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                    userPK_right_userNick = userPK_right_userinfo.nickName
                    userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                    if userPK_right_profileIMG_path:
                        userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                    else:
                        userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    RLS = i.RLS
                    RCS = i.RCS
                    RVS = i.RVS
                    RDS = i.RDS
                    RAS = i.RAS


                    dictinfo = {
                        'left': {
                            'userPK_left':userPK_left,
                            'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                            'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                            'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
                            'userPK_left_userNick':userPK_left_userNick,
                            'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
                            'LLS': LLS,
                            'LVS': LVS,
                            'LDS': LDS,
                            'LCS': LCS,
                            'LAS': LAS
                        },
                        'right': {
                            'userPK_right':userPK_right,
                            'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                            'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                            'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
                            'userPK_right_userNick':userPK_right_userNick,
                            'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
                            'RLS': RLS,
                            'RCS': RCS,
                            'RVS': RVS,
                            'RDS': RDS,
                            'RAS': RAS
                        },
                        'sum': int(LAS) + int(RAS)
                    }
                    versusListinfoList.append(dictinfo)          
                # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)

                text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'versusListinfoList':versusListinfoList}
                return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_videoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 오디션 영상 조회수
@csrf_exempt
def audition_videoViewCount(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            auditionViewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if auditionViewCount_infoCount == 0:
                auditionViewCount_info = Audition_ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                auditionViewCount_info.save()
                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.viewcount = str(int(Audition_Countinfo.viewcount) + 1)
                Audition_Countinfo.save()

                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LLS = str(int(i.LLS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RLS = str(int(i.RLS) + 1)
                #         i.save()
                #     else:
                #         pass

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
                ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
                ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))

        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            auditionViewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if auditionViewCount_infoCount == 0:
                auditionViewCount_info = Audition_ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                auditionViewCount_info.save()
                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.viewcount = str(int(Audition_Countinfo.viewcount) + 1)
                Audition_Countinfo.save()

                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LLS = str(int(i.LLS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RLS = str(int(i.RLS) + 1)
                #         i.save()
                #     else:
                #         pass

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
                ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
                ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# # 오디션 영상 좋아요
# @csrf_exempt
# def audition_videoLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         loginUserPK = data['loginUserPK']
#         videoPK = data['videoPK']


#         audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#         if audition_like_video_infoCount == 0:
#             like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#             like_video_info.save()
#             text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
#             ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
#         else:
#             audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#             status = audition_like_video_info.status
#             if status == "0":
#                 audition_like_video_info.status = "1"
#                 audition_like_video_info.save()
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
#                 ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             elif status == "1":
#                 audition_like_video_info.status = "0"
#                 audition_like_video_info.save()
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
#                 ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    

# # 오디션 영상 좋아요
# @csrf_exempt
# def audition_videoLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         loginUserPK = data['loginUserPK']
#         videoPK = data['videoPK']

#         audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#         if audition_like_video_infoCount == 0:
#             like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#             like_video_info.save()
#             text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
#             ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
#         else:
#             audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#             videoinfoPK = audition_like_video_info.videoPK
#             if videoPK == videoinfoPK:
#                 audition_like_video_info.status = "0"
#                 audition_like_video_info.save()
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
#                 ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 다른 좋아요 있음"
#                 ment = "\033[93m"+"audition_videoLike WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'9'}
#                 return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# 오디션 영상 좋아요
@csrf_exempt
def audition_videoLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if audition_like_video_infoCount == 0:
                like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                like_video_info.save()
                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK


                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
                Audition_Countinfo.save()

                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LLS = str(int(i.LLS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RLS = str(int(i.RLS) + 1)
                #         i.save()
                #     else:
                #         pass

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
                ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = audition_like_video_info.status
                if status == "0":
                    audition_like_video_info.status = "1"
                    audition_like_video_info.save()
                    auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                    videoOwner_userPK = auditionVideoinfo.userPK

                    Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                    Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
                    Audition_Countinfo.save()
                    # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                    # for index, i in enumerate(versusListinfo):
                    #     userPK_left = i.userPK_left
                    #     userPK_right = i.userPK_right
                    #     if videoOwner_userPK == userPK_left:
                    #         i.LLS = str(int(i.LLS) + 1)
                    #         i.save()
                    #     elif videoOwner_userPK == userPK_right:
                    #         i.RLS = str(int(i.RLS) + 1)
                    #         i.save()
                    #     else:
                    #         pass
                    text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
                    ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    audition_like_video_info.status = "0"
                    audition_like_video_info.save()
                    
                    auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                    videoOwner_userPK = auditionVideoinfo.userPK

                    Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                    likeCount = int(Audition_Countinfo.like)
                    if likeCount <= 0:
                        Audition_Countinfo.like = "0"
                        Audition_Countinfo.save()
                    else:
                        Audition_Countinfo.like = str(int(Audition_Countinfo.like) - 1)
                        Audition_Countinfo.save()

                    # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                    # for index, i in enumerate(versusListinfo):
                    #     userPK_left = i.userPK_left
                    #     userPK_right = i.userPK_right
                    #     if videoOwner_userPK == userPK_left:
                    #         i.LLS = str(int(i.LLS) - 1)
                    #         i.save()
                    #     elif videoOwner_userPK == userPK_right:
                    #         i.RLS = str(int(i.RLS) - 1)
                    #         i.save()
                    #     else:
                    #         pass

                    text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
                    ment = "\033[93m"+"audition_audition_videoLike WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if audition_like_video_infoCount == 0:
                like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                like_video_info.save()
                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK


                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
                Audition_Countinfo.save()

                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LLS = str(int(i.LLS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RLS = str(int(i.RLS) + 1)
                #         i.save()
                #     else:
                #         pass

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
                ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = audition_like_video_info.status
                if status == "0":
                    audition_like_video_info.status = "1"
                    audition_like_video_info.save()
                    auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                    videoOwner_userPK = auditionVideoinfo.userPK

                    Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                    Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
                    Audition_Countinfo.save()
                    # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                    # for index, i in enumerate(versusListinfo):
                    #     userPK_left = i.userPK_left
                    #     userPK_right = i.userPK_right
                    #     if videoOwner_userPK == userPK_left:
                    #         i.LLS = str(int(i.LLS) + 1)
                    #         i.save()
                    #     elif videoOwner_userPK == userPK_right:
                    #         i.RLS = str(int(i.RLS) + 1)
                    #         i.save()
                    #     else:
                    #         pass
                    text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
                    ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    audition_like_video_info.status = "0"
                    audition_like_video_info.save()
                    
                    auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                    videoOwner_userPK = auditionVideoinfo.userPK

                    Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                    likeCount = int(Audition_Countinfo.like)
                    if likeCount <= 0:
                        Audition_Countinfo.like = "0"
                        Audition_Countinfo.save()
                    else:
                        Audition_Countinfo.like = str(int(Audition_Countinfo.like) - 1)
                        Audition_Countinfo.save()

                    # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                    # for index, i in enumerate(versusListinfo):
                    #     userPK_left = i.userPK_left
                    #     userPK_right = i.userPK_right
                    #     if videoOwner_userPK == userPK_left:
                    #         i.LLS = str(int(i.LLS) - 1)
                    #         i.save()
                    #     elif videoOwner_userPK == userPK_right:
                    #         i.RLS = str(int(i.RLS) - 1)
                    #         i.save()
                    #     else:
                    #         pass

                    text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
                    ment = "\033[93m"+"audition_audition_videoLike WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 오디션 댓글 리스트
@csrf_exempt
def audition_comentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            audition_comentinfoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()

            if audition_comentinfoCount == 0:
                text = "댓글 없음"
                ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'0', 'comentinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                audition_comentinfo = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
                audition_comentinfoList = []
                for index, i in enumerate(audition_comentinfo):
                    now  = int(round(time.time()))
                    userPK = i.userPK
                    comentPK = i.id
                    createAt = i.createAt
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    previous = ""
                    previous_date = ""
                    likeCount = ""
                    userComentLikeCheck = ""
                    comentONcomentCount = ""
                    userComentONComentCheck = ""
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)

                    # if me_time < 1 :
                    #     previous = '방금전'
                        
                    # elif me_time < 60 :
                    #     previous = str(me_time) + '분전'

                    # elif me_timehour < 24 :
                    #     previous = str(me_timehour) + '시간전'
                    
                    # elif me_timeday < 365 :
                    #     previous = str(me_timeday) + '일전'
                    
                    # elif me_timeyear >= 1 : 
                    #     previous = str(me_timeyear) + '년전'


                    if me_time < 1 :
                        # previous = '방금전'
                        previous = 'B'
                        previous_date = "0"
                        
                    elif me_time < 60 :
                        # previous = str(me_time) + '분전'
                        previous = 'M'
                        previous_date = str(me_time)

                    elif me_timehour < 24 :
                        # previous = str(me_timehour) + '시간전'
                        previous = 'H'
                        previous_date = str(me_timehour)
                    
                    elif me_timeday < 365 :
                        # previous = str(me_timeday) + '일전'
                        previous = 'D'
                        previous_date = str(me_timeday)

                    elif me_timeyear >= 1 : 
                        # previous = str(me_timeyear) + '년전'
                        previous = 'Y'
                        previous_date = str(me_timeyear)

                    audition_like_coment_infoCount = Audition_Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
                    likeCount =  str(audition_like_coment_infoCount)

                    audition_like_coment_infoCount_user = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if audition_like_coment_infoCount_user == 0:
                        userComentLikeCheck = "0"
                    else:
                        audition_Like_coment_info_user = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
                        status = audition_Like_coment_info_user.status
                        if status == "0":
                            userComentLikeCheck = "0"
                        elif status == "1":
                            userComentLikeCheck = "1"


                    audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
                    comentONcomentCount = str(audition_comentOnComent_infoCount)

                    if audition_comentOnComent_infoCount == 0:
                        pass
                    else:
                        audition_comentOnComent_info = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0")
                        for index, k in enumerate(audition_comentOnComent_info):
                            userPK_comentOnComent = k.userPK
                            userBlockListinfoCount_likecomentOnComent = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_comentOnComent, status = "1").count()
                            if userBlockListinfoCount_likecomentOnComent == 1:
                                comentONcomentCount -= 1

                            comentONcomentPK = k.id
                            audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(loginUserPK = loginUserPK, commentCommentPK = comentONcomentPK).count() # 오디션에 넣고 삭제 해야함
                            if audition_CommentCommentDeclarationinfoCount:
                                comentONcomentCount -= 1


                    audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if audition_comentOnComent_infoCount_user == 0:
                        userComentONComentCheck = "0"
                    else:
                        userComentONComentCheck = "1"




                    audition_comentDict = {
                        'comentPK':comentPK,
                        'videoPK':videoPK,
                        'userPK':userPK,
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'previous':previous,
                        'previous_date':previous_date,
                        'likeCount':likeCount,
                        'comentONcomentLen':comentONcomentCount,
                        'userComentLikeCheck':userComentLikeCheck,
                        'userComentONComentCheck':userComentONComentCheck

                    }
                    audition_comentinfoList.append(audition_comentDict)

                text = "\033[92m"+"audition_comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'audition_comentinfoList':audition_comentinfoList}
                return HttpResponse(json.dumps(context))
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            audition_comentinfoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()

            if audition_comentinfoCount == 0:
                text = "댓글 없음"
                ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'0', 'comentinfoList':None}
                return HttpResponse(json.dumps(context))
            else:
                audition_comentinfo = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
                audition_comentinfoList = []
                for index, i in enumerate(audition_comentinfo):
                    now  = int(round(time.time()))
                    userPK = i.userPK
                    comentPK = i.id
                    createAt = i.createAt
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    previous = ""
                    previous_date = ""
                    likeCount = ""
                    userComentLikeCheck = ""
                    comentONcomentCount = ""
                    userComentONComentCheck = ""
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)

                    # if me_time < 1 :
                    #     previous = '방금전'
                        
                    # elif me_time < 60 :
                    #     previous = str(me_time) + '분전'

                    # elif me_timehour < 24 :
                    #     previous = str(me_timehour) + '시간전'
                    
                    # elif me_timeday < 365 :
                    #     previous = str(me_timeday) + '일전'
                    
                    # elif me_timeyear >= 1 : 
                    #     previous = str(me_timeyear) + '년전'


                    if me_time < 1 :
                        # previous = '방금전'
                        previous = 'B'
                        previous_date = "0"
                        
                    elif me_time < 60 :
                        # previous = str(me_time) + '분전'
                        previous = 'M'
                        previous_date = str(me_time)

                    elif me_timehour < 24 :
                        # previous = str(me_timehour) + '시간전'
                        previous = 'H'
                        previous_date = str(me_timehour)
                    
                    elif me_timeday < 365 :
                        # previous = str(me_timeday) + '일전'
                        previous = 'D'
                        previous_date = str(me_timeday)

                    elif me_timeyear >= 1 : 
                        # previous = str(me_timeyear) + '년전'
                        previous = 'Y'
                        previous_date = str(me_timeyear)

                    audition_like_coment_infoCount = Audition_Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
                    likeCount =  str(audition_like_coment_infoCount)

                    audition_like_coment_infoCount_user = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if audition_like_coment_infoCount_user == 0:
                        userComentLikeCheck = "0"
                    else:
                        audition_Like_coment_info_user = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
                        status = audition_Like_coment_info_user.status
                        if status == "0":
                            userComentLikeCheck = "0"
                        elif status == "1":
                            userComentLikeCheck = "1"


                    audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK).count()
                    comentONcomentCount = str(audition_comentOnComent_infoCount)

                    audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if audition_comentOnComent_infoCount_user == 0:
                        userComentONComentCheck = "0"
                    else:
                        userComentONComentCheck = "1"

                    audition_comentDict = {
                        'comentPK':comentPK,
                        'videoPK':videoPK,
                        'userPK':userPK,
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'previous':previous,
                        'previous_date':previous_date,
                        'likeCount':likeCount,
                        'comentONcomentLen':comentONcomentCount,
                        'userComentLikeCheck':userComentLikeCheck,
                        'userComentONComentCheck':userComentONComentCheck

                    }
                    audition_comentinfoList.append(audition_comentDict)

                text = "\033[92m"+"audition_comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'audition_comentinfoList':audition_comentinfoList}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_comentList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99', 'comentinfoList':None}
        return HttpResponse(json.dumps(context))
    


# 오디션 댓글 저장 ( 작품당 1회 카운트 )
@csrf_exempt
def audition_comentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            contents = data['contents']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            audition_comentinfoCount = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if audition_comentinfoCount == 0:

                audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
                audition_comentSubmit.save()

                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK
                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LCS = str(int(i.LCS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RCS = str(int(i.RCS) + 1)
                #         i.save()
                #     else:
                #         pass
                        
                comentPK = audition_comentSubmit.id
                comentinfo = Audition_Coment.objects.get(id = comentPK)
                userPK = comentinfo.userPK
                videoPK = comentinfo.videoPK
                contents = comentinfo.contents
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                name = userinfo.name
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                previous = ""
                previous_date = ""
                userComentLikeCheck = ""
                userComentONComentCheck = ""
                now  = int(round(time.time()))
                createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)

                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'
                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                # comentCount = Coment.objects.filter(videoPK = videoPK).count()

                coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
                comentCount = coment_infoCount

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.coment = str(int(Audition_Countinfo.coment) + 1)
                Audition_Countinfo.save()

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                comentCount = int(Audition_Countinfo.coment)
                
                # if coment_infoCount == 0:
                #     pass
                # else:
                #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
                #     for index, k in enumerate(coment_info):
                #         userPK_coment = k.userPK
                #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                #         if userBlockListinfoCount_coment == 1:
                #             comentCount -= 1


                coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                userComentCheck = ""
                if coment_infoCount_user == 0:
                    userComentCheck = "0"
                else:
                    userComentCheck = "1"

                comentinfo = {
                    'videoOwner_userPK':videoOwner_userPK,
                    'comentPK':str(comentPK),
                    'videoPK':videoPK,
                    'username':username,
                    'nickName':nickName,
                    'name':name,
                    'profileIMG_path':profileIMG_path,
                    'previous':previous,
                    'previous_date':previous_date,
                    'comentCount':str(comentCount),
                    'userComentCheck':userComentCheck
                }

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
                ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
                audition_comentSubmit.save()

                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK

                comentPK = audition_comentSubmit.id
                comentinfo = Audition_Coment.objects.get(id = comentPK)
                userPK = comentinfo.userPK
                videoPK = comentinfo.videoPK
                contents = comentinfo.contents
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                name = userinfo.name
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                previous = ""
                previous_date = ""
                userComentLikeCheck = ""
                userComentONComentCheck = ""
                now  = int(round(time.time()))
                createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)

                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'
                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                # comentCount = Coment.objects.filter(videoPK = videoPK).count()

                # coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
                # comentCount = coment_infoCount

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                comentCount = int(Audition_Countinfo.coment)

                # if coment_infoCount == 0:
                #     pass
                # else:
                #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
                #     for index, k in enumerate(coment_info):
                #         userPK_coment = k.userPK
                #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                #         if userBlockListinfoCount_coment == 1:
                #             comentCount -= 1


                coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                userComentCheck = ""
                if coment_infoCount_user == 0:
                    userComentCheck = "0"
                else:
                    userComentCheck = "1"

                comentinfo = {
                    'videoOwner_userPK':videoOwner_userPK,
                    'comentPK':str(comentPK),
                    'videoPK':videoPK,
                    'username':username,
                    'nickName':nickName,
                    'name':name,
                    'profileIMG_path':profileIMG_path,
                    'previous':previous,
                    'previous_date':previous_date,
                    'comentCount':str(comentCount),
                    'userComentCheck':userComentCheck
                }

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
                ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))  
                      
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
            contents = data['contents']
            auditionListPK = data['auditionListPK']
            tournamentStatus = data['tournamentStatus']
            categoryPK = data['categoryPK']

            audition_comentinfoCount = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus).count()
            if audition_comentinfoCount == 0:

                audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                audition_comentSubmit.save()

                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK
                # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
                # for index, i in enumerate(versusListinfo):
                #     userPK_left = i.userPK_left
                #     userPK_right = i.userPK_right
                #     if videoOwner_userPK == userPK_left:
                #         i.LCS = str(int(i.LCS) + 1)
                #         i.save()
                #     elif videoOwner_userPK == userPK_right:
                #         i.RCS = str(int(i.RCS) + 1)
                #         i.save()
                #     else:
                #         pass
                        
                comentPK = audition_comentSubmit.id
                comentinfo = Audition_Coment.objects.get(id = comentPK)
                userPK = comentinfo.userPK
                videoPK = comentinfo.videoPK
                contents = comentinfo.contents
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                name = userinfo.name
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                previous = ""
                previous_date = ""
                userComentLikeCheck = ""
                userComentONComentCheck = ""
                now  = int(round(time.time()))
                createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)

                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'
                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                # comentCount = Coment.objects.filter(videoPK = videoPK).count()

                coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
                comentCount = coment_infoCount

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                Audition_Countinfo.coment = str(int(Audition_Countinfo.coment) + 1)
                Audition_Countinfo.save()

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                comentCount = int(Audition_Countinfo.coment)
                
                # if coment_infoCount == 0:
                #     pass
                # else:
                #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
                #     for index, k in enumerate(coment_info):
                #         userPK_coment = k.userPK
                #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                #         if userBlockListinfoCount_coment == 1:
                #             comentCount -= 1


                coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                userComentCheck = ""
                if coment_infoCount_user == 0:
                    userComentCheck = "0"
                else:
                    userComentCheck = "1"

                comentinfo = {
                    'videoOwner_userPK':videoOwner_userPK,
                    'comentPK':str(comentPK),
                    'videoPK':videoPK,
                    'username':username,
                    'nickName':nickName,
                    'name':name,
                    'profileIMG_path':profileIMG_path,
                    'previous':previous,
                    'previous_date':previous_date,
                    'comentCount':str(comentCount),
                    'userComentCheck':userComentCheck
                }

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
                ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                audition_comentSubmit.save()

                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK

                comentPK = audition_comentSubmit.id
                comentinfo = Audition_Coment.objects.get(id = comentPK)
                userPK = comentinfo.userPK
                videoPK = comentinfo.videoPK
                contents = comentinfo.contents
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                name = userinfo.name
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                previous = ""
                previous_date = ""
                userComentLikeCheck = ""
                userComentONComentCheck = ""
                now  = int(round(time.time()))
                createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
                me_time = math.floor(((now - createAt_timestamp) / 60))
                me_timehour = math.floor((me_time / 60))
                me_timeday = math.floor((me_timehour / 24))
                me_timeyear = math.floor(me_timeday / 365)

                # if me_time < 1 :
                #     previous = '방금전'
                    
                # elif me_time < 60 :
                #     previous = str(me_time) + '분전'

                # elif me_timehour < 24 :
                #     previous = str(me_timehour) + '시간전'
                
                # elif me_timeday < 365 :
                #     previous = str(me_timeday) + '일전'
                
                # elif me_timeyear >= 1 : 
                #     previous = str(me_timeyear) + '년전'
                if me_time < 1 :
                    # previous = '방금전'
                    previous = 'B'
                    previous_date = "0"
                    
                elif me_time < 60 :
                    # previous = str(me_time) + '분전'
                    previous = 'M'
                    previous_date = str(me_time)

                elif me_timehour < 24 :
                    # previous = str(me_timehour) + '시간전'
                    previous = 'H'
                    previous_date = str(me_timehour)
                
                elif me_timeday < 365 :
                    # previous = str(me_timeday) + '일전'
                    previous = 'D'
                    previous_date = str(me_timeday)

                elif me_timeyear >= 1 : 
                    # previous = str(me_timeyear) + '년전'
                    previous = 'Y'
                    previous_date = str(me_timeyear)

                # comentCount = Coment.objects.filter(videoPK = videoPK).count()

                # coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
                # comentCount = coment_infoCount

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
                comentCount = int(Audition_Countinfo.coment)

                # if coment_infoCount == 0:
                #     pass
                # else:
                #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
                #     for index, k in enumerate(coment_info):
                #         userPK_coment = k.userPK
                #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                #         if userBlockListinfoCount_coment == 1:
                #             comentCount -= 1


                coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                userComentCheck = ""
                if coment_infoCount_user == 0:
                    userComentCheck = "0"
                else:
                    userComentCheck = "1"

                comentinfo = {
                    'videoOwner_userPK':videoOwner_userPK,
                    'comentPK':str(comentPK),
                    'videoPK':videoPK,
                    'username':username,
                    'nickName':nickName,
                    'name':name,
                    'profileIMG_path':profileIMG_path,
                    'previous':previous,
                    'previous_date':previous_date,
                    'comentCount':str(comentCount),
                    'userComentCheck':userComentCheck
                }

                text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
                ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))         


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_comentSubmit Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# 오디션 댓글 저장 ( 전체에서 1회 로직 )
# @csrf_exempt
# def audition_comentSubmit(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         loginUserPK = data['loginUserPK']
#         videoPK = data['videoPK']
#         contents = data['contents']

#         print(videoPK)
#         print(contents)

#         audition_comentinfoCount = Audition_Coment.objects.filter(userPK = loginUserPK, status = "0").count()
#         if audition_comentinfoCount == 0:
#             audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#             audition_comentSubmit.save()
#             comentPK = audition_comentSubmit.id
#             comentinfo = Audition_Coment.objects.get(id = comentPK)
#             userPK = comentinfo.userPK
#             videoPK = comentinfo.videoPK
#             contents = comentinfo.contents
#             userinfo = SignUp.objects.get(id = userPK)
#             username = userinfo.username
#             nickName = userinfo.nickName
#             name = userinfo.name
#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
#             previous = ""
#             likeCount = ""
#             userComentLikeCheck = ""
#             comentONcomentCount = ""
#             userComentONComentCheck = ""
#             now  = int(round(time.time()))
#             createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
#             me_time = math.floor(((now - createAt_timestamp) / 60))
#             me_timehour = math.floor((me_time / 60))
#             me_timeday = math.floor((me_timehour / 24))
#             me_timeyear = math.floor(me_timeday / 365)

#             if me_time < 1 :
#                 previous = '방금전'
                
#             elif me_time < 60 :
#                 previous = str(me_time) + '분전'

#             elif me_timehour < 24 :
#                 previous = str(me_timehour) + '시간전'
            
#             elif me_timeday < 365 :
#                 previous = str(me_timeday) + '일전'
            
#             elif me_timeyear >= 1 : 
#                 previous = str(me_timeyear) + '년전'


#             comentCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#             coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             userComentCheck = ""
#             if coment_infoCount_user == 0:
#                 userComentCheck = "0"
#             else:
#                 userComentCheck = "1"

#             comentinfo = {
#                 'comentPK':comentPK,
#                 'videoPK':videoPK,
#                 'username':username,
#                 'nickName':nickName,
#                 'name':name,
#                 'profileIMG_path':profileIMG_path,
#                 'previous':previous,
#                 'comentCount':comentCount,
#                 'userComentCheck':userComentCheck
#             }

#             text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 오디션 댓글 완료"
#             ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1', 'comentinfo':comentinfo}
#             return HttpResponse(json.dumps(context))               
#         else:
#             text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 오디션 댓글 있음"
#             ment = "\033[93m"+"audition_comentSubmit WARNING -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#             context = {'code':'2'}
#             return HttpResponse(json.dumps(context))
        
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentSubmit Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# 오디션 댓글 삭제
@csrf_exempt
def audition_ComentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        comentPK = data['comentPK']
        loginUserPK = str(data['loginUserPK'])
        videoPK = str(data['videoPK'])
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']
        categoryPK = data['categoryPK']

        auditionVideoinfo = Audition_video.objects.get(id = videoPK)
        videoOwner_userPK = auditionVideoinfo.userPK
        # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
        # for index, i in enumerate(versusListinfo):
        #     userPK_left = i.userPK_left
        #     userPK_right = i.userPK_right
        #     if videoOwner_userPK == userPK_left:
        #         i.LCS = str(int(i.LCS) - 1)
        #         i.save()
        #     elif videoOwner_userPK == userPK_right:
        #         i.RCS = str(int(i.RCS) - 1)
        #         i.save()
        #     else:
        #         pass

        audition_comentinfo = Audition_Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
        audition_comentinfo.status = "9"
        audition_comentinfo.save()

        text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", 오디션 댓글 삭제 완료"
        ment = "\033[92m"+"comentDel SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1'}
        return HttpResponse(json.dumps(context))
        

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))


# # 오디션 댓글 좋아요
# @csrf_exempt
# def audition_comentLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         loginUserPK = str(data['loginUserPK'])
#         comentPK = str(data['comentPK'])
#         videoPK = str(data['videoPK'])

#         audition_like_coment_infoCount = Audition_Like_coment.objects.filter(userPK = loginUserPK).count()
#         if audition_like_coment_infoCount == 0:
#             audition_like_coment_info = Audition_Like_coment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#             audition_like_coment_info.save()
#             text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
#             ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
#         else:
#             audition_like_coment_info = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
#             status = audition_like_coment_info.status
#             if status == "0":
#                 audition_like_coment_info.status = "1"
#                 audition_like_coment_info.save()
#                 text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
#                 ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             elif status == "1":
#                 audition_like_coment_info.status = "0"
#                 audition_like_coment_info.save()
#                 text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
#                 ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))

# 오디션 댓글 좋아요
@csrf_exempt
def audition_comentLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])
            
            audition_like_coment_infoCount = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()


            if audition_like_coment_infoCount == 0:
                audition_like_coment_info = Audition_Like_coment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                audition_like_coment_info.save()

                text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
                ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_coment_info = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)




                status = audition_like_coment_info.status
                if status == "0":
                    audition_like_coment_info.status = "1"
                    audition_like_coment_info.save()
                    text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
                    ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    audition_like_coment_info.status = "0"
                    audition_like_coment_info.save()
                    text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
                    ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])
            
            audition_like_coment_infoCount = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()


            if audition_like_coment_infoCount == 0:
                audition_like_coment_info = Audition_Like_coment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                audition_like_coment_info.save()

                text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
                ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_coment_info = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)




                status = audition_like_coment_info.status
                if status == "0":
                    audition_like_coment_info.status = "1"
                    audition_like_coment_info.save()
                    text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
                    ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    audition_like_coment_info.status = "0"
                    audition_like_coment_info.save()
                    text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
                    ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_comentLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# # 오디션 대댓글 리스트
# @csrf_exempt
# def audition_comentONcomentList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             comentPK = data['comentPK']
#             videoPK = data['videoPK']
            
#             audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
#             if audition_comentOnComentinfoCount == 0:
#                 text = "대댓글 없음"
#                 ment = "\033[93m"+"audition_comentONcomentList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'comentONcomentList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentOnComentinfo = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").order_by('-id')
#                 audition_comentONcomentList = []
#                 for index, i in enumerate(audition_comentOnComentinfo):
#                     comentONcomentPK = i.id
#                     now  = int(round(time.time()))
#                     userPK = i.userPK
#                     createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                     contents = i.contents
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"



#                     likeCount = ""
#                     previous = ""
#                     previous_date = ""
#                     userComentONComentLikeCheck = ""
#                     me_time = math.floor(((now - createAt_timestamp) / 60))
#                     me_timehour = math.floor((me_time / 60))
#                     me_timeday = math.floor((me_timehour / 24))
#                     me_timeyear = math.floor(me_timeday / 365)


                    
#                     # if me_time < 1 :
#                     #     previous = '방금전'
                        
#                     # elif me_time < 60 :
#                     #     previous = str(me_time) + '분전'

#                     # elif me_timehour < 24 :
#                     #     previous = str(me_timehour) + '시간전'
                    
#                     # elif me_timeday < 365 :
#                     #     previous = str(me_timeday) + '일전'
                    
#                     # elif me_timeyear >= 1 : 
#                     #     previous = str(me_timeyear) + '년전'


#                     if me_time < 1 :
#                         # previous = '방금전'
#                         previous = 'B'
#                         previous_date = "0"
                        
#                     elif me_time < 60 :
#                         # previous = str(me_time) + '분전'
#                         previous = 'M'
#                         previous_date = str(me_time)

#                     elif me_timehour < 24 :
#                         # previous = str(me_timehour) + '시간전'
#                         previous = 'H'
#                         previous_date = str(me_timehour)
                    
#                     elif me_timeday < 365 :
#                         # previous = str(me_timeday) + '일전'
#                         previous = 'D'
#                         previous_date = str(me_timeday)

#                     elif me_timeyear >= 1 : 
#                         # previous = str(me_timeyear) + '년전'
#                         previous = 'Y'
#                         previous_date = str(me_timeyear)

#                     audition_like_comentONcoment_infoCount = Audition_Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
#                     likeCount = str(audition_like_comentONcoment_infoCount)

#                     audition_like_comentONcoment_infoCount_user = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
#                     if audition_like_comentONcoment_infoCount_user == 0:
#                         userComentONComentLikeCheck = "0"
#                     else:
#                         audition_like_comentONcoment_info_user = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
#                         status = audition_like_comentONcoment_info_user.status
#                         if status == "0":
#                             userComentONComentLikeCheck = "0"
#                         elif status == "1":
#                             userComentONComentLikeCheck = "1"


#                     audition_comentOnComentinfoDict = {
#                         'comentONcomentPK':comentONcomentPK,
#                         'comentPK':comentPK,
#                         'videoPK':videoPK,
#                         'userPK':userPK,
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'previous':previous,
#                         'previous_date':previous_date,
#                         'likeCount':likeCount,
#                         'userComentONComentLikeCheck':userComentONComentLikeCheck
#                     }
#                     audition_comentONcomentList.append(audition_comentOnComentinfoDict)
                    
#                 text = "\033[92m"+"audition_comentONcomentList SUCCESS -> 대댓글 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_comentONcomentList':audition_comentONcomentList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             loginUserPK = data['loginUserPK']
#             comentPK = data['comentPK']
#             videoPK = data['videoPK']
            
#             audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
#             if audition_comentOnComentinfoCount == 0:
#                 text = "대댓글 없음"
#                 ment = "\033[93m"+"audition_comentONcomentList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'comentONcomentList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentOnComentinfo = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").order_by('-id')
#                 audition_comentONcomentList = []
#                 for index, i in enumerate(audition_comentOnComentinfo):
#                     comentONcomentPK = i.id
#                     now  = int(round(time.time()))
#                     userPK = i.userPK
#                     createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                     contents = i.contents
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3_profileimgPATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"



#                     likeCount = ""
#                     previous = ""
#                     previous_date = ""
#                     userComentONComentLikeCheck = ""
#                     me_time = math.floor(((now - createAt_timestamp) / 60))
#                     me_timehour = math.floor((me_time / 60))
#                     me_timeday = math.floor((me_timehour / 24))
#                     me_timeyear = math.floor(me_timeday / 365)


                    
#                     # if me_time < 1 :
#                     #     previous = '방금전'
                        
#                     # elif me_time < 60 :
#                     #     previous = str(me_time) + '분전'

#                     # elif me_timehour < 24 :
#                     #     previous = str(me_timehour) + '시간전'
                    
#                     # elif me_timeday < 365 :
#                     #     previous = str(me_timeday) + '일전'
                    
#                     # elif me_timeyear >= 1 : 
#                     #     previous = str(me_timeyear) + '년전'


#                     if me_time < 1 :
#                         # previous = '방금전'
#                         previous = 'B'
#                         previous_date = "0"
                        
#                     elif me_time < 60 :
#                         # previous = str(me_time) + '분전'
#                         previous = 'M'
#                         previous_date = str(me_time)

#                     elif me_timehour < 24 :
#                         # previous = str(me_timehour) + '시간전'
#                         previous = 'H'
#                         previous_date = str(me_timehour)
                    
#                     elif me_timeday < 365 :
#                         # previous = str(me_timeday) + '일전'
#                         previous = 'D'
#                         previous_date = str(me_timeday)

#                     elif me_timeyear >= 1 : 
#                         # previous = str(me_timeyear) + '년전'
#                         previous = 'Y'
#                         previous_date = str(me_timeyear)

#                     audition_like_comentONcoment_infoCount = Audition_Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
#                     likeCount = str(audition_like_comentONcoment_infoCount)

#                     audition_like_comentONcoment_infoCount_user = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
#                     if audition_like_comentONcoment_infoCount_user == 0:
#                         userComentONComentLikeCheck = "0"
#                     else:
#                         audition_like_comentONcoment_info_user = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
#                         status = audition_like_comentONcoment_info_user.status
#                         if status == "0":
#                             userComentONComentLikeCheck = "0"
#                         elif status == "1":
#                             userComentONComentLikeCheck = "1"


#                     audition_comentOnComentinfoDict = {
#                         'comentONcomentPK':comentONcomentPK,
#                         'comentPK':comentPK,
#                         'videoPK':videoPK,
#                         'userPK':userPK,
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'previous':previous,
#                         'previous_date':previous_date,
#                         'likeCount':likeCount,
#                         'userComentONComentLikeCheck':userComentONComentLikeCheck
#                     }
#                     audition_comentONcomentList.append(audition_comentOnComentinfoDict)
                    
#                 text = "\033[92m"+"audition_comentONcomentList SUCCESS -> 대댓글 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_comentONcomentList':audition_comentONcomentList}
#                 return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentONcomentList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# 오디션 대댓글 리스트
@csrf_exempt
def audition_comentONcomentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        comentPK = data['comentPK']
        videoPK = data['videoPK']
        
        audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
        if audition_comentOnComentinfoCount == 0:
            text = "대댓글 없음"
            ment = "\033[93m"+"audition_comentONcomentList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'comentONcomentList':None}
            return HttpResponse(json.dumps(context))
        else:
            audition_comentOnComentinfo = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").order_by('-id')
            audition_comentONcomentList = []
            for index, i in enumerate(audition_comentOnComentinfo):
                comentONcomentPK = i.id
                audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(loginUserPK = loginUserPK, commentCommentPK = comentONcomentPK).count()

                if audition_CommentCommentDeclarationinfoCount == 0:
                    now  = int(round(time.time()))
                    userPK = i.userPK
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"



                    likeCount = ""
                    previous = ""
                    previous_date = ""
                    userComentONComentLikeCheck = ""
                    me_time = math.floor(((now - createAt_timestamp) / 60))
                    me_timehour = math.floor((me_time / 60))
                    me_timeday = math.floor((me_timehour / 24))
                    me_timeyear = math.floor(me_timeday / 365)


                    
                    # if me_time < 1 :
                    #     previous = '방금전'
                        
                    # elif me_time < 60 :
                    #     previous = str(me_time) + '분전'

                    # elif me_timehour < 24 :
                    #     previous = str(me_timehour) + '시간전'
                    
                    # elif me_timeday < 365 :
                    #     previous = str(me_timeday) + '일전'
                    
                    # elif me_timeyear >= 1 : 
                    #     previous = str(me_timeyear) + '년전'


                    if me_time < 1 :
                        # previous = '방금전'
                        previous = 'B'
                        previous_date = "0"
                        
                    elif me_time < 60 :
                        # previous = str(me_time) + '분전'
                        previous = 'M'
                        previous_date = str(me_time)

                    elif me_timehour < 24 :
                        # previous = str(me_timehour) + '시간전'
                        previous = 'H'
                        previous_date = str(me_timehour)
                    
                    elif me_timeday < 365 :
                        # previous = str(me_timeday) + '일전'
                        previous = 'D'
                        previous_date = str(me_timeday)

                    elif me_timeyear >= 1 : 
                        # previous = str(me_timeyear) + '년전'
                        previous = 'Y'
                        previous_date = str(me_timeyear)

                    audition_like_comentONcoment_infoCount = Audition_Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
                    likeCount = str(audition_like_comentONcoment_infoCount)

                    audition_like_comentONcoment_infoCount_user = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
                    if audition_like_comentONcoment_infoCount_user == 0:
                        userComentONComentLikeCheck = "0"
                    else:
                        audition_like_comentONcoment_info_user = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                        status = audition_like_comentONcoment_info_user.status
                        if status == "0":
                            userComentONComentLikeCheck = "0"
                        elif status == "1":
                            userComentONComentLikeCheck = "1"


                    audition_comentOnComentinfoDict = {
                        'comentONcomentPK':comentONcomentPK,
                        'comentPK':comentPK,
                        'videoPK':videoPK,
                        'userPK':userPK,
                        'username':username,
                        'nickName':nickName,
                        'profileIMG_path':profileIMG_path,
                        'contents':contents,
                        'previous':previous,
                        'previous_date':previous_date,
                        'likeCount':likeCount,
                        'userComentONComentLikeCheck':userComentONComentLikeCheck
                    }
                    audition_comentONcomentList.append(audition_comentOnComentinfoDict)
                
            text = "\033[92m"+"audition_comentONcomentList SUCCESS -> 대댓글 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'audition_comentONcomentList':audition_comentONcomentList}
            return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_comentONcomentList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))







# 오디션 대댓글 저장
@csrf_exempt
def audition_comentONcomentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            comentPK = data['comentPK']
            videoPK = data['videoPK']
            contents = data['contents']

            # audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
            # if audition_comentOnComentinfoCount == 0:
            audition_comentOnComentSubmit = Audition_ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            audition_comentOnComentSubmit.save()

            text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
            ment = "\033[92m"+"audition_comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            loginUserPK = data['loginUserPK']
            comentPK = data['comentPK']
            videoPK = data['videoPK']
            contents = data['contents']

            # audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
            # if audition_comentOnComentinfoCount == 0:
            audition_comentOnComentSubmit = Audition_ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
            audition_comentOnComentSubmit.save()

            text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
            ment = "\033[92m"+"audition_comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_comentONcomentSubmit Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 오디션 대댓글 삭제
@csrf_exempt
def audition_ComentOnComentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            comentONcomentPK = data['comentONcomentPK']
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            comentONcomentinfo = Audition_ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
        else:
            comentONcomentPK = data['comentONcomentPK']
            loginUserPK = str(data['loginUserPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            comentONcomentinfo = Audition_ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

            comentONcomentinfo.status = "9"
            comentONcomentinfo.save()
            text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
            ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 오디션 대댓글 좋아요
@csrf_exempt
def audition_comentONcomentLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = str(data['loginUserPK'])
            comentONcomentPK = str(data['comentONcomentPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            audition_like_comentONcomentinfoCount = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if audition_like_comentONcomentinfoCount == 0:
                audition_Like_comentONcomentinfo = Audition_Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                audition_Like_comentONcomentinfo.save()
                text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
                ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_comentONcomentinfo = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = audition_like_comentONcomentinfo.status
                if status == "0":
                    audition_like_comentONcomentinfo.status = "1"
                    audition_like_comentONcomentinfo.save()
                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    audition_like_comentONcomentinfo.status = "0"
                    audition_like_comentONcomentinfo.save()

                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = str(data['loginUserPK'])
            comentONcomentPK = str(data['comentONcomentPK'])
            comentPK = str(data['comentPK'])
            videoPK = str(data['videoPK'])

            audition_like_comentONcomentinfoCount = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
            if audition_like_comentONcomentinfoCount == 0:
                audition_Like_comentONcomentinfo = Audition_Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
                audition_Like_comentONcomentinfo.save()
                text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
                ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                audition_like_comentONcomentinfo = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
                status = audition_like_comentONcomentinfo.status
                if status == "0":
                    audition_like_comentONcomentinfo.status = "1"
                    audition_like_comentONcomentinfo.save()
                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    audition_like_comentONcomentinfo.status = "0"
                    audition_like_comentONcomentinfo.save()

                    text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
                    ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"comentONcomentLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# 내가등록한 오디션 영상리스트 현황 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 )
@csrf_exempt
def audition_myVideoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            # page = int(data['page'])
            # pageStart = (page - 1) * 10
            # pageEnd = 10 * page
            loginUserPK = data['loginUserPK']


            videoinfoCount = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
            if videoinfoCount == 0:
                text = "내가 업로드한 비디오 리스트 없음"
                ment = "\033[93m"+"audition_myVideoList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'0', 'videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:        
                # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
                videoinfo = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
                videoinfoList = []
                for index, i in enumerate(videoinfo):
                    userPK = i.userPK
                    videoPK = i.id
                    categoryPK = i.categoryPK
                    tournamentStatus = i.tournamentStatus
                    progressStatus = i.progressStatus
                    auditionListPK = i.auditionListPK
                    status = i.status
                    comment = i.comment
                    createAt = str(i.createAt)
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i.videoPATH
                    thumbnailPATH = i.thumbnailPATH
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status
                    if s3Status == "0":
                        videoPATH = serverURL+"/static/video"+videoPATH
                        thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                    elif s3Status == "1":
                        videoPATH = s3PATH+videoPATH
                        thumbnailPATH = s3PATH+thumbnailPATH

                    audition_Listinfo = Audition_List.objects.get(id = auditionListPK)
                    auditionTitle = audition_Listinfo.title


                    tournamentName = ""
                    if tournamentStatus == "0":
                        tournamentName = "모집중"
                    if tournamentStatus == "1":
                        tournamentName = "예선"
                    if tournamentStatus == "2":
                        tournamentName = "32강"
                    if tournamentStatus == "3":
                        tournamentName = "16강"
                    if tournamentStatus == "4":
                        tournamentName = "8강"
                    if tournamentStatus == "5":
                        tournamentName = "4강"
                    if tournamentStatus == "6":
                        tournamentName = "결승"

                    categoryListinfo = CategoryList.objects.get(id = categoryPK)
                    category = categoryListinfo.category
                    

                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    dictinfo = {
                        'videoPK':str(videoPK),
                        'thumbnailPATH':thumbnailPATH,
                        'dateTime':c,
                        'status':status,
                        'category':category,
                        'auditionTitle':auditionTitle,
                        'tournamentName':tournamentName,
                        'comment':comment,
                    }
                    videoinfoList.append(dictinfo)
                    
                text = "\033[92m"+"audition_myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'videoinfoList':videoinfoList}
                return HttpResponse(json.dumps(context))
            
        else:
            # page = int(data['page'])
            # pageStart = (page - 1) * 10
            # pageEnd = 10 * page
            loginUserPK = data['loginUserPK']


            videoinfoCount = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
            if videoinfoCount == 0:
                text = "내가 업로드한 비디오 리스트 없음"
                ment = "\033[93m"+"audition_myVideoList WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')                
                context = {'code':'0', 'videoinfoList':None}
                return HttpResponse(json.dumps(context))
            else:        
                # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
                videoinfo = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
                videoinfoList = []
                for index, i in enumerate(videoinfo):
                    userPK = i.userPK
                    videoPK = i.id
                    categoryPK = i.categoryPK
                    tournamentStatus = i.tournamentStatus
                    progressStatus = i.progressStatus
                    auditionListPK = i.auditionListPK
                    status = i.status
                    comment = i.comment
                    createAt = str(i.createAt)
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    videoPATH = i.videoPATH
                    thumbnailPATH = i.thumbnailPATH
                    s3Check = S3Check.objects.get(id = 1)
                    s3Status = s3Check.status
                    if s3Status == "0":
                        videoPATH = serverURL+"/static/video"+videoPATH
                        thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
                    elif s3Status == "1":
                        videoPATH = s3PATH+videoPATH
                        thumbnailPATH = s3PATH+thumbnailPATH

                    audition_Listinfo = Audition_List.objects.get(id = auditionListPK)
                    auditionTitle = audition_Listinfo.title


                    tournamentName = ""
                    if tournamentStatus == "0":
                        tournamentName = "모집중"
                    if tournamentStatus == "1":
                        tournamentName = "예선"
                    if tournamentStatus == "2":
                        tournamentName = "32강"
                    if tournamentStatus == "3":
                        tournamentName = "16강"
                    if tournamentStatus == "4":
                        tournamentName = "8강"
                    if tournamentStatus == "5":
                        tournamentName = "4강"
                    if tournamentStatus == "6":
                        tournamentName = "결승"

                    categoryListinfo = CategoryList.objects.get(id = categoryPK)
                    category = categoryListinfo.category
                    

                    timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    b = datetime.fromtimestamp(float(timestamp))
                    c = b.strftime('%Y-%m-%d %H:%M')

                    dictinfo = {
                        'videoPK':str(videoPK),
                        'thumbnailPATH':thumbnailPATH,
                        'dateTime':c,
                        'status':status,
                        'category':category,
                        'auditionTitle':auditionTitle,
                        'tournamentName':tournamentName,
                        'comment':comment,
                    }
                    videoinfoList.append(dictinfo)
                    
                text = "\033[92m"+"audition_myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1', 'videoinfoList':videoinfoList}
                return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_myVideoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 내가등록한 영상리스트 현황 디테일 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 -> 썸내일 터치 )
@csrf_exempt
def audition_myVideoListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
            videoPK = videoinfo.id
            status = videoinfo.status
            tournamentStatus = videoinfo.tournamentStatus
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName

            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = videoinfo.videoPATH
            thumbnailPATH = videoinfo.thumbnailPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status
            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
                thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
                thumbnailPATH = s3PATH+thumbnailPATH


            contents = videoinfo.contents
            hashTag = videoinfo.hashTag


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = str(like_video_infoCount)


            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = str(coment_infoCount)

            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()



            videoinfoList = [{
                'videoPK':videoPK,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'tournamentStatus':tournamentStatus
            }]
            # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
            text = "\033[92m"+"audition_myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
        

        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
            videoPK = videoinfo.id
            status = videoinfo.status
            tournamentStatus = videoinfo.tournamentStatus
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username
            nickName = userinfo.nickName

            profileIMG_path = userinfo.profileIMG_path
            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = videoinfo.videoPATH
            thumbnailPATH = videoinfo.thumbnailPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status
            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
                thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
                thumbnailPATH = s3PATH+thumbnailPATH


            contents = videoinfo.contents
            hashTag = videoinfo.hashTag


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = str(like_video_infoCount)


            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = str(coment_infoCount)

            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()



            videoinfoList = [{
                'videoPK':videoPK,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'tournamentStatus':tournamentStatus
            }]
            # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
            text = "\033[92m"+"audition_myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_myVideoListDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))










#  내가등록한 영상 정보 수정 페이지 이동
@csrf_exempt
def audition_myVideoListDetail_modiHtml(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
            videoPK = videoinfo.id
            status = videoinfo.status
            
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username



            videoPATH = videoinfo.videoPATH
            thumbnailPATH = videoinfo.thumbnailPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status
            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
                thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
                thumbnailPATH = s3PATH+thumbnailPATH



            contents = videoinfo.contents
            hashTag = videoinfo.hashTag
            location = videoinfo.location

            videoinfoList = [{
                'videoPK':videoPK,
                'videoPATH':videoPATH,
                'contents':contents,
                'hashTag':hashTag,
                'location':location,
            }]
            # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
                
            text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
        

        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
            videoPK = videoinfo.id
            status = videoinfo.status
            
            createAt = str(videoinfo.createAt)
            comment = videoinfo.comment
            userinfo = SignUp.objects.get(id = loginUserPK)
            username = userinfo.username



            videoPATH = videoinfo.videoPATH
            thumbnailPATH = videoinfo.thumbnailPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status
            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
                thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
                thumbnailPATH = s3PATH+thumbnailPATH



            contents = videoinfo.contents
            hashTag = videoinfo.hashTag
            location = videoinfo.location

            videoinfoList = [{
                'videoPK':videoPK,
                'videoPATH':videoPATH,
                'contents':contents,
                'hashTag':hashTag,
                'location':location,
            }]
            # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
                
            text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_myVideoListDetail_modiHtml Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    





# 영상 수정 업로드
@csrf_exempt
def audition_myVideoListDetail_modi(request):
    try:
        if request.method == 'POST':
            userPK = str(request.POST.get('loginUserPK'))
            videoPK = request.POST.get('videoPK')
            contents = request.POST.get('contents')
            hashTag = request.POST.get('hashTag')
            location = request.POST.get('location')
            viewable = request.POST.get('viewable')
            status = request.POST.get('status')
            if status == "1":

                img = request.FILES['file']
                print("img >>>", img)


                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                inviteCode = inviteCode + ".jpg"


                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'



                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = ""      # showplus
                )
                s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))




                
                videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + s3VideoPATH

                s3_client.upload_fileobj(
                    img, 
                    bucketName, 
                    videoURL, 
                    ExtraArgs={
                        "ContentType": img.content_type
                    }
                )


                count = 1
                test = 1
                train = 1
                vidcap = cv2.VideoCapture(s3PATH+videoURL)
                thumbnailPath = '/mnt/project/app/static/auditions/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
                if not os.path.exists(thumbnailPath):
                    os.makedirs(thumbnailPath)
                
                thumbnail_savePATH = ""
                

                while(vidcap.isOpened()):
                    ret, image = vidcap.read()
                    if(ret==False):
                        break
                    if(int(vidcap.get(1)) % 5 == 0):
                        num=count % 10
                        thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                        print("thumbnail_savePATH >>", thumbnail_savePATH)
                        cv2.imwrite(thumbnailPath + inviteCode, image)
                        break;
                vidcap.release()



                thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH
                thumbnailimg = thumbnailPath + inviteCode
                with open(thumbnailimg, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        thumbnailURL, 
                        # ExtraArgs={
                        #     "ContentType": image_file.content_type
                        # }
                    )



                savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

                if hashTag == "":
                    hashTag = None


                

                videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
                videoinfo.createAt = datetime.now()
                videoinfo.createAt_timestamp = str(round(time.time()))
                videoinfo.thumbnailPATH = thumbnailURL
                videoinfo.videoPATH = videoURL
                # videoinfo.s3VideoPATH = videoURL
                videoinfo.contents = contents
                videoinfo.hashTag = hashTag
                videoinfo.location = location
                videoinfo.viewable = viewable
                videoinfo.status = "0"
                videoinfo.save()


                text = "user PK값 : " + userPK + ", 동영상 저장 완료"
                ment = "\033[92m"+"audition_myVideoListDetail_modi SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context, default=json_util.default))

            elif status == "0":

                if hashTag == "":
                    hashTag = None


                videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
                videoinfo.createAt = datetime.now()
                videoinfo.createAt_timestamp = str(round(time.time()))
                videoinfo.contents = contents
                videoinfo.hashTag = hashTag
                videoinfo.location = location
                videoinfo.viewable = viewable
                videoinfo.status = "0"
                videoinfo.save()

                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"audition_myVideoListDetail_modi WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'2'}
                return HttpResponse(json.dumps(context, default=json_util.default))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_myVideoListDetail_modi Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# 오디션 내가등록한 영상 삭제
@csrf_exempt
def audition_myVideoDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfoCount = Audition_video.objects.filter(id = videoPK, userPK = loginUserPK).count()
            if videoinfoCount == 0:
                text = "값이 잘못 넘어옴; 이러면 안되는데??"
                ment = "\033[93m"+"audition_myVideoDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
            else:
                videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
                videoinfo.status = "5"
                videoinfo.save()

                text = "\033[92m"+"audition_myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']
        
            videoinfoCount = Audition_video.objects.filter(id = videoPK, userPK = loginUserPK).count()
            if videoinfoCount == 0:
                text = "값이 잘못 넘어옴; 이러면 안되는데??"
                ment = "\033[93m"+"audition_myVideoDel WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))
            else:
                videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
                videoinfo.status = "5"
                videoinfo.save()

                text = "\033[92m"+"audition_myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
                print("["+str(datetime.now())+"] " + text)
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_myVideoDel Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 동영상 업로드
@csrf_exempt
def test33(request):
    try:
        if request.method == 'POST':
            # aa = Audition_video.objects.filter(조건절).select_related('정방향_참조_필드')   
            # userPK = str(request.POST.get('loginUserPK'))
            # userPK = "1"
            # contents = request.POST.get('contents')
            # hashTag = request.POST.get('hashTag')
            # location = request.POST.get('location')
            # viewable = request.POST.get('viewable')
            # reqFile = request.FILES
            # newimgpath = ""
            # if len(reqFile['file']) != 0:
            #     file = reqFile['file']
            #     print(file)
            #     print("file.content_type >>>", file.content_type)
            #     s3_client = boto3.client(
            #         's3',
            #         aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",
            #         aws_secret_access_key = "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"
            #     )
            #     videoPATH = uuid.uuid1().hex
            #     url = 'videos'+'/'+uuid.uuid1().hex
            #     s3_client.upload_fileobj(
            #         file, 
            #         "showplus", 
            #         url, 
            #         ExtraArgs={
            #             "ContentType": file.content_type
            #         }
            #     )
            #     VideoSubmit = Video(userPK = userPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), videoPATH = videoPATH, contents = contents, hashTag = hashTag, location = location, viewable = viewable)
            #     VideoSubmit.save()

            #     text = "user PK값 : " + userPK + ", 동영상 저장 완료"
            #     ment = "\033[92m"+"fileupload SUCCESS -> "+text+"\033[0m"
            #     print("["+str(datetime.now())+"] " + ment + '\033[0m')

            #     context = {'code':'1'}
            #     return HttpResponse(json.dumps(context, default=json_util.default))
            # else:
            #     text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
            #     ment = "\033[93m"+"fileupload WARNING -> "+text+"\033[0m"
            #     print("["+str(datetime.now())+"] " + ment + '\033[0m')  
            #     context = {'code':'9'}
            #     return HttpResponse(json.dumps(context, default=json_util.default))
            text = "user PK값 : "
            ment = "\033[93m"+"fileupload WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')  
            context = {'code':'9'}
            return HttpResponse(json.dumps(context, default=json_util.default))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"fileupload Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




    




@csrf_exempt
def bookmarkList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        if "1.2.9" == aosVer or "1.2.9" == iosVer:

            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            bookmarkListinfoCount = BookmarkList.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if bookmarkListinfoCount == 0:
                bookmarkListinfo = BookmarkList(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                bookmarkListinfo.save()
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 비디오 최초 북마크"
                ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                bookmarkListinfo = BookmarkList.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = bookmarkListinfo.status
                if status == "0":
                    bookmarkListinfo.status = "1"
                    bookmarkListinfo.createAt = datetime.now()
                    bookmarkListinfo.createAt_timestamp = str(round(time.time()))
                    bookmarkListinfo.save()
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 비디오 다시 북마크"
                    ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    bookmarkListinfo.status = "0"
                    bookmarkListinfo.save()
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 북마크 해제"
                    ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))
                
        else:
            loginUserPK = data['loginUserPK']
            videoPK = data['videoPK']

            bookmarkListinfoCount = BookmarkList.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if bookmarkListinfoCount == 0:
                bookmarkListinfo = BookmarkList(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
                bookmarkListinfo.save()
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 비디오 최초 북마크"
                ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            else:
                bookmarkListinfo = BookmarkList.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = bookmarkListinfo.status
                if status == "0":
                    bookmarkListinfo.status = "1"
                    bookmarkListinfo.createAt = datetime.now()
                    bookmarkListinfo.createAt_timestamp = str(round(time.time()))
                    bookmarkListinfo.save()
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 비디오 다시 북마크"
                    ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context))
                elif status == "1":
                    bookmarkListinfo.status = "0"
                    bookmarkListinfo.save()
                    text = "loginUserPK PK값 : " + str(loginUserPK) + ", videoPK PK값 : " + str(videoPK) + ", 북마크 해제"
                    ment = "\033[92m"+"videoLike SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'2'}
                    return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))











# -----------------------------------------------------------------------------------------------------------------
# 개발쪽에서 오디션 테스트하기위해 제작


@csrf_exempt
def dev_auditionSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        title = data['title']
        category = data['category']
        date1_start = data['date1_start']   # 모집중 시작시간
        date1_end = data['date1_end']   # 모집중 종료시간
        date2_start = data['date2_start']   # 예선전
        date2_end = data['date2_end']   # 예선전
        date3_start = data['date3_start']   # 32강
        date3_end = data['date3_end']   # 32강
        date4_start = data['date4_start']   # 16강
        date4_end = data['date4_end']   # 16강
        date5_start = data['date5_start']   # 8강
        date5_end = data['date5_end']   # 8강
        date6_start = data['date6_start']   # 4강
        date6_end = data['date6_end']   # 4강
        date7_start = data['date7_start']   # 결승
        date7_end = data['date7_end']   # 결승


        date1_start_timestamp = time.mktime(datetime.strptime(date1_start, '%Y-%m-%d %H:%M:%S').timetuple())
        date1_start_fromtimestamp = datetime.fromtimestamp(float(date1_start_timestamp))

        date7_end_timestamp = time.mktime(datetime.strptime(date7_end, '%Y-%m-%d %H:%M:%S').timetuple())
        date7_end_fromtimestamp = datetime.fromtimestamp(float(date7_end_timestamp))



        audition_ListSubmit = Audition_List(
            title = title, 
            createAt = datetime.now(), 
            createAt_timestamp = str(round(time.time())), 
            startAt = date1_start_fromtimestamp, 
            startAt_timestamp = str(int(date1_start_timestamp)),
            endAt = date7_end_fromtimestamp,
            endAt_timestamp = str(int(date7_end_timestamp)),
            categoryPK = category,
        )
        audition_ListSubmit.save()



        detailList = [
            {'start':date1_start,'end':date1_end},
            {'start':date2_start,'end':date2_end},
            {'start':date3_start,'end':date3_end},
            {'start':date4_start,'end':date4_end},
            {'start':date5_start,'end':date5_end},
            {'start':date6_start,'end':date6_end},
            {'start':date7_start,'end':date7_end},
        ]
        auditionListPK = audition_ListSubmit.id

        for index, i in enumerate(detailList):
            start = i['start']
            start_timestamp = time.mktime(datetime.strptime(start, '%Y-%m-%d %H:%M:%S').timetuple())
            start_fromtimestamp = datetime.fromtimestamp(float(start_timestamp))            
            end = i['end']
            end_timestamp = time.mktime(datetime.strptime(date7_end, '%Y-%m-%d %H:%M:%S').timetuple())
            end_fromtimestamp = datetime.fromtimestamp(float(end_timestamp))

            auditionDetailSubmit = Audition_DetailList(
                auditionListPK = auditionListPK, 
                startDate = start_fromtimestamp, 
                startDate_timestamp = str(int(start_timestamp)),
                endDate = end_fromtimestamp,
                endDate_timestamp = str(int(end_timestamp)),
                tournamentStatus = str(index),
                createAt = datetime.now(),
                createAt_timestamp = str(round(time.time())),
            )
            auditionDetailSubmit.save()



        context = {'code':'1'}
        return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# ============================================================================================================================================================================================================================
# 2차 개발
# 기존에 있던 함수는 일단 복붙해서 주석해놓고 가져옴 
# 반영할때는 수정한 부분만 잘라서 반영해도 되고 갈아쳐도되고





@csrf_exempt
def follow(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        followUserPK = data['followUserPK']

        print("loginUserPK >>>", loginUserPK)
        print("followUserPK >>>", followUserPK)

        followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followUserPK).count()
        if followListinfoCount == 0:
            followListinfo = FollowList(userPK = loginUserPK, followUserPK = followUserPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            followListinfo.save()

            reqData = {"loginUserPK":loginUserPK, "ownerPK":followUserPK, "thumbnailPATH":None, "typeNum":"6", "itemPK":None}

            sendAlim(reqData)

            text = "loginUserPK PK값 : " + str(loginUserPK) + ", followUserPK PK값 : " + str(followUserPK) + ", 유저 최초 팔로우"
            ment = "\033[92m"+"follow SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = followUserPK)
            status = followListinfo.status
            if status == "0":
                followListinfo.status = "1"
                followListinfo.createAt = datetime.now()
                followListinfo.createAt_timestamp = str(round(time.time()))
                followListinfo.save()

                reqData = {"loginUserPK":loginUserPK, "ownerPK":followUserPK, "thumbnailPATH":None, "typeNum":"6", "itemPK":None}

                sendAlim(reqData)

                text = "loginUserPK PK값 : " + str(loginUserPK) + ", followUserPK PK값 : " + str(followUserPK) + ", 유저 다시 팔로우"
                ment = "\033[92m"+"follow SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1'}
                return HttpResponse(json.dumps(context))
            elif status == "1":
                followListinfo.status = "0"
                followListinfo.save()
                text = "loginUserPK PK값 : " + str(loginUserPK) + ", followUserPK PK값 : " + str(followUserPK) + ", 팔로우 해제"
                ment = "\033[92m"+"follow SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"follow Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 내가 팔로우 한 유저 리스트
@csrf_exempt
def myProfile_followingList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        followingListinfoCount = FollowList.objects.filter(userPK = loginUserPK, status = "1").count()
        if followingListinfoCount == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 팔로잉 리스트 없음"
            ment = "\033[93m"+"myProfile_followingList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
        else:
            followingListinfo = FollowList.objects.filter(userPK = loginUserPK, status = "1").order_by('-id')
            followingList = []
            for index, i in enumerate(followingListinfo):
                followingUserPK = i.followUserPK
                userinfo = SignUp.objects.get(id = followingUserPK)
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                    # profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                nickName = userinfo.nickName

                dictinfo = {'followingUserPK':followingUserPK, 'followingUserNickName':nickName, 'profileIMG_path':profileIMG_path}
                followingList.append(dictinfo)


            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 팔로잉 리스트"
            ment = "\033[92m"+"myProfile_followingList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'followingListinfo':followingList, 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_followingList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 상대방 프로필
@csrf_exempt
def userProfile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userPK = data['userPK']
        userinfo = SignUp.objects.get(id = int(userPK))
        username = userinfo.username
        nickName = userinfo.nickName
        point = userinfo.point
        AboutMe = userinfo.AboutMe
        grade = userinfo.grade
        profileIMG_path = userinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3_profileimgPATH+profileIMG_path
        else:
            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

        videoinfoCount = Video.objects.filter(userPK = userPK, status = "1").count()
        audition_videoinfoCount = Audition_video.objects.filter(userPK = userPK, status = "1").count()
        
        allVideoCount = videoinfoCount + audition_videoinfoCount



        # ====================================================================================================================
        # 20230731 2차 추가
        # 20230807 차단유저 count -1 추가
        followerCount = FollowList.objects.filter(followUserPK = userPK, status = "1").count()
        followerList = []
        if followerCount == 0:
            pass
        else:
            followerListinfo = FollowList.objects.filter(followUserPK = userPK, status = "1").order_by('?')
            for index, i in enumerate(followerListinfo):
                followerUserPK = i.userPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = followerUserPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    followerUserinfo = SignUp.objects.get(id = followerUserPK)
                    followerNickName = followerUserinfo.nickName
                    followerProfileIMG_path = followerUserinfo.profileIMG_path
                    if followerProfileIMG_path:
                        followerProfileIMG_path = s3_profileimgPATH+followerProfileIMG_path
                    else:
                        followerProfileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    
                    dictinfo = {'followerUserPK':followerUserPK, 'followerNickName':followerNickName, 'followerProfileIMG_path':followerProfileIMG_path}
                    followerList.append(dictinfo)
                else:
                    pass

        followerCount = len(followerList)

        followingCount = FollowList.objects.filter(userPK = userPK, status = "1").count()
        if followingCount == 0:
            pass
        else:
            followingListinfo = FollowList.objects.filter(userPK = userPK, status = "1")
            for index, j in enumerate(followingListinfo):
                followingUserPK = j.followUserPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = followingUserPK, status = "1").count()
                if userBlockListinfoCount == 0:
                    pass
                else:
                    followingCount -= 1


        followingCheck = ""
        followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = userPK).count()
        if followListinfoCount == 0:
            followingCheck = "0"
        else:
            followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = userPK)
            status = followListinfo.status
            if status == "0":
                followingCheck = "0"
            else:
                followingCheck = "1"
        # ====================================================================================================================

        userinfoList = [{'username':username, 'nickName':nickName, 'profileIMG_path':profileIMG_path, 'AboutMe':AboutMe, 'grade':grade, 'allVideoCount':allVideoCount, 'followerCount':followerCount, 'followingCount':followingCount, 'followingCheck':followingCheck, 'followerList':followerList}]
    
        text = "user PK값 : " + userPK + ", 상대 유저정보 및 video정보 리스트 Response"
        ment = "\033[92m"+"userProfile SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'userinfoList':userinfoList}
        return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 내 프로필
@csrf_exempt
def myProfile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        userinfo = SignUp.objects.get(id = int(loginUserPK))
        username = userinfo.username
        nickName = userinfo.nickName
        point = userinfo.point
        AboutMe = userinfo.AboutMe
        if int(point) > 1000:
            point = str('{:,}'.format(int(point)))
        profileIMG_path = userinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3_profileimgPATH+profileIMG_path
            # profileIMG_path = serverURL+"/static/profileIMG"+profileIMG_path
        else:
            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

        link = userinfo.link

        videoinfoCount = Video.objects.filter(userPK = loginUserPK, status = "1").count()
        audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, status = "1").count()
        
        allVideoCount = videoinfoCount + audition_videoinfoCount


        # ====================================================================================================================
        # 20230731 2차 추가
        followerCount = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").count()
        followerList = []
        if followerCount == 0:
            pass
        else:
            followerListinfo = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").order_by('?')
            for index, i in enumerate(followerListinfo):
                followerUserPK = i.userPK
                followerUserinfo = SignUp.objects.get(id = followerUserPK)
                followerNickName = followerUserinfo.nickName
                followerProfileIMG_path = followerUserinfo.profileIMG_path
                if followerProfileIMG_path:
                    followerProfileIMG_path = s3_profileimgPATH+followerProfileIMG_path
                else:
                    followerProfileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                
                dictinfo = {'followerUserPK':followerUserPK, 'followerNickName':followerNickName, 'followerProfileIMG_path':followerProfileIMG_path}
                followerList.append(dictinfo)


        followingCount = FollowList.objects.filter(userPK = loginUserPK, status = "1").count()


        alimCheck = False
        aliminfoCount = AlimList.objects.filter(userPK_R = loginUserPK, readStatus = "0").count()
        if aliminfoCount == 0:
            alimCheck = False
        else:
            alimCheck = True
        # ====================================================================================================================




        userinfoList = [{'username':username, 'nickName':nickName, 'profileIMG_path':profileIMG_path, 'point':point, 'AboutMe':AboutMe, 'link':link, 'followerList':followerList, 'allVideoCount':allVideoCount, 'followingCount':followingCount, 'followerCount':followerCount, 'alimCheck':alimCheck}]


        text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
        ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'userinfoList':userinfoList}
        return HttpResponse(json.dumps(context))
            

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 나를 팔로우 한 유저 리스트
@csrf_exempt
def myProfile_followerList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        followerListinfoCount = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").count()
        if followerListinfoCount == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 팔로워 리스트 없음"
            ment = "\033[93m"+"myProfile_followerList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'followerListinfoCount':followerListinfoCount}
            return HttpResponse(json.dumps(context))
        else:
            followerListinfo = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").order_by('?')
            followerList = []
            for index, i in enumerate(followerListinfo):
                followerUserPK = i.userPK
                followingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followerUserPK).count()
                followingCheck = ""
                if followingCheckCount == 0:
                    followingCheck = "0"
                else:
                    followingCheckinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = followerUserPK)
                    status = followingCheckinfo.status
                    if status == "0":
                        followingCheck = "0"
                    else:
                        followingCheck = "1"

                userinfo = SignUp.objects.get(id = followerUserPK)
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                dictinfo = {'followerUserPK':followerUserPK, 'followerUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'followingCheck':followingCheck}
                followerList.append(dictinfo)


            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 팔로워 리스트"
            ment = "\033[92m"+"myProfile_followerList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'followerListinfo':followerList, 'followerListinfoCount':followerListinfoCount}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_followerList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






# 상대가 팔로우 한 유저 리스트
@csrf_exempt
def userProfile_followingList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userPK = data['userPK']
        followingListinfoCount = FollowList.objects.filter(userPK = userPK, status = "1").count()
        if followingListinfoCount == 0:
            text = "userPK PK값 : " + str(userPK) + ", 팔로잉 리스트 없음"
            ment = "\033[93m"+"userProfile_followingList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
        else:
            followingListinfo = FollowList.objects.filter(userPK = userPK, status = "1").order_by('-id')
            followingList = []
            for index, i in enumerate(followingListinfo):
                followingUserPK = i.followUserPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = followingUserPK, status = "1").count()
                blockCheck = ""
                if userBlockListinfoCount == 0:
                    blockCheck = "0"
                    myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followingUserPK).count()
                    myfollowingCheck = ""
                    if myfollowingCheckCount == 0:
                        myfollowingCheck = "0"
                    else:
                        myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = followingUserPK)
                        status = myfollowingCheck.status
                        if status == "0":
                            myfollowingCheck = "0"
                        else:
                            myfollowingCheck = "1"


                    userinfo = SignUp.objects.get(id = followingUserPK)
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    dictinfo = {'followingUserPK':followingUserPK, 'followingUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'myfollowingCheck':myfollowingCheck, 'blockCheck':blockCheck}
                    followingList.append(dictinfo)

                else:
                    blockCheck = "1"
                    pass



                # myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followingUserPK).count()
                # myfollowingCheck = ""
                # if myfollowingCheckCount == 0:
                #     myfollowingCheck = "0"
                # else:
                #     myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = followingUserPK)
                #     status = myfollowingCheck.status
                #     if status == "0":
                #         myfollowingCheck = "0"
                #     else:
                #         myfollowingCheck = "1"


                # userinfo = SignUp.objects.get(id = followingUserPK)
                # nickName = userinfo.nickName
                # profileIMG_path = userinfo.profileIMG_path
                # if profileIMG_path:
                #     profileIMG_path = s3_profileimgPATH+profileIMG_path
                # else:
                #     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # dictinfo = {'followingUserPK':followingUserPK, 'followingUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'myfollowingCheck':myfollowingCheck, 'blockCheck':blockCheck}
                # followingList.append(dictinfo)

            text = "userPK PK값 : " + str(userPK) + ", 팔로잉 리스트"
            ment = "\033[92m"+"userProfile_followingList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'followingListinfo':followingList, 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userProfile_followingList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 상대를 팔로우 한 유저 리스트
@csrf_exempt
def userProfile_followerList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userPK = data['userPK']
        followerListinfoCount = FollowList.objects.filter(followUserPK = userPK, status = "1").count()
        if followerListinfoCount == 0:
            text = "userPK PK값 : " + str(userPK) + ", 팔로워 리스트 없음"
            ment = "\033[93m"+"myProfile_followerList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'followerListinfoCount':followerListinfoCount}
            return HttpResponse(json.dumps(context))
        else:
            followerListinfo = FollowList.objects.filter(followUserPK = userPK, status = "1").order_by('?')
            followerList = []
            for index, i in enumerate(followerListinfo):
                followerUserPK = i.userPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = followerUserPK, status = "1").count()
                blockCheck = ""
                if userBlockListinfoCount == 0:
                    blockCheck = "0"
                    myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followerUserPK).count()
                    myfollowingCheck = ""
                    if myfollowingCheckCount == 0:
                        myfollowingCheck = "0"
                    else:
                        myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = followerUserPK)
                        status = myfollowingCheck.status
                        if status == "0":
                            myfollowingCheck = "0"
                        else:
                            myfollowingCheck = "1"

                    userinfo = SignUp.objects.get(id = followerUserPK)
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                    dictinfo = {'followerUserPK':followerUserPK, 'followerUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'myfollowingCheck':myfollowingCheck, 'blockCheck':blockCheck}
                    followerList.append(dictinfo)
                else:
                    blockCheck = "1"
                    pass

                # myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followerUserPK).count()
                # myfollowingCheck = ""
                # if myfollowingCheckCount == 0:
                #     myfollowingCheck = "0"
                # else:
                #     myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = followerUserPK)
                #     status = myfollowingCheck.status
                #     if status == "0":
                #         myfollowingCheck = "0"
                #     else:
                #         myfollowingCheck = "1"

                # userinfo = SignUp.objects.get(id = followerUserPK)
                # nickName = userinfo.nickName
                # profileIMG_path = userinfo.profileIMG_path
                # if profileIMG_path:
                #     profileIMG_path = s3_profileimgPATH+profileIMG_path
                # else:
                #     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # dictinfo = {'followerUserPK':followerUserPK, 'followerUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'myfollowingCheck':myfollowingCheck, 'blockCheck':blockCheck}
                # followerList.append(dictinfo)


            text = "userPK PK값 : " + str(userPK) + ", 팔로워 리스트"
            ment = "\033[92m"+"myProfile_followerList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'followerListinfo':followerList, 'followerListinfoCount':followerListinfoCount}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_followerList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 유저 차단
@csrf_exempt
def userBlock(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        blockUserPK = data['blockUserPK']

        userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = blockUserPK).count()
        if userBlockListinfoCount == 0:
            userBlockSubmit = UserBlockList(loginUserPK = loginUserPK, blockUserPK = blockUserPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
            userBlockSubmit.save()


            myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = blockUserPK, status = "1").count()
            if myfollowingCheckCount == 0:
                pass
            else:
                myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = blockUserPK, status = "1")
                myfollowingCheck.status = "0"
                myfollowingCheck.save()

            text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
            ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))
        else:
            userBlockListinfo = UserBlockList.objects.get(loginUserPK = loginUserPK, blockUserPK = blockUserPK)
            status = userBlockListinfo.status
            if status == "0":
                userBlockListinfo.createAt = datetime.now()
                userBlockListinfo.createAt_timestamp = str(round(time.time()))
                userBlockListinfo.status = "1"
                userBlockListinfo.save()

                myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = blockUserPK, status = "1").count()
                if myfollowingCheckCount == 0:
                    pass
                else:
                    myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = blockUserPK, status = "1")
                    myfollowingCheck.status = "0"
                    myfollowingCheck.save()

                text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단"
                ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))

            elif status == "1":
                userBlockListinfo.status = "0"
                userBlockListinfo.save()

                text = str(loginUserPK) + " 유저가 -> " + str(blockUserPK) + " 유저 차단 해제"
                ment = "\033[92m"+"userBlock SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'0'}
                return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"userBlock Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 상대가 팔로우 한 유저 리스트
@csrf_exempt
def myfollowVideoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page
        loginUserPK = data['loginUserPK']


        followingListinfoCount = FollowList.objects.filter(userPK = loginUserPK, status = "1").count()
        if followingListinfoCount == 0:
            text = "userPK PK값 : " + str(userPK) + ", 팔로잉 리스트 없음"
            ment = "\033[93m"+"userProfile_followingList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
        else:
            followingListinfo = FollowList.objects.filter(userPK = loginUserPK, status = "1").order_by('?')
            followingVideoList = []
            for index, i in enumerate(followingListinfo):
                followingUserPK = i.followUserPK
                userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = followingUserPK, status = "1").count()
                blockCheck = ""
                if userBlockListinfoCount == 0:
                    blockCheck = "0"
                else:
                    blockCheck = "1"


                if blockCheck == "0":
                    videoinfoCount = Video.objects.filter(userPK = followingUserPK, viewable = "0", status = "1").count()
                    if videoinfoCount == 0:
                        pass
                    else:
                        videoinfo = Video.objects.filter(userPK = followingUserPK, viewable = "0", status = "1").order_by('?')
                        for index, j in enumerate(videoinfo):
                            userPK = j.userPK
                            videoPK = j.id
                            userinfo = SignUp.objects.get(id = userPK)
                            username = userinfo.username
                            nickName = userinfo.nickName
                            profileIMG_path = userinfo.profileIMG_path
                            # s3Check = S3Check.objects.get(id = 1)
                            # s3Status = s3Check.status

                            if profileIMG_path:
                                profileIMG_path = s3_profileimgPATH+profileIMG_path
                            else:
                                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"


                            videoPATH = j.videoPATH
                            videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                            # print("videoPATH >>>>", videoPATH)
                            # s3VideoPATH = j.s3VideoPATH

                            thumbnailPATH = j.thumbnailPATH
                            thumbnailPATH = s3PATH_previous + thumbnailPATH

                            # if s3Status == "0":
                            #     videoPATH = serverURL+"/static/video"+videoPATH
                            # elif s3Status == "1":
                                

                            contents = j.contents
                            hashTag = j.hashTag
                            viewable = j.viewable
                            size = j.size
                            
                            
                            userLikeCheck = ""
                            viewCountCheck = ""


                            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                            likeCount = like_video_infoCount
                            # if like_video_infoCount == 0:
                            #     pass
                            # else:
                            #     like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                            #     for index, n in enumerate(like_video_info):
                            #         userPK_like = n.userPK

                            #         userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                            #         if userBlockListinfoCount_likevideo == 1:
                            #             likeCount -= 1



                            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            if like_video_infoCount_user == 0:
                                userLikeCheck = "0"
                            else:
                                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                                status = like_video_info_user.status
                                if status == "0":
                                    userLikeCheck = "0"
                                elif status == "1":
                                    userLikeCheck = "1"




                            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
                            comentCount = coment_infoCount
                            # if coment_infoCount == 0:
                            #     pass
                            # else:
                            #     coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                            #     for index, k in enumerate(coment_info):
                            #         userPK_coment = k.userPK
                            #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                            #         if userBlockListinfoCount_coment == 1:
                            #             comentCount -= 1


                            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                            if viewCount_infoCount == 0:
                                viewCountCheck = "0"
                            else:
                                viewCountCheck = "1"


                            # ====================================================================================================================
                            # 20230731 2차 추가
                            followingCheck = ""
                            followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followingUserPK).count()
                            if followListinfoCount == 0:
                                followingCheck = "0"
                            else:
                                followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = followingUserPK)
                                status = followListinfo.status
                                if status == "0":
                                    followingCheck = "0"
                                else:
                                    followingCheck = "1"
                            # ====================================================================================================================


                            dictinfo = {
                                'videoPK':int(videoPK), 
                                'userPK':followingUserPK, 
                                'username':username,
                                'nickName':nickName,
                                'profileIMG_path':profileIMG_path,
                                'contents':contents,
                                'hashTag':hashTag,
                                'videoPATH':videoPATH,
                                'thumbnailPATH':thumbnailPATH,
                                'size':size,
                                'viewable':viewable,
                                'likeCount':str(likeCount),
                                'comentCount':str(comentCount),
                                'userLikeCheck':userLikeCheck,
                                'viewCountCheck':viewCountCheck,
                                'followingCheck':followingCheck
                            }
                            followingVideoList.append(dictinfo)                            





                # myfollowingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followingUserPK).count()
                # myfollowingCheck = ""
                # if myfollowingCheckCount == 0:
                #     myfollowingCheck = "0"
                # else:
                #     myfollowingCheck = FollowList.objects.get(userPK = loginUserPK, followUserPK = followingUserPK)
                #     status = myfollowingCheck.status
                #     if status == "0":
                #         myfollowingCheck = "0"
                #     else:
                #         myfollowingCheck = "1"


                # userinfo = SignUp.objects.get(id = followingUserPK)
                # nickName = userinfo.nickName
                # profileIMG_path = userinfo.profileIMG_path
                # if profileIMG_path:
                #     profileIMG_path = s3_profileimgPATH+profileIMG_path
                # else:
                #     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                # dictinfo = {'followingUserPK':followingUserPK, 'followingUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'myfollowingCheck':myfollowingCheck, 'blockCheck':blockCheck}
                # followingVideoList.append(dictinfo)
            followingVideoList_page = followingVideoList[pageStart:pageEnd]
            text = "userPK PK값 : " + str(loginUserPK) + ", 팔로잉 리스트"
            ment = "\033[92m"+"myfollowVideoList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'followingVideoList':followingVideoList_page, 'followingAllVideoList':followingVideoList, 'followingListinfoCount':followingListinfoCount}
            return HttpResponse(json.dumps(context))
        
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myfollowVideoList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 메인 비디오 리스트
@csrf_exempt
def myfollowVideoListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page

        loginUserPK = data['loginUserPK']
        followingAllVideoList = data['followingAllVideoList'][pageStart:pageEnd]
        # followingAllVideoList = json.loads(followingAllVideoList)[pageStart:pageEnd]
        # followingAllVideoList = followingAllVideoList[pageStart:pageEnd]

        # print("followingAllVideoList >>>", followingAllVideoList)
        followingVideoList = []
        for index, i in enumerate(followingAllVideoList):

            userPK = i['userPK']
            # userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
            # if userBlockListinfoCount == 0:
            videoPK = i['videoPK']
            userinfo = SignUp.objects.get(id = userPK)
            username = userinfo.username
            nickName = userinfo.nickName
            profileIMG_path = userinfo.profileIMG_path


            if profileIMG_path:
                profileIMG_path = s3_profileimgPATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = i['videoPATH']
            # videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
            # s3VideoPATH = i['s3VideoPATH']

            thumbnailPATH = i['thumbnailPATH']
            thumbnailPATH = s3PATH + thumbnailPATH

            # if s3Status == "0":
            #     videoPATH = serverURL+"/static/video"+videoPATH
            # elif s3Status == "1":
            #     videoPATH = s3PATH+s3VideoPATH

            contents = i['contents']
            hashTag = i['hashTag']
            viewable = i['viewable']

            
            
            userLikeCheck = ""
            viewCountCheck = ""


            like_video_infoCount = Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            likeCount = like_video_infoCount
            if like_video_infoCount == 0:
                pass
            else:
                like_video_info = Like_video.objects.filter(videoPK = videoPK, status = "1")
                for index, j in enumerate(like_video_info):
                    userPK_like = j.userPK

                    userBlockListinfoCount_likevideo = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_like, status = "1").count()
                    if userBlockListinfoCount_likevideo == 1:
                        likeCount -= 1



            like_video_infoCount_user = Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                like_video_info_user = Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                status = like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"




            coment_infoCount = Coment.objects.filter(videoPK = videoPK, status = "0").count()
            comentCount = coment_infoCount
            if coment_infoCount == 0:
                pass
            else:
                coment_info = Coment.objects.filter(videoPK = videoPK, status = "0")
                for index, k in enumerate(coment_info):
                    userPK_coment = k.userPK
                    userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
                    if userBlockListinfoCount_coment == 1:
                        comentCount -= 1


            viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"

            # ====================================================================================================================
            # 20230731 2차 추가
            # 20230807 추가 ( 팔로우 리스트라 필요없긴한데 일단 넣어둠 )
            followingCheck = ""
            followListinfoCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = userPK).count()
            if followListinfoCount == 0:
                followingCheck = "0"
            else:
                followListinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = userPK)
                status = followListinfo.status
                if status == "0":
                    followingCheck = "0"
                else:
                    followingCheck = "1"
            # ====================================================================================================================

            dictinfo = {
                'videoPK':int(videoPK), 
                'userPK':userPK, 
                'username':username,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'viewable':viewable,
                'likeCount':str(likeCount),
                'comentCount':str(comentCount),
                'userLikeCheck':userLikeCheck,
                'viewCountCheck':viewCountCheck,
                'followingCheck':followingCheck
            }
            followingVideoList.append(dictinfo)

        text = "\033[92m"+"myfollowVideoListMove SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'followingVideoList':followingVideoList}
        return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myfollowVideoListMove Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 차단리스트
@csrf_exempt
def myProfile_blockList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        userBlockListinfoCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, status = "1").count()
        if userBlockListinfoCount == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 차단 리스트 없음"
            ment = "\033[92m"+"myProfile_followerList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))

        else:
            userBlockListinfo = UserBlockList.objects.filter(loginUserPK = loginUserPK, status = "1")
            userBlockList = []
            for index, i in enumerate(userBlockListinfo):
                blockUserPK = i.blockUserPK
                userinfo = SignUp.objects.get(id = blockUserPK)
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                dictinfo = {'blockUserPK':blockUserPK, 'blockUserNick':nickName, 'profileIMG_path':profileIMG_path}
                userBlockList.append(dictinfo)

            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 차단 리스트"
            ment = "\033[92m"+"myProfile_followerList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'userBlockList':userBlockList}
            return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_followerList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 동영상 업로드 ( lambda 적용 )
# 20230818 - mention, tag 추가
@csrf_exempt
def fileupload(request):
    try:
        if request.method == 'POST':

            userPK = str(request.POST.get('loginUserPK'))
            contents = request.POST.get('contents')
            hashTag = request.POST.get('hashTag')
            location = request.POST.get('location', None)
            locationDetail = request.POST.get('locationDetail', None)
            viewable = request.POST.get('viewable')
            size = request.POST.get('size')
            mention = request.POST.get('mention')
            tag = request.POST.get('tag')
            fileCheck = request.POST.get('fileCheck')

            print("userPK  ----------", userPK)
            fileCheck = "0"
            if fileCheck == "0":
                reqFile = request.FILES
                print("reqFile >>", reqFile)
                if len(reqFile['file']) != 0:

                    img = request.FILES['file']
                    print("fileupload >>>", img)


                    
                    inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                    videoinfoCount = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                    check = False
                    if videoinfoCount == 0:
                        pass
                    else:
                        while check == False:
                            inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                            # inviteCode = inviteCode + ".jpg"
                            videoinfoCount_check = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                            if videoinfoCount_check == 0:
                                check = True
                                break;

                    now = datetime.now()
                    year = str(now.year)
                    month = str(now.month)
                    day = str(now.day)



                    s3_client = boto3.client(
                        's3',
                        aws_access_key_id     = "",                         # showplus
                        aws_secret_access_key = "",      # showplus
                        region_name = "ap-northeast-2"
                    )

                    s3_client.put_bucket_accelerate_configuration(
                        Bucket=bucketName,
                        AccelerateConfiguration={'Status': 'Enabled'}
                    )


                

                    videoURL = 'input/videos/videos/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

                    s3_client.upload_fileobj(
                        img, 
                        bucketName, 
                        videoURL, 
                        ExtraArgs={
                            "ContentType": img.content_type
                        }
                    )
                    
                    count = 1
                    test = 1
                    train = 1
                    vidcap = cv2.VideoCapture(s3PATH+videoURL)
                    thumbnailPath = '/mnt/project/app/static/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
                    if not os.path.exists(thumbnailPath):
                        os.makedirs(thumbnailPath)
                    
                    thumbnail_savePATH = ""
                    

                    while(vidcap.isOpened()):
                        ret, image = vidcap.read()
                        if(ret==False):
                            break
                        if(int(vidcap.get(1)) % 5 == 0):
                            num=count % 10
                            thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                            # print("thumbnail_savePATH >>", thumbnail_savePATH)
                            cv2.imwrite(thumbnailPath + inviteCode + ".jpg", image)
                            break;
                    vidcap.release()



                    thumbnailURL = 'thumbnail/dev'+thumbnail_savePATH + ".jpg"
                    thumbnailimg = thumbnailPath + inviteCode + ".jpg"
                    with open(thumbnailimg, 'rb') as image_file:
                        s3_client.upload_fileobj(
                            image_file, 
                            bucketName, 
                            thumbnailURL, 
                        )

                else:
                    text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                    ment = "\033[93m"+"fileupload WARNING -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                    context = {'code':'9'}
                    return HttpResponse(json.dumps(context, default=json_util.default))
                
            else:
                tmpPK = request.POST.get('tmpPK')
                
                videoTMPinfo = VideoTMP.objects.get(id = tmpPK)
                thumbnailURL = videoTMPinfo.thumbnailPATH
                inviteCode = videoTMPinfo.inviteCode



            if hashTag == "":
                hashTag = None

            if location == "":
                location = None

            if locationDetail == "":
                locationDetail = None

            VideoSubmit = Video(
                userPK = userPK, 
                createAt = datetime.now(), 
                createAt_timestamp = str(round(time.time())), 
                thumbnailPATH = thumbnailURL, 
                videoPATH = inviteCode, 
                s3VideoPATH = inviteCode,
                contents = contents, 
                hashTag = hashTag, 
                location = location, 
                locationDetail = locationDetail,
                viewable = viewable, 
                size = size,
                mention = mention,
                tag = tag
            )
            VideoSubmit.save()
            
            bestLocationinfoCount = LocationList.objects.filter(location = location).count()
            if bestLocationinfoCount == 0:
                locationListSubmit = LocationList(
                    userPK= userPK, 
                    videoPK = VideoSubmit.id,
                    location = location,
                    locationDetail = locationDetail,
                    createAt = datetime.now(),
                    createAt_timestamp = str(round(time.time())),
                    count = "0"
                )
                locationListSubmit.save()
            else:
                bestLocationinfo = LocationList.objects.get(location = location)
                bestLocationinfo.count = str(int(bestLocationinfo.count) + 1)
                bestLocationinfo.save()


            latestLocationListCount = LatestLocationList.objects.filter(userPK = userPK, location = location).count()
            if latestLocationListCount == 0:
                latestLocationListSubmit = LatestLocationList(
                    userPK= userPK, 
                    videoPK = VideoSubmit.id,
                    location = location,
                    locationDetail = locationDetail,
                    createAt = datetime.now(),
                    createAt_timestamp = str(round(time.time())),
                )
                latestLocationListSubmit.save()
            else:
                latestLocationListinfo = LatestLocationList.objects.get(userPK= userPK, location = location)
                latestLocationListinfo.createAt = datetime.now()
                latestLocationListinfo.createAt_timestamp = str(round(time.time()))
                latestLocationListinfo.save()

            if mention:
                if ',' in mention:
                    mentionList = mention.split(',')
                else:
                    mentionList = [mention]
                # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                for index, i in enumerate(mentionList):
                    mentionListSubmit = MentionList(
                        loginUserPK = userPK,
                        userPK = i,
                        videoPK = VideoSubmit.id,
                        createAt = datetime.now(),
                        createAt_timestamp = str(round(time.time()))
                    )
                    mentionListSubmit.save()

            if tag:
                if ',' in tag:
                    tagList = tag.split(',')
                else:
                    tagList = [tag]
                # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                for index, j in enumerate(tagList):
                    tagListSubmit = TagList(
                        loginUserPK = userPK,
                        userPK = j,
                        videoPK = VideoSubmit.id,
                        createAt = datetime.now(),
                        createAt_timestamp = str(round(time.time()))
                    )
                    tagListSubmit.save()



            videoURL = s3PATH+"output/"+inviteCode+"/Default/HLS/"+inviteCode+".m3u8"

            text = "user PK값 : " + userPK + ", 동영상 저장 완료"
            ment = "\033[92m"+"fileupload SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

            context = {'code':'1', 'videoURL':videoURL}
            return HttpResponse(json.dumps(context, default=json_util.default))

                


    except Exception as e: 
        text = str(e)
        ment = "\033[91m"+"fileupload Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))








# 위치 검색 리스트
@csrf_exempt
def locationSearchList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']

        latestLocationListCount = LatestLocationList.objects.filter(userPK = loginUserPK).count()
        latestLocationList = []
        if latestLocationListCount == 0:
            pass
        else:
            latestLocationListinfo = LatestLocationList.objects.filter(userPK = loginUserPK).order_by('createAt')[:2]
            for index, i in enumerate(latestLocationListinfo):
                location = i.location
                if location:
                    locationDetail = i.locationDetail
                    dictinfo = {'location':location, 'locationDetail':locationDetail}
                    latestLocationList.append(dictinfo)

        bestLocationinfoCount = LocationList.objects.all().count()
        bestLocationList = []
        if bestLocationinfoCount == 0:
            pass
        else:
            bestLocationinfo = LocationList.objects.all()
            for index, j in enumerate(bestLocationinfo):
                location2 = j.location
                if location2:
                    locationDetail2 = j.locationDetail
                    count = int(j.count)
                    dictinfo2 = {'location':location2, 'locationDetail':locationDetail2, 'count':count}
                    bestLocationList.append(dictinfo2)

        bestLocationList = sorted(bestLocationList, key=lambda x: (x['count']), reverse=True)[:4]

        text = "loginUserPK PK값 : " + str(loginUserPK) + ", 위치 검색 리스트"
        ment = "\033[92m"+"locationSearchList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'latestLocationList':latestLocationList, 'bestLocationList':bestLocationList}

        return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"locationSearchList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 멘션 최신 리스트 & 팔로워 리스트
@csrf_exempt
def latestMentionList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']

        mentionListinfo = MentionList.objects.filter(loginUserPK = loginUserPK).count()
        mentionList = []
        if mentionListinfo == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 최근 멘션 리스트 없음"
            ment = "\033[92m"+"latestMentionList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

        else:
            mentionListinfo = MentionList.objects.filter(loginUserPK = loginUserPK).order_by('-createAt')
            
            for index, i in enumerate(mentionListinfo):
                userPK = i.userPK
                userinfo = SignUp.objects.get(id = userPK)
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                
                dictinfo = {'userPK':userPK, 'nickName':nickName, 'profileIMG_path':profileIMG_path}
                mentionList.append(dictinfo)

            mentionListLen = len(mentionList)
            if mentionListLen > 3:
                mentionList = mentionList[:3]

        print("mentionList >>>", mentionList)

        followerListinfoCount = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").count()
        followerList = []
        if followerListinfoCount == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 팔로워 리스트 없음"
            ment = "\033[93m"+"latestMentionList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
        else:
            followerListinfo = FollowList.objects.filter(followUserPK = loginUserPK, status = "1").order_by('?')
            
            for index, i in enumerate(followerListinfo):
                followerUserPK = i.userPK
                followingCheckCount = FollowList.objects.filter(userPK = loginUserPK, followUserPK = followerUserPK).count()
                followingCheck = ""
                if followingCheckCount == 0:
                    followingCheck = "0"
                else:
                    followingCheckinfo = FollowList.objects.get(userPK = loginUserPK, followUserPK = followerUserPK)
                    status = followingCheckinfo.status
                    if status == "0":
                        followingCheck = "0"
                    else:
                        followingCheck = "1"

                userinfo = SignUp.objects.get(id = followerUserPK)
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                dictinfo = {'followerUserPK':followerUserPK, 'followerUserNickName':nickName, 'profileIMG_path':profileIMG_path, 'followingCheck':followingCheck}
                followerList.append(dictinfo)



        text = "loginUserPK PK값 : " + str(loginUserPK) + ", 최근 멘션 리스트 없음"
        ment = "\033[92m"+"latestMentionList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'mentionList':mentionList, 'followerList':followerList}
        return HttpResponse(json.dumps(context))



    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"latestMentionList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 태그 최신 리스트 & 유저 리스트
@csrf_exempt
def latestTagList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']

        tagListListinfo = TagList.objects.filter(loginUserPK = loginUserPK).count()
        latestTagList = []
        excludeList = []
        if tagListListinfo == 0:
            text = "loginUserPK PK값 : " + str(loginUserPK) + ", 최근 멘션 리스트 없음"
            ment = "\033[92m"+"locationSearchList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

        else:
            tagListinfo = TagList.objects.filter(loginUserPK = loginUserPK).order_by('-createAt')
            for index, i in enumerate(tagListinfo):
                userPK = i.userPK
                userinfo = SignUp.objects.get(id = userPK)
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                
                dictinfo = {'userPK':userPK, 'nickName':nickName, 'profileIMG_path':profileIMG_path}
                latestTagList.append(dictinfo)
                excludeList.append(userPK)

            latestTagListLen = len(latestTagList)
            if latestTagListLen > 3:
                latestTagList = latestTagList[:3]
                excludeList = excludeList[:3]


        
        userinfoList = SignUp.objects.filter(Q(grade = "0") | Q(grade = "1") | Q(grade = "2") | Q(grade = "5")).exclude(id__in = excludeList)
        userList = []
        for index, j in enumerate(userinfoList):
            userPK = j.id
            userBlockListCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
            if userBlockListCount == 0:
                nickName = j.nickName
                profileIMG_path = j.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                
                dictinfo = {'userPK':userPK, 'nickName':nickName, 'profileIMG_path':profileIMG_path}
                userList.append(dictinfo)            

        text = "loginUserPK PK값 : " + str(loginUserPK) + ", 최근 멘션 리스트 없음"
        ment = "\033[92m"+"locationSearchList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'latestTagList':latestTagList, 'userList':userList}
        return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"locationSearchList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 태그 검색 리스트 ( 유저 리스트 )
@csrf_exempt
def searchTagList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        text = data['text']

        userinfoListCount = SignUp.objects.filter(nickName__icontains = text).count()
        userList = []
        if userinfoListCount == 0:
            pass
        else:
            userinfoList = SignUp.objects.filter(nickName__icontains = text)
            for index, i in enumerate(userinfoList):
                userPK = i.id
                userBlockListCount = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK, status = "1").count()
                if userBlockListCount == 0:
                    nickName = i.nickName
                    profileIMG_path = i.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3_profileimgPATH+profileIMG_path
                    else:
                        profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                    
                    dictinfo = {'userPK':userPK, 'nickName':nickName, 'profileIMG_path':profileIMG_path}
                    userList.append(dictinfo)            

        print("userList >>>", userList)

        text = "검색 text 값 : " + text + ", 리스트"
        ment = "\033[92m"+"locationSearchList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1', 'userList':userList}
        return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"locationSearchList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 나를 태그한 영상 리스트 tab
@csrf_exempt
def myProfile_tagListTab(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        userinfo = SignUp.objects.get(id = int(loginUserPK))

        tagListinfoCount = TagList.objects.filter(userPK = loginUserPK).count()
        if tagListinfoCount == 0:
            text = "user PK값 : " + str(loginUserPK) + ", 나를 태그한 영상 없음"
            ment = "\033[93m"+"myProfile WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))            
        
        else:
            tagListinfo = TagList.objects.filter(userPK = loginUserPK)
            videoinfoList = []
            for index, i in enumerate(tagListinfo):
                videoPK = i.videoPK
                videoinfo = Video.objects.get(id = videoPK)


                videoPATH = videoinfo.videoPATH
                videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"
                thumbnailPATH = videoinfo.thumbnailPATH
                thumbnailPATH = s3PATH + thumbnailPATH

                viewCountinfoCount = ViewCount.objects.filter(videoPK = videoPK).count()

                dictinfo = {'videoPK':videoPK, 'thumbnailPATH':thumbnailPATH, 'viewCountinfoCount':str(viewCountinfoCount)}
                videoinfoList.append(dictinfo)
            

            text = "user PK값 : " + str(loginUserPK) + ", 유저정보 및 video정보 리스트 Response"
            ment = "\033[92m"+"myProfile SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'videoinfoList':videoinfoList}
            return HttpResponse(json.dumps(context))

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    









#  내가등록한 영상 정보 수정 페이지 이동
@csrf_exempt
def myVideoListDetail_modiHtml(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
    
        videoinfo = Video.objects.get(id = videoPK, userPK = loginUserPK)
        
        videoPK = videoinfo.id
        status = videoinfo.status
        createAt = str(videoinfo.createAt)
        comment = videoinfo.comment
        userinfo = SignUp.objects.get(id = loginUserPK)
        username = userinfo.username



        videoPATH = videoinfo.videoPATH
        videoPATH = s3PATH+"output/"+videoPATH+"/Default/HLS/"+videoPATH+".m3u8"

        thumbnailPATH = videoinfo.thumbnailPATH
        # thumbnailPATH = s3PATH+"output/"+thumbnailPATH+"/Default/Thumbnails/"+thumbnailPATH+".0000000.jpg"
        thumbnailPATH = s3PATH + thumbnailPATH


        contents = videoinfo.contents
        hashTag = videoinfo.hashTag
        location = videoinfo.location
        viewable = videoinfo.viewable
        locationDetail = videoinfo.locationDetail

        mention = videoinfo.mention
        mentionList = []
        if mention:
            if ',' in mention:
                mentionList = mention.split(',')
            else:
                mentionList = [mention]

        tag = videoinfo.tag
        tagList = []
        if tag:
            if ',' in tag:
                tagSplit = tag.split(',')
            else:
                tagSplit = [tag]

            for index, i in enumerate(tagSplit):
                tagUserinfo = SignUp.objects.get(id = i)
                profileIMG_path = tagUserinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
                dictinfo = {'userPK':i, 'profileIMG_path':profileIMG_path}
                tagList.append(dictinfo)

        # print("tagList <>>>>", tagList)
        videoinfoList = [{
            'videoPK':videoPK,
            'videoPATH':videoPATH,
            'contents':contents,
            'hashTag':hashTag,
            'location':location,
            'locationDetail':locationDetail,
            'viewable':viewable,
            'mention':mention
        }]
        # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
            
        text = "\033[92m"+"myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList, 'tagList':tagList}
        return HttpResponse(json.dumps(context))
        


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myVideoListDetail_modiHtml Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# 내가등록한 영상 정보 수정 ( 영상수정은 안되서  사실상 status == "1" 부분은 필요없음 )
@csrf_exempt
def myVideoListDetail_modi(request):
    try:
        if request.method == 'POST':
            userPK = str(request.POST.get('loginUserPK'))
            videoPK = request.POST.get('videoPK')
            contents = request.POST.get('contents')
            hashTag = request.POST.get('hashTag')
            location = request.POST.get('location')
            locationDetail = request.POST.get('locationDetail')
            viewable = request.POST.get('viewable')
            status = request.POST.get('status')
            mention = request.POST.get('mention')
            tag = request.POST.get('tag')
            if status == "1":
                reqFile = request.FILES
                if len(reqFile['file']) != 0:
                    img = request.FILES['file']

                    inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                    inviteCode = inviteCode + ".jpg"
                    userinfoCount = Video.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                    check = False
                    if userinfoCount == 0:
                        pass
                    else:
                        while check == False:
                            inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                            inviteCode = inviteCode + ".jpg"
                            userinfoCount_check = SignUp.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                            if userinfoCount_check == 0:
                                check = True
                                break;


                    now = datetime.now()
                    year = str(now.year)
                    month = str(now.month)
                    day = str(now.day)

                    path = '/mnt/project/app/static/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'

                    s3_client = boto3.client(
                        's3',
                        aws_access_key_id     = "",                         # showplus
                        aws_secret_access_key = ""      # showplus
                    )
                    s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))




                    videoURL = 'videos/videos/' +year+'/'+month+'/'+day+'/'+userPK+'/' + s3VideoPATH

                    s3_client.upload_fileobj(
                        img, 
                        bucketName, 
                        videoURL, 
                        ExtraArgs={
                            "ContentType": img.content_type
                        }
                    )
                    


                    count = 1
                    test = 1
                    train = 1
                    # vidcap = cv2.VideoCapture(path +str(img))
                    vidcap = cv2.VideoCapture(s3PATH+videoURL)
                    thumbnailPath = '/mnt/project/app/static/thumbnail/dev/'+year+'/'+month+'/'+day+'/'+userPK+'/'
                    if not os.path.exists(thumbnailPath):
                        os.makedirs(thumbnailPath)
                    
                    thumbnail_savePATH = ""
                    

                    while(vidcap.isOpened()):
                        ret, image = vidcap.read()
                        if(ret==False):
                            break
                        if(int(vidcap.get(1)) % 5 == 0):
                            num=count % 10
                            thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                            print("thumbnail_savePATH >>", thumbnail_savePATH)
                            cv2.imwrite(thumbnailPath + inviteCode, image)
                            break;
                    vidcap.release()




                    thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH
                    thumbnailimg = thumbnailPath + inviteCode
                    with open(thumbnailimg, 'rb') as image_file:
                        s3_client.upload_fileobj(
                            image_file, 
                            bucketName, 
                            thumbnailURL, 
                            # ExtraArgs={
                            #     "ContentType": image_file.content_type
                            # }
                        )



                    savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

                    if hashTag == "":
                        hashTag = None



                    videoinfo = Video.objects.get(id = videoPK, userPK = userPK)
                    videoinfo.createAt = datetime.now()
                    videoinfo.createAt_timestamp = str(round(time.time()))
                    videoinfo.thumbnailPATH = thumbnailURL
                    videoinfo.videoPATH = savePATH
                    videoinfo.s3VideoPATH = videoURL
                    videoinfo.contents = contents
                    videoinfo.hashTag = hashTag
                    videoinfo.location = location
                    videoinfo.locationDetail = locationDetail
                    videoinfo.viewable = viewable
                    videoinfo.status = "0"
                    videoinfo.save()
                    
                    text = "user PK값 : " + userPK + ", 동영상 수정 완료"
                    ment = "\033[92m"+"myVideoListDetail_modi SUCCESS -> "+text+"\033[0m"
                    print("["+str(datetime.now())+"] " + ment + '\033[0m')
                    context = {'code':'1'}
                    return HttpResponse(json.dumps(context, default=json_util.default))
                

            elif status == "0":

                if mention:
                    if ',' in mention:
                        mentionList = mention.split(',')
                    else:
                        mentionList = [mention]
                    # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                    for index, i in enumerate(mentionList):
                        mentionListSubmit = MentionList(
                            loginUserPK = userPK,
                            userPK = i,
                            videoPK = videoPK,
                            createAt = datetime.now(),
                            createAt_timestamp = str(round(time.time()))
                        )
                        mentionListSubmit.save()

                if tag:
                    if ',' in tag:
                        tagList = tag.split(',')
                    else:
                        tagList = [tag]
                    # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                    for index, j in enumerate(tagList):
                        tagListSubmit = TagList(
                            loginUserPK = userPK,
                            userPK = j,
                            videoPK = videoPK,
                            createAt = datetime.now(),
                            createAt_timestamp = str(round(time.time()))
                        )
                        tagListSubmit.save()

                if hashTag == "":
                    hashTag = None

                if location == "":
                    location = None

                if locationDetail == "":
                    locationDetail = None

                videoinfo = Video.objects.get(id = videoPK, userPK = userPK)
                videoinfo.createAt = datetime.now()
                videoinfo.createAt_timestamp = str(round(time.time()))
                videoinfo.contents = contents
                videoinfo.hashTag = hashTag
                videoinfo.location = location
                videoinfo.locationDetail = locationDetail
                videoinfo.viewable = viewable
                videoinfo.status = "0"
                videoinfo.mention = mention
                videoinfo.tag = tag
                videoinfo.save()

                text = "user PK값 : " + userPK + ", 영상 제외 수정 완료"
                ment = "\033[92m"+"myVideoListDetail_modi SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context, default=json_util.default))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myVideoListDetail_modi Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    








@csrf_exempt
def tmpVideoUpload_originPATH(request):
    try:
        if request.method == 'POST':

            userPK = str(request.POST.get('loginUserPK'))
            reqFile = request.FILES
            # print("reqFile >>", reqFile)
            if len(reqFile['file']) != 0:

                img = request.FILES['file']
                print("tmpVideoUpload_originPATH >>>", img)

                
                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                videoinfoCount = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                check = False
                if videoinfoCount == 0:
                    pass
                else:
                    while check == False:
                        inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                        # inviteCode = inviteCode + ".jpg"
                        videoinfoCount_check = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                        if videoinfoCount_check == 0:
                            check = True
                            break;

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)



                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = "",      # showplus
                    region_name = "ap-northeast-2"
                )

                s3_client.put_bucket_accelerate_configuration(
                    Bucket=bucketName,
                    AccelerateConfiguration={'Status': 'Enabled'}
                )


                videoURL = 'input/videos/videos/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

                s3_client.upload_fileobj(
                    img, 
                    bucketName, 
                    videoURL, 
                    ExtraArgs={
                        "ContentType": img.content_type
                    }
                )
                
                count = 1
                test = 1
                train = 1
                vidcap = cv2.VideoCapture(s3PATH+videoURL)
                thumbnailPath = '/mnt/project/app/static/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
                if not os.path.exists(thumbnailPath):
                    os.makedirs(thumbnailPath)
                
                thumbnail_savePATH = ""
                

                while(vidcap.isOpened()):
                    ret, image = vidcap.read()
                    if(ret==False):
                        break
                    if(int(vidcap.get(1)) % 5 == 0):
                        num=count % 10
                        thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                        # print("thumbnail_savePATH >>", thumbnail_savePATH)
                        cv2.imwrite(thumbnailPath + inviteCode + ".jpg", image)
                        break;
                vidcap.release()



                thumbnailURL = 'thumbnail/dev'+thumbnail_savePATH + ".jpg"
                thumbnailimg = thumbnailPath + inviteCode + ".jpg"
                with open(thumbnailimg, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        thumbnailURL, 

                    )

                
                videoPATH = s3PATH+videoURL

                videoTMPinfoCount = VideoTMP.objects.filter(loginUserPK = userPK, status = "0").count()
                if videoTMPinfoCount == 0:
                    pass

                else:
                    videoTMPinfo = VideoTMP.objects.get(loginUserPK = userPK, status = "0")
                    videoTMPinfo.status = "9"
                    videoTMPinfo.save()

                videoTMP = VideoTMP(loginUserPK = userPK, videoPATH = videoPATH, thumbnailPATH = thumbnailURL, createAt = datetime.now(), createAt_timestamp = time.time(), inviteCode = inviteCode)
                videoTMP.save()

                tmpVideoPK = videoTMP.id


                text = "user PK값 : " + userPK + ", 동영상 저장 완료"
                ment = "\033[92m"+"tmpVideoUpload_originPATH SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1', 'tmpVideoPK':tmpVideoPK, 'tmpVideoPATH':videoPATH}
                return HttpResponse(json.dumps(context, default=json_util.default))

            else:
                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"tmpVideoUpload_originPATH WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
                


    except Exception as e: 
        text = str(e)
        ment = "\033[91m"+"tmpVideoUpload_originPATH Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






@csrf_exempt
def tmpVideoUpload(request):
    try:
        if request.method == 'POST':

            userPK = str(request.POST.get('loginUserPK'))
            reqFile = request.FILES
            # print("reqFile >>", reqFile)
            if len(reqFile['file']) != 0:

                img = request.FILES['file']
                print("tmpVideoUpload >>>", img)
                tmpVideoPK = request.POST.get('tmpVideoPK')

                accelerated_endpoint_url = "https://newshowplus.s3-accelerate.amazonaws.com"
                
                videoTMPinfo = VideoTMP.objects.get(id = tmpVideoPK)
                inviteCode = videoTMPinfo.inviteCode


                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                # path = '/mnt/project/app/static/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "",                         # showplus
                    aws_secret_access_key = "",      # showplus
                    region_name = "ap-northeast-2"
                    # endpoint_url = accelerated_endpoint_url
                )

                s3_client.put_bucket_accelerate_configuration(
                    Bucket=bucketName,
                    AccelerateConfiguration={'Status': 'Enabled'}
                )



                tmpVideoURL = 'tmp/videos/dev/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

                s3_client.upload_fileobj(
                    img, 
                    bucketName, 
                    tmpVideoURL, 
                    ExtraArgs={
                        "ContentType": img.content_type
                    }
                )
                
                tmpVideoPATH = s3PATH+tmpVideoURL

                
                videoTMPinfo.tmpVideoPATH = tmpVideoPATH
                videoTMPinfo.save()



                text = "user PK값 : " + userPK + ", 동영상 저장 완료"
                ment = "\033[92m"+"tmpVideoUpload SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1', 'tmpVideoPATH':tmpVideoPATH}
                return HttpResponse(json.dumps(context, default=json_util.default))

            else:
                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"tmpVideoUpload WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
                


    except Exception as e: 
        text = str(e)
        ment = "\033[91m"+"tmpVideoUpload Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






# 메시지 전송
@csrf_exempt
def findusername_phoneAuthCode(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        phone = data['phone']
        userCheckCount = SignUp.objects.filter(phone = phone).count()

        if userCheckCount == 0:
            text = "phone : " + phone + ", 존재하지 않는 회원"
            ment = "\033[93m"+"findusername_phoneAuthCode WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))     
        
        else:
            account_sid = "AC620d12d1fc9e0a364eda97c55580a2b4"
            auth_token = "b3bc175dd2fa233c34fd6c4c77c197c4"
            client = Client(account_sid, auth_token)

            authCode = str(random.randint(100000, 999999))
            

            message = client.messages.create(
                body="인증 코드 ["+authCode+"] 입니다.",
                from_='+12515720354',
                to=phone
            )

            userinfo = SignUp.objects.get(phone = phone)
            userPK = userinfo.id
            username = userinfo.username

            text = "phone : " + phone + ", 존재하는 회원"
            ment = "\033[92m"+"findusername_phoneAuthCode SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'authCode':authCode, 'userPK':userPK, 'username':username}
            return HttpResponse(json.dumps(context))

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"findusername_phoneAuthCode Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 비밀번호 재설정
@csrf_exempt
def changePW(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        userPK = data['userPK']
        newPassword = data['pw']


        userinfoCount = SignUp.objects.filter(id = userPK).count()
        if userinfoCount == 0:
            text = "유저가 존재하지 않음"
            ment = "\033[93m"+"changePW WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))
        else:
            userinfo = SignUp.objects.get(id = userPK)

            password = userinfo.password
            checkPW = check_password(newPassword, password)
            if checkPW:
                text = "user PK값 : " + str(userPK) + ", 이전 비밀번호와 동일; 사용불가"
                ment = "\033[92m"+"previous_pwCheck WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))
            else:
                userinfo.set_password(newPassword)
                userinfo.save()
                text = "비밀번호 변경 완료"
                ment = "\033[92m"+"changePW SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1'}
                return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"changePW Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))



# 인증코드 메시지 전송
@csrf_exempt
def changePW_phoneAuthCode(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        phone = data['phone']
        userCheckCount = SignUp.objects.filter(phone = phone).count()

        if userCheckCount == 0:
            text = "phone : " + phone + ", 존재하지 않는 회원"
            ment = "\033[93m"+"findusername_phoneAuthCode WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')       
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))     
        
        else:

            userCheck = SignUp.objects.get(phone = phone)
            userCheck_username = userCheck.username

            if username == userCheck_username:
                account_sid = "AC620d12d1fc9e0a364eda97c55580a2b4"
                auth_token = "b3bc175dd2fa233c34fd6c4c77c197c4"
                client = Client(account_sid, auth_token)

                authCode = str(random.randint(100000, 999999))
                

                message = client.messages.create(
                    body="인증 코드 ["+authCode+"] 입니다.",
                    from_='+12515720354',
                    to=phone
                )

                userinfo = SignUp.objects.get(phone = phone)
                userPK = userinfo.id
                username = userinfo.username

                text = "phone : " + phone + ", 존재하는 회원"
                ment = "\033[92m"+"findusername_phoneAuthCode SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'authCode':authCode, 'userPK':userPK, 'username':username}
                return HttpResponse(json.dumps(context))
            else:
                text = "userCheck_username : " + userCheck_username + ", 유저 정보가 일치하지 않음"
                ment = "\033[93m"+"findusername_phoneAuthCode WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')       
                context = {'code':'2'}
                return HttpResponse(json.dumps(context))     

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"findusername_phoneAuthCode Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    




# 알림 보내기
@csrf_exempt
def sendAlim(reqData):
    try:
        loginUserPK = reqData["loginUserPK"]
        ownerPK = reqData["ownerPK"]
        thumbnailPATH = reqData["thumbnailPATH"]
        typeNum = reqData["typeNum"]
        itemPK = reqData["itemPK"]


        userinfo = SignUp.objects.get(id = loginUserPK)
        userNick = userinfo.nickName

        ownerUserinfo = SignUp.objects.get(id = ownerPK)
        token = ownerUserinfo.fcmToken

        alimTypeListinfo = AlimTypeList.objects.get(typeNum = typeNum)
        text = alimTypeListinfo.text
        alimListinfo = AlimList(
            userPK_S = loginUserPK, 
            userPK_R = ownerPK, 
            thumbnailPATH = thumbnailPATH,
            typeNum = typeNum,
            createAt = datetime.now(),
            createAt_timestamp = str(round(time.time())),
            itemPK = itemPK
        )
        alimListinfo.save()

        body = userNick + text

        if typeNum == "1":
            notif_like = ownerUserinfo.notif_like
            if notif_like == "Y":
                if loginUserPK == ownerPK:
                    pass
                else:
                    data_message = {}
                    result = push_service.notify_single_device(
                        registration_id=token,
                        message_title="Show+",
                        message_body=body,
                        data_message=data_message,
                        sound="default", 
                    )
                    
        elif typeNum == "2":
            pass
        elif typeNum == "3":
            pass
        elif typeNum == "4":
            pass
        elif typeNum == "5":
            pass
        elif typeNum == "6":
            notif_following = ownerUserinfo.notif_following
            if notif_following == "Y":
                if loginUserPK == ownerPK:
                    pass
                else:
                    data_message = {}
                    result = push_service.notify_single_device(
                        registration_id=token,
                        message_title="Show+",
                        message_body=body,
                        data_message=data_message,
                        sound="default", 
                    )

            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"findusername_phoneAuthCode Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 알림 리스트
@csrf_exempt
def myProfile_AlimList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        alimListCount = AlimList.objects.filter(userPK_R = loginUserPK).count()
        if alimListCount == 0:
            text = "loginUserPK : " + loginUserPK + ", 알림 리스트 없음"
            ment = "\033[93m"+"myProfile_AlimList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))
        else:
            alimListinfo = AlimList.objects.filter(userPK_R = loginUserPK).order_by("-id")
            alimList = []
            for index, i in enumerate(alimListinfo):
                alimPK = i.id
                senderPK = i.userPK_S
                typeNum = i.typeNum
                itemPK = i.itemPK
                readStatus = i.readStatus
                createAt_timestamp = i.createAt_timestamp

                alimTypeListinfo = AlimTypeList.objects.get(typeNum = typeNum)
                text = alimTypeListinfo.text
                # body = senderPK + text

                previousReturn = previousDate(createAt_timestamp)
                previous_date = previousReturn['previous_date']
                previous = previousReturn['previous']

                senderUserinfo = SignUp.objects.get(id = senderPK)
                nickname = senderUserinfo.nickName
                profileIMG_path = senderUserinfo.profileIMG_path
                if profileIMG_path:
                    profileIMG_path = s3_profileimgPATH+profileIMG_path
                else:
                    profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                if typeNum == "1":
                    # 영상 좋아요
                    thumbnailPATH = i.thumbnailPATH
                    thumbnailPATH = s3PATH + thumbnailPATH
                    dictinfo = {"typeNum":typeNum, "profileIMG_path":profileIMG_path, "nickname":nickname, "text":text, "previous_date":previous_date, "previous":previous, "thumbnailPATH":thumbnailPATH, "readStatus":readStatus}
                    alimList.append(dictinfo)
                elif typeNum == "2":
                    # 댓글 좋아요
                    pass
                elif typeNum == "3":
                    # 대댓글 좋아요
                    pass
                elif typeNum == "4":
                    # 영상 댓글
                    pass
                elif typeNum == "5":
                    # 댓글 댓글
                    pass
                elif typeNum == "6":
                    # 팔로우
                    dictinfo = {"typeNum":typeNum, "profileIMG_path":profileIMG_path, "nickname":nickname, "text":text, "previous_date":previous_date, "previous":previous, "thumbnailPATH":None, "readStatus":readStatus}
                    alimList.append(dictinfo)


            alimListinfo.update(readStatus = "9")

            text = "loginUserPK : " + loginUserPK + ", 리스트 호출"
            ment = "\033[92m"+"myProfile_AlimList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1', 'alimList':alimList}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"myProfile_AlimList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 이전시간 표기 ( 10분전 / 1시간전 등)
@csrf_exempt
def previousDate(prevTimeStamp):
    try:
        now  = int(round(time.time()))
        createAt_timestamp = int(round(float(prevTimeStamp)))
        me_time = math.floor(((now - createAt_timestamp) / 60))
        me_timehour = math.floor((me_time / 60))
        me_timeday = math.floor((me_timehour / 24))
        me_timeyear = math.floor(me_timeday / 365)

        previous_date = ""

        if me_time < 1 :
            # previous = '방금전'
            previous = 'B'
            previous_date = "0"
            
        elif me_time < 60 :
            # previous = str(me_time) + '분전'
            previous = 'M'
            previous_date = str(me_time)

        elif me_timehour < 24 :
            # previous = str(me_timehour) + '시간전'
            previous = 'H'
            previous_date = str(me_timehour)
        
        elif me_timeday < 365 :
            # previous = str(me_timeday) + '일전'
            previous = 'D'
            previous_date = str(me_timeday)

        elif me_timeyear >= 1 : 
            # previous = str(me_timeyear) + '년전'
            previous = 'Y'
            previous_date = str(me_timeyear)

        return {"previous_date":previous_date, "previous":previous}
    
    except Exception as e:
        return None
    




# 인증코드 메시지 전송
@csrf_exempt
def settings_notifLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        check = data['check']

        userinfo = SignUp.objects.get(id = loginUserPK)
        userinfo.notif_like = check
        userinfo.save()


        text = "loginUserPK : " + loginUserPK + ", 좋아요 알림 : " + check
        ment = "\033[92m"+"settings_notifLike SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1'}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_notifLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




@csrf_exempt
def settings_notifiFollowing(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        check = data['check']

        print("check ====================================", check )

        userinfo = SignUp.objects.get(id = loginUserPK)
        userinfo.notif_following = check
        userinfo.save()


        text = "loginUserPK : " + loginUserPK + ", 팔로우 알림 : " + check
        ment = "\033[92m"+"settings_notifiFollowing SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1'}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"settings_notifiFollowing Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
