from django.urls import path
from . import views
#url配置
urlpatterns = [
    path('',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('login/loginCheck/',views.loginCheck,name="loginCheck"),
    path('userEdit/',views.userEdit,name="userEdit"),
    path('userEdit/queryRight', views.queryRight, name="queryRight"),


    path('userEdit/showAllThemes',views.showAllThemes,name="showAllThemes"),
    path('register/registerApply',views.registerApply,name="registerApply"),
    path('uesrEdit/edit',views.edit,name="edit"),
    path('uesrEdit/editManager', views.editManager, name="editManager"),
    path('uesrEdit/showAllThemes', views.showAllThemes, name="showAllThemes"),
    path('uesrEdit/showManager', views.showManager, name="showManager"),
    path('uesrEdit/showPersonalThemes', views.showPersonalThemes, name="showPersonalThemes"),
    path('uesrEdit/uploadPicture', views.uploadPicture, name="uploadPicture"),
    path('showAllMovies',views.showAllMovies,name="showAllMovies"),
    path('selfPage/show',views.show,name="show"),
    path('selfPage/showManager', views.showManager, name="showManager"),
    path('selfPage',views.selfPage,name="selfPage"),
    path('selfPage/queryRight',views.queryRight,name="queryRight"),
    path('collection', views.collection, name="collection"),
    path('collection/queryRight', views.queryRight, name="queryRight"),

    path('selfClub', views.selfClub, name="selfClub"),
    path('selfClub/queryRight', views.queryRight, name="queryRight"),

    path('selfPage/showJoinedClubs', views.showJoinedClubs, name="showJoinedClubs"),
    path('movieSquare',views.movieSuqare,name="movieSquare"),
    path('movieSquare/showMovieRanks', views.showMovieRanks, name="showMovieRanks"),
    path('movieSquare/queryRight', views.queryRight, name="queryRight"),

    path('movieSquare/moviePage',views.moviePage,name="moviePage"),
    path('movieSquare/workerPage', views.workerPage, name="workerPage"),
    path('movieSquare/showFiveClubs', views.showFiveClubs, name="showFiveClubs"),

    path('movieSquare/workerPage/showParticipatedMovies', views.showParticipatedMovies, name="showParticipatedMovies"),
    path('movieSquare/workerPage/showRelatedWorkers', views.showRelatedWorkers, name="showRelatedWorkers"),
    path('movieSquare/moviePage/showMovie',views.showMovie,name="showMovie"),
    path('movieSquare/moviePage/collect',views.collect,name="collect"),
    path('movieSquare/moviePage/cancelCollect',views.cancelCollect,name="cancelCollect"),

    path('movieSquare/moviePage/showActor', views.showActor, name="showActor"),
    path('movieSquare/moviePage/showDirector', views.showDirector, name="showDirector"),
    path('movieSquare/moviePage/showWriter', views.showWriter, name="showWriter"),
    path('movieSquare/moviePage/showTopics', views.showTopics, name="showTopics"),

    path('movieSquare/moviePage/topicPage', views.topicPage, name="topicPage"),
    path('movieSquare/moviePage/workerPage', views.workerPage, name="workerPage"),
    path('movieSquare/moviePage/workerPage/queryRight', views.queryRight, name="queryRight"),

    path('movieSquare/moviePage/workerPage/addClub', views.addClub, name="addClub"),
    path('movieSquare/moviePage/topicPage/addBroadcast', views.addBroadcast, name="addBroadcast"),
    path('movieSquare/moviePage/topicCreatingPage', views.topicCreatingPage, name="topicCreatingPage"),
    path('movieSquare/moviePage/topicCreatingPage/addTopic', views.addTopic, name="addTopic"),
    path('movieSquare/moviePage/topicCreatingPage/queryRight', views.queryRight, name="queryRight"),

    path('movieSquare/moviePage/topicPage/queryRight', views.queryRight, name="queryRight"),
    path('movieSquare/moviePage/topicPage/showSingleTopic', views.showSingleTopic, name="showSingleTopic"),
    path('movieSquare/moviePage/topicPage/showBroadcasts', views.showBroadcasts, name="showBroadcasts"),
    path('movieSquare/moviePage/deleteTopic', views.deleteTopic, name="deleteTopic"),
    path('movieSquare/moviePage/queryRight', views.queryRight, name="queryRight"),
    path('movieSquare/moviePage/score', views.score, name="score"),

    path('movieSquare/moviePage/topicPage/deleteBroadcast', views.deleteBroadcast, name="deleteBroadcast"),

    path('searchMovieByName',views.searchMovieByName,name="searchMovieByName"),
    path('moviePage/score',views.score,name="score"),
    path('moviePage/showRelatedMovies', views.showRelatedMovies, name="showRelatedMovies"),

    path('movieSquare/showMovieRanks',views.showMovieRanks,name="showMovieRanks"),
    path('movieSquare/showWorkers',views.showWorkers,name="showWorkers"),
    path('movieSquare/showClubs', views.showClubs, name="showClubs"),
    path('movieSquare/searchWorker', views.searchWorker, name="searchWorker"),

    path('selfPage/showPersonalThemes',views.showPersonalThemes,name="showPersonalThemes"),
    path('moviePage/showMovieThemes',views.showMovieThemes,name="showMovieThemes"),
    path('moviePage/showWorkersinPage', views.showWorkersinPage, name="showWorkersinPage"),

    path('movieSquare/showRecommendedMovies',views.showRecommendedMovies,name="showRecommendedMovies"),
    path('movieSquare/showAllWorkers', views.showAllWorkers, name="showAllWorkers"),
    path('movieSquare/showFiveTopics', views.showFiveTopics, name="showFiveTopics"),

    path('movieSquare/moviePage/workerPage/showSingleWorker', views.showSingleWorker, name="showSingleWorker"),

    path('managerLogin/', views.managerLogin, name="managerLogin"),
    #path('managerRegister/', views.managerRegister, name="managerRegister"),
    path('managerLogin/managerLoginCheck', views.managerLoginCheck, name="managerLoginCheck"),
    path('managerRegister/', views.managerRegister, name="managerRegister"),
    path('managerRegister/managerRegisterApply', views.managerRegisterApply, name="managerRegisterApply"),

    path('fanClub/', views.fanClub, name="fanClub"),
    path('fanClub/queryRight', views.queryRight, name="queryRight"),
    path('fanClub/showFans', views.showFans, name="showFans"),
    path('fanClub/clubCheck', views.clubCheck, name="clubCheck"),
    path('fanClub/showWorker', views.showWorker, name="showWorker"),
    path('fanClub/joinClub', views.joinClub, name="joinClub"),
    path('fanClub/quitClub', views.quitClub, name="quitClub"),
    path('fanClub/showClubRelatedMovies', views.showClubRelatedMovies, name="showClubRelatedMovies"),
    path('fanClub/showRelatedClubs', views.showRelatedClubs, name="showRelatedClubs"),

    path('movieAddingPage/', views.movieAddingPage, name="movieAddingPage"),
    path('addWorkerForMovie/', views.addWorkerForMovie, name="addWorkerForMovie"),
    path('addWorkerForMovie/searchWorkerByName', views.searchWorkerByName, name="searchWorkerByName"),
    path('addWorkerForMovie/addWorkerToMovie', views.addWorkerToMovie, name="addWorkerToMovie"),


    path('movieAddingPage/addWorker', views.addWorker, name="addWorker"),
]