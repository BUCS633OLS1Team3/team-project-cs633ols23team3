from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
from PIL import Image
import random

class User(AbstractUser):

    CATEGORY = [
        ('Alumni', 'Alumni'),
        ('Faculty', 'Faculty'),
    ]
    role = models.CharField(max_length=7, choices=CATEGORY, default='Alumni')

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True, null=True)
    profile_pic = models.ImageField(default ='default_pic.jpg', upload_to='img/profile_pic/', blank=True, null=True)
    facebook_url = models.CharField(max_length=250,blank = True, null=True)
    twitter_url = models.CharField(max_length=250,blank = True, null=True)
    linkedin_url = models.CharField(max_length=250,blank = True, null=True)


    def __str__(self):
        return str(self.user)

    def save(self,*args, **kwargs):
        super().save()
        if (self.profile_pic):
            img = Image.open(self.profile_pic.path)

            if (img.height > 350 or img.width >350):
                output_size = (350,350)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)

    

class Requests(models.Model):

    def create_new_ref_no():
        not_unique = True
        while not_unique:
            unique_ref = random.randint(1000000000, 9999999999)
            if not Requests.objects.filter(reference=unique_ref):
                not_unique = False
        return str(unique_ref)

    STATUS = [
        ('SU', 'Submitted'),
        ('AP', 'Approved'),
        ('PR', 'Processed'),
        ('CO', 'Completed'),
        ('CL', 'Closed'),
    ]
    PURPOSE = [
        ('PE', 'Personal'),
        ('OF', 'Official'),
    ]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference = models.CharField(max_length=10, blank=True, unique=True, default=create_new_ref_no)
    delivery_email = models.EmailField(max_length=254)
    purpose = models.CharField(max_length=2, choices=PURPOSE, default='OF',) 
    agreement = models.BooleanField()
    status = models.CharField(max_length=2, choices=STATUS, default='QU', )
    date = models.DateTimeField(auto_now_add=True)
    approve_date = models.DateTimeField(blank=True, )
    process_date = models.DateTimeField(blank=True,)
    complete_date = models.DateTimeField(blank=True,)
    close_date = models.DateTimeField(blank=True,)


    class Meta:
        ordering = ['-date']


    def serialize(self):
        return {
            "reference": self.reference,
            "creator": self.creator.username,
            "status": self.status,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
        }


    def __str__(self):
        return self.reference

class Events(models.Model):
    event_image = models.ImageField(default ='default_pic.jpg', upload_to='img/events/', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    description = models.TextField()
    event_date = models.DateTimeField(blank=True,)


class Comments(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.comment


class Directory(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    student_id = models.IntegerField(default=0,blank=True)
    grad_year = models.IntegerField(default=1900,blank=True)

    def __str__(self):
        return self.student_id


class Transcripts(models.Model):
    alumni = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to ='uploads/', blank=True)

    def __str__(self):
        return self.alumni


