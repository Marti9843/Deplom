from django.db import models
from django.urls import reverse
from django.utils import timezone

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Опис')
    date_published = models.DateTimeField('Дата публікації', default=timezone.now)
    image = models.ImageField('Зображення', upload_to='news_images/', blank=True, null=True)
    slug = models.SlugField('URL', max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-date_published']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})