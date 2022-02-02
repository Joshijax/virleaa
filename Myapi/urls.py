from django.urls import path , include
from . import views, views1
from django.conf.urls import url
from rest_framework import routers
from .models import Course, Course_content, section_material, Tag, course_resource, Instructors, profile
from .serializers import CourseSerializer, Course_contentSerializer, section_materialSerializer, tagSerializer, tagsSerializer, Course_resourceSerializer, instructorSerializer, UserSerializer,profileSerializer, Course_listSerializer1
from rest_framework import generics


router1 = routers.DefaultRouter()
router = routers.DefaultRouter()
# router1.register('coursess', views.CourseView_sett)
router.register('Course', views.CourseView)

router.register('Course_section', views.Course_sectionView)
router.register('section_material', views.section_materialView)
router.register('course-resourse', views.Course_resourse)
router.register('tags', views.TagView)
router.register('add_instructor', views.Instructor_view)
router.register('users', views.UserViewSet)
router.register('profile', views.profileView)
router.register('couse_profile', views.Course_profileView)
router.register('certificate', views.CertificateView)
router.register('category', views.CategoryView)
router.register('user_certi', views.user_certiView)
router.register('payments', views.paymentView)
router.register('comments', views.comment_requestView)
router.register('reviews', views.review_requestView)
router.register('request_course', views.course_requestView)
router.register('feedback', views.feedbackView)
router.register(r'usersss', views.courseViewSet, basename='userss')

urlpatterns = router1.urls

urlpatterns = [
    path('', include(router.urls)),
    path('list/', include(router1.urls)),
    path('Virlearners-confirm/', views.email_confirmed, name='confirmed'),
    path('sample/', views.payPageView.as_view(), name='sample'),
    # path('courseList/', generics.ListCreateAPIView.as_view(queryset=Course.objects.all(), serializer_class=Course_listSerializer1), name='Courses-list')
    path('courseList/', views.CourseList.as_view(), name='Courses-list'),
    path('payment_verify/', views.verifyViewSet.as_view(), name='paynent'),
    path('instructor/', views.UserViewSet1.as_view(), name='Instructor'),
    path('institution/', views.UserViewSet2.as_view(), name='Instructor'),
    path('rest-auth/staff/login/', views1.LoginView.as_view(), name='stafflogin')
]
  