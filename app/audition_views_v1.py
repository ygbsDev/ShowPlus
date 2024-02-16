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

serverURL = "http://43.203.20.234:7777"
aws_access_key_id = "AKIATCKASMRTGPVOBC6H",
aws_secret_access_key = "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"
# -------------------------------------------------------------------------------------------
# ygbs
# s3_profileimgPATH = "https://showplus.s3.ap-northeast-2.amazonaws.com/profileIMG/"
# s3_videoPATH = "https://showplus.s3.ap-northeast-2.amazonaws.com/videos/"
# s3_audition_videoPATH = "https://showplus.s3.ap-northeast-2.amazonaws.com/auditionVideos/"
# -------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
# showplus
s3PATH = "https://newshowplus.s3.ap-northeast-2.amazonaws.com/"
s3_profileimgPATH = "https://newshowplus.s3.ap-northeast-2.amazonaws.com/"
s3_videoPATH = "https://newshowplus.s3.ap-northeast-2.amazonaws.com/"
s3_thumbnailPATH = "https://newshowplus.s3.ap-northeast-2.amazonaws.com/"
s3_audition_videoPATH = "https://newshowplus.s3.ap-northeast-2.amazonaws.com/auditionVideos/"
# -------------------------------------------------------------------------------------------

def print_line_number():
    frame = inspect.currentframe()
    line_number = frame.f_lineno
    print("Current line number:", line_number)




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
#                     aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
#                     aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
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
    



# # 오디션 영상 업로드 체크
# @csrf_exempt
# def audition_uploadCheck(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']

#             audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK).count()
#             if audition_videoinfoCount == 0:
#                 text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
#                 ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_videoinfoDelCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK, status = "5").count()
#                 if audition_videoinfoCount == audition_videoinfoDelCount:
#                     text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
#                     ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'0'}
#                     return HttpResponse(json.dumps(context))
#                 else:                
#                     text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 불가"
#                     ment = "\033[93m"+"audition_uploadCheck WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
                
#         else:
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']

#             audition_videoinfoCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK).count()
#             if audition_videoinfoCount == 0:
#                 text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
#                 ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_videoinfoDelCount = Audition_video.objects.filter(userPK = loginUserPK, auditionListPK = auditionListPK, status = "5").count()
#                 if audition_videoinfoCount == audition_videoinfoDelCount:
#                     text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 가능"
#                     ment = "\033[92m"+"audition_uploadCheck SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'0'}
#                     return HttpResponse(json.dumps(context))
#                 else:                
#                     text = "loginUserPK PK값 : " + str(loginUserPK) + ", 영상 업로드 불가"
#                     ment = "\033[93m"+"audition_uploadCheck WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_uploadCheck Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 오디션 영상 업로드 체크
@csrf_exempt
def audition_uploadCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
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
    


# # 오디션 동영상 업로드
# @csrf_exempt
# def audition_fileupload(request):
#     try:
#         if request.method == 'POST':
#             userPK = str(request.POST.get('loginUserPK'))
#             contents = request.POST.get('contents')
#             hashTag = request.POST.get('hashTag')
#             location = request.POST.get('location')
#             viewable = request.POST.get('viewable')
#             categoryPK = request.POST.get('categoryPK')
#             tournamentStatus = request.POST.get('tournamentStatus')
#             auditionListPK = request.POST.get('auditionListPK')
#             rewardRate = request.POST.get('rewardRate')
#             size = request.POST.get('mention')
#             mention = request.POST.get('mention')
#             tag = request.POST.get('tag')

#             reqFile = request.FILES
#             print("reqFile >>", reqFile)
#             if len(reqFile['file']) != 0:
#                 # bucketName = "showplus"     # ygbs
#                 bucketName = "showpluss3"     # showplus
#                 img = request.FILES['file']
#                 print("img >>>", img)


#                 inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                 inviteCode = inviteCode + ".jpg"
#                 userinfoCount = Audition_video.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
#                 check = False
#                 if userinfoCount == 0:
#                     pass
#                 else:
#                     while check == False:
#                         inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                         inviteCode = inviteCode + ".jpg"
#                         userinfoCount_check = SignUp.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
#                         if userinfoCount_check == 0:
#                             check = True
#                             break;

#                 now = datetime.now()
#                 year = str(now.year)
#                 month = str(now.month)
#                 day = str(now.day)

#                 path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


#                 # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
#                 # aws_secret_access_key = "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"        # ygbs

#                 s3_client = boto3.client(
#                     's3',
#                     aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
#                     aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
#                 )
#                 s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))


#                 # -------------------------------------------------------------------------------------------------------
#                 # 로직 필요없거나 수정해야함
#                 # videoinfoCount = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
#                 # url = ""
#                 # check = False

#                 # if videoinfoCount == 0:
#                 #     url = 'videos/videos/'+s3VideoPATH
#                 # else:
#                 #     while check == False:
#                 #         s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                 #         videoinfoCount_check = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
#                 #         if videoinfoCount_check == 0:
#                 #             check = True
#                 #             url = 'videos/videos/'+s3VideoPATH
#                 #             break;
#                 # -------------------------------------------------------------------------------------------------------


#                 videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + s3VideoPATH

#                 s3_client.upload_fileobj(
#                     img, 
#                     bucketName, 
#                     videoURL, 
#                     ExtraArgs={
#                         "ContentType": img.content_type
#                     }
#                 )
                
#                 # -----------------------------------------------------------
#                 # 간혹 영상 업로드시 오류가있어 서버에 저장하는 부분 뺌
#                 # if not os.path.exists(path):
#                 #     os.makedirs(path)
#                 # if os.path.isfile(path +str(img)):
#                 #     os.remove(path +str(img))

#                 # file_path = path + str(img)
#                 # with open(file_path, 'wb+') as destination:
#                 #     for chunk in img.chunks():
#                 #         destination.write(chunk)
#                 # # 파일 객체가 닫힌 후에 작업 수행
#                 # with open(file_path, 'rb') as file:
#                 #     # 파일 읽기 등 추가 작업 수행
#                 #     data = file.read()
#                 #     # 예시: seek 작업 수행
#                 #     file.seek(0)
#                 #     # 추가 작업 수행            
#                 # -----------------------------------------------------------

#                 count = 1
#                 test = 1
#                 train = 1
#                 vidcap = cv2.VideoCapture(s3PATH+videoURL)
#                 thumbnailPath = '/mnt/project/app/static/auditions/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
#                 if not os.path.exists(thumbnailPath):
#                     os.makedirs(thumbnailPath)
                
#                 thumbnail_savePATH = ""
                

#                 while(vidcap.isOpened()):
#                     ret, image = vidcap.read()
#                     if(ret==False):
#                         break
#                     if(int(vidcap.get(1)) % 5 == 0):
#                         num=count % 10
#                         thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
#                         print("thumbnail_savePATH >>", thumbnail_savePATH)
#                         cv2.imwrite(thumbnailPath + inviteCode, image)
#                         break;
#                 vidcap.release()



#                 thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH
#                 thumbnailimg = thumbnailPath + inviteCode
#                 with open(thumbnailimg, 'rb') as image_file:
#                     s3_client.upload_fileobj(
#                         image_file, 
#                         bucketName, 
#                         thumbnailURL, 
#                         # ExtraArgs={
#                         #     "ContentType": image_file.content_type
#                         # }
#                     )


#                 savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

#                 if hashTag == "":
#                     hashTag = None

#                 videoSubmit = Audition_video(
#                     userPK = userPK, 
#                     createAt = datetime.now(), 
#                     createAt_timestamp = str(round(time.time())), 
#                     thumbnailPATH = thumbnailURL, 
#                     videoPATH = videoURL, 
#                     # s3VideoPATH = videoURL,
#                     contents = contents, 
#                     hashTag = hashTag,
#                     location = location,
#                     viewable = viewable,
#                     categoryPK = categoryPK,
#                     # tournamentStatus = tournamentStatus,
#                     auditionListPK = auditionListPK,
#                     rewardRate = str(rewardRate),
#                     size = size,
#                     mention = mention,
#                     tag = tag
#                 )
#                 videoSubmit.save()
                
#                 videoPK = videoSubmit.id
#                 Audition_CountSubmit = Audition_Count(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK, tournamentStatus = tournamentStatus)
#                 Audition_CountSubmit.save()

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
    



# # 오디션 카테고리2 리스트 
# @csrf_exempt
# def audition_auditionList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             categoryPK = data['categoryPK']
#             categoryName = data['categoryName']


#             auditionListinfoCount = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9").count()

#             if auditionListinfoCount == 0:
#                 text = "오디션 없음"
#                 ment = "\033[93m"+"audition_auditionList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'auditionList':None}
#                 return HttpResponse(json.dumps(context))        
#             else:
#                 auditionListinfo = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9")
#                 auditionList = []
#                 for index, i in enumerate(auditionListinfo):
#                     auditionListPK = i.id
#                     audition_List_tournamentStatus = i.tournamentStatus
#                     TournamentStatusListinfo = TournamentStatusList.objects.get(status = audition_List_tournamentStatus)
#                     tournamentStatus = TournamentStatusListinfo.status
#                     progressStatus = i.progressStatus
#                     title = i.title
#                     auditionImgPATH = i.auditionImgPATH
#                     if auditionImgPATH:
#                         auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH


#                     dictinfo = {'auditionListPK':auditionListPK, 'tournamentStatus':tournamentStatus, 'progressStatus':progressStatus, 'title':title, 'auditionImgPATH':auditionImgPATH}
#                     auditionList.append(dictinfo)



#                 text = "\033[92m"+"audition_auditionList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'categoryName':categoryName, 'auditionList':auditionList}
#                 return HttpResponse(json.dumps(context))

#         else:
#             categoryPK = data['categoryPK']
#             categoryName = data['categoryName']


#             auditionListinfoCount = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9").count()

#             if auditionListinfoCount == 0:
#                 text = "오디션 없음"
#                 ment = "\033[93m"+"audition_auditionList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'auditionList':None}
#                 return HttpResponse(json.dumps(context))        
#             else:
#                 auditionListinfo = Audition_List.objects.filter(categoryPK = categoryPK, useYn = "Y").exclude(progressStatus="9")
#                 auditionList = []
#                 for index, i in enumerate(auditionListinfo):
#                     auditionListPK = i.id
#                     audition_List_tournamentStatus = i.tournamentStatus
#                     TournamentStatusListinfo = TournamentStatusList.objects.get(status = audition_List_tournamentStatus)
#                     tournamentStatus = TournamentStatusListinfo.status
#                     progressStatus = i.progressStatus
#                     title = i.title
#                     auditionImgPATH = i.auditionImgPATH
#                     if auditionImgPATH:
#                         auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH


#                     dictinfo = {'auditionListPK':auditionListPK, 'tournamentStatus':tournamentStatus, 'progressStatus':progressStatus, 'title':title, 'auditionImgPATH':auditionImgPATH}
#                     auditionList.append(dictinfo)



#                 text = "\033[92m"+"audition_auditionList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'categoryName':categoryName, 'auditionList':auditionList}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_auditionList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# 오디션 카테고리2 리스트 
@csrf_exempt
def audition_auditionList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        categoryPK = data['categoryPK']
        # categoryName = data['categoryName']


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
                audition_List_tournamentStatus = i.tournamentStatus
                TournamentStatusListinfo = TournamentStatusList.objects.get(status = audition_List_tournamentStatus)
                tournamentStatus = TournamentStatusListinfo.status
                progressStatus = i.progressStatus
                title = i.title
                auditionImgPATH = i.auditionImgPATH
                # if auditionImgPATH:
                #     auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH


                dictinfo = {'auditionListPK':auditionListPK, 'tournamentStatus':tournamentStatus, 'progressStatus':progressStatus, 'title':title, 'auditionImgPATH':auditionImgPATH}
                auditionList.append(dictinfo)



            text = "\033[92m"+"audition_auditionList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'auditionList':auditionList}
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
    

# # 오디션 비디오 리스트
# @csrf_exempt
# def audition_videoList(request):
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
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']
#             categoryPK = data['categoryPK']

#             # loginUserPK = data['loginUserPK']
#             # auditionListPK = data['auditionListPK']
#             # categoryListPK = data['categoryListPK']
#             # tournamentPK = data['tournamentPK']

#             # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#             if progressStatus == "2":
#                 pass
#             else:
#                 if tournamentStatus == "1":
#                     videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
#                     if videoinfoCount == 0:
#                         text = "비디오 리스트 없음"
#                         ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
#                         print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                         context = {'code':'0', 'audition_videoinfoList':None}
#                         return HttpResponse(json.dumps(context))
#                     else:        
#                         # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
#                         audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").order_by('?')
#                         audition_videoinfoList = []
#                         winnerPoint = 0
#                         for index, i in enumerate(audition_videoinfo):
#                             userPK = i.userPK
#                             videoPK = i.id
#                             userinfo = SignUp.objects.get(id = userPK)
#                             username = userinfo.username
#                             nickName = userinfo.nickName
#                             profileIMG_path = userinfo.profileIMG_path
#                             if profileIMG_path:
#                                 profileIMG_path = s3PATH+profileIMG_path
#                             else:
#                                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                             thumbnailPATH = i.thumbnailPATH
#                             thumbnailPATH = s3PATH+thumbnailPATH

#                             videoPATH = i.videoPATH
#                             s3Check = S3Check.objects.get(id = 1)
#                             s3Status = s3Check.status
#                             if s3Status == "0":
#                                 videoPATH = serverURL+"/static/video"+videoPATH
#                             elif s3Status == "1":
#                                 videoPATH = s3PATH+videoPATH

                            
#                             contents = i.contents
#                             hashTag = i.hashTag
#                             viewable = i.viewable
#                             # likeCount = ""
#                             # comentCount = ""
#                             # userLikeCheck = ""

#                             # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                             # likeCount = str(audition_like_video_infoCount)

#                             # audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                             # if audition_like_video_infoCount_user == 0:
#                             #     userLikeCheck = "0"
#                             # else:
#                             #     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                             #     status = audition_like_video_info_user.status
#                             #     if status == "0":
#                             #         userLikeCheck = "0"
#                             #     elif status == "1":
#                             #         userLikeCheck = "1"

#                             # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                             # comentCount = str(audition_coment_infoCount)

#                             # audition_coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                             # if audition_coment_infoCount_user == 0:
#                             #     userComentCheck = "0"
#                             # else:
#                             #     userComentCheck = "1"
#                             # print("videoPK >>", videoPK)
#                             # print("auditionListPK >>", auditionListPK)
#                             # print("tournamentStatus >>", tournamentStatus)
#                             print("auditionListPK >>", auditionListPK)
#                             print("tournamentStatus >>", tournamentStatus)

#                             audition_Count = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
#                             winnerPoint += int(audition_Count.donation)

#                             dictinfo = {
#                                 'videoPK':str(videoPK), 
#                                 'userPK':userPK, 
#                                 'username':username,
#                                 'nickName':nickName,
#                                 'profileIMG_path':profileIMG_path,
#                                 'contents':contents,
#                                 'hashTag':hashTag,
#                                 'thumbnailPATH':thumbnailPATH,
#                                 'videoPATH':videoPATH,
#                                 'viewable':viewable,
#                                 # 'likeCount':likeCount,
#                                 # 'comentCount':comentCount,
#                                 # 'userLikeCheck':userLikeCheck,
#                                 'auditionListPK':auditionListPK,
#                                 'tournamentStatus':tournamentStatus,
#                                 'categoryPK':categoryPK
#                             }
#                             audition_videoinfoList.append(dictinfo)
#                         # random.shuffle(audition_videoinfoList)
#                         audition_videoAllinfo = audition_videoinfoList
#                         audition_videoinfoList = audition_videoinfoList[pageStart:pageEnd]

#                         text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                         print("["+str(datetime.now())+"] " + text)
#                         context = {'code':'1', 'audition_videoAllinfo':audition_videoAllinfo, 'audition_videoinfoList':audition_videoinfoList, 'winnerPoint':winnerPoint}
#                         return HttpResponse(json.dumps(context))
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 21
#             pageEnd = 21 * page
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']
#             categoryPK = data['categoryPK']

#             # loginUserPK = data['loginUserPK']
#             # auditionListPK = data['auditionListPK']
#             # categoryListPK = data['categoryListPK']
#             # tournamentPK = data['tournamentPK']

#             # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#             if progressStatus == "2":
#                 pass
#             else:
#                 if tournamentStatus == "1":
#                     videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
#                     if videoinfoCount == 0:
#                         text = "비디오 리스트 없음"
#                         ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
#                         print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                         context = {'code':'0', 'audition_videoinfoList':None}
#                         return HttpResponse(json.dumps(context))
#                     else:        
#                         # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
#                         audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").order_by('?')
#                         audition_videoinfoList = []
#                         winnerPoint = 0
#                         for index, i in enumerate(audition_videoinfo):
#                             userPK = i.userPK
#                             videoPK = i.id
#                             userinfo = SignUp.objects.get(id = userPK)
#                             username = userinfo.username
#                             nickName = userinfo.nickName
#                             profileIMG_path = userinfo.profileIMG_path
#                             if profileIMG_path:
#                                 profileIMG_path = s3PATH+profileIMG_path
#                             else:
#                                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                             thumbnailPATH = i.thumbnailPATH
#                             thumbnailPATH = s3PATH+thumbnailPATH

#                             videoPATH = i.videoPATH
#                             s3Check = S3Check.objects.get(id = 1)
#                             s3Status = s3Check.status
#                             if s3Status == "0":
#                                 videoPATH = serverURL+"/static/video"+videoPATH
#                             elif s3Status == "1":
#                                 videoPATH = s3PATH+videoPATH

                            
#                             contents = i.contents
#                             hashTag = i.hashTag
#                             viewable = i.viewable
#                             # likeCount = ""
#                             # comentCount = ""
#                             # userLikeCheck = ""

#                             # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                             # likeCount = str(audition_like_video_infoCount)

#                             # audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                             # if audition_like_video_infoCount_user == 0:
#                             #     userLikeCheck = "0"
#                             # else:
#                             #     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                             #     status = audition_like_video_info_user.status
#                             #     if status == "0":
#                             #         userLikeCheck = "0"
#                             #     elif status == "1":
#                             #         userLikeCheck = "1"

#                             # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                             # comentCount = str(audition_coment_infoCount)

#                             # audition_coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                             # if audition_coment_infoCount_user == 0:
#                             #     userComentCheck = "0"
#                             # else:
#                             #     userComentCheck = "1"
                                
#                             audition_Count = Audition_Count.objects.get(videoPK = videoPK)
#                             winnerPoint += int(audition_Count.donation)

#                             dictinfo = {
#                                 'videoPK':str(videoPK), 
#                                 'userPK':userPK, 
#                                 'username':username,
#                                 'nickName':nickName,
#                                 'profileIMG_path':profileIMG_path,
#                                 'contents':contents,
#                                 'hashTag':hashTag,
#                                 'thumbnailPATH':thumbnailPATH,
#                                 'videoPATH':videoPATH,
#                                 'viewable':viewable,
#                                 # 'likeCount':likeCount,
#                                 # 'comentCount':comentCount,
#                                 # 'userLikeCheck':userLikeCheck,
#                                 'auditionListPK':auditionListPK,
#                                 'tournamentStatus':tournamentStatus,
#                                 'categoryPK':categoryPK
#                             }
#                             audition_videoinfoList.append(dictinfo)
#                         # random.shuffle(audition_videoinfoList)
#                         audition_videoAllinfo = audition_videoinfoList
#                         audition_videoinfoList = audition_videoinfoList[pageStart:pageEnd]

#                         text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                         print("["+str(datetime.now())+"] " + text)
#                         context = {'code':'1', 'audition_videoAllinfo':audition_videoAllinfo, 'audition_videoinfoList':audition_videoinfoList, 'winnerPoint':winnerPoint}
#                         return HttpResponse(json.dumps(context))
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
                            profileIMG_path = s3PATH+profileIMG_path
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
                        # print("videoPK >>", videoPK)
                        # print("auditionListPK >>", auditionListPK)
                        # print("tournamentStatus >>", tournamentStatus)


                        audition_Count = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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



