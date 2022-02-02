from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os
from datetime import timedelta
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save, post_delete, post_init
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from io import BytesIO
from PIL import Image
from django.core.files import File
from star_ratings.models import Rating
from phone_field import PhoneField
from django.db.models import Avg

# Create your models here.

def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=50) 
    new_image = File(im_io, name=image.name)
    return new_image


def user_directory_path(instance, file, **kwargs):
    file_path = 'gallery/{username}/{filename}'.format( username = str(instance.file_name), filename=file)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return file_path

def course_step(instance, **kwargs):
   
    return instance.course.steps

def user_directory_path1(instance, file, **kwargs):
    file_path = 'gallery/{course}/{filename}'.format( course = str(instance.Course_name), filename=file)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return file_path

def user_directory_path2(instance, file, **kwargs):
    file_path = 'gallery/{course}/{filename}'.format( course = str(instance.user.first_name), filename=file)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return file_path

def user_directory_path3(instance, file, **kwargs):
    file_path = 'gallery/certificate/{filename}'.format(filename=file)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return file_path

class Tag(models.Model):
    word        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
    def __unicode__(self):
        return self.word

class Category(models.Model):
    category        = models.CharField(max_length=35)
    created_at  = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.category
    def __unicode__(self):
        return self.category

class Instructors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=35)
    data = models.CharField(max_length=10000)
    file = models.FileField(upload_to=user_directory_path3, null=False, blank=True, max_length = 500)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Course(models.Model):
    file = models.FileField(upload_to=user_directory_path1, null=False, blank=True, max_length = 500)
    Course_name = models.CharField(max_length = 100, blank=True)
    Course_category = models.ManyToManyField(Category, blank=True)
    Course_category_type = models.CharField(max_length = 100, blank=True)
    Course_duration = models.DurationField(default=timedelta(days=3))
    course_status = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500, blank=True)
    About_course = models.TextField(max_length = 10000, blank=True)
    slug = models.SlugField(max_length = 150)
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    instructors = models.ManyToManyField(User, blank=True)
    institution = models.ManyToManyField(User, related_name='institution', blank=True)
    certificate = models.ManyToManyField(Certificate, related_name='certificate', blank=True)
    certificate_name = models.CharField(max_length = 500, blank=True)
    published = models.CharField(max_length = 500, blank=True)
    publish = models.BooleanField(default='False')
    tags = models.ManyToManyField(Tag,related_name='tags', blank=True)
    ratings = GenericRelation(Rating, related_query_name='rate', blank=True)
    steps = models.IntegerField(default= 0 )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Course_name

    def __unicode__(self):
        return '%s' % (self.file.name)

        
    # def save(self, *args, **kwargs):
    #     # self.slug = slugify(self.Course_name, allow_unicode=True)
    #     new_image = compress(self.file)
    #     self.file = new_image
    #     super(Course, self).save(*args, **kwargs)






class profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE,)
    photo_file = models.FileField(upload_to=user_directory_path2, null=False, blank=True)
    name = models.CharField(max_length = 100, blank=True)
    About = models.CharField(max_length = 1000, blank=True)
    email = models.CharField(max_length = 100, blank=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    instructor = models.BooleanField(default='False')
    institution = models.BooleanField(default='False')

    def __str__(self):
        return self.user.username

class course_progress(models.Model):
    content = models.ForeignKey(profile, related_name='courses' , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='user_course' ,on_delete=models.CASCADE)
    steps = models.IntegerField(default= 0 )
    Last_time = models.CharField(max_length = 2000, blank=True)
    completed_time = models.CharField(max_length = 2000, blank=True)
    progress = models.IntegerField(default= 0 )
     
class payments(models.Model):
    user = models.ForeignKey(User, related_name='user' , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    course = models.ManyToManyField(Course,  related_name='all_course', blank=True)
    success = models.BooleanField(default='False')
    ref_num = models.CharField(max_length = 2000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    

class payments_verify(models.Model):
    pd_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    txt_ref = models.CharField(max_length = 2000, blank=True)
    flw_ref = models.CharField(max_length = 2000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
 
class request_course_model(models.Model):
    user = models.ForeignKey(User, related_name='user_request' , on_delete=models.CASCADE)
    course_name = models.CharField(max_length = 2000, blank=True)
    description = models.CharField(max_length = 1000, blank=True)
    duration = models.CharField(max_length = 1000, blank=True)
    section_number = models.CharField(max_length = 1000, blank=True)
    extra = models.CharField(max_length = 1000, blank=True)
    read = models.BooleanField(default='False')
    approved = models.BooleanField(default='False')
    date_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    user = models.ForeignKey(User, related_name='user_comment' , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='comment_course' ,on_delete=models.CASCADE)
    text = models.CharField(max_length = 1000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    user = models.ForeignKey(User, related_name='user_reviews' , on_delete=models.CASCADE)
    text = models.CharField(max_length = 1000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)


class feedback(models.Model):
    SCORE_CHOICES = zip(range(6), range(6) )    
    user =  models.ForeignKey(User, related_name='user_review' , on_delete=models.CASCADE)
    item = models.ForeignKey(Course,  related_name='rating' , on_delete=models.SET_NULL, null= True)
    rating = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, blank=False)
    comment = models.CharField(max_length = 1000, blank=True)
    def __str__(self):
        # return 'Rating(Item ='+ str(self.item)+', Stars ='+ str(self.rating)+')'
        return str(self.rating)

class Certificatess(models.Model):
    contents = models.ForeignKey(profile, related_name='certi_courses' , on_delete=models.CASCADE)
    name =  models.CharField(max_length = 100, blank=True)
    data = models.CharField(max_length = 100, blank=True)

class Course_Uploads(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=False, blank=False)
    file_type = models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now_add=True)

class Course_content(models.Model):
    section_title = models.CharField(max_length = 100)
    content = models.ForeignKey(Course, related_name='course_content' ,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.section_title

class section_material(models.Model):
    file_name = models.CharField(max_length = 300)
    file = models.FileField(upload_to=user_directory_path, null=False, blank=False)
    content = models.ForeignKey(Course_content, related_name='section_material' , on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name


class course_resource(models.Model):
    file_name = models.CharField(max_length = 300)
    file = models.FileField(upload_to=user_directory_path, null=False, blank=False)
    course = models.ForeignKey(Course, related_name='course_resourse' , on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name


@receiver(models.signals.pre_delete, sender=section_material)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)





@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        profile.objects.create(user=instance)
        
        
