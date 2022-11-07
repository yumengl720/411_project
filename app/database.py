from app import db
from datetime import datetime

def fetch_todo() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Parks").fetchall()
    conn.close()
    todo_list = []
    for result in query_results[0:20]:
        item = {
            "id": result[0],
            "park_code": result[2],
            "entrance_fee": result[6],
            "contact": result[5],
           
        }
        todo_list.append(item)
    return todo_list

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
def insert_new_task(text: str) ->  int:
    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
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