# 오디션별 현재 상금
@csrf_exempt
def audition_winnerPoint(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        auditionListPK = data['auditionListPK']
        # audition_Countinfo = Audition_Count.objects.filter(auditionListPK = auditionListPK)
        # winnerPoint = 0
        # for index, i in enumerate(audition_Countinfo):
        #     winnerPoint += int(i.donation)

        # audition_winnerPaymentsinfo = Audition_winnerPayments.objects.filter(auditionListPK = auditionListPK)
        # winnerPoint = 0
        # for index, i in enumerate(audition_winnerPaymentsinfo):
        #     winnerPoint += int(i.amount)
        audition_Countinfo = Audition_Count.objects.filter(auditionListPK = auditionListPK)
        winnerPoint = 0
        for index, i in enumerate(audition_Countinfo):
            winnerPoint += int(i.donation)
        

        text = "\033[92m"+"audition_winnerPoint SUCCESS -> 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'winnerPoint':winnerPoint}
        return HttpResponse(json.dumps(context))
        


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_winnerPoint Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


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
#                         profileIMG_path = s3PATH+profileIMG_path
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
#                         profileIMG_path = s3PATH+profileIMG_path
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


#                     videoPK = i['videoPK']
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status

#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']

#                     thumbnailPATH = i['thumbnailPATH']
                    

#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']




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


#                     videoPK = i['videoPK']
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status

#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']

#                     thumbnailPATH = i['thumbnailPATH']
                    
#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']


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
                    profileIMG_path = s3PATH+profileIMG_path
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
    


# # 오디션 영상 후원
# @csrf_exempt
# def audition_donetion(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             sender_userPK = data['sender_userPK']
#             receiver_userPK = data['receiver_userPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             videoPK = data['videoPK']
#             amount = data['amount']

#             userinfo = SignUp.objects.get(id = sender_userPK)
#             senderUserPoint = userinfo.point
#             if int(senderUserPoint) < int(amount):
#                 text = "잔고 부족"
#                 ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context))
            
#             else:
#                 donetionListSubmit = Audition_DonationList(sender_userPK = sender_userPK, receiver_userPK = receiver_userPK, videoPK = videoPK, amount = amount, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 donetionListSubmit.save()

#                 userinfo = SignUp.objects.get(id = sender_userPK)
#                 userinfo.point = int(userinfo.point) - int(amount)
#                 userinfo.save()

#                 audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 audition_Countinfo.donation = int(audition_Countinfo.donation) + int(amount)
#                 audition_Countinfo.save()

#                 text = "후원 완료"
#                 ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             sender_userPK = data['sender_userPK']
#             receiver_userPK = data['receiver_userPK']
#             videoPK = data['videoPK']
#             amount = data['amount']

#             userinfo = SignUp.objects.get(id = sender_userPK)
#             senderUserPoint = userinfo.point
#             if int(senderUserPoint) < int(amount):
#                 text = "잔고 부족"
#                 ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context))
            
#             else:
#                 donetionListSubmit = Audition_DonationList(sender_userPK = sender_userPK, receiver_userPK = receiver_userPK, videoPK = videoPK, amount = amount, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 donetionListSubmit.save()

#                 userinfo = SignUp.objects.get(id = sender_userPK)
#                 userinfo.point = int(userinfo.point) - int(amount)
#                 userinfo.save()

#                 audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 audition_Countinfo.donation = int(audition_Countinfo.donation) + int(amount)
#                 audition_Countinfo.save()

#                 text = "후원 완료"
#                 ment = "\033[92m"+"donetion SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"donetion Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# 오디션 영상 후원
# 함수명 오타 조심
@csrf_exempt
def audition_donetion(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        sender_userPK = data['sender_userPK']
        receiver_userPK = data['receiver_userPK']
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']
        categoryPK = data['categoryPK']
        videoPK = data['videoPK']
        amount = data['amount']

        audition_List = Audition_List.objects.get(id = auditionListPK )
        auditionTitle = audition_List.title

        

        userinfo = SignUp.objects.get(id = sender_userPK)
        senderUserPoint = userinfo.point
        if int(senderUserPoint) < int(amount):
            text = "잔고 부족"
            ment = "\033[93m"+"donetion WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        
        else:
            donetionListSubmit = Audition_DonationList(
                sender_userPK = sender_userPK, 
                receiver_userPK = receiver_userPK, 
                videoPK = videoPK, 
                amount = amount, 
                createAt = datetime.now(), 
                createAt_timestamp = str(round(time.time())), 
                auditionListPK = auditionListPK,
                categoryPK = categoryPK,
                tournamentStatus = tournamentStatus
            )

            donetionListSubmit.save()

            userinfo = SignUp.objects.get(id = sender_userPK)
            userinfo.point = int(userinfo.point) - int(amount)
            userinfo.save()

            pointHistorySubmit = PointHistory(
                userPK_S = sender_userPK,
                userPK_R = receiver_userPK,
                videoPK = videoPK,
                point = amount,
                title = auditionTitle,
                status = "2",
                contentsStatus = "1",
                createAt = datetime.now(),
                createAt_timestamp = str(round(time.time()))
            )
            pointHistorySubmit.save()



            audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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
    



# # 오디션 예전선 상세 및 위아래 페이지 네이션
# @csrf_exempt
# def audition_DetailListMove(request):
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
#             audition_videoAllinfo = data['audition_videoAllinfo']
#             audition_videoAllinfo = audition_videoAllinfo[pageStart:pageEnd]
#             audition_videoAllinfoLen = len(audition_videoAllinfo)
#             if audition_videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfoList = []
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
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']
#                     # videoPATH = s3PATH+videoPATH

#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+videoPATH
#                     # s3VideoPATH = i['s3VideoPATH']

#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+s3VideoPATH

#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']

                    
                    
#                     userLikeCheck = ""
#                     viewCountCheck = ""


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


#                     audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     likeCount = str(audition_like_video_infoCount)

#                     print("userPK >>", userPK)
#                     print("videoPK >>", videoPK)

#                     audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                     if audition_like_video_infoCount_user == 0:
#                         userLikeCheck = "0"
#                     else:
#                         audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                         status = audition_like_video_info_user.status
#                         if status == "0":
#                             userLikeCheck = "0"
#                         elif status == "1":
#                             userLikeCheck = "1"







#                     audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                     comentCount = str(audition_coment_infoCount)

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


#                     viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     if viewCount_infoCount == 0:
#                         viewCountCheck = "0"
#                     else:
#                         viewCountCheck = "1"


#                     dictinfo = {
#                         'videoPK':int(videoPK), 
#                         'userPK':userPK, 
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'hashTag':hashTag,
#                         'videoPATH':videoPATH,
#                         'viewable':viewable,
#                         'likeCount':str(likeCount),
#                         'comentCount':str(comentCount),
#                         'userLikeCheck':userLikeCheck,
#                         'viewCountCheck':viewCountCheck
#                     }
#                     videoinfoList.append(dictinfo)


#                 # print("videoinfoList >>", videoinfoList)
#                 text = "\033[92m"+"videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             audition_videoAllinfo = data['audition_videoAllinfo']
#             audition_videoAllinfo = audition_videoAllinfo[pageStart:pageEnd]
#             audition_videoAllinfoLen = len(audition_videoAllinfo)
#             if audition_videoAllinfoLen == 0:
#                 text = " :: 페이지 영상 없음"
#                 ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'2', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfoList = []
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
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i['videoPATH']
#                     # videoPATH = s3PATH+videoPATH

#                     # s3Check = S3Check.objects.get(id = 1)
#                     # s3Status = s3Check.status
#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+videoPATH
#                     # s3VideoPATH = i['s3VideoPATH']

#                     # if s3Status == "0":
#                     #     videoPATH = serverURL+"/static/video"+videoPATH
#                     # elif s3Status == "1":
#                     #     videoPATH = s3PATH+s3VideoPATH

#                     contents = i['contents']
#                     hashTag = i['hashTag']
#                     viewable = i['viewable']

                    
                    
#                     userLikeCheck = ""
#                     viewCountCheck = ""


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


#                     audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                     likeCount = str(audition_like_video_infoCount)

#                     audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = userPK, videoPK = videoPK).count()
#                     if audition_like_video_infoCount_user == 0:
#                         userLikeCheck = "0"
#                     else:
#                         audition_like_video_info_user = Audition_Like_video.objects.get(userPK = userPK, videoPK = videoPK)
#                         status = audition_like_video_info_user.status
#                         if status == "0":
#                             userLikeCheck = "0"
#                         elif status == "1":
#                             userLikeCheck = "1"







#                     audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                     comentCount = str(audition_coment_infoCount)

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


#                     viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                     if viewCount_infoCount == 0:
#                         viewCountCheck = "0"
#                     else:
#                         viewCountCheck = "1"


#                     dictinfo = {
#                         'videoPK':int(videoPK), 
#                         'userPK':userPK, 
#                         'username':username,
#                         'nickName':nickName,
#                         'profileIMG_path':profileIMG_path,
#                         'contents':contents,
#                         'hashTag':hashTag,
#                         'videoPATH':videoPATH,
#                         'viewable':viewable,
#                         'likeCount':str(likeCount),
#                         'comentCount':str(comentCount),
#                         'userLikeCheck':userLikeCheck,
#                         'viewCountCheck':viewCountCheck
#                     }
#                     videoinfoList.append(dictinfo)


#                 # print("videoinfoList >>", videoinfoList)
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



# 오디션 예전선 상세 및 위아래 페이지 네이션
@csrf_exempt
def audition_DetailListMove(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        page = int(data['page'])
        pageStart = (page - 1) * 10
        pageEnd = 10 * page
        loginUserPK = data['loginUserPK']
        audition_videoAllinfo = data['audition_videoAllinfo']
        audition_videoAllinfo = audition_videoAllinfo[pageStart:pageEnd]
        audition_videoAllinfoLen = len(audition_videoAllinfo)
        if audition_videoAllinfoLen == 0:
            text = " :: 페이지 영상 없음"
            ment = "\033[92m"+"contentsSearchDetailListMove WARNING -> "+text+"\033[0m"
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
                auditionListPK = i['auditionListPK']
                tournamentStatus = i['tournamentStatus']
                userinfo = SignUp.objects.get(id = userPK)
                username = userinfo.username
                nickName = userinfo.nickName
                profileIMG_path = userinfo.profileIMG_path
                s3Check = S3Check.objects.get(id = 1)
                s3Status = s3Check.status

                if profileIMG_path:
                    profileIMG_path = s3PATH+profileIMG_path
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



                audition_Count = Audition_Count.objects.filter(videoPK = videoPK, auditionListPK = auditionListPK)
                likeSum = 0
                comentSum = 0
                for index, j in enumerate(audition_Count):
                    likeSum += int(j.like)
                    comentSum += int(j.coment)


                # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
                # likeCount = str(audition_like_video_infoCount)


                # audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                # if audition_like_video_infoCount_user == 0:
                #     userLikeCheck = "0"
                # else:
                #     audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
                #     status = audition_like_video_info_user.status
                #     if status == "0":
                #         userLikeCheck = "0"
                #     elif status == "1":
                #         userLikeCheck = "1"

                audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK).count()
                if audition_like_video_infoCount_user == 0:
                    userLikeCheck = "0"
                else:
                    audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK)
                    status = audition_like_video_info_user.status
                    if status == "0":
                        userLikeCheck = "0"
                    elif status == "1":
                        userLikeCheck = "1"






                # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
                # comentCount = str(audition_coment_infoCount)

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


                # viewCount_infoCount = ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
                # if viewCount_infoCount == 0:
                #     viewCountCheck = "0"
                # else:
                #     viewCountCheck = "1"


                viewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus).count()
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
                    'likeCount':str(likeSum),
                    'comentCount':str(comentSum),
                    'userLikeCheck':userLikeCheck,
                    'viewCountCheck':viewCountCheck
                }
                videoinfoList.append(dictinfo)


            # print("videoinfoList >>", videoinfoList)
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



# # 오디션 예선 집계중 페이지
# @csrf_exempt
# def audition_aggregatingList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             # page = int(data['page'])
#             # pageStart = (page - 1) * 21
#             # pageEnd = 21 * page
#             # loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']


#             # loginUserPK = data['loginUserPK']
#             # auditionListPK = data['auditionListPK']
#             # categoryListPK = data['categoryListPK']
#             # tournamentPK = data['tournamentPK']

#             # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#             if progressStatus == "2":
#                 pass
#             else:
#                 if tournamentStatus == "1":
#                     # videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd].count()
#                     videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
#                     if videoinfoCount == 0:
#                         text = "비디오 리스트 없음"
#                         ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
#                         print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                         context = {'code':'0', 'audition_videoinfoList':None}
#                         return HttpResponse(json.dumps(context))
#                     else:        
#                         # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
#                         # audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd]
#                         audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")
#                         aggregatingList = []
#                         for index, i in enumerate(audition_videoinfo):
#                             userPK = i.userPK
#                             videoPK = i.id
#                             userinfo = SignUp.objects.get(id = userPK)
#                             nickName = userinfo.nickName
#                             profileIMG_path = userinfo.profileIMG_path
#                             if profileIMG_path:
#                                 profileIMG_path = s3PATH+profileIMG_path
#                             else:
#                                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                             userLikeCheck = ""

#                             donation = 0
#                             likeCount = 0
#                             comentCount = 0
#                             viewCount = 0

#                             # Audition_Countinfo_count = Audition_Count.objects.filter(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus).count()
#                             # if Audition_Countinfo_count == 0:
#                             #     Audition_CountSubmit = Audition_Count(ownerPK = userPK, videoPK = videoPK)
#                             #     Audition_CountSubmit.save()
#                             # else:
#                             Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
#                             donation = int(Audition_Countinfo.donation)
#                             donationSum = donation * 50
#                             likeCount = int(Audition_Countinfo.like)
#                             likeSum = likeCount * 25
#                             comentCount = int(Audition_Countinfo.coment)
#                             comentSum = comentCount * 10
#                             viewCount = int(Audition_Countinfo.viewcount)
#                             viewCountSum = viewCount * 15



#                             # likeCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                             # comentCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                             # comentinfo = Audition_Coment.objects.filter(videoPK = videoPK)




#                             # viewCount = Audition_ViewCount.objects.filter(videoPK = videoPK).count()
#                             allSum = donationSum + likeSum + comentSum + viewCountSum
                            
#                             dictinfo = {
#                                 'videoPK':str(videoPK), 
#                                 'userPK':userPK, 
#                                 'nickName':nickName,
#                                 'profileIMG_path':profileIMG_path,
#                                 'donation':donation,
#                                 'likeCount':likeCount,
#                                 'comentCount':comentCount,
#                                 'viewCount':viewCount,
#                                 'allSum':allSum,
#                             }
#                             aggregatingList.append(dictinfo)

#                         aggregatingList = sorted(aggregatingList, key=lambda x: x['allSum'], reverse=True)
#                         aggregatingList2 = []
#                         rank = 0
#                         for index, j in enumerate(aggregatingList):
#                             if index == 0:

#                                 videoPK = j['videoPK']
#                                 userPK = j['userPK']
#                                 nickName = j['nickName']
#                                 profileIMG_path = j['profileIMG_path']
#                                 donation = j['donation']
#                                 likeCount = j['likeCount']
#                                 comentCount = j['comentCount']
#                                 viewCount = j['viewCount']
#                                 allSum = j['allSum']

#                                 rank += 1

#                                 dictinfo = {
#                                     'videoPK':str(videoPK), 
#                                     'userPK':userPK, 
#                                     'nickName':nickName,
#                                     'profileIMG_path':profileIMG_path,
#                                     'donation':donation,
#                                     'likeCount':likeCount,
#                                     'comentCount':comentCount,
#                                     'viewCount':viewCount,
#                                     'allSum':allSum,
#                                     'rank': int(rank),
#                                 }
#                                 aggregatingList2.append(dictinfo)
#                             else:

#                                 checkIdx = index - 1
#                                 previous = aggregatingList2[checkIdx]
#                                 previous_allSum = previous['allSum']
#                                 previous_rank = previous['rank']

#                                 videoPK = j['videoPK']
#                                 userPK = j['userPK']
#                                 nickName = j['nickName']
#                                 profileIMG_path = j['profileIMG_path']
#                                 donation = j['donation']
#                                 likeCount = j['likeCount']
#                                 comentCount = j['comentCount']
#                                 viewCount = j['viewCount']
#                                 allSum = j['allSum']


#                                 if int(allSum) == int(previous_allSum):
#                                     rank = int(previous_rank)
#                                 else:
#                                     rankCount = len(aggregatingList2)
#                                     rank = rankCount + 1

#                                 dictinfo = {
#                                     'videoPK':str(videoPK), 
#                                     'userPK':userPK, 
#                                     'nickName':nickName,
#                                     'profileIMG_path':profileIMG_path,
#                                     'donation':donation,
#                                     'likeCount':likeCount,
#                                     'comentCount':comentCount,
#                                     'viewCount':viewCount,
#                                     'allSum':allSum,
#                                     'rank': int(rank),
#                                 }
#                                 aggregatingList2.append(dictinfo)


#                         aggregatingList2 = sorted(aggregatingList2, key=lambda x: x['rank'], reverse=True)




#                         text = "\033[92m"+"aggregatingList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                         print("["+str(datetime.now())+"] " + text)
#                         context = {'code':'1', 'aggregatingList':aggregatingList2}
#                         return HttpResponse(json.dumps(context))
                    

#         else:
#             # page = int(data['page'])
#             # pageStart = (page - 1) * 21
#             # pageEnd = 21 * page
#             # loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             progressStatus = data['progressStatus']


#             # loginUserPK = data['loginUserPK']
#             # auditionListPK = data['auditionListPK']
#             # categoryListPK = data['categoryListPK']
#             # tournamentPK = data['tournamentPK']

#             # audition_List_info = Audition_List.objects.get(category = category, progressStatus = "1")
#             if progressStatus == "2":
#                 pass
#             else:
#                 if tournamentStatus == "1":
#                     # videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd].count()
#                     videoinfoCount = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1").count()
#                     if videoinfoCount == 0:
#                         text = "비디오 리스트 없음"
#                         ment = "\033[93m"+"audition_videoList WARNING -> "+text+"\033[0m"
#                         print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                         context = {'code':'0', 'audition_videoinfoList':None}
#                         return HttpResponse(json.dumps(context))
#                     else:        
#                         # audition_videoinfo = Audition_video.objects.filter(categoryPK = categoryListPK, tournamentStatus = tournamentPK, progressStatus = "1").order_by('?')[pageStart:pageEnd]
#                         # audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")[pageStart:pageEnd]
#                         audition_videoinfo = Audition_video.objects.filter(auditionListPK = auditionListPK, status = "1")
#                         aggregatingList = []
#                         for index, i in enumerate(audition_videoinfo):
#                             userPK = i.userPK
#                             videoPK = i.id
#                             userinfo = SignUp.objects.get(id = userPK)
#                             nickName = userinfo.nickName
#                             profileIMG_path = userinfo.profileIMG_path
#                             if profileIMG_path:
#                                 profileIMG_path = s3PATH+profileIMG_path
#                             else:
#                                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                             userLikeCheck = ""

#                             donation = 0
#                             likeCount = 0
#                             comentCount = 0
#                             viewCount = 0

#                             Audition_Countinfo_count = Audition_Count.objects.filter(videoPK = videoPK).count()
#                             if Audition_Countinfo_count == 0:
#                                 Audition_CountSubmit = Audition_Count(ownerPK = userPK, videoPK = videoPK)
#                                 Audition_CountSubmit.save()
#                             else:
#                                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                                 donation = int(Audition_Countinfo.donation)
#                                 donationSum = donation * 50
#                                 likeCount = int(Audition_Countinfo.like)
#                                 likeSum = likeCount * 25
#                                 comentCount = int(Audition_Countinfo.coment)
#                                 comentSum = comentCount * 10
#                                 viewCount = int(Audition_Countinfo.viewcount)
#                                 viewCountSum = viewCount * 15



#                             # likeCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#                             # comentCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#                             # comentinfo = Audition_Coment.objects.filter(videoPK = videoPK)




#                             # viewCount = Audition_ViewCount.objects.filter(videoPK = videoPK).count()
#                             allSum = donationSum + likeSum + comentSum + viewCountSum
                            
#                             dictinfo = {
#                                 'videoPK':str(videoPK), 
#                                 'userPK':userPK, 
#                                 'nickName':nickName,
#                                 'profileIMG_path':profileIMG_path,
#                                 'donation':donation,
#                                 'likeCount':likeCount,
#                                 'comentCount':comentCount,
#                                 'viewCount':viewCount,
#                                 'allSum':allSum,
#                             }
#                             aggregatingList.append(dictinfo)

#                         aggregatingList = sorted(aggregatingList, key=lambda x: x['allSum'], reverse=True)
#                         aggregatingList2 = []
#                         rank = 0
#                         for index, j in enumerate(aggregatingList):
#                             if index == 0:

#                                 videoPK = j['videoPK']
#                                 userPK = j['userPK']
#                                 nickName = j['nickName']
#                                 profileIMG_path = j['profileIMG_path']
#                                 donation = j['donation']
#                                 likeCount = j['likeCount']
#                                 comentCount = j['comentCount']
#                                 viewCount = j['viewCount']
#                                 allSum = j['allSum']

#                                 rank += 1

#                                 dictinfo = {
#                                     'videoPK':str(videoPK), 
#                                     'userPK':userPK, 
#                                     'nickName':nickName,
#                                     'profileIMG_path':profileIMG_path,
#                                     'donation':donation,
#                                     'likeCount':likeCount,
#                                     'comentCount':comentCount,
#                                     'viewCount':viewCount,
#                                     'allSum':allSum,
#                                     'rank': int(rank),
#                                 }
#                                 aggregatingList2.append(dictinfo)
#                             else:

