"""
Model file of backend
"""
from django.db import models


class Article(models.Model):
    """
    Data structure for news
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=50)
    time = models.DateTimeField(db_index=True)
    content = models.TextField()
    channel = models.CharField(max_length=20, db_index=True)
    tags = models.TextField()
    href = models.TextField(unique=True)
    image = models.TextField()

    def __str__(self):
        return self.title


class User(models.Model):
    """
    Data structure for user
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=30)
    tags = models.TextField()
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Token(models.Model):
    """
    Data structure for user
    """
    id = models.AutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=20)
    code = models.CharField(max_length=6)
    expiretime = models.IntegerField()

    def __str__(self):
        return self.token
