import pymysql
from django.shortcuts import render
from django.http.response import JsonResponse
import pandas as pd
# Create your views here.

user = "root"
password = "123"
database = "movie"
host = "localhost"
#表头
topic_list_name_list = ["topic_id","film_id","user_id","title","topic_text","topic_time"]
broadcast_list_name_list = ["broadcast_id","topic_id","user_id","broadcast_text","broadcast_time"]
film_info_name_list = ["film_id","film_name","film_date",
                       "film_area","film_score","film_score_people","introduction","picture","video"]
worker_list_name_list = ["worker_id","worker_name","worker_picture","worker_introduction"]

#分别定位到不同的html页面
def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

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

def loginCheck(request):
    '''登陆校验'''
    id = request.GET.get("id")
    pwd = request.GET.get("pwd")

    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from user_list where user_id = '%s'" %(id)
    cursor.execute(sql)
    row = cursor.fetchone()

    data = {
        "allowed" : True,
        "idWrong" : False,
        'pwdWrong' : False
    }

    if row:
        if pwd != row[2]:
            data["pwdWrong"] = True
            data["allowed"] = False
    else:
        data["allowed"] = False
        data["idWrong"] = True
    db.close()
    return JsonResponse(data, safe=False)

def registerApply(request):
    '''注册申请'''
    id = request.GET.get("id")

    data = {
        "allowed": True,
        "idWrong": False,
        "nameWrong":False
    }

    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from user_list where user_id = '%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        data["allowed"] = False
        data["idWrong"] = True
        return JsonResponse(data, safe=False)

    name = request.GET.get("name")
    sql = "select * from user_list where user_name = '%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        data["allowed"] = False
        data["nameWrong"] = True
        return JsonResponse(data, safe=False)

    pwd = request.GET.get("pwd")
    sql = "insert into user_list(user_id,user_name,password) values('%s','%s','%s')" % (id,name,pwd)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    return JsonResponse(data, safe=False)

def edit(request):
    '''个人资料编辑'''
    gender = request.GET.get("gender")
    email = request.GET.get("email")
    phone = request.GET.get("phone")
    id = request.GET.get("id")

    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "update user_list set gender = '%s',email = '%s',phone = '%s' where user_id = '%s'" % (gender,email,phone,id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    data = {
        "allowed":True
    }
    db.close()
    return JsonResponse(data, safe=False)

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
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from user_collection where user_id = '%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        film_id = result[2]
        sql2 = "select * from film_info where film_id = '%s'" % (film_id)
        cursor.execute(sql2)
        film = cursor.fetchone()
        data["film_info"].append({
            "film_id":film[0],
            "film_name":film[1],
            "film_date":film[2],
            "film_area":film[3],
            "film_score":film[4],
            "film_score_people":film[5],
            "introduction":film[6],
            "picture":film[7],
            "video":film[8]
        })
    sql3 = "select * from user_list where user_id = '%s'" %(id)
    cursor.execute(sql3)
    user_info = cursor.fetchone()
    try:
        data["name"] = user_info[1]
    except:
        data["name"] = None
    try:
        data["gender"] = user_info[3]
    except:
        data["gender"] = None
    try:
        data["email"] = user_info[4]
    except:
        data["email"] = None
    try:
        data["phone"] = user_info[5]
    except:
        data["phone"] = None

    db.close()
    return JsonResponse(data,safe=False)

def collect(request):
    user_id = request.GET.get("id")
    film_id = request.GET.get("film_id")
    data = True
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from user_collection where user_id = '%s' and film_id = '%s'" % (user_id,film_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        data = False
    else:
        sql = "insert into user_collection(user_id,film_id) values('%s','%s')" % (user_id,film_id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()
    return JsonResponse(data, safe=False)

def cancelCollect(request):
    user_id = request.GET.get("id")
    film_id = request.GET.get("film_id")
    data = True
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from user_collection where user_id = '%s' and film_id = '%s'" % (user_id, film_id)
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        data = False
    else:
        sql = "delete from user_collection where user_id = '%s' and film_id = '%s'" % (user_id,film_id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()
    return JsonResponse(data, safe=False)

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

def insertData(sql):
    '''插入信息'''
    db = pymysql.connect(user=user, password=password, database=database, host=host)
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

def select(sql):
    '''显示信息'''
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results

def delete(sql):
    '''删除信息'''
    db = pymysql.connect(user=user, password=password, database=database, host=host)
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

def update(sql):
    '''更新信息'''
    db = pymysql.connect(user=user, password=password, database=database, host=host)
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

def showTopics(request):
    '''显示所有话题'''
    film_id = request.GET.get("film_id")
    sql = "select * from topic_list where film_id = '%s'" % (film_id)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,topic_list_name_list))
    return JsonResponse(data,safe=False)

def showBroadcasts(request):
    '''显示所有子话题'''
    topic_id = request.GET.get("topic_id")
    sql = "select * from broadcast_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    data = []
    for result in results:
        data.append(generateDictData(result,broadcast_list_name_list))
    return JsonResponse(data,safe=False)

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
    data = insertData(sql)
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
    data = insertData(sql)
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
        mark = insertData(sql)
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

def showMovieRanks(request):
    '''按照电影评分rank返回电影信息'''
    sql = "select * from film_info"
    results = select(sql)
    assert results
    data = []
    for result in results:
        data.append(generateDictData(result,film_info_name_list))
    #按评分降序排列
    data.sort(key=lambda x:x["film_score"],reverse=True)
    return JsonResponse(data,safe=False)

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

def showDirector(film_id):
    sql = "select film_director.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_director,worker_list " \
          "where film_id = '%s' and film_director.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    directors = []
    for result in results:
        directors.append(generateDictData(result,worker_list_name_list))
    return directors


def showActor(film_id):
    sql = "select film_actor.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_actor,worker_list " \
          "where film_id = '%s' and film_actor.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    actors = []
    for result in results:
        actors.append(generateDictData(result, worker_list_name_list))
    return actors

def showWriter(film_id):
    sql = "select film_writer.worker_id,worker_name,worker_picture,worker_introduction " \
          "from film_writer,worker_list " \
          "where film_id = '%s' and film_writer.worker_id = worker_list.worker_id" % (film_id)
    results = select(sql)
    writers = []
    for result in results:
        writers.append(generateDictData(result, worker_list_name_list))
    return writers

def showSingleWorker(request):
    '''显示单个影人信息'''
    worker_id = request.GET.get("worker_id")
    sql = "select * from worker_list where worker_id = '%s'" %(worker_id)
    results = select(sql)
    assert len(results) == 1
    data = generateDictData(results[0],worker_list_name_list)
    return JsonResponse(data,safe=False)

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
    user_id = request.GET.get("user_id")
    sql = "select film_id from user_theme,film_theme " \
          "where user_id = '%s' and user_theme.theme_id = film_theme.theme_id" %(user_id)
    results = select(sql)
    data = []
    for film_id in results:
        data.append(showMovie(request=None,film_id=film_id))
    return JsonResponse(data,safe=False)


