from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor.fields import RichTextField


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=64)
    users = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_('category name'))
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')
    
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, default=1, on_delete=models.SET_DEFAULT,
                               verbose_name=pgettext_lazy("Author", 'Author'))
    title = models.CharField(max_length=128, verbose_name=pgettext_lazy('Title', 'Title'))
    text = RichTextField(blank=True, null=True)
    text_upload = RichTextUploadingFormField()
    time_in = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy('Time_in', 'Time_in'))
    category = models.ForeignKey(Category,null=True, verbose_name=pgettext_lazy('Category', 'Category'), on_delete=models.CASCADE)

    def __str__(self):
        return f'id-{self.pk}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)