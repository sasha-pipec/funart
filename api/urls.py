from django.urls import path

from api.views.banner import BannerListView
from api.views.category import CategoryListView
from api.views.client_theme_coloring import (PersonalThemeListView,
                                             PersonalColoringListView)
from api.views.coloring import (ColoringListCreateView, ColoringDetailView,
                                ColoringDownloadView, ColoringAllDetailView)
from api.views.coloring_like import ColoringLikeCreateDeleteView
from api.views.user_image_coloring import UserColoringDetailView
from api.views.saving_image import SavingUserColoringView
from api.views.theme_like import ThemeLikeCreateDeleteView
from api.views.theme import (ThemeListCreateView, ThemeListByCategoryView,
                             ThemeListBySearchView, ThemePopularListView, )
from api.views.token import TokenGetDeleteView
from api.views.user import CreateUpdateUserView, CurrentUserView
from api.views.user_list_image import UserColoringsListView

urlpatterns = [
    # Category
    path("categories/", CategoryListView.as_view()),
    path("categories/<int:id>/themes/", ThemeListByCategoryView.as_view()),

    # Theme
    path('themes/', ThemeListCreateView.as_view(), name='theme_list_create'),

    path('themes/populars/', ThemePopularListView.as_view()),
    path('themes/<int:id>/colorings/', ColoringListCreateView.as_view()),

    # Coloring
    path('colorings/', ColoringAllDetailView.as_view()),
    path('colorings/<int:id>/', ColoringDetailView.as_view()),
    path('colorings/<int:id>/download/', ColoringDownloadView.as_view()),

    # Personal
    path('personal_area/themes/', PersonalThemeListView.as_view()),
    path('personal_area/colorings/', PersonalColoringListView.as_view()),

    # User coloring
    path('colorings/<int:coloring_id>/user_colorings/', SavingUserColoringView.as_view()),
    path('user_colorings/', UserColoringsListView.as_view()),
    path('user_colorings/<int:id>/', UserColoringDetailView.as_view()),

    # Search
    path('search/', ThemeListBySearchView.as_view()),

    # Banner
    path('banners/', BannerListView.as_view()),

    # User
    path('users/', CreateUpdateUserView.as_view()),
    path('users/me/', CurrentUserView.as_view()),
    path('users/auth/', TokenGetDeleteView.as_view()),

    # Like
    path('themes/<int:id>/likes/', ThemeLikeCreateDeleteView.as_view()),
    path('colorings/<int:id>/likes/', ColoringLikeCreateDeleteView.as_view()),

]
