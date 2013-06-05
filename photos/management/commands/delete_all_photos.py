from django.core.management.base import NoArgsCommand, CommandError
from django.utils.six.moves import input
from photos.models import Photo


class Command(NoArgsCommand):
    help = 'Load a directory of photos'

    def handle_noargs(self, **options):

        confirm = input("\n".join([
            '',
            'Are you sure you want to delete all photos?',
            '',
            "Type 'yes' to continue, or 'no' to cancel: ",
        ]))

        if confirm != 'yes':
            raise CommandError("Deleting photos was cancelled.")

        for p in Photo.objects.all():
            self.stdout.write('Deleting photo "%s" ...' % p.photo.name)
            p.photo.delete_thumbnails()
            p.photo.storage.delete(p.photo.name)
            p.delete()

        self.stdout.write('All photos deleted succesfully.')
