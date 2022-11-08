""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """
    old_record = db_helper.find_comments(task_id)
    data = request.get_json()
    try:
        response1,response2,response3 = '','',''
        if (data["park_code"]!=old_record[0]):
            db_helper.update_park_code(task_id, data["park_code"])
            response1 = "Park Code Updated"
        if (data["rating"]!=old_record[1]):
            db_helper.update_rating(task_id, data["rating"])
            response2 = 'Rating Updated'
        if (data["comments"]!=old_record[2]):
            db_helper.update_comments(task_id, data["comments"])
            response3 = 'comments Updated'
        
        result = {'success': True, 'response': response1 + " " + response2 + " " + response3}
        if (not response1 and not response2 and not response3):
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)





@app.route('/', methods=['GET','POST'])
def index():
    items = db_helper.fetch_park('')
    if request.method == 'POST':
        variable = request.form['variable']
        items = db_helper.fetch_park(variable)
    items_c = db_helper.fetch_comments()
    return render_template("index.html", items=items, items_comment=items_c)

@app.route("/insert", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['park_code'], data['rating'], data['comments'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)
