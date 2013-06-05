from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from photos.models import Photo
import os
import re


class Command(BaseCommand):
    args = '<photo_target_dir>'
    help = 'Load a directory of photos'

    def handle(self, *args, **options):

        if not args:
            raise CommandError("The <photo_target_dir> argument is required")

        img_dir = os.path.join(settings.DJANGO_PROJECT_ROOT, args[0])
        for fn in os.listdir(img_dir):
            if re.match(r'.+\.(png|jpg|gif)', fn) is not None:
                fp = os.path.join(img_dir, fn)
                self.stdout.write('Loading the photo "%s" ...' % fn)

                photo = Photo()
                photo.photo = photo.get_photo_path(fn)
                photo.photo.storage.save(photo.photo.name, File(open(fp)))
                photo.save()

        self.stdout.write('All photos loaded succesfully.')
