from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tinydb import TinyDB, Query
from tinydb.operations import delete
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db = TinyDB('db.json')
user = TinyDB('user.json')


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


@app.route("/checkPassword", methods=['POST'])
def check_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    User = Query()
    result = user.search(User.username == username)
    if result:
        if checkpw(password.encode(), result[0]['password'].encode()):
            return jsonify({"message": "success"})
        else:
            return jsonify({"message": "failed"})
    else:
        return jsonify({"message": "failed"})


@app.route("/updatePassword", methods=['POST'])
def update_password():
    data = request.get_json()
    username = data['username']
    currentPassword = data['currentPassword']
    newPassword = data['newPassword']

    User = Query()
    result = user.search(User.username == username)
    if result:
        if checkpw(currentPassword.encode(), result[0]['password'].encode()):
            user.update(
                {'password': hashpw(newPassword.encode(), gensalt()).decode()}, User.username == username)
            return jsonify({"message": "success"})
        else:
            return jsonify({"message": "failed"})
    else:
        return jsonify({"message": "failed"})


@app.route("/saveEvents", methods=['POST'])
def save_events():
    data = request.get_json()
    print(data)
    # replace whole db with new data
    db.truncate()
    db.insert_multiple(data["events"])
    return jsonify({"message": "success"})


@app.route("/addEvent", methods=['POST'])
def add_event():
    data = request.get_json()
    db.insert(data["event"])
    print(data)
    return jsonify({"message": "success"})


@app.route("/removeEvent", methods=['POST'])
def remove_event():
    data = request.get_json()
    # delete data where id == data["id"]
    print(data)
    Event = Query()
    db.remove(Event.id == data["id"])
    

    # db.remove(Event.id == data["id"])
    return jsonify({"message": "success"})


@app.route("/updateEvent", methods=['POST'])
def update_event():
    data = eval(request.form["event"])
    # save all files
    for file in request.files.getlist("images"):
        file.save("images/"+file.filename)
    Event = Query()
    
    db.update(data, Event.id == data["id"])
    return jsonify({"message": "success"})


@app.route("/uploadImages", methods=['POST'])
def upload_images():
    files = request.files.getlist("images")
    for file in files:
        file.save("images/"+file.filename)
    return jsonify({"message": "success"})


@app.route("/images/<path>")
def images(path):
    return send_file("images/"+path)


@app.route('/events', methods=['POST'])
def get_events():
    events = db.all()
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)
