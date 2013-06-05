Easy Thumbnails Issue Example
=============================

This project was created to test a memory leak [issue][issue] that happens when using
`easy-thumbnails` with Amazon S3.

[issue]: https://github.com/SmileyChris/easy-thumbnails/issues/230


Installation and Setup
----------------------

Create a virtual environment:

    $ mkvirtualenv et_issue_example

Clone the repository:

    $ cd ~/Sites
    $ git clone git://github.com/epicserve/et-issue-example.git

Install the requirements:

    $ cd ~/Sites/et-issue-example
    $ pip install -r requirements.txt

Set the required environment variables:

    $ export DJANGO_SETTINGS_MODULE='et_issue_example.settings'
    $ export AWS_STORAGE_BUCKET_NAME='my-et-issue-example-test-bucket'
    $ export AWS_ACCESS_KEY_ID='********************'
    $ export AWS_SECRET_ACCESS_KEY='****************************************'

Setup the database:

    $ python manage.py syncdb
    $ python manage.py migrate


Run some tests to show the memory leak
--------------------------------------

You need to first add some photos. You can do this using the Django admin or
you can use the management command `load_photos`. If you need some photos you
can do a search on [Flickr][flickr]. I used 100 photos that were each about
2 MB each. You can still see the leak if you don't use as many photos, but the
more you use the more apparent the leak will be.

[flickr]: http://www.flickr.com/search/?q=scenic+cascades+mountains&l=cc&ss=0&ct=0&mt=all&adv=1&s=int

### Add some photos using load_photos

To load photos using the `load_photos` management command do the following ...

    $ cd ~/Sites/et-issue-example
    $ mkdir test_photos

Copy some photos into the `~/Sites/et-issue-example/test_photos` directory.

Load your photos:

    $ python manage.py load_photos test_photos/

### Test the leak

After you've loaded some photos, you can see the memory leak in two ways. You
can start up Django's runserver (`python manage.py runserver`) and then load
up the index page (http://127.0.0.1:8000/) which will create all the aliases
for all photos dynamically before the page loaded.

The other way you can test the leak is by running the management command
`generate_all_thumbnail_aliases`. After loading some photos run the following
command.

    $ python manage.py generate_all_thumbnail_aliases

If your on a Mac, make sure you have the Activity Monitor open to watch your
python process grow! **Make sure you kill the process if you free memory gets to
low, because if you don't your system will become unresponsive.**


My Test Results
---------------

When using the `load_photos` command the memory never grows no matter how many
files you load. This is probably because `load_photos` just uses `boto` and
`django-storages` and never uses `easy-thumbnails`.

When I used the management command `load_photos` to load 20 photos at 2 MB
each for a total of 43.8 MB and then loaded the index page
(http://127.0.0.1:8000/) the memory grew from 24.8 MB to 404.3 MB and took 3.2
minutes to load.

**Also when I looked at the Django Debug Toolbar, it shows 1443 queries!** If I then reload the index page the
queries only go down to **483**!

If I switch to using my personal branch of [easy-
thumbnails](https://github.com/epicserve/easy-thumbnails/tree/reduce_queries),
the frist time the page is loaded the number of queries is 963 and then if you
reload the page queries are reduced to 323. Which is still a lot and that's why
I've [avocated](https://github.com/SmileyChris/easy-thumbnails/pull/226) that
`easy-thumbnails` add a caching backend that caches all the source files and
thumbnails that are in the database.

When running the management command `generate_all_thumbnail_aliases` the
python process grows from 20 MB to 220.8 MB and took 151.84 seconds.

