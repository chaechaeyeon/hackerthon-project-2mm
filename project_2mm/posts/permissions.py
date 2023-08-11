# #수정 삭제 권한 
# from rest_framework import permissions
# from .models import Post

# #게시글 생성 사용자만 해당 편지를 수정하거나 삭제할 수 있도록 권한 제어 
# class IsAuthorOrReadOnly(permissions.BasePermission): 
#     def has_object_permission(self, request, view, obj):
#         # 읽기 권한 모두 허용
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # 요청자 확인
#         return obj.writer == request.user