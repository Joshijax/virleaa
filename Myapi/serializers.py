from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Course_content, section_material, Tag, course_resource, Instructors, profile, course_progress, payments, payments_verify, request_course_model, Comments, Reviews, feedback
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver
from Myapi.models import Category, Certificate, Certificatess
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models import Avg, Count, Sum


class course_progressSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = course_progress
        
        fields = ('content', 'course', 'steps', 'progress', 'Last_time', 'completed_time', 'url')

class commentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Comments
        
        fields = ('course', 'user', 'text', 'date_time', 'url')

class reviewSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Reviews
        
        fields = ('user', 'text', 'date_time', 'url')


class course_paymentteSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = payments
        
        fields = ('user', 'course', 'success', 'amount', 'ref_num', 'url')

class course_certificateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Certificatess
        
        fields = ('contents', 'name', 'data', 'url')

class payment_verifySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = payments_verify
        
        fields = ( 'pd_amount', 'txt_ref', 'flw_ref')

class Course_request(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = request_course_model
        
        fields = ( 'url', 'user', 'course_name', 'description', 'duration', 'section_number', 'extra', 'read', 'approved')

    # def save(self):
    #     pd_amount = self.validated_data['pd_amount']
    #     txt_ref = self.validated_data['txt_ref']
    #     flw_ref = self.validated_data['flw_ref']
    #     send_email(from=email, message=message)

class course_certificateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Certificatess
        
        fields = ('contents', 'name', 'data', 'url')


class profileSerializer(serializers.HyperlinkedModelSerializer):
    certi_courses = course_certificateSerializer(many=True, read_only=True)
    courses = course_progressSerializer(many=True, read_only=True)
    class Meta:
        model = profile
        fields = ('photo_file','user', 'name', 'About', 'email', 'phone', 'instructor', 'institution', 'courses', 'url', 'certi_courses')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='UserViewSet')
    profile = profileSerializer(required=True)
    class Meta:
        model = User
        
        fields = ('id', 'username', 'first_name', 'last_name', 'profile', 'url')
        depth = 2



# class UserSerializer(serializers.ModelSerializer):
#     url = serializers.HyperlinkedRelatedField(view_name='api:userprofile-detail',
#                                               source='profile')


# class UserSerializer(serializers.ModelSerializer):
    

#     class Meta:
#         model = User
#         fields = ['username', 'email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)

    password = serializers.CharField(required=True, write_only=True)
    instructor = serializers.BooleanField(required=False, write_only=True)
    institution = serializers.BooleanField(required=False, write_only=True)




class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    instructor = serializers.BooleanField(required=False, write_only=True)
    institution = serializers.BooleanField(required=False, write_only=True)


    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        profile = user.profile
        
        profile.institution = self.validated_data.get('institution', '')
        profile.instructor = self.validated_data.get('instructor', '')
        profile.save()
        user.save()
        return user

class tagSerializer(serializers.HyperlinkedModelSerializer):
    # def to_representation(self, value):
        
    #     return 'word' + ':' +'%s' % ( value.word)
    class Meta:
        model = Tag
        fields = ('url','word',)
        depth = 2


class CategorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = ['id', 'category', 'url']
        

# class tagsSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Tag
#         fields = ('word',)

 

class instructorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=True, read_only=False)
    class Meta:
        model = Instructors
        fields = ('url','user','name',)

class CertificateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Certificate 
        fields = ('url','name','data', 'file')
        


class tagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # def to_representation(self, value):
        
    #     return 'word: %s' % ( value.word)
    class Meta:
        model = Tag
        fields = ('id', 'word',)
        depth = 2


 

class section_materialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = section_material
        fields = ('id', 'url', 'file', 'file_name', 'content')

class feedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = feedback
        fields = ('user', 'item', 'rating', 'comment')


class Course_resourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = course_resource
        fields = ('id', 'url', 'file', 'file_name', 'course')

class Course_contentSerializer(serializers.HyperlinkedModelSerializer):
    section_material = section_materialSerializer(many=True, read_only=True)
    class Meta:
        model = Course_content
        
        fields = ('id', 'url', 'section_title', 'content', 'section_material', 'created_date')



class CourseSerializer(serializers.HyperlinkedModelSerializer):
    course_content = Course_contentSerializer(many=True, read_only=True)
    course_resourse = Course_resourceSerializer(many=True, read_only=True)
    # rating = feedbackSerializer(many=True, read_only=False)
    # test = serializers.SerializerMethodField()
    # tags = tagSerializer(many=True, read_only=False)
    # tags=tagSerializer(many=True, read_only=False)
    class Meta: 
        model = Course
        fields = ('id', 'url', 'Course_category', 'Course_category_type', 'Course_name', 'Course_duration', 'description', 'file', 'About_course', 'amount', 'course_content','instructors', 'institution', 'certificate_name', 'published', 'tags', 'course_resourse', 'steps','created_date', 'certificate')

    # def get_test(self, obj):
    #     if obj.rating.exists():
    #         obj2 = feedback.objects.filter(item=obj).values('rating').aggregate(Avg('rating'))
            
    #         return obj2
    #     else:
    #         return 0

    # def get_rating_count(self, obj):
    #     if obj.rating.exists():
    #         return obj.rating.first().count
    #     else:
    #         return 0


class Course_listSerializer1(serializers.HyperlinkedModelSerializer):
    course_content = Course_contentSerializer(many=True, read_only=True)
    course_resourse = Course_resourceSerializer(many=True, read_only=True)
    institution = UserSerializer(many=True, read_only=True)
    instructors = UserSerializer(many=True, read_only=True)
    # tags = tagSerializer(many=True, read_only=False)
    tags=tagSerializer(many=True, read_only=False)
    Course_category = CategorySerializer(many=True, read_only=True)
    # tags = serializers.HyperlinkedIdentityField(view_name='TagView', format='html')
    # serializers.StringRelatedField(many=True)
    # tags = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='word'
    #  )
    
    class Meta:
        model = Course
        fields = ('id', 'url', 'Course_category', 'Course_category_type', 'Course_name', 'Course_duration', 'description', 'file', 'About_course', 'amount', 'course_content','instructors', 'institution', 'certificate_name', 'published', 'tags', 'course_resourse','created_date')
        

        def create(self, validated_data):
            ingredients_data = validated_data.pop('tags')
            recipe = Course.objects.create(**validated_data)
            for ingredient_data in ingredients_data:
                Tag.objects.create(**ingredient_data)
            return recipe
        

