from app import db
from datetime import datetime
from ast import literal_eval
from psycopg2.extensions import AsIs,adapt
from psycopg2 import sql

def fetch_park(text1:str,text2:str,text3:str) -> dict:
    conn = db.connect()
    # query_results = conn.execute("Select * from Parks where park_name LIKE %s  and state_code LIKE %s",('%' + text1 + '%',),('%' + text2 + '%',)).fetchall()
    v1 = f"%{text1}%"
    v2 = f"%{text2}%"
    v3 = text3.replace("'","")
    v3 = v3.replace('"',"")
    query = """SELECT t1.id, t1.image_url, t1.park_name, t1.address, t1.entrance_fee,t1.phone_number,t1.url,t1.state_code,t2.avg_rating,t2.comments_cnt
                                    FROM (SELECT * from Parks where park_name LIKE (%s) and state_code LIKE (%s)) as t1, (SELECT AVG(rating) as avg_rating,COUNT(comments) as comments_cnt,park_code from Comments group by park_code) as t2
                                    WHERE t1.park_code = t2.park_code
                                    ORDER BY %s"""

                                    
    query_results = conn.execute(query,(v1,v2,v3)).fetchall() 
    print(v1,v2,type(v3))
   
    
    # for i in query_results:
    #     results.append(i.replace("'",""))
    # results = conn.execute(results).fetchall()

    conn.close()
    park_list = []
    for result in query_results[0:150]:
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
        }
        park_list.append(item)

    if text3=="t1.park_name asc":
        park_list = sorted(park_list, key=lambda d: d['park_name']) 
    if text3=="t1.park_name desc":
        park_list = sorted(park_list, key=lambda d: d['park_name'],reverse=True) 
    if text3=="t2.avg_rating desc":
        park_list = sorted(park_list, key=lambda d: d['avg_rating'],reverse=True)   
    if text3=="t2.avg_rating asc":
        park_list = sorted(park_list, key=lambda d: d['avg_rating'])  
    if text3=="t2.comments_cnt desc":
        park_list = sorted(park_list, key=lambda d: d['comments_cnt'],reverse=True)   
    if text3=="t2.comments_cnt asc":
        park_list = sorted(park_list, key=lambda d: d['comments_cnt'])
    return park_list

def fetch_comments() -> dict:
    conn = db.connect()
    query_results = conn.execute("SELECT * from Comments WHERE user_id = 1;").fetchall()
    conn.close()
    comment_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "park_code": result[2],
            "rating": result[3],
            "comments": result[4],
           
        }
        comment_list.append(item)
    return comment_list



def update_park_code(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update Comments set park_code = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()
def update_rating(task_id: int, rating: int) -> None:
    conn = db.connect()
    query = 'Update Comments set rating = {} where id = {};'.format(rating, task_id)
    conn.execute(query)
    conn.close()

def update_comments(task_id: int, comments: str) -> None:
    conn = db.connect()
    query = 'Update Comments set comments = "{}" where id = {};'.format(comments, task_id)
    conn.execute(query)
    conn.close()

def find_comments(task_id: int) -> None:
    conn = db.connect()
    query = 'SELECT * FROM Comments  where id = {};'.format(task_id)
    
    query_results = conn.execute(query)
    query_results = [x for x in query_results]
    old_park_code = query_results[0][2]
    old_rating = query_results[0][3]
    old_comments = query_results[0][4]
    conn.close()
    return ([old_park_code,old_rating,old_comments])


def insert_new_task(park_code: str,rating: int, text: str) ->  None:
    conn = db.connect()
    #     time = datetime.now()
    query = 'Insert Into Comments (user_id, park_code, rating, comments) VALUES (1,"{}",{}, "{}");'.format(
        park_code, rating, text)
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