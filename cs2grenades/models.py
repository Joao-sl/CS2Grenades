from django.db import models
from django_cleanup import cleanup
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

' "/u200B" this is to order the models in django admin page, u200B is first, /u200B/u200B two is second and so on'


@cleanup.select
class ActiveMapPool(models.Model):
    class Meta:
        verbose_name = 'Active Map Pool'
        verbose_name_plural = '\u200B Active Map Pool'

    map_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Map Name'
    )

    map_image = models.ImageField(
        upload_to='maps/map_image',
        verbose_name='Map Image'
    )

    map_logo = models.ImageField(
        upload_to='maps/map_logo',
        verbose_name='Map Logo Image'
    )

    def __str__(self):
        return self.map_name


@cleanup.select
class ReserveMapPool(models.Model):
    class Meta:
        verbose_name = 'Reserve Map Pool'
        verbose_name_plural = '\u200B\u200B Reserve Map Pool'

    map_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Map Name'
    )

    map_image = models.ImageField(
        upload_to='reserve_pool_maps/map_image',
        verbose_name='Map Image'
    )

    map_logo = models.ImageField(
        upload_to='reserve_pool_maps/map_logo',
        verbose_name='Map Logo Image'
    )

    def __str__(self):
        return self.map_name


class Tags(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = '\u200B\u200B\u200B\u200B Tags'

    tag_name = models.CharField(
        max_length=50,
        verbose_name='Tag Name',
        unique=True
    )
    help_text = models.TextField(
        editable=False,
        default='You can add these tags to the posts'
    )

    def __str__(self):
        return self.tag_name


@cleanup.select
class GuidePosts(models.Model):
    class Meta:
        verbose_name = 'Guide Post'
        verbose_name_plural = 'Guide Posts'

    title = models.CharField(
        max_length=32,
        unique=True,
        blank=False,
        null=False,
    )
    description = models.CharField(
        max_length=112,
        blank=False,
        null=False,
    )
    banner = models.ImageField(
        upload_to='guide_banners/',
        blank=False,
        null=False,
    )

    content = models.TextField()

    tags = models.ManyToManyField(
        Tags,
        blank=True,
        help_text='This will help search engine'
    )
    public = models.BooleanField(
        default=True,
        help_text='If marked the post will be public'
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        null=False,
        help_text='Auto-populated, this will be the URL for the post'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
        editable=False,
        help_text='Auto-populated'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
        editable=False,
        help_text='Auto-populated'
    )

    def __str__(self):
        return self.title


@cleanup.select
class TutorialPosts(models.Model):
    class Meta:
        verbose_name = 'Tutorial Post'
        verbose_name_plural = 'Tutorial Posts'

    tutorial_title = models.CharField(
        max_length=32,
        unique=True,
        blank=False,
        null=False
    )
    tutorial_description = models.CharField(
        max_length=112,
        blank=False,
        null=False,
    )
    tutorial_banner = models.ImageField(
        upload_to='tutorial_banners/',
        blank=False,
        null=False,
    )
    tutorial_video = models.TextField(
        blank=False,
        null=False,
    )
    tags = models.ManyToManyField(
        Tags,
        blank=True,
        help_text='This will help search engine'
    )
    public = models.BooleanField(
        default=True,
        help_text='If marked the post will be public'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
        editable=False,
        help_text='Auto-populated'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=False,
        null=False,
        editable=False,
        help_text='Auto-populated'
    )

    def __str__(self):
        return self.tutorial_title


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    guide = models.ForeignKey(
        GuidePosts,
        on_delete=models.CASCADE,
        related_name='favorite_guide',
        null=True,
        blank=True,
    )
    tutorial = models.ForeignKey(
        TutorialPosts,
        on_delete=models.CASCADE,
        related_name='favorite_tutorial',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # User can favorite only one
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'guide'],
                name='unique_guide_favorite'
            ),
            models.UniqueConstraint(
                fields=['user', 'tutorial'],
                name='unique_tutorial_favorite'
            ),
        ]

    def clean(self):
        if bool(self.guide) == bool(self.tutorial):
            raise ValidationError(
                'It is necessary to fill in one of the fields in detail: Guide or Tutorial'
            )


@cleanup.select
class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
