from django.db import models
from django.contrib.auth.models import User




class Resume(models.Model):
    file = models.FileField(upload_to='resumes/',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    user_name = models.CharField(max_length=100, blank=True)  # Optional user field

    def __str__(self):
        return f"Resume {self.id} - {self.uploaded_at}"
    

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)  
    skills = models.TextField()
    url = models.URLField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    