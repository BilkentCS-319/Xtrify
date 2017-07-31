from django.db import models
from django.contrib.auth.models import User
import hashlib
 
 
class Note(models.Model):
    heading = models.CharField(max_length=140)
    content = models.CharField(max_length=50000)
    keywords = models.CharField(max_length=50000)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
 
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()
 
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])