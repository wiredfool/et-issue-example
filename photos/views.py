from django.views.generic import ListView
from . models import Photo


class PhotoList(ListView):
    model = Photo

photo_list = PhotoList.as_view()
