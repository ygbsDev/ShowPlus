from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime



# 서버점검 체크
class serverStatus(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)    # 점검 상태 값 "0" == "운영", "1" == "점검"
    startDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 시작 일시
    endDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 종료 일시







# 유저 계정 정보
class SignUp(AbstractUser):
    password = models.CharField(max_length=255) # 비밀번호
    nickName = models.CharField(max_length=255, blank=True, null=True)  # 닉네임
    name = models.CharField(max_length=255, blank=True, null=True)	# 이름
    email = models.CharField(max_length=255) # 이메일
    phone_platform = models.CharField(max_length=255, blank=True, null=True) # 통신사
    phone = models.CharField(max_length=255) # 핸드폰번호
    profileIMG_path_tmp = models.CharField(max_length=255, blank=True, null=True) # 프로필 이미지 임시 저장 경로  ( ios 이미지 선택시 액박 이슈 )
    profileIMG_path = models.CharField(max_length=255, blank=True, null=True) # 프로필 이미지 경로
    point = models.CharField(max_length=255, blank=True, null=True, default="0") # 포인트 ( 스타캔디 )
    AboutMe = models.TextField(blank=True, null=True, verbose_name="Description")   # 자기소개
    link = models.CharField(max_length=255, blank=True, null=True) # 링크
    inviteCode = models.CharField(max_length=255, blank=True, null=True) # 초대코드
    CI = models.CharField(max_length=255, blank=True, null=True)	# 핸드폰인증 필수 값
    DI = models.CharField(max_length=255, blank=True, null=True)	# 핸드폰인증 필수 값
    grade = models.CharField(max_length=255, blank=True, null=True, default="0") # 0 == 일반회원, 1 == 스타회원 신청대기, 2 == 스타회원, 5 == 관리자 거절, 9 == 탈퇴
    notif_like = models.CharField(max_length=255, blank=True, null=True, default="Y")
    notif_coment = models.CharField(max_length=255, blank=True, null=True, default="Y")
    notif_following = models.CharField(max_length=255, blank=True, null=True, default="Y")
    notif_notice = models.CharField(max_length=255, blank=True, null=True, default="Y") 
    notif_benefits = models.CharField(max_length=255, blank=True, null=True, default="Y")
    authGroup = models.CharField(max_length=255, blank=True, null=True) # 관리자 권한( ** 추가 건 ** )
    fcmToken = models.CharField(max_length=255, blank=True, null=True)







# 유저 맴버쉽 리스트
class MembershipList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # 유저PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    endDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 종료 일시
    endDate_timestamp = models.CharField(max_length=255, blank=True, null=True) # 종료 일시 타임스탬프





# 포인트 입출금 내역
class PointHistory(models.Model):
    userPK_S = models.CharField(max_length=255, blank=True, null=True)    # 유저PK_Sender
    userPK_R = models.CharField(max_length=255, blank=True, null=True)    # 유저PK_Receiver
    videoPK = models.CharField(max_length=255, blank=True, null=True, default="0")
    point = models.CharField(max_length=255, blank=True, null=True)    # 유저PK_Receiver
    status = models.CharField(max_length=255, blank=True, null=True)    # "0" == "일반영상", "1" == "오디션영상", "2" == "기타"
    title = models.CharField(max_length=255, blank=True, null=True, default="0")    # 오디션 영상일때  auditionList title
    contentsStatus = models.CharField(max_length=255, blank=True, null=True)    # 입출금 내용
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    auditionListPK = models.CharField(max_length=255, blank=True, null=True, default="0")



# 포인트 입출금 상세 내용
class PointContentStatus(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)    # 입출금 내용 구분
    content = models.CharField(max_length=255, blank=True, null=True)    # 입출금 내용







# 유저 신고 리스트
class UserDeclarationList(models.Model):
    loginUserPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    declarationkUserPK = models.CharField(max_length=255, blank=True, null=True)    # 신고한 유저 pk
    comment = models.TextField(blank=True, null=True) # 차단 사유
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    chkYn = models.CharField(max_length=255, blank=True, null=True, default="N")


# 현재 앱 버전
class Version(models.Model):
    aos = models.CharField(max_length=255, blank=True, null=True)
    ios = models.CharField(max_length=255, blank=True, null=True)
    aos_review = models.CharField(max_length=255, blank=True, null=True)
    ios_review = models.CharField(max_length=255, blank=True, null=True)

