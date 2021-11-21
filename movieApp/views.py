import pymysql
from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
import numpy as np
# Create your views here.


db_user = "root"
db_password = "61lyx520837"
database = "movie"
host = "localhost"
#表头
topic_list_name_list = ["topic_id","film_id","user_id","title","topic_text","topic_time"]
broadcast_list_name_list = ["broadcast_id","topic_id","user_id","broadcast_text","broadcast_time"]
film_info_name_list = ["film_id","film_name","film_date",
                       "film_area","film_score","film_score_people","introduction","picture","video"]
worker_list_name_list = ["worker_id","worker_name","worker_picture","worker_introduction"]
theme_list_name_list = ["theme_id","theme_name"]
user_list_name_list = ["user_id","user_name","gender","email","phone","user_picture"]
#no password
fan_club_name_list = ["club_id","club_name"]

#分别定位到不同的html页面
def login(request):
    # ip = getIp(request)
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def managerLogin(request):
    return render(request, "managerLogin.html")

def managerRegister(request):
    return render(request, "managerRegister.html")

def userEdit(request):
    return render(request,"userEdit.html")

def selfPage(request):
    return render(request,"selfPage.html")

def movieSuqare(request):
    return render(request,"movieSquare.html")

def moviePage(request):
    return render(request,"moviePage.html")

def topicPage(request):
    return render(request,"topicPage.html")

def topicCreatingPage(request):
    return render(request,"topicCreatingPage.html")

def workerPage(request):
    return render(request,"workerPage.html")

def fanClub(request):
    return render(request,"fanClub.html")

def movieAddingPage(request):
    return render(request, "movieAddingPage.html")

def collection(request):
    return render(request, "collection.html")

def selfClub(request):
    return render(request, "selfClub.html")

def getIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def select(sql):
    '''显示信息'''
    db = pymysql.connect(user=db_user, password=db_password, database=database, host=host)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results

def execute(sql):
    '''执行sql语句'''
    db = pymysql.connect(user=db_user, password=db_password, database=database, host=host)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        mark = True
    except:
        db.rollback()
        mark = False
    db.close()
    return mark

def delete(sql):
    '''删除信息'''
    return execute(sql)

def update(sql):
    '''更新信息'''
    return execute(sql)

def insert(sql):
    '''插入信息'''
    return execute(sql)

def procedureCall(sql):
    '''执行存储过程'''
    db = pymysql.connect(user=db_user, password=db_password, database=database, host=host)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        mark = True
    except:
        db.rollback()
        mark = False
    db.close()
    return mark

def generateDictData(result,name_list):
    '''根据sql结果和列名生成字典'''
    dict = {}
    assert len(result) == len(name_list)
    for i in range(len(result)):
        dict[name_list[i]] = result[i]
    return dict

def loginCheck(request):
    '''登陆校验'''
    id = request.GET.get("id")
    pwd = request.GET.get("pwd")

    sql = "select * from user_list where user_id = '%s'" %(id)
    results = select(sql)
    data = {
        "allowed" : True,
        "idWrong" : False,
        'pwdWrong' : False
    }
    #记录mark
    if results:
        row = results[0]
        if pwd != row[2]:
            data["pwdWrong"] = True
            data["allowed"] = False
    else:
        data["allowed"] = False
        data["idWrong"] = True
    return JsonResponse(data, safe=False)

def registerApply(request):
    '''注册申请'''
    id = request.GET.get("id")
    name = request.GET.get("name")
    pwd = request.GET.get("pwd")

    data = {
        "allowed": True,
        "idWrong": False,
        "nameWrong":False
    }
    # 记录mark
    sql = "select * from user_list where user_id = '%s'" % (id)
    results = select(sql)
    if results:
        data["allowed"] = False
        data["idWrong"] = True
        return JsonResponse(data, safe=False)

    sql = "select * from user_list where user_name = '%s'" % (name)
    results = select(sql)
    if results:
        data["allowed"] = False
        data["nameWrong"] = True
        return JsonResponse(data, safe=False)

    sql = "insert into user_list(user_id,user_name,password) values('%s','%s','%s')" % (id,name,pwd)
    data = insert(sql)
    return JsonResponse(data, safe=False)

