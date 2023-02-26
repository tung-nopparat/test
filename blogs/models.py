from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.TextField()
    cover_img = models.ImageField(upload_to="images",blank=True)
    category = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    blog_content = models.TextField()
    tag = models.TextField()
    publish = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    writer = models.CharField(max_length=50,null=True)
    view = models.IntegerField(default=0,null=True)
    
    def __str__(self) -> str:
        return self.title

    
class ReviewRating(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject

    

    