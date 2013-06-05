from django.core.management.base import NoArgsCommand
from easy_thumbnails.files import generate_all_aliases
from photos.models import Photo
import time
import gc
gc.enable()
gc.set_debug(gc.DEBUG_LEAK)


def dump_garbage():
    """
    show us what's the garbage about
    """

    # force collection
    print("\nGARBAGE:")
    gc.collect()

    print("\nGARBAGE OBJECTS:")
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80:
            s = s[:80]
        print(type(x), "\n  ", s)


def time_function(func, *args, **kwargs):
    st = time.time()
    result = func(*args, **kwargs)
    del result
    print('It took %.2f seconds to generate all thumbnail aliases.' % (time.time() - st))


class Command(NoArgsCommand):
    help = 'Generate thumbnail aliases for all photos'

    def handle_noargs(self, **options):

        START_TIME = time.time()

        for p in Photo.objects.all():
            self.stdout.write("Generating thumbnails for photo #%s" % p.pk)
            time_function(generate_all_aliases, *[p.photo], **{'include_global': True})

        print('It took %.2f seconds to generate all thumbnails and aliases.' % (time.time() - START_TIME))
        import ipdb
        ipdb.set_trace()
        dump_garbage()
        self.stdout.write('All thumbnail aliases generated succesfully.')
