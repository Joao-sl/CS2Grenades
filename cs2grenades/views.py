import json
from django.http import JsonResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from cs2grenades.models import ActiveMapPool, ReserveMapPool, GuidePosts, Favorite, TutorialPosts, Avatar
from cs2grenades.utils.email import email_validator
from cs2grenades.utils.images import validate_img_size_for_view
from haystack.query import SearchQuerySet
from itertools import chain

PER_PAGE = 16


def index(request):
    guides = GuidePosts.objects.filter(public=True).order_by('-pk')[:4]
    tutorials = TutorialPosts.objects.filter(public=True).order_by('-pk')[:4]

    return render(
        request,
        'cs2grenades/pages/home.html',
        {
            'page_title': 'Home',
            'guides': guides,
            'tutorials': tutorials,
        }
    )


def check_authenticated(request):
    return JsonResponse({'authenticated': request.user.is_authenticated})


def login_modal(request):
    if request.headers.get('X-CS2Grenades-Requested-With') != 'FetchRequest':
        return redirect('/')
    return render(
        request,
        'cs2grenades/partials/login.html',
    )


def register_modal(request):
    if request.headers.get('X-CS2Grenades-Requested-With') != 'FetchRequest':
        return redirect('cs2grenades:index')
    return render(
        request,
        'cs2grenades/partials/register.html',
    )


def login_auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})

        if user.check_password(password):
            # Specifying backend= because we have 2 django.auth.backends and django-axes
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Senha Incorreta'})

    return JsonResponse({'erro': 'Método não permitido'})


def register_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('passwordConfirm')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Usuário já cadastrado'})

        if len(username) < 3:
            return JsonResponse({'success': False, 'error': 'Nome de usuário muito curto.'})

        if password != password_confirm:
            return JsonResponse({'success': False, 'error': 'As senhas não coincidem.'})

        if not email_validator(email):
            return JsonResponse({'success': False, 'error': 'Email inválido'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email já cadastrado.'})

        # Saving User
        user = User.objects.create_user(
            username=username, first_name=username, email=email, password=password)
        user.save()

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def logout_view(request):
    logout(request)

    return redirect('cs2grenades:index')


@login_required
def delete_user(request):
    if request.headers.get('X-CS2Grenades-Requested-With') != 'FetchRequest':
        return redirect('cs2grenades:index')

    if request.method == 'GET' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':
        return render(request, 'cs2grenades/partials/user_delete_account.html')

    if request.method == 'POST' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':
        try:
            data = json.loads(request.body)

            confirmation = data.get('confirmation')

            if confirmation == 'deletar':
                user = request.user
                user.delete()
                logout(request)
                return JsonResponse({'success': True, 'successMsg': 'User Deleted'})
        except:
            return JsonResponse({'success': False, 'error': 'Desculpe, não foi possível deletar sua conta por favor tente novamente mais tarde'})
    return JsonResponse({'success': False, 'error': 'Acesso Negado'})


@login_required
def profile(request):
    return render(
        request,
        'cs2grenades/pages/profile.html',
        {
            'page_title': 'Perfil'
        })


@login_required
def user_update(request):
    if request.headers.get('X-CS2Grenades-Requested-With') != 'FetchRequest':
        return redirect('cs2grenades:index')

    if request.method == 'GET' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':
        return render(
            request,
            'cs2grenades/partials/user_update.html',
        )

    if request.method == 'POST' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':

        # Avatar Form
        if request.FILES:
            avatar_file = request.FILES.get('avatar')

            if avatar_file and validate_img_size_for_view(avatar_file):

                avatar_obj, created = Avatar.objects.get_or_create(
                    user=request.user)
                avatar_obj.image = avatar_file
                avatar_obj.save()

                return JsonResponse({'success': True, 'success': 'Avatar salvo com sucesso.'})

            else:
                return JsonResponse({'success': False, 'error': 'Imagem muito grande, a imagem deve ter no máximo 1MB'})

        # Name Username Email Form
        data = json.loads(request.body)

        new_name = data.get('name')
        new_username = data.get('username')
        new_email = data.get('email')

        user = request.user

        if len(new_name) < 3 or len(new_username) < 3:
            return JsonResponse({'success': False, 'error': 'O nome ou usuário deve conter no mínimo 3 caracteres'})

        if not email_validator(new_email):
            return JsonResponse({'success': False, 'error': 'E-mail inválido.'})

        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'E-mail já cadastrado.'})

        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'Usuário já cadastrado.'})

        if user.first_name == new_name and user.username == new_username and user.email == new_email:
            return JsonResponse({'success': False, 'Error': 'Nenhum dado alterado.'})

        if user.first_name != new_name:
            user.first_name = new_name
        if user.username != new_username:
            user.username = new_username
        if user.email != new_email:
            user.email = new_email
        user.save()

        return JsonResponse({'success': True, 'successMsg': 'Dados alterados com sucesso.'})

    return JsonResponse({'success': False, 'error': 'Acesso Negado'})