#                                 checkIdx = index - 1
#                                 previous = aggregatingList2[checkIdx]
#                                 previous_allSum = previous['allSum']
#                                 previous_rank = previous['rank']

#                                 videoPK = j['videoPK']
#                                 userPK = j['userPK']
#                                 nickName = j['nickName']
#                                 profileIMG_path = j['profileIMG_path']
#                                 donation = j['donation']
#                                 likeCount = j['likeCount']
#                                 comentCount = j['comentCount']
#                                 viewCount = j['viewCount']
#                                 allSum = j['allSum']


#                                 if int(allSum) == int(previous_allSum):
#                                     rank = int(previous_rank)
#                                 else:
#                                     rankCount = len(aggregatingList2)
#                                     rank = rankCount + 1

#                                 dictinfo = {
#                                     'videoPK':str(videoPK), 
#                                     'userPK':userPK, 
#                                     'nickName':nickName,
#                                     'profileIMG_path':profileIMG_path,
#                                     'donation':donation,
#                                     'likeCount':likeCount,
#                                     'comentCount':comentCount,
#                                     'viewCount':viewCount,
#                                     'allSum':allSum,
#                                     'rank': int(rank),
#                                 }
#                                 aggregatingList2.append(dictinfo)


#                         aggregatingList2 = sorted(aggregatingList2, key=lambda x: x['rank'], reverse=True)




#                         text = "\033[92m"+"aggregatingList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                         print("["+str(datetime.now())+"] " + text)
#                         context = {'code':'1', 'aggregatingList':aggregatingList2}
#                         return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"aggregatingList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))




# 오디션 예선 집계중 페이지
@csrf_exempt
def audition_aggregatingList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
                            profileIMG_path = s3PATH+profileIMG_path
                        else:
                            profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                        userLikeCheck = ""

                        donation = 0
                        likeCount = 0
                        comentCount = 0
                        viewCount = 0

                        # Audition_Countinfo_count = Audition_Count.objects.filter(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus).count()
                        # if Audition_Countinfo_count == 0:
                        #     Audition_CountSubmit = Audition_Count(ownerPK = userPK, videoPK = videoPK)
                        #     Audition_CountSubmit.save()
                        # else:
                        Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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


# # 32강부터는 여기서
# @csrf_exempt
# def audition_matchesList(request):
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
#             auditionListPK = data['auditionListPK']
#             categoryListPK = data['categoryListPK']
#             tournamentStatus = data['tournamentStatus']

#             versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
#             if versusListinfoCount == 0:
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
#                 versusListinfoList = []
                
#                 for index, i in enumerate(versusListinfo):
#                     userPK_left = i.userPK_left
#                     userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
#                     userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
#                     userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
#                     userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
#                     userPK_left_userNick = userPK_left_userinfo.nickName
#                     userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
#                     if userPK_left_profileIMG_path:
#                         userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
#                     else:
#                         userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     LLS = i.LLS
#                     LVS = i.LVS
#                     LDS = i.LDS
#                     LCS = i.LCS
#                     LAS = i.LAS


                    
#                     userPK_right = i.userPK_right
#                     userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
#                     userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
#                     userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
#                     userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
#                     userPK_right_userNick = userPK_right_userinfo.nickName
#                     userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
#                     if userPK_right_profileIMG_path:
#                         userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
#                     else:
#                         userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     RLS = i.RLS
#                     RCS = i.RCS
#                     RVS = i.RVS
#                     RDS = i.RDS
#                     RAS = i.RAS

#                     # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
#                     # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

#                     # 작업완료되면 위에걸로 다시 바꿔야함 gogo
#                     audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "26")
#                     audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "26")

#                     videoPK_left = str(audition_videoinfo_left.id)
#                     videoPK_right = str(audition_videoinfo_right.id)
#                     thumbnailPATH_left = ""
#                     thumbnailPATH_right = ""
#                     if tournamentStatus == "6":
                        
#                         thumbnailPATH_left = audition_videoinfo_left.thumbnailPATH
#                         thumbnailPATH_left = s3PATH+thumbnailPATH_left

                        
#                         thumbnailPATH_right = audition_videoinfo_right.thumbnailPATH
#                         thumbnailPATH_right = s3PATH+thumbnailPATH_right

#                     dictinfo = {
#                         'left': {
#                             'userPK_left':userPK_left,
#                             'videoPK_left':videoPK_left,
#                             'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
#                             'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
#                             'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
#                             'userPK_left_userNick':userPK_left_userNick,
#                             'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
#                             'thumbnailPATH_left':thumbnailPATH_left,
#                             'LLS': LLS,
#                             'LVS': LVS,
#                             'LDS': LDS,
#                             'LCS': LCS,
#                             'LAS': LAS
#                         },
#                         'right': {
#                             'userPK_right':userPK_right,
#                             'videoPK_right':videoPK_right,
#                             'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
#                             'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
#                             'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
#                             'userPK_right_userNick':userPK_right_userNick,
#                             'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
#                             'thumbnailPATH_right':thumbnailPATH_right,
#                             'RLS': RLS,
#                             'RCS': RCS,
#                             'RVS': RVS,
#                             'RDS': RDS,
#                             'RAS': RAS
#                         },
#                         'sum': int(LAS) + int(RAS)
#                     }
#                     versusListinfoList.append(dictinfo)
#                 # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)
#                 text = "\033[92m"+"audition_matchesList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'versusListinfoList':versusListinfoList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             categoryListPK = data['categoryListPK']
#             tournamentStatus = data['tournamentStatus']

#             versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
#             if versusListinfoCount == 0:
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
#                 versusListinfoList = []
                
#                 for index, i in enumerate(versusListinfo):
#                     userPK_left = i.userPK_left
#                     userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
#                     userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
#                     userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
#                     userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
#                     userPK_left_userNick = userPK_left_userinfo.nickName
#                     userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
#                     if userPK_left_profileIMG_path:
#                         userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
#                     else:
#                         userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     LLS = i.LLS
#                     LVS = i.LVS
#                     LDS = i.LDS
#                     LCS = i.LCS
#                     LAS = i.LAS


                    
#                     userPK_right = i.userPK_right
#                     userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
#                     userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
#                     userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
#                     userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
#                     userPK_right_userNick = userPK_right_userinfo.nickName
#                     userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
#                     if userPK_right_profileIMG_path:
#                         userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
#                     else:
#                         userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     RLS = i.RLS
#                     RCS = i.RCS
#                     RVS = i.RVS
#                     RDS = i.RDS
#                     RAS = i.RAS

#                     # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
#                     # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

#                     # 작업완료되면 위에걸로 다시 바꿔야함 gogo
#                     audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "20")
#                     audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "20")

#                     videoPK_left = str(audition_videoinfo_left.id)
#                     videoPK_right = str(audition_videoinfo_right.id)
#                     thumbnailPATH_left = ""
#                     thumbnailPATH_right = ""
#                     if tournamentStatus == "6":
                        
#                         thumbnailPATH_left = audition_videoinfo_left.thumbnailPATH
#                         thumbnailPATH_left = s3PATH+thumbnailPATH_left

                        
#                         thumbnailPATH_right = audition_videoinfo_right.thumbnailPATH
#                         thumbnailPATH_right = s3PATH+thumbnailPATH_right

#                     dictinfo = {
#                         'left': {
#                             'userPK_left':userPK_left,
#                             'videoPK_left':videoPK_left,
#                             'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
#                             'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
#                             'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
#                             'userPK_left_userNick':userPK_left_userNick,
#                             'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
#                             'thumbnailPATH_left':thumbnailPATH_left,
#                             'LLS': LLS,
#                             'LVS': LVS,
#                             'LDS': LDS,
#                             'LCS': LCS,
#                             'LAS': LAS
#                         },
#                         'right': {
#                             'userPK_right':userPK_right,
#                             'videoPK_right':videoPK_right,
#                             'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
#                             'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
#                             'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
#                             'userPK_right_userNick':userPK_right_userNick,
#                             'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
#                             'thumbnailPATH_right':thumbnailPATH_right,
#                             'RLS': RLS,
#                             'RCS': RCS,
#                             'RVS': RVS,
#                             'RDS': RDS,
#                             'RAS': RAS
#                         },
#                         'sum': int(LAS) + int(RAS)
#                     }
#                     versusListinfoList.append(dictinfo)
#                 # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)
#                 text = "\033[92m"+"audition_matchesList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'versusListinfoList':versusListinfoList}
#                 return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_matchesList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 32강부터는 여기서
@csrf_exempt
def audition_matchesList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
                # print(i)
                userPK_left = i.userPK_left
                

                # userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                # userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                # userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                
                userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                userPK_left_userNick = userPK_left_userinfo.nickName
                userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                if userPK_left_profileIMG_path:
                    userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                else:
                    userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                audition_Count_left = Audition_Count.objects.get(ownerPK = userPK_left, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                LLS = audition_Count_left.like
                LVS = audition_Count_left.viewcount
                LDS = audition_Count_left.donation
                LCS = audition_Count_left.coment
                LAS = (int(LLS) * 25) + (int(LVS) * 15) + (int(LDS) * 50) + (int(LCS) * 10)


                
                userPK_right = i.userPK_right
                # userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                # userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                # userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                userPK_right_userNick = userPK_right_userinfo.nickName
                userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                if userPK_right_profileIMG_path:
                    userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                else:
                    userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                audition_Count_right = Audition_Count.objects.get(ownerPK = userPK_right, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                RLS = audition_Count_right.like
                RCS = audition_Count_right.coment
                RVS = audition_Count_right.viewcount
                RDS = audition_Count_right.donation
                RAS = (int(RLS) * 25) + (int(RVS) * 15) + (int(RDS) * 50) + (int(RCS) * 10)

                audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
                audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

                # 작업완료되면 위에걸로 다시 바꿔야함 gogo
                # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "26")
                # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "26")

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
                        # 'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                        # 'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                        # 'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
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
                        # 'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                        # 'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                        # 'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
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







# # 매치 리스트 영상 상세보기 
# @csrf_exempt
# def audition_matchesListDetail(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK)
#             ownerPK = videoinfo.userPK
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = ownerPK)
#             username = userinfo.username
#             nickName = userinfo.nickName

#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3PATH+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             videoPATH = videoinfo.videoPATH
#             s3Check = S3Check.objects.get(id = 1)
#             s3Status = s3Check.status


#             if s3Status == "0":
#                 videoPATH = serverURL+"/static/video"+videoPATH
#             elif s3Status == "1":
#                 videoPATH = s3PATH+videoPATH
            
#             # 작업완료되면 위에걸로 다시 바꿔야함 gogo
#             # videoPATH = serverURL+"/static/audition_video"+videoPATH

#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag


#             audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#             likeCount = str(audition_like_video_infoCount)

#             audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_like_video_infoCount_user == 0:
#                 userLikeCheck = "0"
#             else:
#                 audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                 status = audition_like_video_info_user.status
#                 if status == "0":
#                     userLikeCheck = "0"
#                 elif status == "1":
#                     userLikeCheck = "1"

#             viewCountCheck = ""
#             viewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if viewCount_infoCount == 0:
#                 viewCountCheck = "0"
#             else:
#                 viewCountCheck = "1"


#             audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#             comentCount = str(audition_coment_infoCount)


#             videoinfo = {
#                 'ownerPK':ownerPK,
#                 'videoPK':videoPK,
#                 'nickName':nickName,
#                 'profileIMG_path':profileIMG_path,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'videoPATH':videoPATH,
#                 'userLikeCheck':userLikeCheck,
#                 'likeCount':likeCount,
#                 'comentCount':comentCount,
#                 'viewCountCheck':viewCountCheck
#             }

#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfo':videoinfo}
#             return HttpResponse(json.dumps(context))


#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK)
#             ownerPK = videoinfo.userPK
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = ownerPK)
#             username = userinfo.username
#             nickName = userinfo.nickName

#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3PATH+profileIMG_path
#             else:
#                 profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#             videoPATH = videoinfo.videoPATH
#             s3Check = S3Check.objects.get(id = 1)
#             s3Status = s3Check.status


#             if s3Status == "0":
#                 videoPATH = serverURL+"/static/video"+videoPATH
#             elif s3Status == "1":
#                 videoPATH = s3PATH+videoPATH
            
#             # 작업완료되면 위에걸로 다시 바꿔야함 gogo
#             # videoPATH = serverURL+"/static/audition_video"+videoPATH

#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag


#             audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
#             likeCount = str(audition_like_video_infoCount)

#             audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_like_video_infoCount_user == 0:
#                 userLikeCheck = "0"
#             else:
#                 audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                 status = audition_like_video_info_user.status
#                 if status == "0":
#                     userLikeCheck = "0"
#                 elif status == "1":
#                     userLikeCheck = "1"




#             audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
#             comentCount = str(audition_coment_infoCount)


#             videoinfo = {
#                 'ownerPK':ownerPK,
#                 'videoPK':videoPK,
#                 'nickName':nickName,
#                 'profileIMG_path':profileIMG_path,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'videoPATH':videoPATH,
#                 'userLikeCheck':userLikeCheck,
#                 'likeCount':likeCount,
#                 'comentCount':comentCount
#             }

#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfo':videoinfo}
#             return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_matchesListDetail Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))




# 매치 리스트 영상 상세보기 
@csrf_exempt
def audition_matchesListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        
        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']
    
        videoinfo = Audition_video.objects.get(id = videoPK)
        videoTournmentStatus = videoinfo.tournamentStatus
        if videoTournmentStatus == "7":
            print("우승자")
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
                profileIMG_path = s3PATH+profileIMG_path
            else:
                profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

            videoPATH = videoinfo.videoPATH
            s3Check = S3Check.objects.get(id = 1)
            s3Status = s3Check.status


            if s3Status == "0":
                videoPATH = serverURL+"/static/video"+videoPATH
            elif s3Status == "1":
                videoPATH = s3PATH+videoPATH
            
            contents = videoinfo.contents
            hashTag = videoinfo.hashTag

            likeCount = 0
            comentCount = 0
            audition_CountinfoCount = Audition_Count.objects.filter(videoPK = videoPK, auditionListPK = auditionListPK).count()
            if audition_CountinfoCount == 0:
                likeCount = 0
                comentCount = 0
            else:
                audition_Countinfo = Audition_Count.objects.filter(videoPK = videoPK, auditionListPK = auditionListPK)
                for index, i in enumerate(audition_Countinfo):
                    likeCount += int(i.like)
                    comentCount += int(i.coment)
                



            audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK, status = "1").count()
            if audition_like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK, status = "1")
                status = audition_like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"

            viewCountCheck = ""
            viewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"


            videoinfo = {
                'ownerPK':ownerPK,
                'videoPK':videoPK,
                'nickName':nickName,
                'profileIMG_path':profileIMG_path,
                'contents':contents,
                'hashTag':hashTag,
                'videoPATH':videoPATH,
                'userLikeCheck':userLikeCheck,
                'likeCount':str(likeCount),
                'comentCount':str(comentCount),
                'viewCountCheck':viewCountCheck
            }
                
            text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfo':videoinfo}
            return HttpResponse(json.dumps(context))
        else:
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
                profileIMG_path = s3PATH+profileIMG_path
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

            # audition_Countinfo = Audition_Count.objects.filter()

            # audition_like_video_infoCount = Audition_Like_video.objects.filter(videoPK = videoPK, status = "1").count()
            # likeCount = str(audition_like_video_infoCount)

            # audition_coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK).count()
            # comentCount = str(audition_coment_infoCount)
            print("videoPK >>", videoPK)
            print("auditionListPK >>", auditionListPK)
            print("tournamentStatus >>", tournamentStatus)

            audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
            likeCount = audition_Countinfo.like
            comentCount = audition_Countinfo.coment



            audition_like_video_infoCount_user = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus).count()
            if audition_like_video_infoCount_user == 0:
                userLikeCheck = "0"
            else:
                audition_like_video_info_user = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus)
                status = audition_like_video_info_user.status
                if status == "0":
                    userLikeCheck = "0"
                elif status == "1":
                    userLikeCheck = "1"

            viewCountCheck = ""
            viewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus).count()
            if viewCount_infoCount == 0:
                viewCountCheck = "0"
            else:
                viewCountCheck = "1"





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
                'comentCount':comentCount,
                'viewCountCheck':viewCountCheck
            }

            # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
            text = "\033[92m"+"audition_matchesListDetail SUCCESS -> 매치 리스트 영상 상세보기 Response"+"\033[0m"
            print("["+str(datetime.now())+"] " + text)
            context = {'code':'1', 'videoinfo':videoinfo}
            return HttpResponse(json.dumps(context))


    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_matchesListDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




















# # 이전 대진 내역
# @csrf_exempt
# def audition_previousMatcheslist(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         deviceVer = "1.2.9"
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if deviceVer == aosVer or deviceVer == iosVer:

#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             categoryListPK = data['categoryListPK']
#             tournamentStatus = data['tournamentStatus']

#             versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
#             if versusListinfoCount == 0:
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
#                 versusListinfoList = []
                
#                 for index, i in enumerate(versusListinfo):
#                     userPK_left = i.userPK_left
#                     userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
#                     userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
#                     userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
#                     userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
#                     userPK_left_userNick = userPK_left_userinfo.nickName
#                     userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
#                     if userPK_left_profileIMG_path:
#                         userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
#                     else:
#                         userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     LLS = i.LLS
#                     LVS = i.LVS
#                     LDS = i.LDS
#                     LCS = i.LCS
#                     LAS = i.LAS
                    
#                     userPK_right = i.userPK_right
#                     userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
#                     userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
#                     userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
#                     userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
#                     userPK_right_userNick = userPK_right_userinfo.nickName
#                     userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
#                     if userPK_right_profileIMG_path:
#                         userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
#                     else:
#                         userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     RLS = i.RLS
#                     RCS = i.RCS
#                     RVS = i.RVS
#                     RDS = i.RDS
#                     RAS = i.RAS

#                     audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
#                     audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

#                     # 작업완료되면 위에걸로 다시 바꿔야함 gogo
#                     # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "26")
#                     # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "26")

#                     videoPK_left = str(audition_videoinfo_left.id)
#                     videoPK_right = str(audition_videoinfo_right.id)

                    
#                     dictinfo = {
#                         'left': {
#                             'userPK_left':userPK_left,
#                             'videoPK_left':videoPK_left,
#                             'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
#                             'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
#                             'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
#                             'userPK_left_userNick':userPK_left_userNick,
#                             'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
#                             'LLS': LLS,
#                             'LVS': LVS,
#                             'LDS': LDS,
#                             'LCS': LCS,
#                             'LAS': LAS
#                         },
#                         'right': {
#                             'userPK_right':userPK_right,
#                             'videoPK_right':videoPK_right,
#                             'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
#                             'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
#                             'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
#                             'userPK_right_userNick':userPK_right_userNick,
#                             'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
#                             'RLS': RLS,
#                             'RCS': RCS,
#                             'RVS': RVS,
#                             'RDS': RDS,
#                             'RAS': RAS
#                         },
#                         'sum': int(LAS) + int(RAS)
#                     }
#                     versusListinfoList.append(dictinfo)          
#                 # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)

#                 text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'versusListinfoList':versusListinfoList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             page = int(data['page'])
#             pageStart = (page - 1) * 10
#             pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']
#             auditionListPK = data['auditionListPK']
#             categoryListPK = data['categoryListPK']
#             tournamentStatus = data['tournamentStatus']

#             versusListinfoCount = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus).count()
#             if versusListinfoCount == 0:
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryListPK, tournamentStatus = tournamentStatus)
#                 versusListinfoList = []
                
#                 for index, i in enumerate(versusListinfo):
#                     userPK_left = i.userPK_left
#                     userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
#                     userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
#                     userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
#                     userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
#                     userPK_left_userNick = userPK_left_userinfo.nickName
#                     userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
#                     if userPK_left_profileIMG_path:
#                         userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
#                     else:
#                         userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     LLS = i.LLS
#                     LVS = i.LVS
#                     LDS = i.LDS
#                     LCS = i.LCS
#                     LAS = i.LAS
                    
#                     userPK_right = i.userPK_right
#                     userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
#                     userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
#                     userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
#                     userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
#                     userPK_right_userNick = userPK_right_userinfo.nickName
#                     userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
#                     if userPK_right_profileIMG_path:
#                         userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
#                     else:
#                         userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     RLS = i.RLS
#                     RCS = i.RCS
#                     RVS = i.RVS
#                     RDS = i.RDS
#                     RAS = i.RAS


