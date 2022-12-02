from app import db
from datetime import datetime
from ast import literal_eval
from psycopg2.extensions import AsIs,adapt
from psycopg2 import sql

def fetch_park(text1:str,text2:str,text3:str) -> dict:
    conn = db.connect()
    v1 = f"%{text1}%"
    v2 = f"%{text2}%"
    v3 = text3.replace("'","")
    v3 = v3.replace('"',"")
    query = """CALL sort_park(%s,%s,%s)"""
    query_results = conn.execute(query,(v1,v2,v3)).fetchall() 
    conn.close()
    park_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "image_url": result[1],
            "park_name": result[2], 
            "address": literal_eval(result[3])[0]["line1"]+", "+literal_eval(result[3])[0]["line2"]+literal_eval(result[3])[0]["line3"]+literal_eval(result[3])[0]["city"]+", "+literal_eval(result[3])[0]["stateCode"]+", "+literal_eval(result[3])[0]["postalCode"],
            "entrance_fee": result[4],
            "contact": result[5],
            "url": result[6],
            "state_code": result[7],
            "avg_rating": result[8],
            "comments_cnt": result[9],
            "park_code": result[10],
            "event_cnt": result[11]
        }
        park_list.append(item)
    return park_list

def fetch_park_without_rating() -> dict:
    conn = db.connect()

    query = """SELECT id,image_url,park_name,address,entrance_fee,phone_number,url, 'NA' AS avg_rating, 'NA' AS comments_cnt, 'NA' AS event_cnt, park_code from Parks"""
    query_results = conn.execute(query).fetchall() 
    conn.close()
    park_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "image_url": result[1],
            "park_name": result[2], 
            "address": literal_eval(result[3])[0]["line1"]+", "+literal_eval(result[3])[0]["line2"]+literal_eval(result[3])[0]["line3"]+literal_eval(result[3])[0]["city"]+", "+literal_eval(result[3])[0]["stateCode"]+", "+literal_eval(result[3])[0]["postalCode"],
            "entrance_fee": result[4],
            "contact": result[5],
            "url": result[6],
            "avg_rating": result[7],
            "comments_cnt": result[8],
            "event_cnt": result[9],
            "park_code":result[10]
        }
        park_list.append(item)
    return park_list

def fetch_comments(userid:int) -> dict:
    conn = db.connect()
    query_results = conn.execute("""SELECT id,park_name, rating, comments FROM Comments
                                    WHERE user_id ={};""".format(userid)).fetchall()
    conn.close()
    comment_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "park_name": result[1],
            "rating": result[2],
            "comments": result[3],
           
        }
        comment_list.append(item)
    return comment_list



def update_park_code(task_id: int, text: str ,now) -> None:
    conn = db.connect()
    query = 'Update Comments set park_name = "{}", update_time = "{}" where id = {};'.format(text, now,task_id)
    conn.execute(query)
    conn.close()
def update_rating(task_id: int, rating: int,now) -> None:
    conn = db.connect()
    query = 'Update Comments set rating = {}, update_time = "{}" where id = {};'.format(rating,now, task_id)
    conn.execute(query)
    conn.close()

def update_comments(task_id: int, comments: str,now) -> None:
    conn = db.connect()
    query = 'Update Comments set comments = "{}", update_time = "{}" where id = {};'.format(comments, now,task_id)
    conn.execute(query)
    conn.close()

def find_comments(task_id: int) -> None:
    conn = db.connect()
    query = 'SELECT * FROM Comments  where id = {};'.format(task_id)
    
    query_results = conn.execute(query)
    query_results = [x for x in query_results]
    old_park_name = query_results[0][6]
    old_rating = query_results[0][3]
    old_comments = query_results[0][4]
    conn.close()
    return ([old_park_name,old_rating,old_comments])
####################
def find_user_id(username:str) -> int:
    conn = db.connect()
    if username == "":
        query = 'SELECT id FROM Users;'
    else:
        query = 'SELECT id FROM Users WHERE username = "{}";'.format(username)
    query_results = conn.execute(query)
    query_results = [x for x in query_results]
    return (query_results[0][0])

###
def insert_new_task(park_name: str,rating: int, text: str, userid:int, now) ->  None:

    conn = db.connect()
    #     time = datetime.now()
    query = 'Insert Into Comments (user_id, park_name, rating, comments, update_time) VALUES ({},"{}",{}, "{}","{}");'.format(
        userid, park_name, rating, text,now)
    conn.execute(query)
    # query_results = conn.execute("Select LAST_INSERT_ID();")
    # query_results = [x for x in query_results]
    # task_id = query_results[0][0]
    conn.close()
    #return task_id

