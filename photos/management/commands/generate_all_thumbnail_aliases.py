from django.core.management.base import NoArgsCommand
from easy_thumbnails.files import generate_all_aliases
from photos.models import Photo
import time
import gc
import resource

gc.enable()
#gc.set_debug(gc.DEBUG_LEAK)

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


import collections

def count_objs():
    cnt = collections.Counter()
    for obj in gc.get_objects():
       cnt[type(obj)] += 1
    return cnt

class Command(NoArgsCommand):
    help = 'Generate thumbnail aliases for all photos'

    def handle_noargs(self, **options):
        START_TIME = time.time()
        i = 0;
        #baseline = count_objs()
        baseline = None
        #print baseline.most_common(20)
        #last = None
        for p in Photo.objects.all():
            generate_all_aliases(p.photo, include_global=True)
            cur_count = count_objs()
            #print cur_count.most_common(20)
            if baseline:
                print ("Object count:")
                print ("\n".join("  %s: %s"%(ct, tp) for (tp,ct) in
                                 (cur_count - baseline).most_common(20)))
            if not baseline:
                baseline = cur_count

            i+= 1
            usage = resource.getrusage(resource.RUSAGE_SELF)
            print("%i; RSS: %i; Unshared: %i; Obj: %i"%(i, usage.ru_maxrss, usage.ru_idrss,
                                              len(gc.get_objects())))

        print('It took %.2f seconds to generate all thumbnails and aliases.' % (time.time() - START_TIME))
        self.stdout.write('All thumbnail aliases generated succesfully.')