#                     dictinfo = {
#                         'left': {
#                             'userPK_left':userPK_left,
#                             'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
#                             'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
#                             'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
#                             'userPK_left_userNick':userPK_left_userNick,
#                             'userPK_left_profileIMG_path':userPK_left_profileIMG_path,
#                             'LLS': LLS,
#                             'LVS': LVS,
#                             'LDS': LDS,
#                             'LCS': LCS,
#                             'LAS': LAS
#                         },
#                         'right': {
#                             'userPK_right':userPK_right,
#                             'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
#                             'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
#                             'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
#                             'userPK_right_userNick':userPK_right_userNick,
#                             'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
#                             'RLS': RLS,
#                             'RCS': RCS,
#                             'RVS': RVS,
#                             'RDS': RDS,
#                             'RAS': RAS
#                         },
#                         'sum': int(LAS) + int(RAS)
#                     }
#                     versusListinfoList.append(dictinfo)          
#                 # versusListinfoList = sorted(versusListinfoList, key=lambda x: x['sum'], reverse=True)

#                 text = "\033[92m"+"audition_videoList SUCCESS -> 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'versusListinfoList':versusListinfoList}
#                 return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_videoList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 이전 대진 내역
@csrf_exempt
def audition_previousMatcheslist(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
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
                # userPK_left_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_left, status = "1").count()
                # userPK_left_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_left).count()
                # userPK_left_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_left).count()
                userPK_left_userinfo = SignUp.objects.get(id = userPK_left)
                userPK_left_userNick = userPK_left_userinfo.nickName
                userPK_left_profileIMG_path = userPK_left_userinfo.profileIMG_path
                if userPK_left_profileIMG_path:
                    userPK_left_profileIMG_path = s3PATH+userPK_left_profileIMG_path
                else:
                    userPK_left_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                audition_Count_left = Audition_Count.objects.get(ownerPK = userPK_left, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                LLS = audition_Count_left.like
                LVS = audition_Count_left.viewcount
                LDS = audition_Count_left.donation
                LCS = audition_Count_left.coment
                # LAS = int(LLS) + int(LVS) + int(LDS) + int(LCS)
                LAS = (int(LLS) * 25) + (int(LVS) * 15) + (int(LDS) * 50) + (int(LCS) * 10)

                # LLS = i.LLS
                # LVS = i.LVS
                # LDS = i.LDS
                # LCS = i.LCS
                # LAS = i.LAS
                
                userPK_right = i.userPK_right
                # userPK_right_audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = userPK_right, status = "1").count()
                # userPK_right_audition_coment_infoCount = Audition_Coment.objects.filter(userPK = userPK_right).count()
                # userPK_right_audition_viewcount_infoCount = Audition_ViewCount.objects.filter(userPK = userPK_right).count()
                userPK_right_userinfo = SignUp.objects.get(id = userPK_right)
                userPK_right_userNick = userPK_right_userinfo.nickName
                userPK_right_profileIMG_path = userPK_right_userinfo.profileIMG_path
                if userPK_right_profileIMG_path:
                    userPK_right_profileIMG_path = s3PATH+userPK_right_profileIMG_path
                else:
                    userPK_right_profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

                audition_Count_right = Audition_Count.objects.get(ownerPK = userPK_right, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
                RLS = audition_Count_right.like
                RCS = audition_Count_right.coment
                RVS = audition_Count_right.viewcount
                RDS = audition_Count_right.donation
                # RAS = int(RLS) + int(RVS) + int(RDS) + int(RCS)
                RAS = (int(RLS) * 25) + (int(RVS) * 15) + (int(RDS) * 50) + (int(RCS) * 10)

                # RLS = i.RLS
                # RCS = i.RCS
                # RVS = i.RVS
                # RDS = i.RDS
                # RAS = i.RAS

                audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = auditionListPK)
                audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = auditionListPK)

                # 작업완료되면 위에걸로 다시 바꿔야함 gogo
                # audition_videoinfo_left = Audition_video.objects.get(userPK = userPK_left, auditionListPK = "26")
                # audition_videoinfo_right = Audition_video.objects.get(userPK = userPK_right, auditionListPK = "26")

                videoPK_left = str(audition_videoinfo_left.id)
                videoPK_right = str(audition_videoinfo_right.id)

                
                dictinfo = {
                    'left': {
                        'userPK_left':userPK_left,
                        'videoPK_left':videoPK_left,
                        # 'userPK_left_audition_like_video_infoCount':userPK_left_audition_like_video_infoCount,
                        # 'userPK_left_audition_coment_infoCount':userPK_left_audition_coment_infoCount,
                        # 'userPK_left_audition_viewcount_infoCount':userPK_left_audition_viewcount_infoCount,
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
                        'videoPK_right':videoPK_right,
                        # 'userPK_right_audition_like_video_infoCount':userPK_right_audition_like_video_infoCount,
                        # 'userPK_right_audition_coment_infoCount':userPK_right_audition_coment_infoCount,
                        # 'userPK_right_audition_viewcount_infoCount':userPK_right_audition_viewcount_infoCount,
                        'userPK_right_userNick':userPK_right_userNick,
                        'userPK_right_profileIMG_path':userPK_right_profileIMG_path,
                        'RLS': RLS,
                        'RCS': RCS,
                        'RVS': RVS,
                        'RDS': RDS,
                        'RAS': RAS
                    },
                    # 'sum': int(LAS) + int(RAS)
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
    

# # 오디션 영상 조회수
# @csrf_exempt
# def audition_videoViewCount(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             # auditionListPK = data['auditionListPK']
#             # tournamentStatus = data['tournamentStatus']
#             # categoryPK = data['categoryPK']

#             auditionViewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if auditionViewCount_infoCount == 0:
#                 auditionViewCount_info = Audition_ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 auditionViewCount_info.save()
#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 Audition_Countinfo.viewcount = str(int(Audition_Countinfo.viewcount) + 1)
#                 Audition_Countinfo.save()

#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LLS = str(int(i.LLS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RLS = str(int(i.RLS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
#                 ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
#                 ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))

#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             # auditionListPK = data['auditionListPK']
#             # tournamentStatus = data['tournamentStatus']
#             # categoryPK = data['categoryPK']

#             auditionViewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if auditionViewCount_infoCount == 0:
#                 auditionViewCount_info = Audition_ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())))
#                 auditionViewCount_info.save()
#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 Audition_Countinfo.viewcount = str(int(Audition_Countinfo.viewcount) + 1)
#                 Audition_Countinfo.save()

#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LLS = str(int(i.LLS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RLS = str(int(i.RLS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 영상조회 완료"
#                 ment = "\033[92m"+"videoViewCount SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 이미 봤던 영상"
#                 ment = "\033[93m"+"videoViewCount WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'0'}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    

# 오디션 영상 조회수
@csrf_exempt
def audition_videoViewCount(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']
        # categoryPK = data['categoryPK']

        auditionViewCount_infoCount = Audition_ViewCount.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus).count()
        if auditionViewCount_infoCount == 0:
            auditionViewCount_info = Audition_ViewCount(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), tournamentStatus = tournamentStatus)
            auditionViewCount_info.save()
            auditionVideoinfo = Audition_video.objects.get(id = videoPK)
            videoOwner_userPK = auditionVideoinfo.userPK

            Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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


# # 오디션 영상 좋아요
# @csrf_exempt
# def audition_videoLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         deviceVer = "1.2.9"
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if deviceVer == aosVer or deviceVer == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_like_video_infoCount == 0:
#                 like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 like_video_info.save()
#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK


#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
#                 Audition_Countinfo.save()

#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LLS = str(int(i.LLS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RLS = str(int(i.RLS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
#                 ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                 status = audition_like_video_info.status
#                 if status == "0":
#                     audition_like_video_info.status = "1"
#                     audition_like_video_info.save()
#                     auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                     videoOwner_userPK = auditionVideoinfo.userPK

#                     Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                     Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
#                     Audition_Countinfo.save()
#                     # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                     # for index, i in enumerate(versusListinfo):
#                     #     userPK_left = i.userPK_left
#                     #     userPK_right = i.userPK_right
#                     #     if videoOwner_userPK == userPK_left:
#                     #         i.LLS = str(int(i.LLS) + 1)
#                     #         i.save()
#                     #     elif videoOwner_userPK == userPK_right:
#                     #         i.RLS = str(int(i.RLS) + 1)
#                     #         i.save()
#                     #     else:
#                     #         pass
#                     text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
#                     ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 else:
#                     audition_like_video_info.status = "0"
#                     audition_like_video_info.save()
                    
#                     auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                     videoOwner_userPK = auditionVideoinfo.userPK

#                     Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                     likeCount = int(Audition_Countinfo.like)
#                     if likeCount <= 0:
#                         Audition_Countinfo.like = "0"
#                         Audition_Countinfo.save()
#                     else:
#                         Audition_Countinfo.like = str(int(Audition_Countinfo.like) - 1)
#                         Audition_Countinfo.save()

#                     # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                     # for index, i in enumerate(versusListinfo):
#                     #     userPK_left = i.userPK_left
#                     #     userPK_right = i.userPK_right
#                     #     if videoOwner_userPK == userPK_left:
#                     #         i.LLS = str(int(i.LLS) - 1)
#                     #         i.save()
#                     #     elif videoOwner_userPK == userPK_right:
#                     #         i.RLS = str(int(i.RLS) - 1)
#                     #         i.save()
#                     #     else:
#                     #         pass

#                     text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
#                     ment = "\033[93m"+"audition_audition_videoLike WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))
                
#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_like_video_infoCount == 0:
#                 like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 like_video_info.save()
#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK


#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
#                 Audition_Countinfo.save()

#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LLS = str(int(i.LLS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RLS = str(int(i.RLS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 최초 좋아요 완료"
#                 ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK)
#                 status = audition_like_video_info.status
#                 if status == "0":
#                     audition_like_video_info.status = "1"
#                     audition_like_video_info.save()
#                     auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                     videoOwner_userPK = auditionVideoinfo.userPK

#                     Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                     Audition_Countinfo.like = str(int(Audition_Countinfo.like) + 1)
#                     Audition_Countinfo.save()
#                     # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                     # for index, i in enumerate(versusListinfo):
#                     #     userPK_left = i.userPK_left
#                     #     userPK_right = i.userPK_right
#                     #     if videoOwner_userPK == userPK_left:
#                     #         i.LLS = str(int(i.LLS) + 1)
#                     #         i.save()
#                     #     elif videoOwner_userPK == userPK_right:
#                     #         i.RLS = str(int(i.RLS) + 1)
#                     #         i.save()
#                     #     else:
#                     #         pass
#                     text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 완료"
#                     ment = "\033[92m"+"audition_videoLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 else:
#                     audition_like_video_info.status = "0"
#                     audition_like_video_info.save()
                    
#                     auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                     videoOwner_userPK = auditionVideoinfo.userPK

#                     Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                     likeCount = int(Audition_Countinfo.like)
#                     if likeCount <= 0:
#                         Audition_Countinfo.like = "0"
#                         Audition_Countinfo.save()
#                     else:
#                         Audition_Countinfo.like = str(int(Audition_Countinfo.like) - 1)
#                         Audition_Countinfo.save()

#                     # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                     # for index, i in enumerate(versusListinfo):
#                     #     userPK_left = i.userPK_left
#                     #     userPK_right = i.userPK_right
#                     #     if videoOwner_userPK == userPK_left:
#                     #         i.LLS = str(int(i.LLS) - 1)
#                     #         i.save()
#                     #     elif videoOwner_userPK == userPK_right:
#                     #         i.RLS = str(int(i.RLS) - 1)
#                     #         i.save()
#                     #     else:
#                     #         pass

#                     text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 좋아요 취소"
#                     ment = "\033[93m"+"audition_audition_videoLike WARNING -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_videoLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    

# 오디션 영상 좋아요
@csrf_exempt
def audition_videoLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # deviceVer = data['deviceVer']
        deviceVer = "1.2.9"
        versioninfo = Version.objects.get(id = 1)
        aosVer = versioninfo.aos
        iosVer = versioninfo.ios
        # if deviceVer == aosVer or deviceVer == iosVer:

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']
        categoryPK = data['categoryPK']

        audition_like_video_infoCount = Audition_Like_video.objects.filter(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK).count()
        if audition_like_video_infoCount == 0:
            like_video_info = Audition_Like_video(userPK = loginUserPK, videoPK = videoPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1", tournamentStatus = tournamentStatus, auditionListPK = auditionListPK)
            like_video_info.save()
            auditionVideoinfo = Audition_video.objects.get(id = videoPK)
            videoOwner_userPK = auditionVideoinfo.userPK


            Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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
            audition_like_video_info = Audition_Like_video.objects.get(userPK = loginUserPK, videoPK = videoPK, tournamentStatus = tournamentStatus, auditionListPK = auditionListPK)
            status = audition_like_video_info.status
            if status == "0":
                audition_like_video_info.status = "1"
                audition_like_video_info.save()
                auditionVideoinfo = Audition_video.objects.get(id = videoPK)
                videoOwner_userPK = auditionVideoinfo.userPK

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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

                Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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



# # 오디션 댓글 리스트
# @csrf_exempt
# def audition_comentList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']

#             audition_comentinfoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()

#             if audition_comentinfoCount == 0:
#                 text = "댓글 없음"
#                 ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'comentinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentinfo = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
#                 audition_comentinfoList = []
#                 for index, i in enumerate(audition_comentinfo):
#                     now  = int(round(time.time()))
#                     userPK = i.userPK
#                     comentPK = i.id
#                     createAt = i.createAt
#                     createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                     contents = i.contents
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     previous = ""
#                     previous_date = ""
#                     likeCount = ""
#                     userComentLikeCheck = ""
#                     comentONcomentCount = ""
#                     userComentONComentCheck = ""
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

#                     audition_like_coment_infoCount = Audition_Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
#                     likeCount =  str(audition_like_coment_infoCount)

#                     audition_like_coment_infoCount_user = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                     if audition_like_coment_infoCount_user == 0:
#                         userComentLikeCheck = "0"
#                     else:
#                         audition_Like_coment_info_user = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
#                         status = audition_Like_coment_info_user.status
#                         if status == "0":
#                             userComentLikeCheck = "0"
#                         elif status == "1":
#                             userComentLikeCheck = "1"


#                     audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK).count()
#                     comentONcomentCount = str(audition_comentOnComent_infoCount)

#                     audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                     if audition_comentOnComent_infoCount_user == 0:
#                         userComentONComentCheck = "0"
#                     else:
#                         userComentONComentCheck = "1"

#                     audition_comentDict = {
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
#                         'comentONcomentLen':comentONcomentCount,
#                         'userComentLikeCheck':userComentLikeCheck,
#                         'userComentONComentCheck':userComentONComentCheck

#                     }
#                     audition_comentinfoList.append(audition_comentDict)

#                 text = "\033[92m"+"audition_comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_comentinfoList':audition_comentinfoList}
#                 return HttpResponse(json.dumps(context))
#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']

#             audition_comentinfoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()

#             if audition_comentinfoCount == 0:
#                 text = "댓글 없음"
#                 ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'comentinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentinfo = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
#                 audition_comentinfoList = []
#                 for index, i in enumerate(audition_comentinfo):
#                     now  = int(round(time.time()))
#                     userPK = i.userPK
#                     comentPK = i.id
#                     createAt = i.createAt
#                     createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                     contents = i.contents
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                     previous = ""
#                     previous_date = ""
#                     likeCount = ""
#                     userComentLikeCheck = ""
#                     comentONcomentCount = ""
#                     userComentONComentCheck = ""
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

#                     audition_like_coment_infoCount = Audition_Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
#                     likeCount =  str(audition_like_coment_infoCount)

#                     audition_like_coment_infoCount_user = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                     if audition_like_coment_infoCount_user == 0:
#                         userComentLikeCheck = "0"
#                     else:
#                         audition_Like_coment_info_user = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
#                         status = audition_Like_coment_info_user.status
#                         if status == "0":
#                             userComentLikeCheck = "0"
#                         elif status == "1":
#                             userComentLikeCheck = "1"


#                     audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK).count()
#                     comentONcomentCount = str(audition_comentOnComent_infoCount)

#                     audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                     if audition_comentOnComent_infoCount_user == 0:
#                         userComentONComentCheck = "0"
#                     else:
#                         userComentONComentCheck = "1"

#                     audition_comentDict = {
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
#                         'comentONcomentLen':comentONcomentCount,
#                         'userComentLikeCheck':userComentLikeCheck,
#                         'userComentONComentCheck':userComentONComentCheck

#                     }
#                     audition_comentinfoList.append(audition_comentDict)

#                 text = "\033[92m"+"audition_comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'audition_comentinfoList':audition_comentinfoList}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99', 'comentinfoList':None}
#         return HttpResponse(json.dumps(context))
    



# # 오디션 댓글 리스트
# @csrf_exempt
# def audition_comentList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         loginUserPK = data['loginUserPK']
#         videoPK = data['videoPK']

#         audition_comentinfoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()

#         if audition_comentinfoCount == 0:
#             text = "댓글 없음"
#             ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#             context = {'code':'0', 'comentinfoList':None}
#             return HttpResponse(json.dumps(context))
#         else:
#             audition_comentinfo = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").order_by('-id')
#             audition_comentinfoList = []
#             for index, i in enumerate(audition_comentinfo):
#                 now  = int(round(time.time()))
#                 userPK = i.userPK
#                 comentPK = i.id
#                 createAt = i.createAt
#                 createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                 contents = i.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"
#                 previous = ""
#                 previous_date = ""
#                 likeCount = ""
#                 userComentLikeCheck = ""
#                 comentONcomentCount = ""
#                 userComentONComentCheck = ""
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)

#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'


#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 audition_like_coment_infoCount = Audition_Like_coment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1").count()
#                 likeCount =  str(audition_like_coment_infoCount)

#                 audition_like_coment_infoCount_user = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                 if audition_like_coment_infoCount_user == 0:
#                     userComentLikeCheck = "0"
#                 else:
#                     audition_Like_coment_info_user = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)
#                     status = audition_Like_coment_info_user.status
#                     if status == "0":
#                         userComentLikeCheck = "0"
#                     elif status == "1":
#                         userComentLikeCheck = "1"


#                 audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK).count()
#                 comentONcomentCount = str(audition_comentOnComent_infoCount)

#                 audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
#                 if audition_comentOnComent_infoCount_user == 0:
#                     userComentONComentCheck = "0"
#                 else:
#                     userComentONComentCheck = "1"

#                 audition_comentDict = {
#                     'comentPK':comentPK,
#                     'videoPK':videoPK,
#                     'userPK':userPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'likeCount':likeCount,
#                     'comentONcomentLen':comentONcomentCount,
#                     'userComentLikeCheck':userComentLikeCheck,
#                     'userComentONComentCheck':userComentONComentCheck

#                 }
#                 audition_comentinfoList.append(audition_comentDict)

#             text = "\033[92m"+"audition_comentList SUCCESS -> 댓글 리스트 Response "+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'audition_comentinfoList':audition_comentinfoList}
#             return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99', 'comentinfoList':None}
#         return HttpResponse(json.dumps(context))
    


# # 오디션 댓글 저장 ( 작품당 1회 카운트 )
# @csrf_exempt
# def audition_comentSubmit(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             contents = data['contents']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             audition_comentinfoCount = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_comentinfoCount == 0:

#                 audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#                 audition_comentSubmit.save()

#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK
#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LCS = str(int(i.LCS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RCS = str(int(i.RCS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass
                        
#                 comentPK = audition_comentSubmit.id
#                 comentinfo = Audition_Coment.objects.get(id = comentPK)
#                 userPK = comentinfo.userPK
#                 videoPK = comentinfo.videoPK
#                 contents = comentinfo.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 name = userinfo.name
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 previous = ""
#                 previous_date = ""
#                 userComentLikeCheck = ""
#                 userComentONComentCheck = ""
#                 now  = int(round(time.time()))
#                 createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)

#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'
#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 # comentCount = Coment.objects.filter(videoPK = videoPK).count()

#                 coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount

#                 print("videoPK >>", videoPK)
#                 print("videoPK >>", auditionListPK)
#                 print("videoPK >>", tournamentStatus)

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
#                 Audition_Countinfo.coment = str(int(Audition_Countinfo.coment) + 1)
#                 Audition_Countinfo.save()

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
#                 comentCount = int(Audition_Countinfo.coment)
                
#                 # if coment_infoCount == 0:
#                 #     pass
#                 # else:
#                 #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
#                 #     for index, k in enumerate(coment_info):
#                 #         userPK_coment = k.userPK
#                 #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                 #         if userBlockListinfoCount_coment == 1:
#                 #             comentCount -= 1


#                 coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 userComentCheck = ""
#                 if coment_infoCount_user == 0:
#                     userComentCheck = "0"
#                 else:
#                     userComentCheck = "1"

#                 comentinfo = {
#                     'videoOwner_userPK':videoOwner_userPK,
#                     'comentPK':str(comentPK),
#                     'videoPK':videoPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'name':name,
#                     'profileIMG_path':profileIMG_path,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'comentCount':str(comentCount),
#                     'userComentCheck':userComentCheck
#                 }

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
#                 ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#                 audition_comentSubmit.save()

#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK

#                 comentPK = audition_comentSubmit.id
#                 comentinfo = Audition_Coment.objects.get(id = comentPK)
#                 userPK = comentinfo.userPK
#                 videoPK = comentinfo.videoPK
#                 contents = comentinfo.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 name = userinfo.name
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 previous = ""
#                 previous_date = ""
#                 userComentLikeCheck = ""
#                 userComentONComentCheck = ""
#                 now  = int(round(time.time()))
#                 createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)

#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'
#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 # comentCount = Coment.objects.filter(videoPK = videoPK).count()

#                 # coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = coment_infoCount

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 comentCount = int(Audition_Countinfo.coment)

#                 # if coment_infoCount == 0:
#                 #     pass
#                 # else:
#                 #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
#                 #     for index, k in enumerate(coment_info):
#                 #         userPK_coment = k.userPK
#                 #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                 #         if userBlockListinfoCount_coment == 1:
#                 #             comentCount -= 1


#                 coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 userComentCheck = ""
#                 if coment_infoCount_user == 0:
#                     userComentCheck = "0"
#                 else:
#                     userComentCheck = "1"

#                 comentinfo = {
#                     'videoOwner_userPK':videoOwner_userPK,
#                     'comentPK':str(comentPK),
#                     'videoPK':videoPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'name':name,
#                     'profileIMG_path':profileIMG_path,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'comentCount':str(comentCount),
#                     'userComentCheck':userComentCheck
#                 }

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
#                 ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))  
                      
#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
#             contents = data['contents']
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             audition_comentinfoCount = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#             if audition_comentinfoCount == 0:

#                 audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#                 audition_comentSubmit.save()

#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK
#                 # versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#                 # for index, i in enumerate(versusListinfo):
#                 #     userPK_left = i.userPK_left
#                 #     userPK_right = i.userPK_right
#                 #     if videoOwner_userPK == userPK_left:
#                 #         i.LCS = str(int(i.LCS) + 1)
#                 #         i.save()
#                 #     elif videoOwner_userPK == userPK_right:
#                 #         i.RCS = str(int(i.RCS) + 1)
#                 #         i.save()
#                 #     else:
#                 #         pass
                        
#                 comentPK = audition_comentSubmit.id
#                 comentinfo = Audition_Coment.objects.get(id = comentPK)
#                 userPK = comentinfo.userPK
#                 videoPK = comentinfo.videoPK
#                 contents = comentinfo.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 name = userinfo.name
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 previous = ""
#                 previous_date = ""
#                 userComentLikeCheck = ""
#                 userComentONComentCheck = ""
#                 now  = int(round(time.time()))
#                 createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)

#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'
#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 # comentCount = Coment.objects.filter(videoPK = videoPK).count()

#                 coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 comentCount = coment_infoCount

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 Audition_Countinfo.coment = str(int(Audition_Countinfo.coment) + 1)
#                 Audition_Countinfo.save()

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 comentCount = int(Audition_Countinfo.coment)
                
#                 # if coment_infoCount == 0:
#                 #     pass
#                 # else:
#                 #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
#                 #     for index, k in enumerate(coment_info):
#                 #         userPK_coment = k.userPK
#                 #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                 #         if userBlockListinfoCount_coment == 1:
#                 #             comentCount -= 1


#                 coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 userComentCheck = ""
#                 if coment_infoCount_user == 0:
#                     userComentCheck = "0"
#                 else:
#                     userComentCheck = "1"

#                 comentinfo = {
#                     'videoOwner_userPK':videoOwner_userPK,
#                     'comentPK':str(comentPK),
#                     'videoPK':videoPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'name':name,
#                     'profileIMG_path':profileIMG_path,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'comentCount':str(comentCount),
#                     'userComentCheck':userComentCheck
#                 }

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
#                 ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_comentSubmit = Audition_Coment(userPK = str(loginUserPK), videoPK = str(videoPK), createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#                 audition_comentSubmit.save()

#                 auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#                 videoOwner_userPK = auditionVideoinfo.userPK

#                 comentPK = audition_comentSubmit.id
#                 comentinfo = Audition_Coment.objects.get(id = comentPK)
#                 userPK = comentinfo.userPK
#                 videoPK = comentinfo.videoPK
#                 contents = comentinfo.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 name = userinfo.name
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                 previous = ""
#                 previous_date = ""
#                 userComentLikeCheck = ""
#                 userComentONComentCheck = ""
#                 now  = int(round(time.time()))
#                 createAt_timestamp = int(round(float(comentinfo.createAt_timestamp)))
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)