# 현재 배포중인 version 페이지 체크
class VersionPage(models.Model):
    nowPage = models.CharField(max_length=255, blank=True, null=True)
    newPage = models.CharField(max_length=255, blank=True, null=True)



# s3 상태값
class S3Check(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)



# 유저 차단 리스트
class UserBlockList(models.Model):
    loginUserPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    blockUserPK = models.CharField(max_length=255, blank=True, null=True)    # 차단한 유저 pk
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="1")   # "0" == 차단 해제 / "1" == 차단





# 인앱결제 종류 리스트
class purchaseItemList(models.Model):
    productName = models.CharField(max_length=255, blank=True, null=True)    # 제품 이름
    productID = models.CharField(max_length=255, blank=True, null=True)    # 제품 ID
    point = models.CharField(max_length=255, blank=True, null=True)    # 스타 개수
    cash = models.CharField(max_length=255, blank=True, null=True)    # 현금
    candy = models.CharField(max_length=255, blank=True, null=True)     # 사탕 개수 ( front에서 이미지 개수 채킹으로 사용)ㄴ


# 인앱결제
class InapppurchaseList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    point = models.CharField(max_length=255, blank=True, null=True)    # 스타 개수
    cash = models.CharField(max_length=255, blank=True, null=True)    # 현금
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프







# 영상 신고 리스트
class VideoDeclarationList(models.Model):
    declarationUserPK = models.CharField(max_length=255, blank=True, null=True) # 신고자 (user PK)
    videoPK = models.CharField(max_length=255, blank=True, null=True) # 신고한 영상
    comment = models.CharField(max_length=255, blank=True, null=True) # 신고한 이유
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    chkYn = models.CharField(max_length=255, blank=True, null=True, default="N")

