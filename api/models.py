from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import gettext_lazy as _


class User(AbstractUser):
    contacts = models.ManyToManyField('self',
                                      symmetrical=True,
                                      related_name='contacts',
                                      related_query_name='contact',
                                      verbose_name=_('contacts'))
    groups = models.ManyToManyField('Group',
                                    related_name='groups',
                                    related_query_name='group',
                                    verbose_name=_('groups'))


class Group(models.Model):
    creator = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), auto_now_add=True)


class Message(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='message',
                              verbose_name=_('group'))
    creator = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='creator',
                                verbose_name=_('creator')),
    text = models.TextField(_('message text'))
    created = models.DateTimeField(_('created'), auto_now_add=True)

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
