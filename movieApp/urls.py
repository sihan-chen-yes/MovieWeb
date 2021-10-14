from django.urls import path
from . import views
#url配置
urlpatterns = [
    path('',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('login/loginCheck/',views.loginCheck,name="loginCheck"),
    path('userEdit/',views.userEdit,name="userEdit"),
    path('register/registerApply',views.registerApply,name="registerApply"),
    path('uesrEdit/edit',views.edit,name="edit"),
    path('showAllMovies',views.showAllMovies,name="showAllMovies"),
    path('selfPage/show',views.show,name="show"),
    path('selfPage',views.selfPage,name="selfPage"),
    path('movieSquare',views.movieSuqare,name="movieSquare"),
    path('movieSquare/moviePage',views.moviePage,name="moviePage"),
    path('movieSquare/moviePage/showMovie',views.showMovie,name="showMovie"),
    path('movieSquare/moviePage/collect',views.collect,name="collect"),
    path('movieSquare/moviePage/cancelCollect',views.cancelCollect,name="cancelCollect"),
    path('searchMovieByName',views.searchMovieByName,name="searchMovieByName"),
]