#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'
#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 # comentCount = Coment.objects.filter(videoPK = videoPK).count()

#                 # coment_infoCount = Audition_Coment.objects.filter(videoPK = videoPK, status = "0").count()
#                 # comentCount = coment_infoCount

#                 Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK)
#                 comentCount = int(Audition_Countinfo.coment)

#                 # if coment_infoCount == 0:
#                 #     pass
#                 # else:
#                 #     coment_info = Audition_Coment.objects.filter(videoPK = videoPK, status = "0")
#                 #     for index, k in enumerate(coment_info):
#                 #         userPK_coment = k.userPK
#                 #         userBlockListinfoCount_coment = UserBlockList.objects.filter(loginUserPK = loginUserPK, blockUserPK = userPK_coment, status = "1").count()
#                 #         if userBlockListinfoCount_coment == 1:
#                 #             comentCount -= 1


#                 coment_infoCount_user = Audition_Coment.objects.filter(userPK = loginUserPK, videoPK = videoPK).count()
#                 userComentCheck = ""
#                 if coment_infoCount_user == 0:
#                     userComentCheck = "0"
#                 else:
#                     userComentCheck = "1"

#                 comentinfo = {
#                     'videoOwner_userPK':videoOwner_userPK,
#                     'comentPK':str(comentPK),
#                     'videoPK':videoPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'name':name,
#                     'profileIMG_path':profileIMG_path,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'comentCount':str(comentCount),
#                     'userComentCheck':userComentCheck
#                 }

#                 text = "video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 댓글 완료"
#                 ment = "\033[92m"+"audition_comentSubmit SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))         


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentSubmit Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# 오디션 댓글 저장 ( 작품당 1회 카운트 )
@csrf_exempt
def audition_comentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
                profileIMG_path = s3PATH+profileIMG_path
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

            Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
            Audition_Countinfo.coment = str(int(Audition_Countinfo.coment) + 1)
            Audition_Countinfo.save()

            Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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
                profileIMG_path = s3PATH+profileIMG_path
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

            Audition_Countinfo = Audition_Count.objects.get(videoPK = videoPK, auditionListPK = auditionListPK, tournamentStatus = tournamentStatus)
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
    



# # 오디션 댓글 삭제
# @csrf_exempt
# def audition_ComentDel(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             comentPK = data['comentPK']
#             loginUserPK = str(data['loginUserPK'])
#             videoPK = str(data['videoPK'])
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#             videoOwner_userPK = auditionVideoinfo.userPK
#             versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#             for index, i in enumerate(versusListinfo):
#                 userPK_left = i.userPK_left
#                 userPK_right = i.userPK_right
#                 if videoOwner_userPK == userPK_left:
#                     i.LCS = str(int(i.LCS) - 1)
#                     i.save()
#                 elif videoOwner_userPK == userPK_right:
#                     i.RCS = str(int(i.RCS) - 1)
#                     i.save()
#                 else:
#                     pass

#             audition_comentinfo = Audition_Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK)
#             audition_comentinfo.status = "9"
#             audition_comentinfo.save()

#             text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", 오디션 댓글 삭제 완료"
#             ment = "\033[92m"+"comentDel SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             comentPK = data['comentPK']
#             loginUserPK = str(data['loginUserPK'])
#             videoPK = str(data['videoPK'])
#             auditionListPK = data['auditionListPK']
#             tournamentStatus = data['tournamentStatus']
#             categoryPK = data['categoryPK']

#             auditionVideoinfo = Audition_video.objects.get(id = videoPK)
#             videoOwner_userPK = auditionVideoinfo.userPK
#             versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
#             for index, i in enumerate(versusListinfo):
#                 userPK_left = i.userPK_left
#                 userPK_right = i.userPK_right
#                 if videoOwner_userPK == userPK_left:
#                     i.LCS = str(int(i.LCS) - 1)
#                     i.save()
#                 elif videoOwner_userPK == userPK_right:
#                     i.RCS = str(int(i.RCS) - 1)
#                     i.save()
#                 else:
#                     pass

#             audition_comentinfo = Audition_Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK)
#             audition_comentinfo.status = "9"
#             audition_comentinfo.save()

#             text = "coment PK값 : " + str(comentPK) + ", user PK값 : " + loginUserPK + ", 오디션 댓글 삭제 완료"
#             ment = "\033[92m"+"comentDel SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"comentDel Exception ERROR -> "+text+"\033[0m"
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
        versusListinfo = VersusList.objects.filter(auditionListPK = auditionListPK, categoryPK = categoryPK, tournamentStatus = tournamentStatus)
        for index, i in enumerate(versusListinfo):
            userPK_left = i.userPK_left
            userPK_right = i.userPK_right
            if videoOwner_userPK == userPK_left:
                i.LCS = str(int(i.LCS) - 1)
                i.save()
            elif videoOwner_userPK == userPK_right:
                i.RCS = str(int(i.RCS) - 1)
                i.save()
            else:
                pass

        audition_comentinfo = Audition_Coment.objects.get(id = int(comentPK), userPK = loginUserPK, videoPK = videoPK)
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

# # 오디션 댓글 좋아요
# @csrf_exempt
# def audition_comentLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = str(data['loginUserPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])
            
#             audition_like_coment_infoCount = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()


#             if audition_like_coment_infoCount == 0:
#                 audition_like_coment_info = Audition_Like_coment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 audition_like_coment_info.save()

#                 text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
#                 ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_coment_info = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)




#                 status = audition_like_coment_info.status
#                 if status == "0":
#                     audition_like_coment_info.status = "1"
#                     audition_like_coment_info.save()
#                     text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
#                     ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 elif status == "1":
#                     audition_like_coment_info.status = "0"
#                     audition_like_coment_info.save()
#                     text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
#                     ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))
                
#         else:
#             loginUserPK = str(data['loginUserPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])
            
#             audition_like_coment_infoCount = Audition_Like_coment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()


#             if audition_like_coment_infoCount == 0:
#                 audition_like_coment_info = Audition_Like_coment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 audition_like_coment_info.save()

#                 text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 최초 완료"
#                 ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_coment_info = Audition_Like_coment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)




#                 status = audition_like_coment_info.status
#                 if status == "0":
#                     audition_like_coment_info.status = "1"
#                     audition_like_coment_info.save()
#                     text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 완료"
#                     ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 elif status == "1":
#                     audition_like_coment_info.status = "0"
#                     audition_like_coment_info.save()
#                     text = "video PK값 : " + comentPK + ", user PK값 : " + loginUserPK + ", 댓글 좋아요 취소"
#                     ment = "\033[92m"+"audition_comentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))

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
#                         profileIMG_path = s3PATH+profileIMG_path
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
#                         profileIMG_path = s3PATH+profileIMG_path
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
    

# # 오디션 대댓글 리스트
# @csrf_exempt
# def audition_comentONcomentList(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))

#         loginUserPK = data['loginUserPK']
#         comentPK = data['comentPK']
#         videoPK = data['videoPK']
        
#         audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
#         if audition_comentOnComentinfoCount == 0:
#             text = "대댓글 없음"
#             ment = "\033[93m"+"audition_comentONcomentList WARNING -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#             context = {'code':'0', 'comentONcomentList':None}
#             return HttpResponse(json.dumps(context))
#         else:
#             audition_comentOnComentinfo = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").order_by('-id')
#             audition_comentONcomentList = []
#             for index, i in enumerate(audition_comentOnComentinfo):
#                 comentONcomentPK = i.id
#                 now  = int(round(time.time()))
#                 userPK = i.userPK
#                 createAt_timestamp = int(round(float(i.createAt_timestamp)))
#                 contents = i.contents
#                 userinfo = SignUp.objects.get(id = userPK)
#                 username = userinfo.username
#                 nickName = userinfo.nickName
#                 profileIMG_path = userinfo.profileIMG_path
#                 if profileIMG_path:
#                     profileIMG_path = s3PATH+profileIMG_path
#                 else:
#                     profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"



#                 likeCount = ""
#                 previous = ""
#                 previous_date = ""
#                 userComentONComentLikeCheck = ""
#                 me_time = math.floor(((now - createAt_timestamp) / 60))
#                 me_timehour = math.floor((me_time / 60))
#                 me_timeday = math.floor((me_timehour / 24))
#                 me_timeyear = math.floor(me_timeday / 365)


                
#                 # if me_time < 1 :
#                 #     previous = '방금전'
                    
#                 # elif me_time < 60 :
#                 #     previous = str(me_time) + '분전'

#                 # elif me_timehour < 24 :
#                 #     previous = str(me_timehour) + '시간전'
                
#                 # elif me_timeday < 365 :
#                 #     previous = str(me_timeday) + '일전'
                
#                 # elif me_timeyear >= 1 : 
#                 #     previous = str(me_timeyear) + '년전'


#                 if me_time < 1 :
#                     # previous = '방금전'
#                     previous = 'B'
#                     previous_date = "0"
                    
#                 elif me_time < 60 :
#                     # previous = str(me_time) + '분전'
#                     previous = 'M'
#                     previous_date = str(me_time)

#                 elif me_timehour < 24 :
#                     # previous = str(me_timehour) + '시간전'
#                     previous = 'H'
#                     previous_date = str(me_timehour)
                
#                 elif me_timeday < 365 :
#                     # previous = str(me_timeday) + '일전'
#                     previous = 'D'
#                     previous_date = str(me_timeday)

#                 elif me_timeyear >= 1 : 
#                     # previous = str(me_timeyear) + '년전'
#                     previous = 'Y'
#                     previous_date = str(me_timeyear)

#                 audition_like_comentONcoment_infoCount = Audition_Like_comentONcoment.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "1", comentONcomentPK = comentONcomentPK).count()
#                 likeCount = str(audition_like_comentONcoment_infoCount)

#                 audition_like_comentONcoment_infoCount_user = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
#                 if audition_like_comentONcoment_infoCount_user == 0:
#                     userComentONComentLikeCheck = "0"
#                 else:
#                     audition_like_comentONcoment_info_user = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
#                     status = audition_like_comentONcoment_info_user.status
#                     if status == "0":
#                         userComentONComentLikeCheck = "0"
#                     elif status == "1":
#                         userComentONComentLikeCheck = "1"


#                 audition_comentOnComentinfoDict = {
#                     'comentONcomentPK':comentONcomentPK,
#                     'comentPK':comentPK,
#                     'videoPK':videoPK,
#                     'userPK':userPK,
#                     'username':username,
#                     'nickName':nickName,
#                     'profileIMG_path':profileIMG_path,
#                     'contents':contents,
#                     'previous':previous,
#                     'previous_date':previous_date,
#                     'likeCount':likeCount,
#                     'userComentONComentLikeCheck':userComentONComentLikeCheck
#                 }
#                 audition_comentONcomentList.append(audition_comentOnComentinfoDict)
                
#             text = "\033[92m"+"audition_comentONcomentList SUCCESS -> 대댓글 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'audition_comentONcomentList':audition_comentONcomentList}
#             return HttpResponse(json.dumps(context))
            

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentONcomentList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))

# # 오디션 대댓글 저장
# @csrf_exempt
# def audition_comentONcomentSubmit(request):
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
#             contents = data['contents']

#             # audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
#             # if audition_comentOnComentinfoCount == 0:
#             audition_comentOnComentSubmit = Audition_ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#             audition_comentOnComentSubmit.save()

#             text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
#             ment = "\033[92m"+"audition_comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             loginUserPK = data['loginUserPK']
#             comentPK = data['comentPK']
#             videoPK = data['videoPK']
#             contents = data['contents']

#             # audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK).count()
#             # if audition_comentOnComentinfoCount == 0:
#             audition_comentOnComentSubmit = Audition_ComentOnComent(userPK = str(loginUserPK), videoPK = str(videoPK), comentPK = comentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), contents = contents)
#             audition_comentOnComentSubmit.save()

#             text = "coment PK값 : " + str(comentPK) + ", video PK값 : " + str(videoPK) + ", user PK값 : " + str(loginUserPK) + ", 대댓글 완료"
#             ment = "\033[92m"+"audition_comentONcomentSubmit SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
        
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_comentONcomentSubmit Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    


