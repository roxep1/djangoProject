from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField(verbose_name='Тэг', max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def get_update_url(self):
        return reverse("tag_update_url", kwargs={"id_tag": self.pk})

    def get_delete_url(self):
        return reverse("tag_delete_url", kwargs={"id_tag": self.pk})



class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название статьи')
    text = models.TextField(verbose_name='Текст', max_length=500)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now=True)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(verbose_name='Тэги', to=Tag)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return reverse("post_detail_url", kwargs={"id_post": self.pk})

    def get_update_url(self):
        return reverse("post_update_url", kwargs={"id_post": self.pk})

    def get_delete_url(self):
        return reverse("post_delete_url", kwargs={"id_post": self.pk})


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст', max_length=500)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now=True)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    fk_post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fk_post} - {self.author}'

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