def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Comments where id={};'.format(task_id)
    conn.execute(query)
    conn.close()

def advance_query1() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT park_code, ROUND(AVG(rating),2) AS avg_rating FROM Comments GROUP BY park_code HAVING AVG(rating) >3 and park_code IN (SELECT park_code FROM Parks WHERE park_name NOT IN (SELECT DISTINCT park_name FROM Events)) UNION SELECT park_code, ROUND(AVG(rating),2)AS avg_rating FROM Comments GROUP BY park_code HAVING AVG(rating) >2 and park_code IN (SELECT park_code FROM Parks WHERE park_name IN (SELECT DISTINCT park_name FROM Events));").fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "park_code": result[0],
            "avg_rating": result[1],
        }
        query_list.append(item)
    return query_list


def advance_query2() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT Events.id, park_name, comment_cnt FROM (SELECT park_code, COUNT(*) AS comment_cnt FROM Comments WHERE YEAR(update_time) >=2021 GROUP BY park_code HAVING AVG(rating) >3 ORDER BY  comment_cnt DESC) a JOIN Parks USING (park_code) JOIN Events USING (park_name) WHERE date_start LIKE %s or date_end LIKE %s;",('2022-10%','2022-11%')).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "event_id": result[0],
            "park_name": result[1],
            "comment_cnt": result[2],
        }
        query_list.append(item)
    return query_list

def fetch_users() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT * from Users;").fetchall()
    # if query_results:
    #     return True
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "username": result[1],
            "password": result[2],
        }
        query_list.append(item)
    return query_list

def insert_new_user(username: str,password: str) ->  None:
    conn = db.connect()
    query = 'Insert Into Users (username,password) VALUES ("{}","{}");'.format(
        username,password)
    conn.execute(query)
    # query_results = conn.execute("Select LAST_INSERT_ID();")
    # query_results = [x for x in query_results]
    # task_id = query_results[0][0]
    conn.close()
    #return task_id

def fetch_all_parks() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT park_name from Parks;").fetchall()
    # if query_results:
    #     return True
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "park_name": result[0]
        }
        query_list.append(item)
    return query_list

def fetch_visit_center(park_code:str) ->  dict:
    conn = db.connect()
    query = 'SELECT DISTINCT phone_number, facility_name, description, standard_hours, url FROM Visitorcenters WHERE park_code = "{}";'.format(
        park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "phone_number": result[0],
            "facility_name": result[1],
            "description": result[2],
            "standard_hours": result[3],
            "url": result[4]
        }
        query_list.append(item)
    return query_list

def fetch_image_url(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT image_url FROM Parks WHERE park_code = "{}" limit 1;'.format(
        park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "image_url": result[0]
        }
        query_list.append(item)
    return query_list

def fetch_basic(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT DISTINCT description,standard_hour,entrance_fee,url FROM Parks WHERE park_code = "{}";'.format(
        park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "description": result[0],
            "standard_hour": result[1],
            "entrance_fee": result[2],
            "url": result[3]
        }
        query_list.append(item)
    return query_list

def fetch_park_name(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT park_name FROM Parks WHERE park_code = "{}" limit 1;'.format(
        park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "park_name": result[0]
        }
        query_list.append(item)
    return query_list

def fetch_event(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT title, regres_url, dates,description FROM Events WHERE park_name = (SELECT park_name FROM Parks WHERE park_code  = "{}") '.format(park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "title": result[0],
            "regres_url": result[1],
            "dates": result[2],
            "description": result[3]
        }
        query_list.append(item)
    return query_list

def fetch_alerts(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT category, description, title, url FROM Alerts WHERE park_code = "{}" and title IS NOT NULL;'.format(park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "category": result[0],
            "description": result[1],
            "title": result[2],
            "url": result[3]
        }
        query_list.append(item)
    return query_list

def park_comments(park_code: str) -> dict:
    conn = db.connect()
    query = 'SELECT user_id,comments, rating,update_time FROM Comments  WHERE park_code = "{}";'.format(park_code)
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "user_id": result[0],
            "comments": result[1],
            "rating": result[2],
            "update_time": result[3]
        }
        query_list.append(item)
    return query_list

def fetch_position() -> dict:
    conn = db.connect()
    query = 'SELECT latitude, longitude, park_name, park_code FROM Parks WHERE park_name != "Blackwell School National Historic Site"; '
    query_results = conn.execute(query).fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "lat": result[0],
            "lon": result[1],
            "popup": result[2],
            "park_code":result[3]
        }
        query_list.append(item)
    return query_list