# 오디션 대댓글 저장
@csrf_exempt
def audition_comentONcomentSubmit(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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




# # 오디션 대댓글 삭제
# @csrf_exempt
# def audition_ComentOnComentDel(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             comentONcomentPK = data['comentONcomentPK']
#             loginUserPK = str(data['loginUserPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])

#             comentONcomentinfo = Audition_ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

#             comentONcomentinfo.status = "9"
#             comentONcomentinfo.save()
#             text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
#             ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
        
#         else:
#             comentONcomentPK = data['comentONcomentPK']
#             loginUserPK = str(data['loginUserPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])

#             comentONcomentinfo = Audition_ComentOnComent.objects.get(id = int(comentONcomentPK), userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK)

#             comentONcomentinfo.status = "9"
#             comentONcomentinfo.save()
#             text = "comentONcoment PK값 : " + str(comentONcomentPK) + ", user PK값 : " + loginUserPK + ", 대댓글 삭제 완료"
#             ment = "\033[92m"+"comentONcomentDel SUCCESS -> "+text+"\033[0m"
#             print("["+str(datetime.now())+"] " + ment + '\033[0m')
#             context = {'code':'1'}
#             return HttpResponse(json.dumps(context))
        
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"comentONcomentDel Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# 오디션 대댓글 삭제
@csrf_exempt
def audition_ComentOnComentDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
    




# # 오디션 대댓글 좋아요
# @csrf_exempt
# def audition_comentONcomentLike(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = str(data['loginUserPK'])
#             comentONcomentPK = str(data['comentONcomentPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])

#             audition_like_comentONcomentinfoCount = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
#             if audition_like_comentONcomentinfoCount == 0:
#                 audition_Like_comentONcomentinfo = Audition_Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 audition_Like_comentONcomentinfo.save()
#                 text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
#                 ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_comentONcomentinfo = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
#                 status = audition_like_comentONcomentinfo.status
#                 if status == "0":
#                     audition_like_comentONcomentinfo.status = "1"
#                     audition_like_comentONcomentinfo.save()
#                     text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
#                     ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 elif status == "1":
#                     audition_like_comentONcomentinfo.status = "0"
#                     audition_like_comentONcomentinfo.save()

#                     text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
#                     ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))
                
#         else:
#             loginUserPK = str(data['loginUserPK'])
#             comentONcomentPK = str(data['comentONcomentPK'])
#             comentPK = str(data['comentPK'])
#             videoPK = str(data['videoPK'])

#             audition_like_comentONcomentinfoCount = Audition_Like_comentONcoment.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK).count()
#             if audition_like_comentONcomentinfoCount == 0:
#                 audition_Like_comentONcomentinfo = Audition_Like_comentONcoment(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK, createAt = datetime.now(), createAt_timestamp = str(round(time.time())), status = "1")
#                 audition_Like_comentONcomentinfo.save()
#                 text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 최초 좋아요 완료"
#                 ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 audition_like_comentONcomentinfo = Audition_Like_comentONcoment.objects.get(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK, comentONcomentPK = comentONcomentPK)
#                 status = audition_like_comentONcomentinfo.status
#                 if status == "0":
#                     audition_like_comentONcomentinfo.status = "1"
#                     audition_like_comentONcomentinfo.save()
#                     text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 완료"
#                     ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'1'}
#                     return HttpResponse(json.dumps(context))
#                 elif status == "1":
#                     audition_like_comentONcomentinfo.status = "0"
#                     audition_like_comentONcomentinfo.save()

#                     text = "comentONcoment PK값 : " + comentONcomentPK + ", user PK값 : " + loginUserPK + ", 대댓글 좋아요 취소"
#                     ment = "\033[92m"+"comentONcomentLike SUCCESS -> "+text+"\033[0m"
#                     print("["+str(datetime.now())+"] " + ment + '\033[0m')
#                     context = {'code':'2'}
#                     return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"comentONcomentLike Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 오디션 대댓글 좋아요
@csrf_exempt
def audition_comentONcomentLike(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
    


# # 내가등록한 오디션 영상리스트 현황 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 )
# @csrf_exempt
# def audition_myVideoList(request):
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


#             videoinfoCount = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
#             if videoinfoCount == 0:
#                 text = "내가 업로드한 비디오 리스트 없음"
#                 ment = "\033[93m"+"audition_myVideoList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:        
#                 # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
#                 videoinfo = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     userPK = i.userPK
#                     videoPK = i.id
#                     categoryPK = i.categoryPK
#                     tournamentStatus = i.tournamentStatus
#                     progressStatus = i.progressStatus
#                     auditionListPK = i.auditionListPK
#                     status = i.status
#                     comment = i.comment
#                     createAt = str(i.createAt)
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i.videoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status
#                     if s3Status == "0":
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     elif s3Status == "1":
#                         videoPATH = s3PATH+videoPATH
#                         thumbnailPATH = s3PATH+thumbnailPATH

#                     audition_Listinfo = Audition_List.objects.get(id = auditionListPK)
#                     auditionTitle = audition_Listinfo.title


#                     tournamentName = ""
#                     if tournamentStatus == "0":
#                         tournamentName = "모집중"
#                     if tournamentStatus == "1":
#                         tournamentName = "예선"
#                     if tournamentStatus == "2":
#                         tournamentName = "32강"
#                     if tournamentStatus == "3":
#                         tournamentName = "16강"
#                     if tournamentStatus == "4":
#                         tournamentName = "8강"
#                     if tournamentStatus == "5":
#                         tournamentName = "4강"
#                     if tournamentStatus == "6":
#                         tournamentName = "결승"

#                     categoryListinfo = CategoryList.objects.get(id = categoryPK)
#                     category = categoryListinfo.category
                    

#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {
#                         'videoPK':str(videoPK),
#                         'thumbnailPATH':thumbnailPATH,
#                         'dateTime':c,
#                         'status':status,
#                         'category':category,
#                         'auditionTitle':auditionTitle,
#                         'tournamentName':tournamentName,
#                         'comment':comment,
#                     }
#                     videoinfoList.append(dictinfo)
                    
#                 text = "\033[92m"+"audition_myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             # page = int(data['page'])
#             # pageStart = (page - 1) * 10
#             # pageEnd = 10 * page
#             loginUserPK = data['loginUserPK']


#             videoinfoCount = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).count()
#             if videoinfoCount == 0:
#                 text = "내가 업로드한 비디오 리스트 없음"
#                 ment = "\033[93m"+"audition_myVideoList WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')                
#                 context = {'code':'0', 'videoinfoList':None}
#                 return HttpResponse(json.dumps(context))
#             else:        
#                 # videoinfo = Video.objects.filter(status = "1").order_by('?')[pageStart:pageEnd]
#                 videoinfo = Audition_video.objects.filter(Q(userPK = loginUserPK, status = "0") | Q(userPK = loginUserPK, status = "1") | Q(userPK = loginUserPK, status = "9")).order_by('createAt')
#                 videoinfoList = []
#                 for index, i in enumerate(videoinfo):
#                     userPK = i.userPK
#                     videoPK = i.id
#                     categoryPK = i.categoryPK
#                     tournamentStatus = i.tournamentStatus
#                     progressStatus = i.progressStatus
#                     auditionListPK = i.auditionListPK
#                     status = i.status
#                     comment = i.comment
#                     createAt = str(i.createAt)
#                     userinfo = SignUp.objects.get(id = userPK)
#                     username = userinfo.username
#                     nickName = userinfo.nickName
#                     profileIMG_path = userinfo.profileIMG_path
#                     if profileIMG_path:
#                         profileIMG_path = s3PATH+profileIMG_path
#                     else:
#                         profileIMG_path = serverURL+"/static/profileIMG/baseprofile.svg"

#                     videoPATH = i.videoPATH
#                     thumbnailPATH = i.thumbnailPATH
#                     s3Check = S3Check.objects.get(id = 1)
#                     s3Status = s3Check.status
#                     if s3Status == "0":
#                         videoPATH = serverURL+"/static/video"+videoPATH
#                         thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#                     elif s3Status == "1":
#                         videoPATH = s3PATH+videoPATH
#                         thumbnailPATH = s3PATH+thumbnailPATH

#                     audition_Listinfo = Audition_List.objects.get(id = auditionListPK)
#                     auditionTitle = audition_Listinfo.title


#                     tournamentName = ""
#                     if tournamentStatus == "0":
#                         tournamentName = "모집중"
#                     if tournamentStatus == "1":
#                         tournamentName = "예선"
#                     if tournamentStatus == "2":
#                         tournamentName = "32강"
#                     if tournamentStatus == "3":
#                         tournamentName = "16강"
#                     if tournamentStatus == "4":
#                         tournamentName = "8강"
#                     if tournamentStatus == "5":
#                         tournamentName = "4강"
#                     if tournamentStatus == "6":
#                         tournamentName = "결승"

#                     categoryListinfo = CategoryList.objects.get(id = categoryPK)
#                     category = categoryListinfo.category
                    

#                     timestamp = time.mktime(datetime.strptime(createAt, '%Y-%m-%d %H:%M:%S.%f').timetuple())
#                     b = datetime.fromtimestamp(float(timestamp))
#                     c = b.strftime('%Y-%m-%d %H:%M')

#                     dictinfo = {
#                         'videoPK':str(videoPK),
#                         'thumbnailPATH':thumbnailPATH,
#                         'dateTime':c,
#                         'status':status,
#                         'category':category,
#                         'auditionTitle':auditionTitle,
#                         'tournamentName':tournamentName,
#                         'comment':comment,
#                     }
#                     videoinfoList.append(dictinfo)
                    
#                 text = "\033[92m"+"audition_myVideoList SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1', 'videoinfoList':videoinfoList}
#                 return HttpResponse(json.dumps(context))


#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoList Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 내가등록한 오디션 영상리스트 현황 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 )
@csrf_exempt
def audition_myVideoList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

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
                    profileIMG_path = s3PATH+profileIMG_path
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
                    'videoPATH':videoPATH
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




# # 내가등록한 영상리스트 현황 디테일 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 -> 썸내일 터치 )
# @csrf_exempt
# def audition_myVideoListDetail(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             tournamentStatus = videoinfo.tournamentStatus
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username
#             nickName = userinfo.nickName

#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3PATH+profileIMG_path
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
#                 videoPATH = s3PATH+videoPATH
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
#                 'tournamentStatus':tournamentStatus
#             }]
#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"audition_myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
        

#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
#             tournamentStatus = videoinfo.tournamentStatus
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username
#             nickName = userinfo.nickName

#             profileIMG_path = userinfo.profileIMG_path
#             if profileIMG_path:
#                 profileIMG_path = s3PATH+profileIMG_path
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
#                 videoPATH = s3PATH+videoPATH
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
#                 'tournamentStatus':tournamentStatus
#             }]
#             # videoinfoList = [nickName, profileIMG_path, contents, hashTag, videoPATH]
                
#             text = "\033[92m"+"audition_myVideoListDetail SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoListDetail Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))



# 내가등록한 영상리스트 현황 디테일 ( 마이프로필 -> 햄버거메뉴 -> 영상리스트 -> 썸내일 터치 )
@csrf_exempt
def audition_myVideoListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # # deviceVer = data['deviceVer']
        # versioninfo = Version.objects.get(id = 1)
        # aosVer = versioninfo.aos
        # iosVer = versioninfo.ios
        # if "1.2.9" == aosVer or "1.2.9" == iosVer:
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
            profileIMG_path = s3PATH+profileIMG_path
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






# #  내가등록한 영상 정보 수정 페이지 이동
# @csrf_exempt
# def audition_myVideoListDetail_modiHtml(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
            
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username



#             videoPATH = videoinfo.videoPATH
#             thumbnailPATH = videoinfo.thumbnailPATH
#             s3Check = S3Check.objects.get(id = 1)
#             s3Status = s3Check.status
#             if s3Status == "0":
#                 videoPATH = serverURL+"/static/video"+videoPATH
#                 thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#             elif s3Status == "1":
#                 videoPATH = s3PATH+videoPATH
#                 thumbnailPATH = s3PATH+thumbnailPATH



#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag
#             location = videoinfo.location

#             videoinfoList = [{
#                 'videoPK':videoPK,
#                 'videoPATH':videoPATH,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'location':location,
#             }]
#             # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
                
#             text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
        

#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
            
#             videoPK = videoinfo.id
#             status = videoinfo.status
            
#             createAt = str(videoinfo.createAt)
#             comment = videoinfo.comment
#             userinfo = SignUp.objects.get(id = loginUserPK)
#             username = userinfo.username



#             videoPATH = videoinfo.videoPATH
#             thumbnailPATH = videoinfo.thumbnailPATH
#             s3Check = S3Check.objects.get(id = 1)
#             s3Status = s3Check.status
#             if s3Status == "0":
#                 videoPATH = serverURL+"/static/video"+videoPATH
#                 thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#             elif s3Status == "1":
#                 videoPATH = s3PATH+videoPATH
#                 thumbnailPATH = s3PATH+thumbnailPATH



#             contents = videoinfo.contents
#             hashTag = videoinfo.hashTag
#             location = videoinfo.location

#             videoinfoList = [{
#                 'videoPK':videoPK,
#                 'videoPATH':videoPATH,
#                 'contents':contents,
#                 'hashTag':hashTag,
#                 'location':location,
#             }]
#             # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
                
#             text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#             print("["+str(datetime.now())+"] " + text)
#             context = {'code':'1', 'videoinfoList':videoinfoList}
#             return HttpResponse(json.dumps(context))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoListDetail_modiHtml Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    



# #  내가등록한 영상 정보 수정 페이지 이동
# @csrf_exempt
# def audition_myVideoListDetail_modiHtml(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # # deviceVer = data['deviceVer']
#         # versioninfo = Version.objects.get(id = 1)
#         # aosVer = versioninfo.aos
#         # iosVer = versioninfo.ios
#         # if "1.2.9" == aosVer or "1.2.9" == iosVer:

#         loginUserPK = data['loginUserPK']
#         videoPK = data['videoPK']
    
#         videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
        
#         videoPK = videoinfo.id
#         status = videoinfo.status
        
#         createAt = str(videoinfo.createAt)
#         comment = videoinfo.comment
#         userinfo = SignUp.objects.get(id = loginUserPK)
#         username = userinfo.username



#         videoPATH = videoinfo.videoPATH
#         thumbnailPATH = videoinfo.thumbnailPATH
#         s3Check = S3Check.objects.get(id = 1)
#         s3Status = s3Check.status
#         if s3Status == "0":
#             videoPATH = serverURL+"/static/video"+videoPATH
#             thumbnailPATH = serverURL+"/static/thumbnail"+thumbnailPATH
#         elif s3Status == "1":
#             videoPATH = s3PATH+videoPATH
#             thumbnailPATH = s3PATH+thumbnailPATH



#         contents = videoinfo.contents
#         hashTag = videoinfo.hashTag
#         location = videoinfo.location

#         videoinfoList = [{
#             'videoPK':videoPK,
#             'videoPATH':videoPATH,
#             'contents':contents,
#             'hashTag':hashTag,
#             'location':location,
#         }]
#         # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
            
#         text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
#         print("["+str(datetime.now())+"] " + text)
#         context = {'code':'1', 'videoinfoList':videoinfoList}
#         return HttpResponse(json.dumps(context))
        

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoListDetail_modiHtml Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))


# # 영상 수정 업로드
# @csrf_exempt
# def audition_myVideoListDetail_modi(request):
#     try:
#         if request.method == 'POST':
#             userPK = str(request.POST.get('loginUserPK'))
#             videoPK = request.POST.get('videoPK')
#             contents = request.POST.get('contents')
#             hashTag = request.POST.get('hashTag')
#             location = request.POST.get('location')
#             viewable = request.POST.get('viewable')
#             status = request.POST.get('status')
#             if status == "1":
#             # rewardRate = request.POST.get('rewardRate')
#             # reqFile = request.FILES
#             # print("reqFile >>", reqFile)
#             # if len(reqFile['file']) != 0:
#                 # bucketName = "showplus"     # ygbs
#                 bucketName = "showpluss3"     # showplus
#                 img = request.FILES['file']
#                 print("img >>>", img)


#                 inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                 inviteCode = inviteCode + ".jpg"
#                 # userinfoCount = Audition_video.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
#                 # check = False
#                 # if userinfoCount == 0:
#                 #     pass
#                 # else:
#                 #     while check == False:
#                 #         inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
#                 #         inviteCode = inviteCode + ".jpg"
#                 #         userinfoCount_check = SignUp.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
#                 #         if userinfoCount_check == 0:
#                 #             check = True
#                 #             break;

#                 now = datetime.now()
#                 year = str(now.year)
#                 month = str(now.month)
#                 day = str(now.day)

#                 path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


#                 # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
#                 # aws_secret_access_key = "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"        # ygbs

#                 s3_client = boto3.client(
#                     's3',
#                     aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
#                     aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
#                 )
#                 s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))




                
#                 videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + s3VideoPATH

#                 s3_client.upload_fileobj(
#                     img, 
#                     bucketName, 
#                     videoURL, 
#                     ExtraArgs={
#                         "ContentType": img.content_type
#                     }
#                 )
                
#                 # -----------------------------------------------------------
#                 # 간혹 영상 업로드시 오류가있어 서버에 저장하는 부분 뺌
#                 # if not os.path.exists(path):
#                 #     os.makedirs(path)
#                 # if os.path.isfile(path +str(img)):
#                 #     os.remove(path +str(img))

#                 # file_path = path + str(img)
#                 # with open(file_path, 'wb+') as destination:
#                 #     for chunk in img.chunks():
#                 #         destination.write(chunk)
#                 # # 파일 객체가 닫힌 후에 작업 수행
#                 # with open(file_path, 'rb') as file:
#                 #     # 파일 읽기 등 추가 작업 수행
#                 #     data = file.read()
#                 #     # 예시: seek 작업 수행
#                 #     file.seek(0)
#                 #     # 추가 작업 수행            
#                 # -----------------------------------------------------------

#                 count = 1
#                 test = 1
#                 train = 1
#                 vidcap = cv2.VideoCapture(s3PATH+videoURL)
#                 thumbnailPath = '/mnt/project/app/static/auditions/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
#                 if not os.path.exists(thumbnailPath):
#                     os.makedirs(thumbnailPath)
                
#                 thumbnail_savePATH = ""
                

#                 while(vidcap.isOpened()):
#                     ret, image = vidcap.read()
#                     if(ret==False):
#                         break
#                     if(int(vidcap.get(1)) % 5 == 0):
#                         num=count % 10
#                         thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
#                         print("thumbnail_savePATH >>", thumbnail_savePATH)
#                         cv2.imwrite(thumbnailPath + inviteCode, image)
#                         break;
#                 vidcap.release()



#                 thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH
#                 thumbnailimg = thumbnailPath + inviteCode
#                 with open(thumbnailimg, 'rb') as image_file:
#                     s3_client.upload_fileobj(
#                         image_file, 
#                         bucketName, 
#                         thumbnailURL, 
#                         # ExtraArgs={
#                         #     "ContentType": image_file.content_type
#                         # }
#                     )



#                 savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

#                 if hashTag == "":
#                     hashTag = None


                

#                 videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
#                 videoinfo.createAt = datetime.now()
#                 videoinfo.createAt_timestamp = str(round(time.time()))
#                 videoinfo.thumbnailPATH = thumbnailURL
#                 videoinfo.videoPATH = videoURL
#                 # videoinfo.s3VideoPATH = videoURL
#                 videoinfo.contents = contents
#                 videoinfo.hashTag = hashTag
#                 videoinfo.location = location
#                 videoinfo.viewable = viewable
#                 videoinfo.status = "0"
#                 videoinfo.save()


#                 text = "user PK값 : " + userPK + ", 동영상 저장 완료"
#                 ment = "\033[92m"+"audition_myVideoListDetail_modi SUCCESS -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')

#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))

#             elif status == "0":

#                 if hashTag == "":
#                     hashTag = None


#                 videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
#                 videoinfo.createAt = datetime.now()
#                 videoinfo.createAt_timestamp = str(round(time.time()))
#                 videoinfo.contents = contents
#                 videoinfo.hashTag = hashTag
#                 videoinfo.location = location
#                 videoinfo.viewable = viewable
#                 videoinfo.status = "0"
#                 videoinfo.save()

#                 text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
#                 ment = "\033[93m"+"audition_myVideoListDetail_modi WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'2'}
#                 return HttpResponse(json.dumps(context, default=json_util.default))
#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoListDetail_modi Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))
    




# #  오디션 내가등록한 영상 삭제
# @csrf_exempt
# def audition_myVideoDel(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         # deviceVer = data['deviceVer']
#         versioninfo = Version.objects.get(id = 1)
#         aosVer = versioninfo.aos
#         iosVer = versioninfo.ios
#         if "1.2.9" == aosVer or "1.2.9" == iosVer:

#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfoCount = Audition_video.objects.filter(id = videoPK, userPK = loginUserPK).count()
#             if videoinfoCount == 0:
#                 text = "값이 잘못 넘어옴; 이러면 안되는데??"
#                 ment = "\033[93m"+"audition_myVideoDel WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'9'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
#                 videoinfo.status = "5"
#                 videoinfo.save()

#                 text = "\033[92m"+"audition_myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))
            
#         else:
#             loginUserPK = data['loginUserPK']
#             videoPK = data['videoPK']
        
#             videoinfoCount = Audition_video.objects.filter(id = videoPK, userPK = loginUserPK).count()
#             if videoinfoCount == 0:
#                 text = "값이 잘못 넘어옴; 이러면 안되는데??"
#                 ment = "\033[93m"+"audition_myVideoDel WARNING -> "+text+"\033[0m"
#                 print("["+str(datetime.now())+"] " + ment + '\033[0m')  
#                 context = {'code':'9'}
#                 return HttpResponse(json.dumps(context))
#             else:
#                 videoinfo = Audition_video.objects.get(id = videoPK, userPK = loginUserPK)
#                 videoinfo.status = "5"
#                 videoinfo.save()

#                 text = "\033[92m"+"audition_myVideoDel SUCCESS -> 영상 삭제 완료"+"\033[0m"
#                 print("["+str(datetime.now())+"] " + text)
#                 context = {'code':'1'}
#                 return HttpResponse(json.dumps(context))

#     except Exception as e:
#         text = str(e)
#         ment = "\033[91m"+"audition_myVideoDel Exception ERROR -> "+text+"\033[0m"
#         print("["+str(datetime.now())+"] " + ment + '\033[0m')
#         context = {'code':'99'}
#         return HttpResponse(json.dumps(context))




#  오디션 내가등록한 영상 삭제
@csrf_exempt
def audition_myVideoDel(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # # deviceVer = data['deviceVer']
        # versioninfo = Version.objects.get(id = 1)
        # aosVer = versioninfo.aos
        # iosVer = versioninfo.ios
        # if "1.2.9" == aosVer or "1.2.9" == iosVer:

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




# 오디션 진행 사항 체크
@csrf_exempt
def audition_StatusCheck(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        auditionListPK = data['auditionListPK']

        audition_Listinfo = Audition_List.objects.get(id = auditionListPK)
        progressStatus = audition_Listinfo.progressStatus
        tournamentStatus = audition_Listinfo.tournamentStatus

        text = "오디션 진행 사항 체크"
        ment = "\033[92m"+"audition_endList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')

        context = {'code':'1', 'progressStatus':progressStatus, 'tournamentStatus':tournamentStatus}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_EndList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 오디션 종료 리스트
@csrf_exempt
def audition_EndList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        categoryPK = data['categoryPK']
        audition_ListinfoCount = Audition_List.objects.filter(categoryPK = categoryPK, progressStatus = "9", tournamentStatus = "6").count()
        if audition_ListinfoCount == 0:
            text = "종료된 오디션 없음"
            ment = "\033[93m"+"audition_endList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        else:
            audition_Listinfo = Audition_List.objects.filter(categoryPK = categoryPK, progressStatus = "9", tournamentStatus = "6").order_by('-id')
            auditionEndList = []
            for index, i in enumerate(audition_Listinfo):
                auditionListPK = i.id
                title = i.title
                tournamentStatus = i.tournamentStatus
                auditionImgPATH = i.auditionImgPATH
                # if auditionImgPATH:
                #     auditionImgPATH = serverURL+"/static/auditionMainIMG/"+str(categoryPK)+auditionImgPATH
                dictinfo = {'auditionListPK':auditionListPK, 'title':title, 'tournamentStatus':tournamentStatus, 'auditionImgPATH':auditionImgPATH}
                auditionEndList.append(dictinfo)

            text = "종료된 오디션 추출"
            ment = "\033[92m"+"audition_endList SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

            context = {'code':'1', 'auditionEndList':auditionEndList}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_EndList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))




