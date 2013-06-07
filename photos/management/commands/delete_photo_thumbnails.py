from django.core.management.base import NoArgsCommand, CommandError
from django.utils.six.moves import input
from photos.models import Photo


class Command(NoArgsCommand):
    help = 'Load a directory of photos'

    def handle_noargs(self, **options):

        confirm = input("\n".join([
            '',
            'Are you sure you want to delete all thumbnails for all photos? (y/n) ',
        ]))

        if confirm != 'y':
            raise CommandError("Deleting thumbnails was cancelled.")

        for p in Photo.objects.all():
            self.stdout.write('Deleting thumbnails for photo "%s" ...' % p.photo.name)
            p.photo.delete_thumbnails()

        self.stdout.write('All thumbnails were deleted succesfully.')
