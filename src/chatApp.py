from flask import Flask, redirect, request, render_template, session
import csv
import os
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tamar_gilamiriam_!_@_?_chat_app"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


#app routes
@app.route("/", methods=['GET', 'POST'])
def toHomePage():
    return redirect("/register")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form["username"]
        password = request.form["password"]
        saveInCsv(name, password)
        return redirect('/login')
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form["username"]
        password = request.form["password"]
        exist = checkIfExist(name, password)
        if exist:
            session['username'] = name
            return redirect('/lobby')
    return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    session.pop('username', None)
    return redirect("/login")

@app.route("/lobby", methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            path='./rooms/'+room_name+".txt"
            open(path, 'w')
        rooms = os.listdir('./rooms')
        new_rooms = [x[:-4] for x in rooms]
        print(new_rooms)
        return render_template('lobby.html', room_names = new_rooms)
    else:
        return redirect('/login')

@app.route("/chat/<room>", methods=['GET', 'POST'])
def chatPage(room):
    return render_template('chat.html', room = room)


@app.route("/api/chat/<room>", methods=['GET', 'POST'])
def update_chat(room):
    path = os.getenv('CHAT_ROOM_PATH')
    path = f'{path}{room}.txt'
    if request.method == 'POST':
        if 'username' in session:
            name = session['username']
        else:
            name = "guest"
        message = request.form['msg']
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(path, 'a') as f:
            f.write(f'[{time}] {name}: {message}\n')
        f.close()
   
    if request.method == "GET":
        with open(path, 'rt') as f:
            f.seek(0)
            content = f.read()
            return content

# help functions

def saveInCsv(name, password):
    with open('users.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row != "":
                if name == row[0]:
                    f.close()
                    return True
    with open('users.csv', 'a') as f:
        enc_password = password.encode('ascii')
        enc64_password = base64.b64encode(enc_password)
        password = enc64_password.decode('ascii')
        writer = csv.writer(f)
        writer.writerow([name, password])
    return False

def checkIfExist(name, password):
    enc_password = password.encode('ascii')
    enc64_password = base64.b64encode(enc_password)
    password = enc64_password.decode('ascii')    
    with open('users.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if name == row[0] and password == row[1]:
                return True
        return False
    

@app.route('/clear/<room>', methods=['GET', 'POST'])
def clear(room):
    name = session['username']
    with open("./rooms/"+room+".txt", 'r') as f:
        lines = f.readlines()

    with open("./rooms/"+room+".txt", 'w') as f:
        for line in lines:
            if name not in line:
                f.write(line)
    return render_template('chat.html', room=room)

@app.route('/health')
def health():
    return ("OK",200)


if __name__ == "__main__":
    app.run(host='0.0.0.0')