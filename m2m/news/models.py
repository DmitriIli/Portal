from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse, reverse_lazy


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.author.username

    class Meta:
        pass

    def update_rating(self):
        rating_post = self.post_set.aggregate(post_rating=Sum('rating'))
        r_post = 0
        r_post += rating_post.get('post_rating')

        rating_comment = self.author.comment_set.aggregate(comment_rating=Sum('rating'))
        r_comment = 0
        r_comment += rating_comment.get('comment_rating')

        self.rating = r_post * 3 + r_comment
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribe = models.ManyToManyField(User, through='Subscribers')

    def __str__(self):
        return f'{self.name}'


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    news = 'NW'
    article = 'AT'

    TYPES = [
        (news, 'новости'),
        (article, 'статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    types_of_topic = models.CharField(max_length=2, default=news, choices=TYPES)
    date = models.DateField(auto_now=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256, default='title')
    text = models.TextField(default='text')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title}:\n' \
               f'{self.date}, ' \
               f'{self.text[:20]}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:123]}...'

    def get_absolute_url(self):
        return reverse_lazy('news')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title}'


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='comment text')
    datetime_comment = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



