from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Photo(models.Model):

    def get_photo_path(instance, filename):
        return "photos/%s" % filename

    photo = ThumbnailerImageField(upload_to=get_photo_path, max_length=255)

    def __unicode__(self):
        return self.photo.name
