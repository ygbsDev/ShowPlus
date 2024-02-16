# chat/urls.py
from django.urls import path
from . import views_v1, audition_views_v1
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('', views_v1.index, name='index'),

    path('mainBanner', views_v1.mainBanner, name='mainBanner'),
    

    path('signup', views_v1.signup, name='signup'),
	path('login', views_v1.login, name='login'),
    path('signup_usernameCheck', views_v1.signup_usernameCheck, name='signup_usernameCheck'),
    path('changePW_phoneConfirm', views_v1.changePW_phoneConfirm, name='changePW_phoneConfirm'),
    path('changePW', views_v1.changePW, name='changePW'),
    
    path('appVersionCheck', views_v1.appVersionCheck, name='appVersionCheck'),

	path('fileupload', views_v1.fileupload, name='fileupload'),
	path('videoLike', views_v1.videoLike, name='videoLike'),
    # path('comentCheck', views_v1.comentCheck, name='comentCheck'),
    path('comentList', views_v1.comentList, name='comentList'),
    path('comentSubmit', views_v1.comentSubmit, name='comentSubmit'),
    path('comentDel', views_v1.comentDel, name='comentDel'),
    path('comentONcomentList', views_v1.comentONcomentList, name='comentONcomentList'),
    path('videoViewCount', views_v1.videoViewCount, name='videoViewCount'),
    
	path('videoList', views_v1.videoList, name='videoList'),
    path('videoListMove', views_v1.videoListMove, name='videoListMove'),
    
    path('comentLike', views_v1.comentLike, name='comentLike'),
    path('comentONcomentSubmit', views_v1.comentONcomentSubmit, name='comentONcomentSubmit'),
    path('comentONcomentDel', views_v1.comentONcomentDel, name='comentONcomentDel'),
    path('comentONcomentLike', views_v1.comentONcomentLike, name='comentONcomentLike'),
    
	path('myProfile', views_v1.myProfile, name='myProfile'),
    path('myProfile_videoDetail', views_v1.myProfile_videoDetail, name='myProfile_videoDetail'),
    path('myProfile_modifyinfo', views_v1.myProfile_modifyinfo, name='myProfile_modifyinfo'),
    
    path('modify_name', views_v1.modify_name, name='modify_name'),
    path('modify_username', views_v1.modify_username, name='modify_username'),
    path('modify_AboutMe', views_v1.modify_AboutMe, name='modify_AboutMe'),
    path('modify_link', views_v1.modify_link, name='modify_link'),
    
    path('modify_profileIMG_tmp', views_v1.modify_profileIMG_tmp, name='modify_profileIMG_tmp'),
    path('modify_profileIMG_tmpDel', views_v1.modify_profileIMG_tmpDel, name='modify_profileIMG_tmpDel'),
    path('modify_profileIMG', views_v1.modify_profileIMG, name='modify_profileIMG'),




    path('userProfile', views_v1.userProfile, name='userProfile'),

    path('userProfile_videoListTab', views_v1.userProfile_videoListTab, name='userProfile_videoListTab'),

    path('userProfile_videoDetail', views_v1.userProfile_videoDetail, name='userProfile_videoDetail'),

    path('userProfile_auditionVideoTab', views_v1.userProfile_auditionVideoTab, name='userProfile_auditionVideoTab'),
    path('userProfile_auditionVideoDetail', views_v1.userProfile_auditionVideoDetail, name='userProfile_auditionVideoDetail'),
    
    




    path('modify_name_check', views_v1.modify_name_check, name='modify_name_check'),
    path('modify_username_check', views_v1.modify_username_check, name='modify_username_check'),
    
    path('signup_nickNameCheck', views_v1.signup_nickNameCheck, name='signup_nickNameCheck'),
    path('modify_userNick_check', views_v1.modify_userNick_check, name='modify_userNick_check'),
    path('modify_userNick', views_v1.modify_userNick, name='modify_userNick'),
    
    path('signup_CIDICheck', views_v1.signup_CIDICheck, name='signup_CIDICheck'),
    path('videoOwner_comentDel', views_v1.videoOwner_comentDel, name='videoOwner_comentDel'),
    # path('tournamentList', views_v1.tournamentList, name='tournamentList'),
    path('videoOwner_comentONcomentDel', views_v1.videoOwner_comentONcomentDel, name='videoOwner_comentONcomentDel'),
    
    
    path('searchHtml', views_v1.searchHtml, name='searchHtml'),
    path('searchListDel', views_v1.searchListDel, name='searchListDel'),
    path('contentsSearch', views_v1.contentsSearch, name='contentsSearch'),
    path('contentsSearchMove', views_v1.contentsSearchMove, name='contentsSearchMove'),
    
    path('contentsSearchDetailListMove', views_v1.contentsSearchDetailListMove, name='contentsSearchDetailListMove'),
    
    path('featuredSearch', views_v1.featuredSearch, name='featuredSearch'),

    path('updateUserinfo', views_v1.updateUserinfo, name='updateUserinfo'),

    

    path('purchaselist', views_v1.purchaselist, name='purchaselist'),

    path('inapppurchase', views_v1.inapppurchase, name='inapppurchase'),

    path('findusername_phoneCheck', views_v1.findusername_phoneCheck, name='findusername_phoneCheck'),
    path('findusername_CIDICheck', views_v1.findusername_CIDICheck, name='findusername_CIDICheck'),


    path('settings_modiPhoneNum', views_v1.settings_modiPhoneNum, name='settings_modiPhoneNum'),
    path('changePW_check', views_v1.changePW_check, name='changePW_check'),
    path('settings_pwCheck', views_v1.settings_pwCheck, name='settings_pwCheck'),
    path('settings_changePW', views_v1.settings_changePW, name='settings_changePW'),
    path('settings_changeMembership', views_v1.settings_changeMembership, name='settings_changeMembership'),
    path('settings_userSignOut_starCheck', views_v1.settings_userSignOut_starCheck, name='settings_userSignOut_starCheck'),
    path('settings_userSignOut', views_v1.settings_userSignOut, name='settings_userSignOut'),

    path('videoDeclaration', views_v1.videoDeclaration, name='videoDeclaration'),

    path('myVideoList', views_v1.myVideoList, name='myVideoList'),
    path('myVideoListDetail', views_v1.myVideoListDetail, name='myVideoListDetail'),
    path('myVideoListDetail_modiHtml', views_v1.myVideoListDetail_modiHtml, name='myVideoListDetail_modiHtml'),
    path('myVideoListDetail_modi', views_v1.myVideoListDetail_modi, name='myVideoListDetail_modi'),
    path('myVideoDel', views_v1.myVideoDel, name='myVideoDel'),

    path('myProfile_videoListTab', views_v1.myProfile_videoListTab, name='myProfile_videoListTab'),
    path('myProfile_auditionVideoTab', views_v1.myProfile_auditionVideoTab, name='myProfile_auditionVideoTab'),
    path('myProfile_auditionVideoDetail', views_v1.myProfile_auditionVideoDetail, name='myProfile_auditionVideoDetail'),
    
    


    path('donetion', views_v1.donetion, name='donetion'),
    path('donetionList', views_v1.donetionList, name='donetionList'),

    
    
    path('userBlock', views_v1.userBlock, name='userBlock'),
    path('userBlockList', views_v1.userBlockList, name='userBlockList'),
    path('userDeclaration', views_v1.userDeclaration, name='userDeclaration'),
    
    path('pointHistory', views_v1.pointHistory, name='pointHistory'),
    



	path('auditionHtml', audition_views_v1.auditionHtml, name='auditionHtml'),
    path('audition_uploadCheck', audition_views_v1.audition_uploadCheck, name='audition_uploadCheck'),
	path('audition_fileupload', audition_views_v1.audition_fileupload, name='audition_fileupload'),
    path('audition_videoList', audition_views_v1.audition_videoList, name='audition_videoList'),
    path('audition_winnerPoint', audition_views_v1.audition_winnerPoint, name='audition_winnerPoint'),
    path('audition_videoListMove', audition_views_v1.audition_videoListMove, name='audition_videoListMove'),
    path('audition_DetailListMove', audition_views_v1.audition_DetailListMove, name='audition_DetailListMove'),
    path('audition_aggregatingList', audition_views_v1.audition_aggregatingList, name='audition_aggregatingList'),
    path('audition_donetion', audition_views_v1.audition_donetion, name='audition_donetion'),
    path('audition_videoViewCount', audition_views_v1.audition_videoViewCount, name='audition_videoViewCount'),
    path('audition_videoLike', audition_views_v1.audition_videoLike, name='audition_videoLike'),
    path('audition_comentList', audition_views_v1.audition_comentList, name='audition_comentList'),
    path('audition_comentSubmit', audition_views_v1.audition_comentSubmit, name='audition_comentSubmit'),
    path('audition_comentLike', audition_views_v1.audition_comentLike, name='audition_comentLike'),
    path('audition_comentONcomentList', audition_views_v1.audition_comentONcomentList, name='audition_comentONcomentList'),
    path('audition_comentONcomentSubmit', audition_views_v1.audition_comentONcomentSubmit, name='audition_comentONcomentSubmit'),
    path('audition_comentONcomentLike', audition_views_v1.audition_comentONcomentLike, name='audition_comentONcomentLike'),

    path('auditionMainHtml', audition_views_v1.auditionMainHtml, name='auditionMainHtml'),
    path('audition_categoryList', audition_views_v1.audition_categoryList, name='audition_categoryList'),
    path('audition_auditionList', audition_views_v1.audition_auditionList, name='audition_auditionList'),
    path('audition_matchesList', audition_views_v1.audition_matchesList, name='audition_matchesList'),
    path('audition_matchesListDetail', audition_views_v1.audition_matchesListDetail, name='audition_matchesListDetail'),
    path('audition_previousMatcheslist', audition_views_v1.audition_previousMatcheslist, name='audition_previousMatcheslist'),

    
    path('audition_myVideoList', audition_views_v1.audition_myVideoList, name='audition_myVideoList'),
    path('audition_myVideoListDetail', audition_views_v1.audition_myVideoListDetail, name='audition_myVideoListDetail'),
    path('audition_myVideoListDetail_modiHtml', audition_views_v1.audition_myVideoListDetail_modiHtml, name='audition_myVideoListDetail_modiHtml'),
    path('audition_myVideoListDetail_modi', audition_views_v1.audition_myVideoListDetail_modi, name='audition_myVideoListDetail_modi'),
    path('audition_myVideoDel', audition_views_v1.audition_myVideoDel, name='audition_myVideoDel'),

    
    path('audition_StatusCheck', audition_views_v1.audition_StatusCheck, name='audition_StatusCheck'),
    path('audition_EndList', audition_views_v1.audition_EndList, name='audition_EndList'),
    path('audition_EndListDetail', audition_views_v1.audition_EndListDetail, name='audition_EndListDetail'),
    path('audition_WinnerVideoDetail', audition_views_v1.audition_WinnerVideoDetail, name='audition_WinnerVideoDetail'),

    # 2023-07-28
    path('audition_contentDetailPop', audition_views_v1.audition_contentDetailPop, name='audition_contentDetailPop'),
    path('audition_check', audition_views_v1.audition_check, name='audition_check'),



    # path('testAAAAA', views_v1.testAAAAA, name='testAAAAA'),
    
    path('test33', views_v1.test33, name='test33'),
    path('fileupload_test', views_v1.fileupload_test, name='fileupload_test'),
    path('fileupload_test2', views_v1.fileupload_test2, name='fileupload_test2'),
    
    # path('searchTest', views_v1.searchTest, name='searchTest'),
    path('testttt333', views_v1.testttt333, name='testttt333'),
    
    path('dev_auditionSubmit', audition_views_v1.dev_auditionSubmit, name='dev_auditionSubmit'),
    

    path('testFunction', audition_views_v1.testFunction, name='testFunction'),
    


    # ======================================================================================================================================================================================================================
    # 2차 개발

    path('follow', views_v1.follow, name='follow'),
    path('myProfile_followingList', views_v1.myProfile_followingList, name='myProfile_followingList'),
    path('myProfile_followerList', views_v1.myProfile_followerList, name='myProfile_followerList'),

    path('userProfile_followingList', views_v1.userProfile_followingList, name='userProfile_followingList'),
    path('userProfile_followerList', views_v1.userProfile_followerList, name='userProfile_followerList'),

    path('myfollowVideoList', views_v1.myfollowVideoList, name='myfollowVideoList'),
    path('myfollowVideoListMove', views_v1.myfollowVideoListMove, name='myfollowVideoListMove'),
    
    path('audition_commentDeclaration', audition_views_v1.audition_commentDeclaration, name='audition_commentDeclaration'),
    path('audition_commentCommentDeclaration', audition_views_v1.audition_commentCommentDeclaration, name='audition_commentCommentDeclaration'),

    path('myProfile_blockList', views_v1.myProfile_blockList, name='myProfile_blockList'),


    path('locationSearchList', views_v1.locationSearchList, name='locationSearchList'),


    path('latestMentionList', views_v1.latestMentionList, name='latestMentionList'),
    path('latestTagList', views_v1.latestTagList, name='latestTagList'),

    path('searchTagList', views_v1.searchTagList, name='searchTagList'),
    path('myProfile_tagListTab', views_v1.myProfile_tagListTab, name='myProfile_tagListTab'),
    


    path('audition_latestMentionList', audition_views_v1.audition_latestMentionList, name='audition_latestMentionList'),
    path('audition_latestTagList', audition_views_v1.audition_latestTagList, name='audition_latestTagList'),
    path('audition_searchTagList', audition_views_v1.audition_searchTagList, name='audition_searchTagList'),

    
    path('audition_noticeSave', audition_views_v1.audition_noticeSave, name='audition_noticeSave'),
    path('audition_notice', audition_views_v1.audition_notice, name='audition_notice'),


    path('phoneAuthCode', views_v1.phoneAuthCode, name='phoneAuthCode'),
    path('findusername_phoneAuthCode', views_v1.findusername_phoneAuthCode, name='findusername_phoneAuthCode'),

    path('tmpVideoUpload_originPATH', views_v1.tmpVideoUpload_originPATH, name='tmpVideoUpload_originPATH'),
    path('tmpVideoUpload', views_v1.tmpVideoUpload, name='tmpVideoUpload'),

    
    path('audition_tmpVideoUpload_originPATH', audition_views_v1.audition_tmpVideoUpload_originPATH, name='audition_tmpVideoUpload_originPATH'),
    path('audition_tmpVideoUpload', audition_views_v1.audition_tmpVideoUpload, name='audition_tmpVideoUpload'),

    path('changePW_phoneAuthCode', views_v1.changePW_phoneAuthCode, name='changePW_phoneAuthCode'),
    path('myProfile_AlimList', views_v1.myProfile_AlimList, name='myProfile_AlimList'),
    path('settings_notifLike', views_v1.settings_notifLike, name='settings_notifLike'),
    path('settings_notifiFollowing', views_v1.settings_notifiFollowing, name='settings_notifiFollowing'),




]