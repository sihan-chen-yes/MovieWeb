import pymysql
from django.shortcuts import render
from django.http.response import JsonResponse
# Create your views here.

user = "root"
password = "123"
database = "movie"
host = "localhost"

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

def showAllMovies(request):
    '''显示film_info中的所有电影'''
    data = {}
    data["film_info"] = []
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from film_info"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        data["film_info"].append({
            "film_id":result[0],
            "film_name":result[1],
            "film_date":result[2],
            "film_area":result[3],
            "film_score":result[4],
            "film_score_people":result[5],
            "introduction":result[6],
            "picture":result[7],
            "video":result[8]
        })
    db.close()
    return JsonResponse(data, safe=False)

def showMovie(request):
    '''根据电影id显示该电影信息'''
    film_id = request.GET.get("film_id")
    data = {}
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from film_info where film_id = '%s'" % (film_id)
    cursor.execute(sql)
    film = cursor.fetchone()
    data["film_id"] = film[0]
    data["film_name"] = film[1]
    data["film_date"] = film[2]
    data["film_area"] = film[3]
    data["film_score"] = film[4]
    data["film_score_people"] = film[5]
    data["introduction"] = film[6]
    data["picture"] = film[7]
    data["video"] = film[8]
    db.close()
    return JsonResponse(data,safe=False)

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
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    sql = "select * from film_info where film_name like '%s'" % (film_name)
    cursor.execute(sql)
    results = cursor.fetchall()
    data = []
    for film in results:
        data.append({
            "film_id": film[0],
            "film_name": film[1],
            "film_date": film[2],
            "film_area": film[3],
            "film_score": film[4],
            "film_score_people": film[5],
            "introduction": film[6],
            "picture": film[7],
            "video": film[8]
        })
    db.close()
    return JsonResponse(data,safe=False)

def insertData(sql):
    db = pymysql.connect(user=user, password=password, database=database, host=host)
    cursor = db.cursor()
    cursor.execute(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def select(sql):
    db = pymysql.connect(user=user,password=password,database=database,host=host)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results

def generateDictData(result,name_list):
    dict = {}
    for i in range(len(result)):
        dict[name_list[i]] = result[i]
    return dict

def showTopics(request):
    film_id = request.GET.get("film_id")
    sql = "select * from topic_list where film_id = '%s'" % (film_id)
    results = select(sql)
    data = []
    name_list = ["topic_id","film_id","user_id","title","topic_text","topic_time"]
    for result in results:
        data.append(generateDictData(result,name_list))
    return JsonResponse(data,safe=False)

def showBroadcasts(request):
    topic_id = request.GET.get("topic_id")
    sql = "select * from broadcast_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    data = []
    name_list = ["broadcast_id","topic_id","user_id","broadcast_text","broadcast_time"]
    for result in results:
        data.append(generateDictData(result,name_list))
    return JsonResponse(data,safe=False)

def showSingleTopic(request):
    topic_id = request.GET.get("topic_id")
    sql = "select * from topic_list where topic_id = '%s'" % (topic_id)
    results = select(sql)
    name_list = ["topic_id","film_id","user_id","title","topic_text","topic_time"]
    for result in results:
        data = generateDictData(result,name_list)
        break
    return JsonResponse(data,safe=False)

def addTopic(request):
    film_id = request.GET.get("film_id")
    user_id = request.GET.get("user_id")
    title = request.GET.get("title")
    topic_text = request.GET.get("topic_text")
    topic_time = request.GET.get("topic_time")
    sql = "insert into topic_list(film_id,user_id,title,topic_text,topic_time) values('%s','%s','%s','%s','%s')" % \
          (film_id,user_id,title,topic_text,topic_time)
    insertData(sql)
    # op success
    data = True
    return JsonResponse(data,safe=False)

def addBroadcast(request):
    topic_id = request.GET.get("topic_id")
    user_id = request.GET.get("user_id")
    broadcast_text = request.GET.get("broadcast_text")
    broadcast_time = request.GET.get("broadcast_time")
    sql = "insert into broadcast_list(topic_id, user_id, broadcast_text, broadcast_time) values('%s','%s','%s','%s')" % \
          (topic_id, user_id, broadcast_text, broadcast_time)
    insertData(sql)
    #op success
    data = True
    return JsonResponse(data,safe=False)