def edit(request):
    '''个人资料编辑'''
    gender = request.GET.get("gender")
    email = request.GET.get("email")
    phone = request.GET.get("phone")
    id = request.GET.get("id")
    themes = request.GET.get("themes")
    #前端传入是字符串 转化成list
    tempThemes = themes
    tempThemes = tempThemes.replace('[','')
    tempThemes = tempThemes.replace(']','')
    tempThemes = tempThemes.replace('\"','')
    themes = tempThemes.split(',')

    sql = "update user_list set gender = '%s',email = '%s',phone = '%s' where user_id = '%s'" % (gender,email,phone,id)
    mark = update(sql)
    if not mark:
        return JsonResponse(mark,saft=False)
    sql = "delete from user_theme where user_id = '%s'" %(id)
    mark = delete(sql)
    if not mark:
        return JsonResponse(mark,safe=False)
    for theme in themes:
        sql = "insert into user_theme (user_id,theme_id) values ('%s','%s')"%(id,theme)
        mark = insert(sql)
        if not mark:
            return JsonResponse(mark,safe=False)
    return JsonResponse(mark, safe=False)

def showAllMovies(request=None):
    '''显示所有电影信息'''
    data = []
    sql = "select * from film_info"
    results = select(sql)
    for result in results:
        film_id = result[0]
        data.append(showMovie(request=None,film_id=film_id))
    if request:
        return JsonResponse(data, safe=False)
    else:
        return data

def showMovie(request=None,film_id=None):
    '''根据电影id显示该电影信息'''
    if request:
        film_id = request.GET.get("film_id")
    else:
        assert film_id
    sql = "select * from film_info where film_id = '%s'" % (film_id)
    results = select(sql)
    assert len(results) == 1
    data = showWorkers(request=None,film_id=film_id)
    data["film_info"] = generateDictData(results[0],film_info_name_list)
    data["themes"] = showMovieThemes(request=None,film_id=film_id)
    if request:
        return JsonResponse(data,safe=False)
    else:
        return data

def show(request):
    '''显示用户收藏的电影以及用户信息'''
    id = request.GET.get("id")

    data = {}
    data["film_info"] = []
    sql = "select * from user_collection where user_id = '%s'" % (id)
    results = select(sql)
    for result in results:
        film_id = result[2]
        sql = "select * from film_info where film_id = '%s'" % (film_id)
        info_results = select(sql)
        assert len(info_results) == 1
        info_result = info_results[0]
        data["film_info"].append(generateDictData(info_result,film_info_name_list))
    sql = "select * from user_list where user_id = '%s'" %(id)
    user_results = select(sql)
    assert len(user_results) == 1
    user_info = user_results[0]
    try:
        data["name"] = user_info[1]
        data["gender"] = user_info[3]
        data["email"] = user_info[4]
        data["phone"] = user_info[5]
        data["picture"] = user_info[6]
    except:
        data["name"] = None
        data["gender"] = None
        data["email"] = None
        data["phone"] = None
        data["picture"] = None
    return JsonResponse(data,safe=False)

def collect(request):
    user_id = request.GET.get("id")
    film_id = request.GET.get("film_id")
    sql = "select * from user_collection where user_id = '%s' and film_id = '%s'" % (user_id,film_id)
    results = select(sql)
    if results:
        mark = False
    else:
        sql = "insert into user_collection(user_id,film_id) values('%s','%s')" % (user_id,film_id)
        mark = insert(sql)
    return JsonResponse(mark, safe=False)

def cancelCollect(request):
    user_id = request.GET.get("id")
    film_id = request.GET.get("film_id")
    sql = "select * from user_collection where user_id = '%s' and film_id = '%s'" % (user_id, film_id)
    results = select(sql)
    if not results:
        mark = False
    else:
        sql = "delete from user_collection where user_id = '%s' and film_id = '%s'" % (user_id,film_id)
        mark = delete(sql)
    return JsonResponse(mark, safe=False)