# 오디션 종료 상세
@csrf_exempt
def audition_EndListDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        auditionListPK = data['auditionListPK']
        # categoryPK = data['categoryPK']
        audition_WinnerListinfoCount = Audition_WinnerList.objects.filter(auditionListPK = auditionListPK).count()
        if audition_WinnerListinfoCount == 0:
            text = "우승자 없음???"
            ment = "\033[93m"+"audition_EndListDetail WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))
        else:
            audition_WinnerListinfo = Audition_WinnerList.objects.get(auditionListPK = auditionListPK)
            ownerPK = audition_WinnerListinfo.userPK
            videoPK = audition_WinnerListinfo.videoPK

            audition_Countinfo = Audition_Count.objects.filter(ownerPK = ownerPK, auditionListPK = auditionListPK)
            donationSum = 0
            likeSum = 0
            comentSum = 0
            viewcountSum = 0
            for index, i in enumerate(audition_Countinfo):
                donationSum += int(i.donation)
                likeSum += int(i.like)
                comentSum += int(i.coment)
                viewcountSum += int(i.viewcount)

            videoinfo = Audition_video.objects.get(id = videoPK)
            videoPATH = videoinfo.videoPATH
            videoPATH = s3PATH+videoPATH
            thumbnailPATH = videoinfo.thumbnailPATH
            thumbnailPATH = s3PATH+thumbnailPATH

            auditionWinnerList = [{'ownerPK':ownerPK, 'videoPK':videoPK, 'videoPATH':videoPATH, 'thumbnailPATH':thumbnailPATH, 'DS':donationSum, 'VS':viewcountSum, 'LS':likeSum, 'CS':comentSum}]
            


            # auditionWinnerList = []

            # for index, i in enumerate(audition_WinnerListinfo):
            #     ownerPK = i.userPK
            #     videoPK = i.videoPK
            #     # DS = int(i.DS) * 50
            #     # VS = int(i.VS) * 15
            #     # LS = int(i.LS) * 25
            #     # CS = int(i.CS) * 10
            #     DS = i.DS
            #     VS = i.VS
            #     LS = i.LS
            #     CS = i.CS
                # videoinfo = Audition_video.objects.get(id = videoPK)
                # videoPATH = videoinfo.videoPATH
                # videoPATH = s3PATH+videoPATH

                # thumbnailPATH = videoinfo.thumbnailPATH
                # thumbnailPATH = s3PATH+thumbnailPATH
                

            #     dictinfo = {'ownerPK':ownerPK, 'videoPK':videoPK, 'videoPATH':videoPATH, 'thumbnailPATH':thumbnailPATH, 'DS':DS, 'VS':VS, 'LS':LS, 'CS':CS}
            #     auditionWinnerList.append(dictinfo)

            audition_winnerPaymentsinfo = Audition_winnerPayments.objects.filter(auditionListPK = auditionListPK)
            winnerPoint = 0
            for index, i in enumerate(audition_winnerPaymentsinfo):
                winnerPoint += int(i.amount)

            text = "오디션 우승자 추출"
            ment = "\033[92m"+"audition_EndListDetail SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')

            context = {'code':'1', 'auditionWinnerList':auditionWinnerList, 'winnerPoint':winnerPoint}
            return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_EndListDetail Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 우승자 영상 상세
