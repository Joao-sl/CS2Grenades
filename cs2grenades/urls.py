from django.urls import path
from cs2grenades.views import index, guide, guide_post, maps, login_modal, register_modal, register_data, login_auth, logout_view, profile, user_update, password_update, search, favorites_page, toggle_favorite, check_authenticated, tutorials_page, delete_user

app_name = 'cs2grenades'

urlpatterns = [
    path('', index, name='index'),

    path('is_authenticated/', check_authenticated, name='check_authenticated'),

    # User
    path('login/', login_modal, name='login_modal'),
    path('register/', register_modal, name='register_modal'),
    path('login_auth/', login_auth, name='login_auth'),
    path('register_data/', register_data, name='register_data'),
    path('logout/', logout_view, name='logout'),
    path('user_update/', user_update, name='user_update'),
    path('password_update/', password_update, name='password_update'),
    path("delete_user/", delete_user, name="delete_user"),
    path('profile/', profile, name='profile'),

    path('guides/', guide, name='guides'),
    path('guides/<slug:slug>/', guide_post, name='guide_post'),

    path('maps/', maps, name='maps'),

    path('search/', search, name='search'),

    path('favorites/', favorites_page, name='favorites'),
    path('toggle_favorite/guide/<int:guide_id>',
         toggle_favorite,
         name='toggle_favorite'
         ),
    path('toggle_favorite/tutorial/<int:tutorial_id>',
         toggle_favorite,
         name='toggle_favorite'
         ),

    path('tutorials/', tutorials_page, name='tutorials'),
]