def searchMovieByName(request):
    '''根据输入的电影名模糊搜索'''
    film_name = request.GET.get("keyword")
    film_name = "%" + film_name + "%"
    sql = "select * from film_info where film_name like '%s'" % (film_name)
    results = select(sql)
    data = []
    for result in results:
        film_id = result[0]
        data.append(showMovie(request=None,film_id=film_id))
    return JsonResponse(data,safe=False)

def getTopics():
    sql = "select * from topic_list"
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result, topic_list_name_list))
    return data

def showTopics(request):
    '''显示所有话题'''
    film_id = request.GET.get("film_id")
    sql = "select * from topic_list where film_id = '%s'" % (film_id)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,topic_list_name_list))
    return JsonResponse(data,safe=False)

def getBroadcasts(topic_id):
    sql = "select * from broadcast_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result, broadcast_list_name_list))
    return data

def showBroadcasts(request):
    '''显示所有子话题'''
    topic_id = request.GET.get("topic_id")
    sql = "select * from broadcast_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,broadcast_list_name_list))
    return JsonResponse(data,safe=False)

def getTopicAndBroadcast():
    num = 1
    topics = getTopics()
    assert type(topics) == list
    for topic,index in enumerate(topics):
        assert type(topic) == dict
        topic_id = topic["topic_id"]
        broadcasts = getBroadcasts(topic_id)
        topic["broadcasts"] = broadcasts[:num]
    return topics

def showSingleTopic(request):
    '''显示单个话题'''
    topic_id = request.GET.get("topic_id")
    sql = "select * from topic_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    for result in results:
        data = generateDictData(result,topic_list_name_list)
        break
    return JsonResponse(data,safe=False)

def addTopic(request):
    '''增加话题'''
    film_id = request.GET.get("film_id")
    user_id = request.GET.get("user_id")
    title = request.GET.get("title")
    topic_text = request.GET.get("topic_text")
    topic_time = pd.to_datetime(request.GET.get("topic_time"))
    sql = "insert into topic_list(film_id,user_id,title,topic_text,topic_time) values('%s','%s','%s','%s','%s')" % \
          (film_id,user_id,title,topic_text,topic_time)
    data = insert(sql)
    #successful or not op
    return JsonResponse(data,safe=False)

def addBroadcast(request):
    '''增加子话题'''
    topic_id = request.GET.get("topic_id")
    user_id = request.GET.get("user_id")
    broadcast_text = request.GET.get("broadcast_text")
    broadcast_time = pd.to_datetime(request.GET.get("broadcast_time"))
    sql = "insert into broadcast_list(topic_id, user_id, broadcast_text, broadcast_time) values('%s','%s','%s','%s')" % \
          (topic_id, user_id, broadcast_text, broadcast_time)
    data = insert(sql)
    #successful or not op
    return JsonResponse(data,safe=False)

def deleteTopic(request):
    '''删除话题'''
    topic_id = request.GET.get("topic_id")
    sql = "delete from topic_list where topic_id = '%s'" % (topic_id)
    data = delete(sql)
    return JsonResponse(data,safe=False)

def deleteBroadcast(request):
    '''删除子话题'''
    broadcast_id = request.GET.get("broadcast_id")
    sql = "delete from broadcast_list where broadcast_id = '%s'" % (broadcast_id)
    data = delete(sql)
    return JsonResponse(data,safe=False)

