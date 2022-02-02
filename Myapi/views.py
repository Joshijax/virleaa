from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import Course, Course_content, section_material, Tag, course_resource, Instructors, profile, course_progress, Certificate, payments, payments_verify, request_course_model, Comments, Reviews, feedback
from .serializers import CourseSerializer, Course_contentSerializer, section_materialSerializer, tagSerializer, tagsSerializer, Course_resourceSerializer, instructorSerializer, UserSerializer,profileSerializer, Course_listSerializer1, CategorySerializer, course_progressSerializer, LoginSerializer, CertificateSerializer, course_paymentteSerializer, payment_verifySerializer, Course_request, commentSerializer, reviewSerializer, feedbackSerializer
from rest_framework.decorators import api_view, permission_classes
from allauth.account.views import logout
from django.http import HttpResponse
from django.contrib.auth.models import AbstractUser, User
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from Myapi.models import Category, Certificatess
from rest_framework import parsers, renderers
from rest_framework.pagination import PageNumberPagination
from Myapi.serializers import course_certificateSerializer
from django.views.generic.base import TemplateView
from django.conf import settings
from django.utils.crypto import get_random_string
from ravepay.views import verify_payment_api
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins



class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['Course_name', 'Course_category__category', 'Course_category_type', 'tags__word']
    pagination_class =  PageNumberPagination

class CertificateView(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    pagination_class = None

class paymentView(viewsets.ModelViewSet):
    queryset = payments.objects.all()
    serializer_class = course_paymentteSerializer
    pagination_class = None

class feedbackView(viewsets.ModelViewSet):
    queryset = feedback.objects.all()
    serializer_class = feedbackSerializer
    pagination_class = None

class course_requestView(viewsets.ModelViewSet):
    queryset = request_course_model.objects.all()
    serializer_class = Course_request
    pagination_class = None

class comment_requestView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = commentSerializer
    pagination_class = None

class review_requestView(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = reviewSerializer
    pagination_class = None
     

class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = Course_listSerializer1
    filter_backends = [SearchFilter]
    search_fields = ['Course_name', 'Course_category__category', 'Course_category_type', 'tags__word']
    pagination_class = None
    
class courseViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Course.objects.all()
        serializer = Course_listSerializer1(request, queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = Course_listSerializer1(user)
        return Response(serializer.data)

class CourseView_sett(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = Course_listSerializer1
    filter_backends = [SearchFilter]
    search_fields = ['Course_name', 'Course_category', 'Course_category_type', 'tags__word']
    pagination_class = None


class Course_sectionView(viewsets.ModelViewSet):
    queryset = Course_content.objects.all()
    serializer_class = Course_contentSerializer
    pagination_class = None

class Course_resourse(viewsets.ModelViewSet):
    queryset = course_resource.objects.all()
    serializer_class = Course_resourceSerializer
    pagination_class = None

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class Instructor_view(viewsets.ModelViewSet):
    queryset = Instructors.objects.all()
    serializer_class = instructorSerializer
    pagination_class = None

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = tagsSerializer
    pagination_class = None

class section_materialView(viewsets.ModelViewSet):
    queryset = section_material.objects.all()
    serializer_class = section_materialSerializer
    pagination_class = None
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ['profile__instructor', 'profile__institution']
    pagination_class = None

class UserViewSet1(generics.ListAPIView):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    
    queryset = User.objects.filter(profile__instructor = True)
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ['profile__instructor', 'profile__institution']
    pagination_class = None

class UserViewSet2(generics.ListAPIView):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    
    queryset = User.objects.filter(profile__institution = True)
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ['profile__instructor', 'profile__institution']
    pagination_class = None

class profileView(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    queryset = profile.objects.all()
    serializer_class = profileSerializer
    pagination_class = None

class Course_profileView(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    queryset = course_progress.objects.all()
    serializer_class = course_progressSerializer
    pagination_class = None

class user_certiView(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions
    """
    queryset = Certificatess.objects.all()
    serializer_class = course_certificateSerializer
    pagination_class = None



@api_view(['POST',])
def api_newUser(request):
    if request.method == 'POST':
        serializer = payment_verifySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            confirm = verify_payment_api(user.txt_ref, user.flw_ref, user.amount)
            print(confirm)

            
        else:
            data = serializer.errors
        return Response(data)

class verifyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = payments_verify.objects.all()
    serializer_class = payment_verifySerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
        
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = payment_verifySerializer(request.data)

    #     print(request.data)
    #     print(user.txt_ref)
    #     confirm = verify_payment_api(user.txt_ref, user.flw_ref, user.pd_amount)
    #     print(confirm)
    #     return self.create(request, *args, **kwargs)

    # def get(self, request, format=None):
    #     snippets = payments_verify.objects.all()
    #     serializer = payment_verifySerializer(request, snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = payment_verifySerializer(data=request.data, context={'request': request})
        print(request.POST['txt_ref'])
        data = {}
        if serializer.is_valid():
            
            confirm = verify_payment_api(request.POST['txt_ref'], request.POST['flw_ref'], request.POST['pd_amount'])
            print(confirm)
            if confirm == 'success':
                data['success'] = 'Payments was successful'
                serializer.save()
                return Response(data=data)
                
            data['error'] = 'Verification Error'
            return Response(data=data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
def email_confirmed(request):
    
    return render(request, 'confirm_email.html')

def sampler(request):
    
    return render(request, 'sample.html') 



class payPageView(TemplateView):
    template_name = 'sample1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_ref = get_random_string().upper()
        if settings.RAVE_SANDBOX:
            context['key'] = settings.RAVE_SANDBOX_PUBLIC_KEY
        else:
            context['key'] = settings.RAVE_PRODUCTION_PUBLIC_KEY
        context['txref'] = new_ref
        context['amount'] = float(50)
        print(context['amount'])
        return context
        