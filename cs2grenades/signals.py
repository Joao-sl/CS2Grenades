from django.db.models.signals import m2m_changed
from haystack import connections
from cs2grenades.models import GuidePosts, TutorialPosts


# Update tags index when save posts
def update_index_on_tags_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        unified_index = connections['default'].get_unified_index()
        index = unified_index.get_index(instance.__class__)
        index.update_object(instance)


m2m_changed.connect(update_index_on_tags_change,
                    sender=GuidePosts.tags.through)
m2m_changed.connect(update_index_on_tags_change,
                    sender=TutorialPosts.tags.through)