def score(request):
    '''增加电影评分'''
    film_id = request.GET.get("film_id")
    user_id = request.GET.get("user_id")
    score_number = request.GET.get("score_number")
    mark = False
    #先检查之前是否评分过
    sql = "select * from user_score where user_id = '%s' and film_id = '%s'" % (user_id,film_id)
    results = select(sql)
    if results:
        sql = "select score_number from user_score where film_id = '%s' and user_id = '%s'" % (film_id,user_id)
        results = select(sql)
        assert len(results) == 1
        origin_score = results[0][0]
        sql = "update user_score set score_number = '%s' where user_id = '%s' and film_id = '%s'" \
              % (score_number,user_id,film_id)
        mark = update(sql)
        if not mark:
            msg = "更新user_score失败"
            return JsonResponse(data=msg, safe=False)
        # 更新电影信息
        sql = "select film_score,film_score_people from film_info where film_id = '%s'" % (film_id)
        results = select(sql)
        assert len(results) == 1
        result = results[0]
        film_score = result[0]
        film_score_people = result[1]
        total_score = film_score * film_score_people
        total_score = total_score - origin_score + float(score_number)
        film_score = total_score / film_score_people
        sql = "update film_info set film_score = '%s',film_score_people = '%s' where film_id = '%s'" \
              % (film_score, film_score_people, film_id)
        mark = update(sql)
    else:
        sql = "insert into user_score (user_id,film_id,score_number) values('%s','%s','%s')" \
              % (user_id,film_id,score_number)
        mark = insert(sql)
        if not mark:
            msg = "更新user_score失败"
            return JsonResponse(data=msg, safe=False)
        # 更新电影信息
        sql = "select film_score,film_score_people from film_info where film_id = '%s'" % (film_id)
        results = select(sql)
        assert len(results) == 1
        result = results[0]
        film_score = result[0]
        film_score_people = result[1]
        total_score = film_score * film_score_people
        total_score += float(score_number)
        film_score_people += 1
        film_score = total_score / film_score_people
        sql = "update film_info set film_score = '%s',film_score_people = '%s' where film_id = '%s'" \
              % (film_score, film_score_people, film_id)
        mark = update(sql)
    return JsonResponse(mark,safe=False)

def showMovieRanks(request=None):
    '''按照电影评分rank返回电影信息'''
    sql = "select * from film_info"
    results = select(sql)
    assert results
    data = []
    for result in results:
        data.append(generateDictData(result,film_info_name_list))
    #按评分降序排列
    data.sort(key=lambda x:x["film_score"],reverse=True)
    if request:
        return JsonResponse(data,safe=False)
    return data

def showWorkers(request=None,film_id=None):
    '''显示与特定电影有关的所有影人信息'''
    if request:
        film_id = request.GET.get("film_id")
    else:
        assert film_id
    data = {}
    data["directors"] = showDirector(film_id)
    data["actors"] = showActor(film_id)
    data["writers"] = showWriter(film_id)
    if request:
        return JsonResponse(data, safe=False)
    else:
        return data

def getDirectorIds(film_id):
    sql = "select worker_id from film_director where film_id = '%s'" % (film_id)
    director_ids = select(sql)
    return director_ids

def showDirector(film_id):
    sql = "select film_director.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_director,worker_list " \
          "where film_id = '%s' and film_director.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    directors = []
    for result in results:
        directors.append(generateDictData(result,worker_list_name_list))
    return directors

def getActorIds(film_id):
    sql = "select worker_id from film_actor where film_id = '%s'" % (film_id)
    actor_ids = select(sql)
    return actor_ids

def showActor(film_id):
    sql = "select film_actor.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_actor,worker_list " \
          "where film_id = '%s' and film_actor.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    actors = []
    for result in results:
        actors.append(generateDictData(result, worker_list_name_list))
    return actors

def getWriterIds(film_id):
    sql = "select worker_id from film_writer where film_id = '%s'" % (film_id)
    writer_ids = select(sql)
    return writer_ids

def showWriter(film_id):
    sql = "select film_writer.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_writer,worker_list " \
          "where film_id = '%s' and film_writer.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    writers = []
    for result in results:
        writers.append(generateDictData(result, worker_list_name_list))
    return writers