@login_required
def password_update(request):
    if request.headers.get('X-CS2Grenades-Requested-With') != 'FetchRequest':
        return redirect('cs2grenades:index')

    if request.method == 'GET' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':
        return render(
            request,
            'cs2grenades/partials/user_password_update.html',
        )

    if request.method == 'POST' and request.headers.get('X-CS2Grenades-Requested-With') == 'FetchRequest':
        data = json.loads(request.body)

        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        new_password_confirm = data.get('newPasswordConfirm')

        user = request.user

        if not user.check_password(current_password):
            return JsonResponse({'success': False, 'error': 'A senha atual esta incorreta.'})

        if new_password != new_password_confirm:
            return JsonResponse({'success': False, 'error': 'A nova senha e a confirmação não coincidem.'})

        user.set_password(new_password)
        user.save()

        # Keep the user logged in
        login(request, user)

        return JsonResponse({'success': True, 'successMsg': 'Senha alterada com sucesso.'})

    return JsonResponse({'success': False, 'error': 'Acesso Negado'})


def guide(request):
    guides = GuidePosts.objects.filter(public=True).order_by('-pk')

    paginator = Paginator(guides, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        favorite_ids = request.user.favorites.values_list(
            'guide_id',
            flat=True
        )
    else:
        favorite_ids = None

    return render(
        request,
        'cs2grenades/pages/guides.html',
        {
            'page_title': 'Guias',
            'page_obj': page_obj,
            'favorites_ids': favorite_ids
        }
    )


def guide_post(request, slug):
    guide = get_object_or_404(GuidePosts, slug=slug)

    if not guide.public:
        raise Http404()

    return render(
        request,
        'cs2grenades/pages/guide_post.html',
        {
            'page_title': guide.title,
            'guide': guide
        }
    )


def maps(request):
    maps = ActiveMapPool.objects.all()
    reserve_pool_maps = ReserveMapPool.objects.all()

    return render(
        request,
        'cs2grenades/pages/maps.html',
        {
            'page_title': 'Mapas',
            'maps': maps,
            'reserve_map_pool': reserve_pool_maps
        }
    )


def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value:
        # search_value + "~" = its fuzzy search, HayStack "|" join the queries, its like "or" in python
        guide_posts_results = \
            SearchQuerySet().models(GuidePosts).filter(content_auto__contains=search_value) | \
            SearchQuerySet().models(GuidePosts).filter(text=search_value + "~")
        guide_posts_results = guide_posts_results[:12]

        # Getting the complete object
        found_guide_ids = [result.pk for result in guide_posts_results]
        guide_posts_results = GuidePosts.objects.filter(
            id__in=found_guide_ids, public=True)

        tutorial_posts_results = \
            SearchQuerySet().models(TutorialPosts).filter(content_auto__contains=search_value) | \
            SearchQuerySet().models(TutorialPosts).filter(text=search_value + "~")
        tutorial_posts_results = tutorial_posts_results[:12]

        found_tutorial_ids = [result.pk for result in tutorial_posts_results]
        tutorial_posts_results = TutorialPosts.objects.filter(
            id__in=found_tutorial_ids, public=True)

    return render(
        request,
        'cs2grenades/pages/search.html',
        {
            'page_title': search_value,
            'search_value': search_value,
            'posts': guide_posts_results,
            'tutorials': tutorial_posts_results,
        }
    )


@login_required
def favorites_page(request):
    favorites_guides_ids = Favorite.objects.filter(
        user=request.user).values_list('guide_id', flat=True)
    favorites_guides = GuidePosts.objects.filter(
        id__in=favorites_guides_ids, public=True)

    tutorial_fav_ids = Favorite.objects.filter(
        user=request.user).values_list('tutorial_id', flat=True)
    favorites_tutorials = TutorialPosts.objects.filter(
        id__in=tutorial_fav_ids, public=True)

    all_favorites = list(chain(
        [{'object': fav, 'type': 'guide'} for fav in favorites_guides],
        [{'object': fav, 'type': 'tutorial'} for fav in favorites_tutorials]
    ))

    paginator = Paginator(all_favorites, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'cs2grenades/pages/favorites.html',
        {
            'page_title': 'Favoritos',
            'favorites_ids': favorites_guides_ids,
            'tutorials_fav_ids': tutorial_fav_ids,
            'page_obj': page_obj
        }
    )


@login_required
def toggle_favorite(request, guide_id=None, tutorial_id=None):

    if guide_id is not None:
        guide = get_object_or_404(GuidePosts, id=guide_id)
        # get_or_create return a tuple
        # Whether the object was created (the favorite was added) favorite = object Created = True
        # Whether the object already existed favorite = object Created = False
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            guide=guide
        )

        if created:
            is_favorite = True
        else:
            favorite.delete()
            is_favorite = False

        return JsonResponse({'is_favorite': is_favorite})

    if tutorial_id is not None:
        tutorial = get_object_or_404(TutorialPosts, id=tutorial_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            tutorial=tutorial
        )

        if created:
            is_favorite = True
        else:
            favorite.delete()
            is_favorite = False

        return JsonResponse({'is_favorite': is_favorite})

    return JsonResponse({'is_favorite': 'Server Error'})


def tutorials_page(request):
    tutorials = TutorialPosts.objects.filter(public=True).order_by('-pk')

    paginator = Paginator(tutorials, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        tutorial_fav_ids = request.user.favorites.values_list(
            'tutorial_id',
            flat=True
        )
    else:
        tutorial_fav_ids = None

    return render(
        request,
        'cs2grenades/pages/tutorials.html',
        {
            'page_title': 'Tutoriais',
            'page_obj': page_obj,
            'tutorial_fav_ids': tutorial_fav_ids,
        }
    )