# 검색리스트
class SearchList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # 검색자
    searchContents = models.CharField(max_length=255, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    count = models.CharField(max_length=255, blank=True, null=True, default="1")     # 동일 유저가 같은 단어 검색 횟수 ( 현재는 필요없지만 혹시몰라 넣어둠 )
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "기본",  9 == "삭제"



# 추천콘텐츠 ( 일단 완전 일치 단어 2023.05.08)
class FeaturedContent(models.Model):
    contents = models.CharField(max_length=255, blank=True, null=True)
    count = models.CharField(max_length=255, blank=True, null=True, default="1")
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    


# 영상 조회수
class ViewCount(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프



# 영상 좋아요
class Like_video(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"


# 댓글 리스트
class Coment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True) # 작성자 (user PK )
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    contents = models.TextField(blank=True, null=True)                      # 내용
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 댓글 삭제 여부 9 == "삭제"


# 댓글 좋아요
class Like_coment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"


# 대댓글 리스트
class ComentOnComent(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    contents = models.TextField(blank=True, null=True)                      # 내용
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 댓글 삭제 여부 9 == "삭제"

# 대댓글 좋아요
class Like_comentONcoment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user Table PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video Table PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    comentONcomentPK = models.CharField(max_length=255, blank=True, null=True)  # ComentOnComent Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"


# 유저 이름 변경
class Modify_name(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    previousName = models.CharField(max_length=255, blank=True, null=True) # 이전 이름
    newName = models.CharField(max_length=255, blank=True, null=True)       # 신규 이름
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프


# 유저 아이디 변경
class Modify_username(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    previousUsername = models.CharField(max_length=255, blank=True, null=True) # 이전 아이디
    newUsername = models.CharField(max_length=255, blank=True, null=True)       # 신규 아이디
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프


# 유저 닉네임 변경
class Modify_userNick(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    previousUserNick = models.CharField(max_length=255, blank=True, null=True) # 이전 닉네임
    newUserNick = models.CharField(max_length=255, blank=True, null=True)       # 신규 닉네임
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프


# 카테고리 리스트
class CategoryList(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True) # 카테고리
    categoryImgPATH = models.CharField(max_length=255, blank=True, null=True) # 카테고리 이미지
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 카테고리 삭제 여부 상태값  "9" == 삭제
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프

# 토너먼트 상태 리스트
class TournamentStatusList(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True) # 상태
    statusNm = models.CharField(max_length=255, blank=True, null=True) # 상태이름



# 토너먼트 대결 구도 리스트
class VersusList(models.Model):
    userPK_left = models.CharField(max_length=255, blank=True, null=True)
    videoPK_left = models.CharField(max_length=255, blank=True, null=True)
    userPK_right = models.CharField(max_length=255, blank=True, null=True)
    videoPK_right = models.CharField(max_length=255, blank=True, null=True)
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    categoryPK = models.CharField(max_length=255, blank=True, null=True) # CategoryList PK
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="1") # 토너먼트 상태 ( 예선, 32강, 16강, 8강, 4강, 결승
    LLS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 좋아요 점수 ( Like Score ) == 좋아요 카운트 * 배점비율
    LCS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 댓글 점수 ( Coment Score )== 댓글 카운트 * 배점비율
    LVS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 조회수 점수 ( Viewcount Score ) == 조회수 카운트 * 배점비율
    LDS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 도네이션 점수 ( Donation Score ) == 도네이션 * 배점비율
    LAS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 총 점수 == LS + CS + VS + DS
    RLS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 좋아요 점수 ( Like Score ) == 좋아요 카운트 * 배점비율
    RCS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 댓글 점수 ( Coment Score )== 댓글 카운트 * 배점비율
    RVS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 조회수 점수 ( Viewcount Score ) == 조회수 카운트 * 배점비율
    RDS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 도네이션 점수 ( Donation Score ) == 도네이션 * 배점비율
    RAS = models.CharField(max_length=255, blank=True, null=True, default="0")        # 총 점수 == LS + CS + VS + DS






# 오디션 리스트 ( 오디션 기본 정보 )
class Audition_check(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 오디션 잠금 상태 "0" == "close", "1" == "open"

# 오디션 영상 제한 체크
class Audition_videoLimit(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 오디션 잠금 상태 "0" == "close", "1" == "open"





# 오디션 리스트 ( 오디션 기본 정보 )
class Audition_List(models.Model):
    categoryPK = models.CharField(max_length=255, blank=True, null=True) # CategoryList PK
    title = models.CharField(max_length=255, blank=True, null=True) # 상태
    auditionImgPATH = models.CharField(max_length=255, blank=True, null=True) # 오디션 이미지
    startAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 예선전 시작일시
    startAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 예선전 시작일시 타임스탬프
    endAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 토너먼트 종료 일시
    endAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 토너먼트 종료 일시 타임스탬프
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 토너먼트 상태 (모집중, 예선, 32강, 16강, 8강, 4강, 결승 )
    progressStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 0 =="대기중", 1 == "진행중", 2 == "집계중", 3 == "토너먼트 대진 종료", 9 == "토너먼트 완전 종료"
    useYn = models.CharField(max_length=255, blank=True, null=True, default="N") # Y == "활성화" ,  N == 비활성화
    content = models.TextField(blank=True, null=True) # 
    



# 오디션 상세 리스트 ( 오디션 토너먼트 별 상세 정보 )
class Audition_DetailList(models.Model):
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    startDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 시작 일시
    startDate_timestamp = models.CharField(max_length=255, blank=True, null=True) # 시작 일시 타임스탬프
    endDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 종료 일시
    endDate_timestamp = models.CharField(max_length=255, blank=True, null=True) # 종료 일시 타임스탬프
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 토너먼트 상태 (모집중, 예선, 32강, 16강, 8강, 4강, 결승 )
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    progressStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 0 =="대기중", 1 == "진행중", 2 == "집계중", 3 == "토너먼트 대진 종료", 9 == "토너먼트 완전 종료"




# 오디션 info count
class Audition_Count(models.Model):
    ownerPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    donation = models.CharField(max_length=255, blank=True, null=True, default="0")    # 후원
    like = models.CharField(max_length=255, blank=True, null=True, default="0")    # 좋아요
    coment = models.CharField(max_length=255, blank=True, null=True, default="0")    # 댓글
    viewcount = models.CharField(max_length=255, blank=True, null=True, default="0")    # 조회수
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0")    # 토너먼트 상태


# 오디션 후원 리스트
class Audition_DonationList(models.Model):
    sender_userPK = models.CharField(max_length=255, blank=True, null=True) # 후원자 (user PK )
    receiver_userPK = models.CharField(max_length=255, blank=True, null=True) # 후원받은자 (user PK )
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    amount = models.TextField(blank=True, null=True) # 수량
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    auditionListPK = models.CharField(max_length=255, blank=True, null=True) 
    categoryPK = models.CharField(max_length=255, blank=True, null=True) # CategoryList PK
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True) # 토너먼트 상태 ( 예선, 32강, 16강, 8강, 4강, 결승


# 오디션 영상 조회수
class Audition_ViewCount(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 토너먼트 상태 (모집중, 예선, 32강, 16강, 8강, 4강, 결승 )


# 오디션 영상 좋아요
class Audition_Like_video(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK ( 좋아요 누른사람 )
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 토너먼트 상태 (모집중, 예선, 32강, 16강, 8강, 4강, 결승 )


# 오디션 댓글 리스트
class Audition_Coment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True) # 작성자 (user PK )
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    contents = models.TextField(blank=True, null=True)                      # 내용
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 댓글 삭제 여부  5 == "유저가 신고",   9 == "삭제"
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    tournamentStatus = models.CharField(max_length=255, blank=True, null=True, default="0") # 토너먼트 상태 (모집중, 예선, 32강, 16강, 8강, 4강, 결승 )

# 오디션 댓글 좋아요
class Audition_Like_coment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"


# 오디션 대댓글 리스트
class Audition_ComentOnComent(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    contents = models.TextField(blank=True, null=True)                      # 내용
    status = models.CharField(max_length=255, blank=True, null=True, default="0") # 댓글 삭제 여부 9 == "삭제"


# 오디션 대댓글 좋아요
class Audition_Like_comentONcoment(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user Table PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video Table PK
    comentPK = models.CharField(max_length=255, blank=True, null=True)  # Coment Table PK
    comentONcomentPK = models.CharField(max_length=255, blank=True, null=True)  # ComentOnComent Table PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="0")    # 0 == "좋아요 끔",  1 == "좋아요 켬"

# 오디션 우승 리스트
class Audition_WinnerList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user Table PK
    auditionListPK = models.CharField(max_length=255, blank=True, null=True)
    categoryPK = models.CharField(max_length=255, blank=True, null=True) # CategoryList PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video Table PK
    LS = models.CharField(max_length=255, blank=True, null=True)        # 좋아요 점수 ( Like Score ) == 좋아요 카운트 * 배점비율
    CS = models.CharField(max_length=255, blank=True, null=True)        # 댓글 점수 ( Coment Score )== 댓글 카운트 * 배점비율
    VS = models.CharField(max_length=255, blank=True, null=True)        # 조회수 점수 ( Viewcount Score ) == 조회수 카운트 * 배점비율
    DS = models.CharField(max_length=255, blank=True, null=True)        # 도네이션 점수 ( Donation Score ) == 도네이션 * 배점비율
    AS = models.CharField(max_length=255, blank=True, null=True)        # 총 점수 == LS + CS + VS + DS
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    winnerPayments = models.CharField(max_length=255, blank=True, null=True, default="0")        # 우승상금


# 북마크
class BookmarkList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True)    # user PK
    videoPK = models.CharField(max_length=255, blank=True, null=True)    # video PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="1")    # 0 == "북마크 끔",  1 == "북마크 함"


# 후원 리스트
class DonationList(models.Model):
    sender_userPK = models.CharField(max_length=255, blank=True, null=True) # 후원자 (user PK )
    receiver_userPK = models.CharField(max_length=255, blank=True, null=True) # 후원받은자 (user PK )
    videoPK = models.CharField(max_length=255, blank=True, null=True)   # Video Table PK
    amount = models.TextField(blank=True, null=True) # 수량
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    


# 팔로우 리스트
class FollowList(models.Model):
    userPK = models.CharField(max_length=255, blank=True, null=True) # 팔로우 한 유저 PK ( 로그인 중인 유저 )
    followUserPK = models.CharField(max_length=255, blank=True, null=True) # 팔로우 받은 유저 PK
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프
    status = models.CharField(max_length=255, blank=True, null=True, default="1")    # 0 == "팔로우 해제",  1 == "팔로우"


# 권한정보 - 신규
class Auth(models.Model): 
    authId = models.CharField(max_length=255,  null=False) # 권한아이디
    authName = models.CharField(max_length=255,  null=False)  # 권한이름
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프

# 권한그룹정보 - 신규
class Auth_group(models.Model):
    authGroupName = models.CharField(max_length=255, null=False) # 그룹권한명
    status = models.CharField(max_length=255, null=False)  # 활성화여부
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프

# 권한그룹리스트정보 - 신규
class Auth_grouplist(models.Model):
    authId = models.CharField(max_length=255, null=False) # 권한아이디
    authGroupId = models.CharField(max_length=255, null=False)  # 그룹권한아이디
    createAt = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)  # 저장 일시
    createAt_timestamp = models.CharField(max_length=255, blank=True, null=True) # 저장 일시 타임스탬프