def showSingleWorker(request=None,worker_id=None):
    '''显示单个影人信息'''
    if request:
        worker_id = request.GET.get("worker_id")
    sql = "select * from worker_list where worker_id = '%s'" %(worker_id)
    results = select(sql)
    assert len(results) == 1
    data = generateDictData(results[0],worker_list_name_list)
    if request:
        return JsonResponse(data,safe=False)
    return data

def showPersonalThemes(request):
    '''显示个人主题'''
    user_id = request.GET.get("user_id")
    sql = "select user_theme.theme_id,theme_name from user_theme,theme_list " \
          "where user_id = '%s' and user_theme.theme_id = theme_list.theme_id" % (user_id)
    results = select(sql)
    name_list = ["theme_id", "theme_name"]
    data = []
    for result in results:
        data.append(generateDictData(result, name_list))
    return JsonResponse(data, safe=False)

def showMovieThemes(request=None,film_id=None):
    '''显示与特定电影有关的主题'''
    if request:
        film_id = request.GET.get("film_id")
    else:
        assert film_id
    sql = "select film_theme.theme_id,theme_name from film_theme,theme_list " \
          "where film_id = '%s' and film_theme.theme_id = theme_list.theme_id" % (film_id)
    results = select(sql)
    name_list = ["theme_id","theme_name"]
    data = []
    for result in results:
        data.append(generateDictData(result,name_list))
    if request:
        return JsonResponse(data,safe=False)
    else:
        return data

def showRecommendedMovies(request):
    '''根据用户的偏好主题推荐电影'''
    user_id = request.GET.get("id")
    sql = "select film_id from user_theme,film_theme " \
          "where user_id = '%s' and user_theme.theme_id = film_theme.theme_id" %(user_id)
    results = (np.unique(select(sql))).tolist()
    data = []
    for film_id in results:
        data.append(showMovie(request=None,film_id=film_id))
    return JsonResponse(data,safe=False)

def showAllThemes(request):
    '''显示所有主题'''
    sql = "select * from theme_list"
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,theme_list_name_list))
    return JsonResponse(data,safe=False)

def managerRegisterApply(request):
    '''管理员登陆注册'''
    manager_id = request.GET.get("manager_id")
    manager_name = request.GET.get("manager_name")
    password = request.GET.get("password")

    data = {
        "allowed": True,
        "idWrong": False,
        "nameWrong":False
    }
    # 记录mark
    sql = "select * from manager_list where manager_id = '%s'" % (manager_id)
    results = select(sql)
    if results:
        data["allowed"] = False
        data["idWrong"] = True
        return JsonResponse(data, safe=False)

    sql = "select * from manager_list where manager_name = '%s'" % (manager_name)
    results = select(sql)
    if results:
        data["allowed"] = False
        data["nameWrong"] = True
        return JsonResponse(data, safe=False)

    sql = "insert into manager_list(manager_id,manager_name,password) values('%s','%s','%s')"\
          % (manager_id,manager_name,password)
    insert(sql)
    return JsonResponse(data, safe=False)

def managerLoginCheck(request):
    '''管理员登陆校验'''
    manager_id = request.GET.get("manager_id")
    password = request.GET.get("password")

    sql = "select * from manager_list where manager_id = '%s'" % (manager_id)
    results = select(sql)
    data = {
        "allowed": True,
        "idWrong": False,
        'pwdWrong': False
    }
    # 记录mark
    if results:
        row = results[0]
        if password != row[2]:
            #密码不对
            data["pwdWrong"] = True
            data["allowed"] = False
    else:
        data["allowed"] = False
        data["idWrong"] = True
    return JsonResponse(data, safe=False)

def addWorker(request):
    worker_name = request.GET.get("worker_name")
    worker_picture = request.GET.get("worker_picture")
    worker_introduction = request.GET.get("worker_introduction")
    film_id = request.GET.get("film_id")
    type = request.GET.get("type")
    sql = "call addWorker('%s','%s','%s','%s'，'%s')" % (worker_name,worker_picture,worker_introduction,film_id,type)
    mark = procedureCall(sql)
    return JsonResponse(mark,safe=False)

