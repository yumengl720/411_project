from app import db
from datetime import datetime

def fetch_park(text:str) -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Parks where park_name LIKE %s",('%' + text + '%',)).fetchall()
    conn.close()
    park_list = []
    for result in query_results[0:20]:
        item = {
            "id": result[0],
            "park_name": result[3],
            "entrance_fee": result[6],
            "contact": result[5],
           
        }
        park_list.append(item)
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



def update_task_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

def update_status_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()
def insert_new_task(park_code: str,rating: int, text: str) ->  int:
    time = datetime.now()
    conn = db.connect()
    query = 'Insert Into Comments (user_id, park_code, rating, comments, update_time) VALUES (1,"{}",{}, "{}", time);'.format(
        park_code, rating, text)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()
    return task_id

# def insert_comments(comment: str, parkcode: str, rating: int):
#     conn = db.connect()
#     cursor = conn.cursor()
#     cursor.execute("select * from Comments")
#     results = cursor.fetchall()
#     userid = len(results)
#     time = datetime.now()
#     query = 'Insert Into Comment`s (user_id, park_code, rating, comments, update_time) 
#             VALUES ("{userid}");'.format(text, "Todo")



def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()