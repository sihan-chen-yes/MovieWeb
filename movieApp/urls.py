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
    path('workerPage', views.workerPage, name="workerPage"),
    path('movieSquare',views.movieSuqare,name="movieSquare"),
    path('movieSquare/moviePage',views.moviePage,name="moviePage"),
    path('movieSquare/moviePage/showMovie',views.showMovie,name="showMovie"),
    path('movieSquare/moviePage/collect',views.collect,name="collect"),
    path('movieSquare/moviePage/cancelCollect',views.cancelCollect,name="cancelCollect"),

    path('movieSquare/moviePage/showTopics', views.showTopics, name="showTopics"),
    path('movieSquare/moviePage/topicPage', views.topicPage, name="topicPage"),
    path('movieSquare/moviePage/topicPage/addBroadcast', views.addBroadcast, name="addBroadcast"),
    path('movieSquare/moviePage/topicCreatingPage', views.topicCreatingPage, name="topicCreatingPage"),
    path('movieSquare/moviePage/topicCreatingPage/addTopic', views.addTopic, name="addTopic"),
    path('movieSquare/moviePage/topicPage/showSingleTopic', views.showSingleTopic, name="showSingleTopic"),
    path('movieSquare/moviePage/topicPage/showBroadcasts', views.showBroadcasts, name="showBroadcasts"),
    path('movieSquare/moviePage/deleteTopic', views.deleteTopic, name="deleteTopic"),
    path('movieSquare/moviePage/score', views.score, name="score"),
    path('movieSquare/moviePage/topicPage/deleteBroadcast', views.deleteBroadcast, name="deleteBroadcast"),

    path('searchMovieByName',views.searchMovieByName,name="searchMovieByName"),
    path('moviePage/score',views.score,name="score"),
    path('movieSquare/showMovieRanks',views.showMovieRanks,name="showMovieRanks"),
    path('movieSquare/showWorkers',views.showWokers,name="showWorkers"),
    path('selfPage/showPersonalThemes',views.showPersonalThemes,name="showPersonalThemes"),
    path('moviePage/showMovieThemes',views.showMovieThemes,name="showMovieThemes"),
    path('movieSquare/showRecommendedMovies',views.showRecommendedMovies,name="showRecommendedMovies"),
]