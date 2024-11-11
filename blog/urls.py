from . import views
from django.urls import path

urlpatterns = [
    # 调用Views中类视图 MoreArticles 的 .as_view() 方法，将其转化为可调用的视图
    # 在大多数情况下，应始终使用 .as_view() 方法来引用类视图。这是 Django 的标准做法，确保视图能够正确初始化并响应 HTTP 请求
    path('more-articles/', views.MoreArticles.as_view(), name='more_articles'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('', views.PostList.as_view(), name='home'),
]