def uploadPicture(request):
    user_id = request.GET.get("user_id")
    user_picture = request.GET.get("user_picture")
    sql = "select * from user_list where user_id = '%s'" % (user_id)
    mark = False
    if select(sql):
        sql = "update user_list set user_picture = '%s' where user_id = '%s'" % (user_picture,user_id)
        mark = update(sql)
    return JsonResponse(mark,safe=False)

def addClub(request):
    '''添加粉丝团'''
    worker_id = request.GET.get("worker_id")
    club_name = request.GET.get("club_name")

    data = {
        "success":True
    }

    sql = "select * from fan_club where worker_id = '%s'" % (worker_id)
    results = select(sql)
    if results:
        data["success"] = False
        return JsonResponse(data,safe=False)
    sql = "insert into fan_club(worker_id,club_name) values('%s','%s')"%(worker_id,club_name)
    data["success"] = insert(sql)
    return JsonResponse(data,safe=False)

def joinClub(request):
    '''将用户移入粉丝团'''
    user_id = request.GET.get("user_id")
    club_id = request.GET.get("club_id")
    sql = "select * from fan_club where club_id = '%s'" % (club_id)
    results = select(sql)
    if not results:
        mark = False
        return JsonResponse(mark,safe=False)
    sql = "insert into user_in_club(user_id,club_id) values('%s','%s')"%(user_id,club_id)
    mark = insert(sql)
    return JsonResponse(mark,safe=False)

def quitClub(request):
    '''将用户移出粉丝团'''
    user_id = request.GET.get("user_id")
    club_id = request.GET.get("club_id")
    sql = "select * from user_in_club where user_id = '%s' and club_id = '%s'" % (user_id,club_id)
    results = select(sql)
    if results:
        sql = "delete from user_in_club where user_id = '%s' and club_id = '%s'" % (user_id,club_id)
        mark = delete(sql)
        return JsonResponse(mark,safe=False)
    else:
        mark = False
        return JsonResponse(mark,safe=False)

def showFans(request):
    '''显示所有粉丝信息 除了密码'''
    club_id = request.GET.get("club_id")
    data = []
    sql = "select user_list.user_id,user_list.user_name,user_list.gender,user_list.email,user_list.phone,user_list.user_picture from user_in_club,user_list " \
          "where user_in_club.club_id = '%s' and user_in_club.user_id = user_list.user_id" % (club_id)
    results = select(sql)
    for result in results:
        data.append(generateDictData(result,user_list_name_list))
    return JsonResponse(data,safe=False)

def showWorker(request):
    '''显示粉丝团的worker'''
    club_id = request.GET.get("club_id")
    sql = "select worker_list.worker_id,worker_list.worker_name,worker_list.worker_picture,worker_list.worker_introduction " \
          "from worker_list,fan_club " \
          "where worker_list.worker_id = fan_club.worker_id and fan_club.club_id = '%s'" % (club_id)
    results = select(sql)
    assert len(results) == 1
    for result in results:
        data = generateDictData(result,worker_list_name_list)
        return JsonResponse(data,safe=False)

def showClubs(request):
    '''显示粉丝团所有信息(不包括粉丝)'''
    data = []
    sql = "select fan_club.club_id,fan_club.club_name," \
          "worker_list.worker_id,worker_list.worker_name,worker_list.worker_picture,worker_list.worker_introduction " \
          "from worker_list,fan_club " \
          "where worker_list.worker_id = fan_club.worker_id"
    results = select(sql)
    for result in results:
        data.append(generateDictData(result,fan_club_name_list + worker_list_name_list))
    return JsonResponse(data,safe=False)

def showJoinedClubs(request):
    '''显示用户已经加入的粉丝团'''
    user_id = request.GET.get("user_id")
    data = []
    sql = "select fan_club.club_id,fan_club.club_name," \
          "worker_list.worker_id,worker_list.worker_name,worker_list.worker_picture,worker_list.worker_introduction " \
          "from worker_list,fan_club,user_in_club " \
          "where user_in_club.user_id = '%s' and user_in_club.club_id = fan_club.club_id " \
          "and fan_club.worker_id = worker_list.worker_id" % (user_id)
    results = select(sql)
    for result in results:
        data.append(generateDictData(result, fan_club_name_list + worker_list_name_list))
    return JsonResponse(data, safe=False)

