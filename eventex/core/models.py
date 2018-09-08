from django.db import models
from django.shortcuts import resolve_url as r

class Speaker(models.Model):
    name = models.CharField('nome', max_length=250)
    slug = models.SlugField('slug')
    description = models.TextField('descrição', blank=True)
    photo = models.URLField('foto')
    website = models.URLField('website')

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)