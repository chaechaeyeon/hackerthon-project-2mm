from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

# group_router = DefaultRouter()
# group_router.register('groups', views.GroupListAPIView, basename='groups')

# groupDetail_router = SimpleRouter()
# groupDetail_router.register('group_detail', views.GroupDetailViewSet, basename='group_detail')
urlpatterns = [
    #로그인 
    path('api/login/', views.Loginview.as_view(), name='phone_login_view'),
    path('api/logout/', views.LogoutView.as_view(), name='phone_logout_view'),
    #회원가입 
    # path('username/', views.UsernameView.as_view(), name='username-view'),
    # path('phonenumber/', views.PhoneNumberView.as_view(), name='phone-number-view'),
    # path('password/', views.PasswordView.as_view(), name='password-view'),
    path('signup/', views.SingupView.as_view(), name='signup'),
    #

    path('group/', views.GroupListCreateView.as_view(), name='group-list-create'),
    path('group/<uuid:code>/', views.GroupDetailView.as_view(), name='group-detail'),
    #path('', include(group_router.urls)),
    #path('groups/', views.GroupListAPIView.as_view()),
    #path('groups/<uuid:group_pk>/', views.GroupDetailAPIView.as_view()),
    
    #path('groups/<uuid:gruop_pk>/', include(groupDetail_router.urls)),
    # path('groups/<uuid:group_code>/name/', views.GroupDataViewSet.as_view({'post': 'create_name'}), name='group-name'),
    # path('groups/<uuid:group_code>/profile/', views.GroupDataViewSet.as_view({'post': 'create_profile'}), name='group-profile'),
]