def clubCheck(request):
    user_id = request.GET.get("user_id")
    club_id = request.GET.get("club_id")
    data = {}
    data["inClub"] = True
    sql = "select * from user_in_club where user_id = '%s' and club_id = '%s'" % (user_id,club_id)
    results = select(sql)
    if not results:
        data["inClub"] = False
    return JsonResponse(data,safe=False)

def getMoviesOfWorker(worker_id):
    '''返回与worker有关的电影id(已去重)'''
    num = 5
    sql = "select film_id from film_actor where worker_id = '%s'" % (worker_id)
    film_ids = select(sql)
    sql = "select film_id from film_director where worker_id = '%s'" % (worker_id)
    film_ids += select(sql)
    sql = "select film_id from film_writer where worker_id = '%s'" % (worker_id)
    film_ids += select(sql)
    film_ids = list(set(film_ids))[:num]
    return film_ids

def getWorkersOfFilmId(film_id):
    '''返回与film_id对应电影下的所有worker(已去重)'''
    sql = "select worker_id from film_actor where film_id = '%s'" % (film_id)
    worker_ids = select(sql)
    sql = "select worker_id from film_director where film_id = '%s'" % (film_id)
    worker_ids += select(sql)
    sql = "select worker_id from film_writer where film_id = '%s'" % (film_id)
    worker_ids += select(sql)
    worker_ids = list(set(worker_ids))
    return worker_ids

def getPartialFilmInfo(film_ids):
    data = []
    for film_id in film_ids:
        sql = "select * from film_info where film_id = '%s'" % (film_id)
        results = select(sql)
        assert len(results) == 1
        result = results[0]
        data.append(generateDictData(result,film_info_name_list))
    return data

def showParticipatedMovies(request):
    '''搜索出该影人参演的所有电影'''
    worker_id = request.GET.get("worker_id")
    film_ids = getMoviesOfWorker(worker_id)
    data = getPartialFilmInfo(film_ids)
    return JsonResponse(data,safe=False)

def getRelatedWorkerId(worker_id):
    '''返回所有与worker合作过的workers(不包括自己)'''
    num = 10
    film_ids = getMoviesOfWorker(worker_id)
    worker_ids = []
    for film_id in film_ids:
        worker_ids += getWorkersOfFilmId(film_id)
    worker_ids = list(set(worker_ids))[:num]
    if worker_id in worker_ids:
        worker_ids.remove(worker_id)
    return worker_ids

def showRelatedWorkers(request):
    '''搜索出该影人参演的所有电影中包含的影人们（不包括自己）'''
    worker_id = request.GET.get("worker_id")
    worker_ids = getRelatedWorkerId(worker_id)
    data = []
    for worker_id in worker_ids:
        data.append(showSingleWorker(request=None,worker_id=worker_id))
    return JsonResponse(data,safe=False)

def showClubRelatedMovies(request):
    '''搜索出粉丝团对应影人的所有参演电影'''
    club_id = request.GET.get("club_id")
    sql = "select worker_id from fan_club where club_id = '%s'" % (club_id)
    results = select(sql)
    assert len(results) == 1
    worker_id = results[0]
    film_ids = getMoviesOfWorker(worker_id)
    data = getPartialFilmInfo(film_ids)
    return JsonResponse(data,safe=False)

