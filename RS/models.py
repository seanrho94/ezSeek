# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


       

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # ONE TO ONE FIELD IS IMPORTANT
    name = models.CharField(max_length=50, default = 'null')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    industry = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(max_length=12, blank=True)
    qualification = models.CharField(max_length=30, blank=True)
    profession = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    applied = models.ManyToManyField(User, related_name='applied', blank=True)
    #company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
       return self.title

    def get_absolute_url(self):
        return reverse('jobDetail', kwargs={'pk': self.pk})
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return self.user.username +  'Profile'

class Application(models.Model):
    application_id = models.AutoField(primary_key = True)
    js_id = models.ForeignKey(JobSeeker, on_delete = models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete = models.CASCADE)
    job_id = models.ForeignKey(Post, on_delete = models.CASCADE)
    status = models.CharField(default='In Progress', max_length=200)