@csrf_exempt
def audition_WinnerVideoDetail(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        videoPK = data['videoPK']
        # categoryPK = data['categoryPK']

        videoinfo = Audition_video.objects.get(id = videoPK)
        videoPK = videoinfo.id
        ownerPK = videoinfo.userPK
        status = videoinfo.status
        tournamentStatus = videoinfo.tournamentStatus
        createAt = str(videoinfo.createAt)
        comment = videoinfo.comment
        ownerinfo = SignUp.objects.get(id = ownerPK)
        username = ownerinfo.username
        nickName = ownerinfo.nickName

        profileIMG_path = ownerinfo.profileIMG_path
        if profileIMG_path:
            profileIMG_path = s3PATH+profileIMG_path
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

        viewCount_infoCount = ViewCount.objects.filter(userPK = ownerPK, videoPK = videoPK).count()



        videoinfoList = [{
            'videoPK':videoPK,
            'nickName':nickName,
            'profileIMG_path':profileIMG_path,
            'contents':contents,
            'hashTag':hashTag,
            'videoPATH':videoPATH,
            'tournamentStatus':tournamentStatus
        }]



        text = "오디션 우승자 추출"
        ment = "\033[92m"+"audition_WinnerVideoDetail SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')

        context = {'code':'1', 'videoinfoList':videoinfoList}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_WinnerVideoDetail Exception ERROR -> "+text+"\033[0m"
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
            print("iiii", i)
            start = i['start']
            start_timestamp = time.mktime(datetime.strptime(start, '%Y-%m-%d %H:%M:%S').timetuple())
            start_fromtimestamp = datetime.fromtimestamp(float(start_timestamp))            
            end = i['end']
            end_timestamp = time.mktime(datetime.strptime(end, '%Y-%m-%d %H:%M:%S').timetuple())
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
    


@csrf_exempt
def testFunction(request):
    try:
        print("?????")
        audition_List_PK = "56"
        audition_videoinfo = Audition_video.objects.filter(auditionListPK = audition_List_PK)

        allCountList = []
        for index, k in enumerate(audition_videoinfo):
            ownerPK = k.userPK
            videoPK = k.id
            audition_Countinfo = Audition_Count.objects.get(ownerPK = ownerPK, videoPK = videoPK, auditionListPK = audition_List_PK, tournamentStatus = "1")
            donation = int(audition_Countinfo.donation)
            donationScore = donation * 50
            likeCount = int(audition_Countinfo.like)
            likeScore = likeCount * 25
            comentCount = int(audition_Countinfo.coment)
            comentScore = comentCount * 10
            viewCount = int(audition_Countinfo.viewcount)
            viewCountScore = viewCount * 15

            allScore = donation + likeCount + comentCount + viewCount
            allSum = donationScore + likeScore + comentScore + viewCountScore

            dictinfo = {"ownerPK":ownerPK, "videoPK":videoPK, "DS":donation, "LS":likeCount, "CS":comentCount, "VS":viewCountScore, "AS":allScore, "allSum":allSum}
            allCountList.append(dictinfo)

        allCountListSorted = sorted(allCountList, key=lambda x: x['allSum'], reverse=True)
        print("allCountListSorted >>", allCountListSorted)
        print("=======================================================================================================================================================================================================================================")
        allCountListSlicing = sorted(allCountList, key=lambda x: x['allSum'], reverse=True)[0:32]

        print("=======================================================================================================================================================================================================================================")

        
        for index, i in enumerate(allCountListSorted):
            for index, j in enumerate(allCountListSlicing):
                if i == j:
                    print("iiiiiiiiiiiiiiii", i)
                    print("jjjjjjjjjjjjjjjj", j)
                    allCountList.remove(j)

        removeList = []
        removeList = allCountList
        print("removeList >>", removeList)
        for index, m in enumerate(removeList):
            print("mmmmmmmmmmmmm", m)


        context = {'code':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"videoLike Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






# 오디션 on / off
@csrf_exempt
def audition_check(request):
    try:
        audition_statuscheck = Audition_check.objects.get(id = 1)
        status = audition_statuscheck.status


        text = "오디션 on / off 체크"
        ment = "\033[92m"+"audition_check SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')

        context = {'code':'1', 'status':status}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_check Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))






# 오디션 상세 팝업
@csrf_exempt
def audition_contentDetailPop(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        auditionListPK = data['auditionListPK']

        audition_Listinfo = Audition_List.objects.get(id = auditionListPK)

        title = audition_Listinfo.title
        content = audition_Listinfo.content
        auditionImgPATH = audition_Listinfo.auditionImgPATH
        tournamentStatus = audition_Listinfo.tournamentStatus

        auditioninfoList = [{'title':title, 'content':content, 'tournamentStatus':tournamentStatus, 'auditionImgPATH':auditionImgPATH}]

        text = "종료된 오디션 추출"
        ment = "\033[92m"+"audition_endList SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')

        context = {'code':'1', 'auditioninfoList':auditioninfoList}
        return HttpResponse(json.dumps(context))
            
    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_EndList Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# =================================================================================================================================================================================================================
# 2차 추가 및 수정


# 오디션 댓글 신고
@csrf_exempt
def audition_commentDeclaration(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        # commentUserPK = data['commentUserPK']
        commentPK = data['commentPK']
        comment = data['comment']
        auditionListPK = data['auditionListPK']
        tournamentStatus = data['tournamentStatus']

        audition_CommentDeclarationinfoCount = Audition_CommentDeclaration.objects.filter(Q(loginUserPK = loginUserPK, commentPK = commentPK, status = "5") | Q(commentPK = commentPK, status = "9")).count()
        if audition_CommentDeclarationinfoCount == 0:
            Audition_Comentinfo = Audition_Coment.objects.get(id = commentPK)
            userPK = Audition_Comentinfo.userPK
            audition_CommentDeclarationSubmit = Audition_CommentDeclaration(
                loginUserPK = loginUserPK,
                videoPK = videoPK,
                commentUserPK = userPK,
                commentPK = commentPK,
                comment = comment,
                createAt = datetime.now(),
                createAt_timestamp = str(round(time.time())),
                auditionListPK = auditionListPK,
                tournamentStatus = tournamentStatus
            )
            audition_CommentDeclarationSubmit.save()

            
            Audition_Comentinfo.status = "5"
            Audition_Comentinfo.save()


            text = "comment PK값 : " + str(commentPK) + ", loginUserPK PK값 : " + str(loginUserPK) + ", 댓글 신고 완료"
            ment = "\033[92m"+"audition_commentDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

        else:
            text = "comment PK값 : " + str(commentPK) + ", loginUserPK PK값 : " + str(loginUserPK) + ", 이미 신고함"
            ment = "\033[92m"+"audition_commentDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_commentDeclaration Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    


# 오디션 댓글 리스트 ( 2차 / 댓글 신고 추가 )
@csrf_exempt
def audition_comentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']

        audition_comentinfoCount = Audition_Coment.objects.filter(Q(videoPK = videoPK, status = "0") | Q(videoPK = videoPK, status = "5")).count()

        if audition_comentinfoCount == 0:
            text = "댓글 없음"
            ment = "\033[93m"+"audition_comentList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'comentinfoList':None}
            return HttpResponse(json.dumps(context))
        else:
            audition_comentinfo = Audition_Coment.objects.filter(Q(videoPK = videoPK, status = "0") | Q(videoPK = videoPK, status = "5")).order_by('-id')
            audition_comentinfoList = []
            for index, i in enumerate(audition_comentinfo):
                now  = int(round(time.time()))
                userPK = i.userPK
                comentPK = i.id
                Audition_CommentDeclarationinfoCount = Audition_CommentDeclaration.objects.filter(Q(loginUserPK = loginUserPK, commentPK = comentPK, status = "5") | Q(commentPK = comentPK, status = "9")).count()
                if Audition_CommentDeclarationinfoCount == 0:
                    createAt = i.createAt
                    createAt_timestamp = int(round(float(i.createAt_timestamp)))
                    contents = i.contents
                    userinfo = SignUp.objects.get(id = userPK)
                    username = userinfo.username
                    nickName = userinfo.nickName
                    profileIMG_path = userinfo.profileIMG_path
                    if profileIMG_path:
                        profileIMG_path = s3PATH+profileIMG_path
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


                    # audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK).count()
                    # comentONcomentCount = str(audition_comentOnComent_infoCount)

                    audition_comentOnComent_infoCount = Audition_ComentOnComent.objects.filter(videoPK = videoPK, comentPK = comentPK, status = "0").count()
                    comentONcomentCount = audition_comentOnComent_infoCount

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
                            audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(Q(loginUserPK = loginUserPK, commentCommentPK = comentONcomentPK, status = "5") | Q(commentCommentPK = comentONcomentPK, status = "9")).count()
                            if audition_CommentCommentDeclarationinfoCount:
                                comentONcomentCount -= 1


                    audition_comentOnComent_infoCount_user = Audition_ComentOnComent.objects.filter(userPK = loginUserPK, videoPK = videoPK, comentPK = comentPK).count()
                    if audition_comentOnComent_infoCount_user == 0:
                        userComentONComentCheck = "0"
                    else:
                        userComentONComentCheck = "1"

                    audition_CommentDeclaration_myCountCheck = Audition_CommentDeclaration.objects.filter(Q(commentUserPK = loginUserPK, status = "5") | Q(commentUserPK = loginUserPK, status = "9")).count()
                    myDecCheck = ""
                    if audition_CommentDeclaration_myCountCheck == 0:
                        myDecCheck = "0"
                    else:
                        myDecCheck = "1"


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
                        'comentONcomentLen':str(comentONcomentCount),
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
    





# 오디션 대댓글 신고
@csrf_exempt
def audition_commentCommentDeclaration(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        loginUserPK = data['loginUserPK']
        videoPK = data['videoPK']
        # commentUserPK = data['commentUserPK']
        commentPK = data['commentPK']
        commentCommentPK = data['commentCommentPK']
        comment = data['comment']


        audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(Q(loginUserPK = loginUserPK, commentCommentPK = commentCommentPK, status = "5") | Q(commentCommentPK = commentCommentPK, status = "9")).count()
        if audition_CommentCommentDeclarationinfoCount == 0:

            audition_CommentCommentDeclarationSubmit = Audition_CommentCommentDeclaration(
                loginUserPK = loginUserPK,
                videoPK = videoPK,
                # commentUserPK = commentUserPK,
                commentPK = commentPK,
                commentCommentPK = commentCommentPK,
                comment = comment,
                createAt = datetime.now(),
                createAt_timestamp = str(round(time.time())),
            )
            audition_CommentCommentDeclarationSubmit.save()
            text = "comment PK값 : " + str(commentPK) + ", loginUserPK PK값 : " + str(loginUserPK) + ", 대댓글 신고 완료"
            ment = "\033[92m"+"audition_commentCommentDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'1'}
            return HttpResponse(json.dumps(context))

        else:
            text = "comment PK값 : " + str(commentPK) + ", loginUserPK PK값 : " + str(loginUserPK) + ", 이미 신고함"
            ment = "\033[92m"+"audition_commentCommentDeclaration SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'2'}
            return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_commentCommentDeclaration Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    



# 오디션 대댓글 리스트
@csrf_exempt
def audition_comentONcomentList(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        loginUserPK = data['loginUserPK']
        comentPK = data['comentPK']
        videoPK = data['videoPK']
        
        audition_comentOnComentinfoCount = Audition_ComentOnComent.objects.filter(Q(videoPK = videoPK, comentPK = comentPK, status = "0") | Q(videoPK = videoPK, comentPK = comentPK, status = "5")).count()
        if audition_comentOnComentinfoCount == 0:
            text = "대댓글 없음"
            ment = "\033[93m"+"audition_comentONcomentList WARNING -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')                
            context = {'code':'0', 'comentONcomentList':None}
            return HttpResponse(json.dumps(context))
        else:
            audition_comentOnComentinfo = Audition_ComentOnComent.objects.filter(Q(videoPK = videoPK, comentPK = comentPK, status = "0") | Q(videoPK = videoPK, comentPK = comentPK, status = "5")).order_by('-id')
            audition_comentONcomentList = []
            for index, i in enumerate(audition_comentOnComentinfo):
                comentONcomentPK = i.id
                audition_CommentCommentDeclarationinfoCount = Audition_CommentCommentDeclaration.objects.filter(Q(loginUserPK = loginUserPK, commentCommentPK = comentONcomentPK, status = "5") | Q(commentCommentPK = comentONcomentPK, status = "9")).count()
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
                        profileIMG_path = s3PATH+profileIMG_path
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
    


# # 오디션 동영상 업로드
# # 20230808 - size, mention, tag 추가
# @csrf_exempt
# def audition_fileupload(request):
#     try:
#         if request.method == 'POST':
#             userPK = str(request.POST.get('loginUserPK'))
#             contents = request.POST.get('contents')
#             hashTag = request.POST.get('hashTag')
#             viewable = request.POST.get('viewable')
#             categoryPK = request.POST.get('categoryPK')
#             tournamentStatus = request.POST.get('tournamentStatus')
#             auditionListPK = request.POST.get('auditionListPK')
#             rewardRate = request.POST.get('rewardRate')
#             size = request.POST.get('size')
#             mention = request.POST.get('mention')
#             tag = request.POST.get('tag')
            

#             reqFile = request.FILES
#             print("reqFile >>", reqFile)
#             if len(reqFile['file']) != 0:
#                 # bucketName = "showplus"     # ygbs
#                 bucketName = "showpluss3"     # showplus
#                 img = request.FILES['file']
#                 print("img >>>", img)


#                 inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                 # inviteCode_thumbnail = inviteCode + ".jpg"
#                 audition_VideoCount = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
#                 check = False
#                 if audition_VideoCount == 0:
#                     pass
#                 else:
#                     while check == False:
#                         inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                         # inviteCode_thumbnail = inviteCode + ".jpg"
#                         audition_VideoCount_check = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
#                         if audition_VideoCount_check == 0:
#                             check = True
#                             break;

#                 now = datetime.now()
#                 year = str(now.year)
#                 month = str(now.month)
#                 day = str(now.day)

#                 path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


#                 # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
#                 # aws_secret_access_key = "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"        # ygbs

#                 s3_client = boto3.client(
#                     's3',
#                     aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
#                     aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
#                 )

#                 # s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))


#                 # -------------------------------------------------------------------------------------------------------
#                 # 로직 필요없거나 수정해야함
#                 # videoinfoCount = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
#                 # url = ""
#                 # check = False

#                 # if videoinfoCount == 0:
#                 #     url = 'videos/videos/'+s3VideoPATH
#                 # else:
#                 #     while check == False:
#                 #         s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
#                 #         videoinfoCount_check = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
#                 #         if videoinfoCount_check == 0:
#                 #             check = True
#                 #             url = 'videos/videos/'+s3VideoPATH
#                 #             break;
#                 # -------------------------------------------------------------------------------------------------------


#                 videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

#                 s3_client.upload_fileobj(
#                     img, 
#                     bucketName, 
#                     videoURL, 
#                     ExtraArgs={
#                         "ContentType": img.content_type
#                     }
#                 )
                
#                 # -----------------------------------------------------------
#                 # 간혹 영상 업로드시 오류가있어 서버에 저장하는 부분 뺌
#                 # if not os.path.exists(path):
#                 #     os.makedirs(path)
#                 # if os.path.isfile(path +str(img)):
#                 #     os.remove(path +str(img))

#                 # file_path = path + str(img)
#                 # with open(file_path, 'wb+') as destination:
#                 #     for chunk in img.chunks():
#                 #         destination.write(chunk)
#                 # # 파일 객체가 닫힌 후에 작업 수행
#                 # with open(file_path, 'rb') as file:
#                 #     # 파일 읽기 등 추가 작업 수행
#                 #     data = file.read()
#                 #     # 예시: seek 작업 수행
#                 #     file.seek(0)
#                 #     # 추가 작업 수행            
#                 # -----------------------------------------------------------

#                 count = 1
#                 test = 1
#                 train = 1
#                 vidcap = cv2.VideoCapture(s3PATH+videoURL)
#                 thumbnailPath = '/mnt/project/app/static/auditions/thumbnail/'+year+'/'+month+'/'+day+'/'+userPK+'/'
#                 if not os.path.exists(thumbnailPath):
#                     os.makedirs(thumbnailPath)
                
#                 thumbnail_savePATH = ""
                

#                 while(vidcap.isOpened()):
#                     ret, image = vidcap.read()
#                     if(ret==False):
#                         break
#                     if(int(vidcap.get(1)) % 5 == 0):
#                         num=count % 10
#                         thumbnail_savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
#                         print("thumbnail_savePATH >>", thumbnail_savePATH)
#                         cv2.imwrite(thumbnailPath + inviteCode+".jpg", image)
#                         break;
#                 vidcap.release()



#                 thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH+".jpg"
#                 thumbnailimg = thumbnailPath + inviteCode+".jpg"
#                 with open(thumbnailimg, 'rb') as image_file:
#                     s3_client.upload_fileobj(
#                         image_file, 
#                         bucketName, 
#                         thumbnailURL, 
#                         # ExtraArgs={
#                         #     "ContentType": image_file.content_type
#                         # }
#                     )


#                 savePATH = '/'+year+'/'+month+'/'+day+'/'+userPK+'/'+str(img)

#                 if hashTag == "":
#                     hashTag = None

#                 videoSubmit = Audition_video(
#                     userPK = userPK, 
#                     createAt = datetime.now(), 
#                     createAt_timestamp = str(round(time.time())), 
#                     thumbnailPATH = thumbnailURL, 
#                     videoPATH = videoURL, 
#                     # s3VideoPATH = videoURL,
#                     contents = contents, 
#                     hashTag = hashTag,
#                     viewable = viewable,
#                     categoryPK = categoryPK,
#                     # tournamentStatus = tournamentStatus,
#                     auditionListPK = auditionListPK,
#                     rewardRate = str(rewardRate),
#                     size = size,
#                     mention = mention,
#                     tag = tag
#                 )
#                 videoSubmit.save()
                
#                 videoPK = videoSubmit.id


#                 if mention:
#                     if ',' in mention:
#                         mentionList = mention.split(',')
#                     else:
#                         mentionList = [mention]
#                     # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
#                     for index, i in enumerate(mentionList):
#                         mentionListSubmit = Audition_MentionList(
#                             loginUserPK = userPK,
#                             userPK = i,
#                             auditionListPK = auditionListPK,
#                             videoPK = videoPK,
#                             createAt = datetime.now(),
#                             createAt_timestamp = str(round(time.time()))
#                         )
#                         mentionListSubmit.save()

#                 if tag:
#                     if ',' in tag:
#                         tagList = tag.split(',')
#                     else:
#                         tagList = [tag]
#                     # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
#                     for index, j in enumerate(tagList):
#                         tagListSubmit = Audition_TagList(
#                             loginUserPK = userPK,
#                             userPK = j,
#                             auditionListPK = auditionListPK,
#                             videoPK = videoPK,
#                             createAt = datetime.now(),
#                             createAt_timestamp = str(round(time.time()))
#                         )
#                         tagListSubmit.save()



#                 Audition_CountSubmit = Audition_Count(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK, tournamentStatus = tournamentStatus)
#                 Audition_CountSubmit.save()

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



# 오디션 동영상 업로드
# 20230808 - size, mention, tag 추가
@csrf_exempt
def audition_fileupload(request):
    try:
        if request.method == 'POST':
            userPK = str(request.POST.get('loginUserPK'))
            contents = request.POST.get('contents')
            hashTag = request.POST.get('hashTag')
            viewable = request.POST.get('viewable')
            categoryPK = request.POST.get('categoryPK')
            tournamentStatus = request.POST.get('tournamentStatus')
            auditionListPK = request.POST.get('auditionListPK')
            rewardRate = request.POST.get('rewardRate')
            size = request.POST.get('size')
            mention = request.POST.get('mention')
            tag = request.POST.get('tag')
            fileCheck = request.POST.get('fileCheck')
            inviteCode = ""
            s3VideoPATH = ""
            thumbnailURL = ""

            if fileCheck == "0":
                reqFile = request.FILES
                print("reqFile >>", reqFile)
                if len(reqFile['file']) != 0:
                    # bucketName = "showplus"     # ygbs
                    bucketName = "showpluss3"     # showplus
                    img = request.FILES['file']
                    print("img >>>", img)


                    inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                    # inviteCode_thumbnail = inviteCode + ".jpg"
                    audition_VideoCount = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                    check = False
                    if audition_VideoCount == 0:
                        pass
                    else:
                        while check == False:
                            inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                            # inviteCode_thumbnail = inviteCode + ".jpg"
                            audition_VideoCount_check = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                            if audition_VideoCount_check == 0:
                                check = True
                                break;

                    now = datetime.now()
                    year = str(now.year)
                    month = str(now.month)
                    day = str(now.day)

                    path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


                    # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
                    # aws_secret_access_key = "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"        # ygbs

                    s3_client = boto3.client(
                        's3',
                        aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
                        aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
                    )

                    # s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))


                    # -------------------------------------------------------------------------------------------------------
                    # 로직 필요없거나 수정해야함
                    # videoinfoCount = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
                    # url = ""
                    # check = False

                    # if videoinfoCount == 0:
                    #     url = 'videos/videos/'+s3VideoPATH
                    # else:
                    #     while check == False:
                    #         s3VideoPATH = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                    #         videoinfoCount_check = Video.objects.filter(s3VideoPATH=s3VideoPATH).count()
                    #         if videoinfoCount_check == 0:
                    #             check = True
                    #             url = 'videos/videos/'+s3VideoPATH
                    #             break;
                    # -------------------------------------------------------------------------------------------------------


                    videoURL = 'auditions/videos/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

                    s3_client.upload_fileobj(
                        img, 
                        bucketName, 
                        videoURL, 
                        ExtraArgs={
                            "ContentType": img.content_type
                        }
                    )
                    
                    # -----------------------------------------------------------
                    # 간혹 영상 업로드시 오류가있어 서버에 저장하는 부분 뺌
                    # if not os.path.exists(path):
                    #     os.makedirs(path)
                    # if os.path.isfile(path +str(img)):
                    #     os.remove(path +str(img))

                    # file_path = path + str(img)
                    # with open(file_path, 'wb+') as destination:
                    #     for chunk in img.chunks():
                    #         destination.write(chunk)
                    # # 파일 객체가 닫힌 후에 작업 수행
                    # with open(file_path, 'rb') as file:
                    #     # 파일 읽기 등 추가 작업 수행
                    #     data = file.read()
                    #     # 예시: seek 작업 수행
                    #     file.seek(0)
                    #     # 추가 작업 수행            
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
                            cv2.imwrite(thumbnailPath + inviteCode+".jpg", image)
                            break;
                    vidcap.release()



                    thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH+".jpg"
                    thumbnailimg = thumbnailPath + inviteCode+".jpg"
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

                    s3VideoPATH = s3PATH + videoURL

            else:
                tmpPK = request.POST.get('tmpPK')
                
                videoTMPinfo = Audition_VideoTMP.objects.get(id = tmpPK)
                thumbnailURL = videoTMPinfo.thumbnailPATH
                inviteCode = videoTMPinfo.inviteCode
                s3VideoPATH = videoTMPinfo.videoPATH


            if hashTag == "":
                hashTag = None

            videoSubmit = Audition_video(
                userPK = userPK, 
                createAt = datetime.now(), 
                createAt_timestamp = str(round(time.time())), 
                thumbnailPATH = thumbnailURL, 
                videoPATH = inviteCode, 
                s3VideoPATH = s3VideoPATH,
                contents = contents, 
                hashTag = hashTag,
                viewable = viewable,
                categoryPK = categoryPK,
                # tournamentStatus = tournamentStatus,
                auditionListPK = auditionListPK,
                rewardRate = str(rewardRate),
                size = size,
                mention = mention,
                tag = tag
            )
            videoSubmit.save()
            
            videoPK = videoSubmit.id


            if mention:
                if ',' in mention:
                    mentionList = mention.split(',')
                else:
                    mentionList = [mention]
                # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                for index, i in enumerate(mentionList):
                    mentionListSubmit = Audition_MentionList(
                        loginUserPK = userPK,
                        userPK = i,
                        auditionListPK = auditionListPK,
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
                    tagListSubmit = Audition_TagList(
                        loginUserPK = userPK,
                        userPK = j,
                        auditionListPK = auditionListPK,
                        videoPK = videoPK,
                        createAt = datetime.now(),
                        createAt_timestamp = str(round(time.time()))
                    )
                    tagListSubmit.save()



            Audition_CountSubmit = Audition_Count(ownerPK = userPK, auditionListPK = auditionListPK, videoPK = videoPK, tournamentStatus = tournamentStatus)
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
    




# 멘션 최신 리스트
@csrf_exempt
def audition_latestMentionList(request):
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
    


# 오디션 최신 태그 리스트 & 유저 리스트
@csrf_exempt
def audition_latestTagList(request):
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
    



# 태그 검색 리스트
@csrf_exempt
def audition_searchTagList(request):
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
    


#  내가등록한 영상 정보 수정 페이지 이동
@csrf_exempt
def audition_myVideoListDetail_modiHtml(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        # # deviceVer = data['deviceVer']
        # versioninfo = Version.objects.get(id = 1)
        # aosVer = versioninfo.aos
        # iosVer = versioninfo.ios
        # if "1.2.9" == aosVer or "1.2.9" == iosVer:

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

        videoinfoList = [{
            'videoPK':videoPK,
            'videoPATH':videoPATH,
            'contents':contents,
            'hashTag':hashTag,
            'location':location,
            'mention':mentionList
        }]
        # videoinfoList = [videoPK, videoPATH, contents, hashTag, location, viewable]
            
        text = "\033[92m"+"audition_myVideoListDetail_modiHtml SUCCESS -> 내가 업로드한 비디오 리스트 Response"+"\033[0m"
        print("["+str(datetime.now())+"] " + text)
        context = {'code':'1', 'videoinfoList':videoinfoList, 'tagList':tagList}
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
            mention = request.POST.get('mention')
            tag = request.POST.get('tag')

            if status == "1":
            # rewardRate = request.POST.get('rewardRate')
            # reqFile = request.FILES
            # print("reqFile >>", reqFile)
            # if len(reqFile['file']) != 0:
                # bucketName = "showplus"     # ygbs
                bucketName = "showpluss3"     # showplus
                img = request.FILES['file']
                print("img >>>", img)


                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                inviteCode = inviteCode + ".jpg"
                # userinfoCount = Audition_video.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                # check = False
                # if userinfoCount == 0:
                #     pass
                # else:
                #     while check == False:
                #         inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 6))
                #         inviteCode = inviteCode + ".jpg"
                #         userinfoCount_check = SignUp.objects.filter(userPK = userPK, thumbnailPATH = inviteCode).count()
                #         if userinfoCount_check == 0:
                #             check = True
                #             break;

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                path = '/mnt/project/app/static/auditions/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


                # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
                # aws_secret_access_key = "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"        # ygbs

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
                    aws_secret_access_key = "q5nQCJ/PBR7XY/jHmZI8494GzWgoxUMMlkHMXHNK"      # showplus
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
                # 간혹 영상 업로드시 오류가있어 서버에 저장하는 부분 뺌
                # if not os.path.exists(path):
                #     os.makedirs(path)
                # if os.path.isfile(path +str(img)):
                #     os.remove(path +str(img))

                # file_path = path + str(img)
                # with open(file_path, 'wb+') as destination:
                #     for chunk in img.chunks():
                #         destination.write(chunk)
                # # 파일 객체가 닫힌 후에 작업 수행
                # with open(file_path, 'rb') as file:
                #     # 파일 읽기 등 추가 작업 수행
                #     data = file.read()
                #     # 예시: seek 작업 수행
                #     file.seek(0)
                #     # 추가 작업 수행            
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

                videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
                auditionListPK = videoinfo.auditionListPK
                if hashTag == "":
                    hashTag = None


                if mention:
                    if ',' in mention:
                        mentionList = mention.split(',')
                    else:
                        mentionList = [mention]
                    # userPK 변수명이 헷갈릴수도 있음 체크 잘 해야함
                    for index, i in enumerate(mentionList):
                        mentionListSubmit = Audition_MentionList(
                            loginUserPK = userPK,
                            userPK = i,
                            auditionListPK = auditionListPK,
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
                        tagListSubmit = Audition_TagList(
                            loginUserPK = userPK,
                            userPK = j,
                            auditionListPK = auditionListPK,
                            videoPK = videoPK,
                            createAt = datetime.now(),
                            createAt_timestamp = str(round(time.time()))
                        )
                        tagListSubmit.save()


                # videoinfo = Audition_video.objects.get(id = videoPK, userPK = userPK)
                videoinfo.createAt = datetime.now()
                videoinfo.createAt_timestamp = str(round(time.time()))
                videoinfo.contents = contents
                videoinfo.hashTag = hashTag
                videoinfo.location = location
                videoinfo.viewable = viewable
                videoinfo.status = "0"
                videoinfo.mention = mention
                videoinfo.tag = tag
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
    



# 오디션 공지 ( 오디션 진행 전 )
@csrf_exempt
def audition_noticeSave(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        userPK = data['userPK']
        contents = data['contents']


        Audition_NoticeSubmit = Audition_Notice(userPK = userPK, contents = contents, createAt = datetime.now())
        Audition_NoticeSubmit.save()


        text = "userPK값 : " + str(userPK) + ", 오디션 공지 등록"
        ment = "\033[92m"+"audition_notice SUCCESS -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'1'}
        return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_notice Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    

# 오디션 공지 ( 오디션 진행 전 )
@csrf_exempt
def audition_notice(request):
    try:

        Audition_NoticeCount = Audition_Notice.objects.filter(useYN = "Y").count()
        if Audition_NoticeCount == 0:
            text = "오디션 공지 없음"
            ment = "\033[92m"+"audition_notice SUCCESS -> "+text+"\033[0m"
            print("["+str(datetime.now())+"] " + ment + '\033[0m')
            context = {'code':'0'}
            return HttpResponse(json.dumps(context))
        else:
            if Audition_NoticeCount == 1:
                Audition_Noticeinfo = Audition_Notice.objects.get(useYN = "Y")
                contents = Audition_Noticeinfo.contents

                text = "오디션 공지 있음"
                ment = "\033[92m"+"audition_notice SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'1', 'contents':contents}
                return HttpResponse(json.dumps(context))
            
            else:
                text = "오디션 공지 있는데 2개이상?? 문제있음"
                ment = "\033[91m"+"audition_notice Exception ERROR -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')
                context = {'code':'9'}
                return HttpResponse(json.dumps(context))

    except Exception as e:
        text = str(e)
        ment = "\033[91m"+"audition_notice Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))











@csrf_exempt
def audition_tmpVideoUpload_originPATH(request):
    try:
        if request.method == 'POST':

            userPK = str(request.POST.get('loginUserPK'))
            reqFile = request.FILES
            print("reqFile >>", reqFile)
            if len(reqFile['file']) != 0:
                # bucketName = "showplus"     # ygbs
                # bucketName = "showpluss3"     # showplus
                bucketName = "showpluslambda" # showplus lambda 작업
                img = request.FILES['file']
                print("tmpVideoUpload_originPATH >>>", img)
                s3PATH = "https://showpluslambda.s3.ap-northeast-2.amazonaws.com/"
                accelerated_endpoint_url = "https://showpluslambda.s3-accelerate.amazonaws.com"
                
                inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                # inviteCode_thumbnail = inviteCode + ".jpg"
                audition_VideoCount = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                check = False
                if audition_VideoCount == 0:
                    pass
                else:
                    while check == False:
                        inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                        # inviteCode_thumbnail = inviteCode + ".jpg"
                        audition_VideoCount_check = Audition_video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                        if audition_VideoCount_check == 0:
                            check = True
                            break;

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                # path = '/mnt/project/app/static/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


                # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
                # aws_secret_access_key = "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"        # ygbs

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
                    aws_secret_access_key = "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",      # showplus
                    region_name = "ap-northeast-2"
                    # endpoint_url = accelerated_endpoint_url
                )

                s3_client.put_bucket_accelerate_configuration(
                    Bucket=bucketName,
                    AccelerateConfiguration={'Status': 'Enabled'}
                )


                # videoURL = 'input/videos/videos/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                videoURL = 'input/auditions/dev/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

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
                        # print("thumbnail_savePATH >>", thumbnail_savePATH)
                        cv2.imwrite(thumbnailPath + inviteCode + ".jpg", image)
                        break;
                vidcap.release()



                thumbnailURL = 'auditions/thumbnail/dev'+thumbnail_savePATH + ".jpg"
                thumbnailimg = thumbnailPath + inviteCode + ".jpg"
                with open(thumbnailimg, 'rb') as image_file:
                    s3_client.upload_fileobj(
                        image_file, 
                        bucketName, 
                        thumbnailURL, 
                        # ExtraArgs={
                        #     "ContentType": image_file.content_type
                        # }
                    )

                
                videoPATH = s3PATH+videoURL

                videoTMPinfoCount = Audition_VideoTMP.objects.filter(loginUserPK = userPK, status = "0").count()
                if videoTMPinfoCount == 0:
                    pass

                else:
                    videoTMPinfo = Audition_VideoTMP.objects.get(loginUserPK = userPK, status = "0")
                    videoTMPinfo.status = "9"
                    videoTMPinfo.save()

                videoTMP = Audition_VideoTMP(loginUserPK = userPK, videoPATH = videoPATH, thumbnailPATH = thumbnailURL, createAt = datetime.now(), createAt_timestamp = time.time(), inviteCode = inviteCode)
                videoTMP.save()

                tmpVideoPK = videoTMP.id


                text = "user PK값 : " + userPK + ", 동영상 저장 완료"
                ment = "\033[92m"+"audition_tmpVideoUpload_originPATH SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1', 'tmpVideoPK':tmpVideoPK}
                return HttpResponse(json.dumps(context, default=json_util.default))

            else:
                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"audition_tmpVideoUpload_originPATH WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
                


    except Exception as e: 
        text = str(e)
        ment = "\033[91m"+"audition_tmpVideoUpload_originPATH Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))
    






@csrf_exempt
def audition_tmpVideoUpload(request):
    try:
        if request.method == 'POST':

            userPK = str(request.POST.get('loginUserPK'))
            reqFile = request.FILES
            # print("reqFile >>", reqFile)
            if len(reqFile['file']) != 0:
                # bucketName = "showplus"     # ygbs
                # bucketName = "showpluss3"     # showplus
                bucketName = "showpluslambda" # showplus lambda 작업
                img = request.FILES['file']
                print("tmpVideoUpload >>>", img)
                tmpVideoPK = request.POST.get('tmpVideoPK')

                accelerated_endpoint_url = "https://showpluslambda.s3-accelerate.amazonaws.com"
                
                # inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                # # inviteCode = inviteCode + ".jpg"
                # videoinfoCount = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                # check = False
                # if videoinfoCount == 0:
                #     pass
                # else:
                #     while check == False:
                #         inviteCode = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits , 12))
                #         # inviteCode = inviteCode + ".jpg"
                #         videoinfoCount_check = Video.objects.filter(userPK = userPK, videoPATH = inviteCode).count()
                #         if videoinfoCount_check == 0:
                #             check = True
                #             break;

                videoTMPinfo = Audition_VideoTMP.objects.get(id = tmpVideoPK)
                inviteCode = videoTMPinfo.inviteCode

                now = datetime.now()
                year = str(now.year)
                month = str(now.month)
                day = str(now.day)

                # path = '/mnt/project/app/static/video/'+year+'/'+month+'/'+day+'/'+userPK+'/'


                # aws_access_key_id     = "AKIAVVO65WBXK4EDIYTZ",                           # ygbs
                # aws_secret_access_key = "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"        # ygbs

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id     = "AKIA4LOFJUC4HLMJ44JQ",                         # showplus
                    aws_secret_access_key = "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",      # showplus
                    region_name = "ap-northeast-2"
                    # endpoint_url = accelerated_endpoint_url
                )

                s3_client.put_bucket_accelerate_configuration(
                    Bucket=bucketName,
                    AccelerateConfiguration={'Status': 'Enabled'}
                )



                # videoURL = 'input/videos/videos/' +year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode
                tmpVideoURL = 'tmp/audition_videos/dev/'+year+'/'+month+'/'+day+'/'+userPK+'/' + inviteCode

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
                ment = "\033[92m"+"audition_tmpVideoUpload SUCCESS -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')

                context = {'code':'1', 'tmpVideoPATH':tmpVideoPATH}
                return HttpResponse(json.dumps(context, default=json_util.default))

            else:
                text = "user PK값 : " + userPK + ", 동영상이 파일이 안넘어옴"
                ment = "\033[93m"+"audition_tmpVideoUpload WARNING -> "+text+"\033[0m"
                print("["+str(datetime.now())+"] " + ment + '\033[0m')  
                context = {'code':'9'}
                return HttpResponse(json.dumps(context, default=json_util.default))
                


    except Exception as e: 
        text = str(e)
        ment = "\033[91m"+"audition_tmpVideoUpload Exception ERROR -> "+text+"\033[0m"
        print("["+str(datetime.now())+"] " + ment + '\033[0m')
        context = {'code':'99'}
        return HttpResponse(json.dumps(context))





# --------------------------------------------------------------------------------------------------------------------------------------
# SMS 테스트

# # AWS 자격 증명 설정 (AWS Management Console에서 얻은 자격 증명을 사용)
# aws_access_key_id = 'AKIA4LOFJUC4KVGL7Y4G'
# aws_secret_access_key = '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'
# region_name = 'ap-northeast-2'  # 예: 'us-east-1'

# # SNS 클라이언트 생성
# sns = boto3.client('sns', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# # 메시지 발송
# phone_number = '+821022239856'
# # phone_number = '+821022239856'  # 수신자 전화번호 (E.164 형식)
# topic_arn = 'arn:aws:sns:ap-northeast-2:849206681784:ShowPlus_SMS'
# message = 'Hello from AWS SNS!'
# response = sns.publish(PhoneNumber=phone_number, Message=message)
# # response = sns.publish(TopicArn=topic_arn, Message=message)

# print(response)

# --------------------------------------------------------------------------------------------------------------------------------------

# account_sid = "AC620d12d1fc9e0a364eda97c55580a2b4"
# auth_token  = "b3bc175dd2fa233c34fd6c4c77c197c4"
# client = Client(account_sid, auth_token)

# # 걸러진 전화번호를 저장하여 message API 사용
# # message = client.messages.create(to='+821022239856',from_="+821022239856",body="<메세지 내용>")
# # message = client.messages.create(body="블라블라",from_="+19475002669",to='+821022239856')
# text = "Show+ 문자인증 일이삼사오육칠팔구십 블라블라블라 인증코드는 [123456] 입니다"
# # message = client.messages.create(body=text,messaging_service_sid='MG629dfa16d0929dcf9c6e8c6c37046d32',from_="+19475002669",to='+821022239856')
# message = client.messages.create(body=text, from_="+12515720354",to='+821022239856')