def showRelatedClubs(request):
    '''搜索出粉丝团对应影人 所有合作影人 的 粉丝团（不包括自己）'''
    club_id = request.GET.get("club_id")
    sql = "select worker_id from fan_club where club_id = '%s'" % (club_id)
    results = select(sql)
    assert len(results) == 1
    worker_id = results[0]
    worker_ids = getRelatedWorkerId(worker_id)
    data = []
    for worker_id in worker_ids:
        sql = "select fan_club.club_id,fan_club.club_name,worker_list.worker_picture " \
              "from fan_club,worker_list " \
              "where fan_club.worker_id = '%s' and fan_club.worker_id = worker_list.worker_id" % (worker_id)
        results = select(sql)
        assert len(results) <= 1
        if len(results) == 0:
            continue
        result = results[0]
        data.append(generateDictData(result,fan_club_name_list + [worker_list_name_list[2]]))
    return JsonResponse(data,safe=False)

def searchWorker(request):
    keyword = request.GET.get("keyword")
    keyword = "%" + keyword + "%"
    sql = "select * from woker_list where worker_name like '%s'" % (keyword)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,worker_list_name_list))
    return JsonResponse(data,safe=False)

def searchClub(request):
    keyword = request.GET.get("keyword")
    keyword = "%" + keyword + "%"
    sql = "select fan_club.club_id,fan_club.club_name,worker_list.worker_name,worker_list.worker_picture " \
          "from fan_club,woker_list " \
          "where fan_club.club_name like '%s' and fan_club.worker_id = worker_list.worker_id" % (keyword)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result, fan_club_name_list + worker_list_name_list[1:3]))
    return JsonResponse(data, safe=False)

def getThemeIds(film_id):
    sql = "select theme_id from film_theme where film_id = '%s'" % (film_id)
    theme_ids = select(sql)
    assert theme_ids
    return theme_ids

def getFilmIds():
    sql = "select film_id from film_info"
    film_ids = select(sql)
    assert film_ids
    return film_ids

def judgeSimilarity(judging, tar):
    cnt = 0
    for theme_id in judging:
        if theme_id in tar:
            cnt += 1
        if cnt >= 2:
            return True
    return False

def showRelatedMovies(request):
    film_id = request.GET.get("film_id")
    theme_ids = getThemeIds(film_id)
    all_film_ids = getFilmIds()
    data = []
    for judging_film_id in all_film_ids:
        if judgeSimilarity(getThemeIds(judging_film_id),theme_ids):
            data.append(showMovie(request=None,film_id=judging_film_id))
    return JsonResponse(data,safe=False)

def showRelatedClubOfMovie(request):
    film_id = request.GET.get("film_id")
    worker_ids = getDirectorIds(film_id) + getActorIds(film_id) + getWriterIds(film_id)
    assert worker_ids
    data = []
    for worker_id in worker_ids:
        sql = "select fan_club.club_id,fan_club.club_name,worker_list.worker_name,worker_list.worker_picture " \
              "from fan_club,woker_list " \
              "where fan_club.worker_id = worker_list.worker_id and worker_list.worker_id = '%s'" % (worker_id)
        results = select(sql)
        assert len(results) == 1
        data.append(generateDictData(results[0],fan_club_name_list + worker_list_name_list[1:3]))
    return JsonResponse(data,safe=False)

def getClubs():
    data = []
    sql = "select fan_club.club_id,fan_club.club_name,worker_list.worker_name,worker_list.worker_picture " \
          "from fan_club,woker_list " \
          "where fan_club.worker_id = worker_list.worker_id"
    results = select(sql)
    for result in results:
        data.append(generateDictData(result, fan_club_name_list + worker_list_name_list[1:3]))
    return data

def showAllWorkers(request):
    data = []
    sql = "select * from worker_list"
    results = select(sql)
    for result in results:
        data.append(generateDictData(result, worker_list_name_list))
    return JsonResponse(data, safe=False)

def showFiveClubs(request):
    num = 5
    data = getClubs()[-num:]
    return JsonResponse(data,safe=False)

def showTopFiveMovies(request):
    num = 5
    data = showMovieRanks(request=None)[:num]
    return JsonResponse(data,safe=False)

def showFiveTopics(request):
    num = 5
    data = getTopics()[:num]
    return JsonResponse(data,safe=False)