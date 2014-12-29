from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from pytils.translit import slugify


def set_slug(model, src, length=60):
    slug = slugify(src)[0:length]
    try:
        obj = model.objects.get(slug=slug)
        slug = set_slug(model, slug, length)
    except model.DoesNotExist:
        return slug


class PostManager(models.Manager):
    def last_news(self, category=None, count=None):
        if count is None:
            try:
                count = settings.LAST_NEWS_COUNT
            except Exception:
                count = 10
        posts = self.filter(published=True).order_by('-created')[0:count]
        if not category is None:
            posts = posts.filter(category=category)
        return posts

    def published_news(self, count=None):
        news = self.filter(published=True)
        if not count is None:
            news = news[0:count]
        return news


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), blank=True, null=False)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

    seo_title = models.CharField(max_length=255, verbose_name=_('SEO title'), null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, verbose_name=_('Keywords meta tag'), null=True, blank=True)
    seo_description = models.CharField(max_length=255, verbose_name=_('Description meta tag'), null=True, blank=True)

    def clean(self):
        if not self.slug:
            self.slug = set_slug(Category, self.title, length=60)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Post(models.Model):
    title = models.CharField(max_length = 255, verbose_name=_('Title'))
    category = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True)
    slug = models.CharField(max_length = 60, unique=True, verbose_name=_('Slug'), null=True, blank=True)
    intro = models.TextField(verbose_name=_('Intro'), null=True, blank=True)
    content = models.TextField(verbose_name=_('Content'))
    until = models.DateField(verbose_name=_('Publicate until'), null=True, blank=True)
    origin = models.URLField(null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Author'))
    published = models.BooleanField(default=False, verbose_name=_('Published'))
    created = models.DateField(default=datetime.datetime.now(), verbose_name=_('Created'))

    seo_title = models.CharField(max_length=255, verbose_name=_('SEO title'), null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, verbose_name=_('Keywords meta tag'), null=True, blank=True)
    seo_description = models.CharField(max_length=255, verbose_name=_('Description meta tag'), null=True, blank=True)

    objects = PostManager()
    
    def __unicode__(self):
        return '%s [ %s ]' % (self.title, self.created)
    
    def clean(self):
        if not self.slug:
            self.slug = set_slug(Post, self.title, length=60)

    class Meta:
        ordering = ('-created', 'title')
        verbose_name = _('News post')
        verbose_name_plural = _('News posts')
                              
