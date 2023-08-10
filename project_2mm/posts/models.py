from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
import uuid
User = get_user_model()

# 게시글 데이터 저장 
class Post(models.Model) :
    content = models.TextField()
    image = models.ImageField(verbose_name="이미지", blank=True, null=True, upload_to='posts_img')
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    #writer =
    #like_count = 

# 앨범 데이터 저장 
class Album(models.Model) :
    # 수정 ) 나중에 로그인 구현되면 null 불가하도록 
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(verbose_name="이미지", upload_to='album_img')
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    test = models.TextField(verbose_name="테스트용", default="기본값")
# 사용자 그룹 관리 
class Group(models.Model) :
    name = models.CharField(verbose_name="모임명", max_length=24)
    #user = models.ManyToManyField()
    info = models.CharField(verbose_name="모임소개글", max_length=128, null=True, blank=True)
    code = models.UUIDField(primary_key=True, verbose_name="모임초대코드", default=uuid.uuid4, unique=True)
    profile = models.ImageField(verbose_name="모임이미지", upload_to='group_profile', null=True)
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4()
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# 사용자 정보 관리 
class UserInfo(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(verbose_name="프로필이미지", upload_to="user_profile", null=True, blank=True)
    # phoneNumber 필드 : 모듈 사용함 
    # phoneNumber = UserInfo.phone.as_e164 로 값을 가져오면 되어요 
    phone = PhoneNumberField(verbose_name="전화번호", max_length=15, unique=True, null=False, blank=False)
    def __str__(self):
        return str(self.id)