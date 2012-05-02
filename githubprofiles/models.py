from django.db import models

# Create your models here.


class Users(models.Model):
    type = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)
    collaborators = models.IntegerField(max_length=10)
    public_repos = models.IntegerField(max_length=10)
    private_repos = models.IntegerField(max_length=10)
    public_gists = models.IntegerField(max_length=10)
    private_gists = models.IntegerField(max_length=10)
    followers = models.IntegerField(max_length=10)
    gravatar_id = models.CharField(max_length=200)
    html_url = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField('date created')

    def __unicode__(self):
        return self.login


class Repos(models.Model):
    url = models.CharField(max_length=100)
    homepage = models.CharField(max_length=100)
    watchers = models.IntegerField(max_length=10)
    open_issues = models.IntegerField(max_length=10)
    created_at = models.CharField(max_length=35)
    pushed_at = models.CharField(max_length=35)
    has_issues = models.BooleanField()
    fork = models.BooleanField()
    has_downloads = models.BooleanField()
    private = models.BooleanField()
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=500)
    forks = models.IntegerField(max_length=10)
    owner = models.CharField(max_length=30)
    has_wiki = models.BooleanField()

    def __unicode__(self):
        return self.name
