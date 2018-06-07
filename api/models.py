from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contacts = models.ManyToManyField('self', symmetrical=True, related_name='contacts')
    groups = models.ManyToManyField('Group', related_name='members')
    workplace = models.CharField(max_length=50)
    position = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=50)
    root = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)


'''
class Content(models.Model):
    class Meta:
        abstract = True
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                verbose_name=_('message'))


class FileContent(Content):
    file = models.FileField(_('message file'), upload_to='files/')


class ImageContent(Content):
    image = models.ImageField(_('message image'), upload_to='images/')


class VideoCall(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='video_call',
                              verbose_name=_('group'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    finished = models.DateTimeField(_('finished'), blank=True, default=None)
    duration = models.DurationField(_('duration'), blank=True, default=None)
    '''
