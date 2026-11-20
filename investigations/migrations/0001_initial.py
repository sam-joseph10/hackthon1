import uuid
from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[]
 operations=[
 migrations.CreateModel(name='Investigation',fields=[('id',models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,serialize=False)),('title',models.CharField(default='Untitled investigation',max_length=180)),('created_at',models.DateTimeField(auto_now_add=True)),('status',models.CharField(default='complete',max_length=20)),('findings',models.JSONField(default=dict)),('notes',models.TextField(blank=True))]),
 migrations.CreateModel(name='Evidence',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),('kind',models.CharField(max_length=12)),('file',models.FileField(blank=True,upload_to='evidence/%Y/%m/%d/')),('original_name',models.CharField(blank=True,max_length=255)),('sha256',models.CharField(blank=True,max_length=64)),('size',models.BigIntegerField(default=0)),('analysis',models.JSONField(default=dict)),('created_at',models.DateTimeField(auto_now_add=True)),('investigation',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='evidence',to='investigations.investigation'))])]
