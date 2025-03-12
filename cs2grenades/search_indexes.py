from haystack import indexes
from cs2grenades.models import GuidePosts, TutorialPosts
from whoosh.analysis import RegexTokenizer, LowercaseFilter, CharsetFilter
from whoosh.support.charset import accent_map

custom_analyzer = RegexTokenizer() | LowercaseFilter() | CharsetFilter(accent_map)


class GuidePostsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        analyzer=custom_analyzer
    )
    title = indexes.CharField(
        model_attr='title',
        analyzer=custom_analyzer
    )
    description = indexes.CharField(
        model_attr='description',
        analyzer=custom_analyzer
    )
    tags = indexes.MultiValueField(
        null=True,
        analyzer=custom_analyzer
    )

    # Auto-complete search's
    content_auto = indexes.EdgeNgramField(
        model_attr='title',
        analyzer=custom_analyzer
    )

    def get_model(self):
        return GuidePosts

    def prepare_tags(self, obj):
        # Return tag names
        return [tag.tag_name for tag in obj.tags.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(public=True)


class TutorialPostsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        analyzer=custom_analyzer
    )
    tutorial_title = indexes.CharField(
        model_attr='tutorial_title',
        analyzer=custom_analyzer
    )
    tutorial_description = indexes.CharField(
        model_attr='tutorial_description',
        analyzer=custom_analyzer
    )
    tags = indexes.MultiValueField(
        null=True,
        analyzer=custom_analyzer
    )

    # Auto-complete search's
    content_auto = indexes.EdgeNgramField(
        model_attr='tutorial_title',
        analyzer=custom_analyzer
    )

    def get_model(self):
        return TutorialPosts

    def prepare_tags(self, obj):
        # Return tag names
        return [tag.tag_name for tag in obj.tags.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(public=True)
