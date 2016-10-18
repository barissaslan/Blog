from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


# class PostQuerySet(models.QuerySet):
#     def draft(self):
#         return self.filter(draft=False)
#
#     def publish(self):
#         return self.filter(publish__lte=timezone.now())


class PostManager(models.Manager):
    def active(self):
        return self.filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "post/{}/{}".format(instance.slug, filename)


class Post(models.Model):
    user = models.ForeignKey('auth.User', default=1)
    title = models.CharField(max_length=100)
    content = RichTextField()
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    tags = TaggableManager()
    slug = models.SlugField(unique=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *arg, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


# class CommentManager(models.Manager):
#     def approved_comments(self):
#         return self.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # objects = CommentManager()

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.post.slug})

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


