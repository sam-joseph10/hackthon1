import uuid
from django.db import models
class Investigation(models.Model):
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
 title=models.CharField(max_length=180,default='Untitled investigation')
 created_at=models.DateTimeField(auto_now_add=True)
 status=models.CharField(max_length=20,default='complete')
 findings=models.JSONField(default=dict)
 notes=models.TextField(blank=True)
 def __str__(self):return self.title
class Evidence(models.Model):
 investigation=models.ForeignKey(Investigation,on_delete=models.CASCADE,related_name='evidence')
 kind=models.CharField(max_length=12)
 file=models.FileField(upload_to='evidence/%Y/%m/%d/',blank=True)
 original_name=models.CharField(max_length=255,blank=True)
 sha256=models.CharField(max_length=64,blank=True)
 size=models.BigIntegerField(default=0)
 analysis=models.JSONField(default=dict)
 created_at=models.DateTimeField(auto_now_add=True)
