# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
import os
import codecs
from django.conf import settings

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))


class Logger:
    def __init__(self, filename, src):
        file = codecs.open(os.path.join(MEDIA_ROOT, 'logs', filename), 'utf-8', 'a')
        file.write(src)
        file.close()
