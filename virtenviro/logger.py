# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
import os
from django.conf import settings

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))


class Logger:
    def __init__(self, filename):
        self.file = open(os.path.join(MEDIA_ROOT, 'logs', filename), 'a')

    def write(self, src):
        self.file.write(src)

    def close(self):
        self.file.close()

    def __del__(self):
        if not self.file.closed:
            self.file.close()