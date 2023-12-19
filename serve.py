from flask import Flask, render_template, request, redirect, url_for, session
import logging
from cryptography.fernet import Fernet
import hashlib

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

wait = "ablest"

answer = "reject";

key = Fernet.generate_key()
fernet = Fernet(key)
token = fernet.encrypt(wait.encode())


hashpass = hashlib.new("sha256")
hashpass.update(wait.encode())
hashKey = hashpass.hexdigest()

# def verifyPassword(password):
#     checkToken = fernet.encrypt(password.encode())
#     return fernet.decrypt(token).decode() == fernet.decrypt(checkToken).decode()

def verifyPassword(password):
    tempHashpass = hashlib.new("sha256")
    tempHashpass.update(password.encode())
    tempHashKey = tempHashpass.hexdigest()
    print(hashKey)
    print(tempHashKey)
    return tempHashKey == hashKey

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")

        mess = ""
        # print(password)
        if(verifyPassword(password)):
            mess = "accept"
        elif (password != wait and password != ""):
            mess = "reject"
        else: 
            mess = "write password"
        global answer
        if (answer == "accept"):
            answer = "reject"
        answer = mess;

        return render_template("index.html", message = mess);
    else:
        return render_template("index.html", message="write password");

@app.route("/getAnswer", methods=["GET", "POST"])
def getAnswer():
    global answer
    if request.method == "GET":
        return answer;

@app.route("/getKey", methods=["GET", "POST"])
def getKey():
    return key;


if __name__ == "__main__":
    app.run()