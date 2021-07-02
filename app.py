from flask import Flask , render_template, request
from datetime import datetime, timedelta
import time 
import requests
import re
from bs4 import BeautifulSoup
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    try: 
        payload={
            'userId': request.form['username'],
            'password': request.form['password'],
            'Cluster_Id':'8'
        }
        data = checkPay(payload)
        return render_template('hello_there.html',data = data)
    except:
        return render_template("error.html")

def checkPay(payload):
   
    todayDate = datetime.today()
    yesterdayDate = todayDate - timedelta(days=1)
    url1 = "https://abs.rafflesmedical.com.sg/eroster/Account/Login"

    url2 ="https://abs.rafflesmedical.com.sg/eroster/Attendance/History?DateFrom={}&DateTo={}".format("01-March-2021",yesterdayDate.strftime("%d-%B-%Y"))

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post(url1, data=payload)
        # print the html returned or something more intelligent to see if it's a successful login page.
        r = s.get(url2)
        soup = BeautifulSoup(r.text,"lxml")
        # print(workHistory)
        shiftList =[]
        ciList =[]
        coList=[]
        
        for row in soup.find_all("li",class_="list-group-item"):
            if row.text.split('\n')[4] == " Pasir Ris Elias":
                shiftList.append(row.text.split("\n")[3])
                ciList.append(datetime.strptime(row.text.split("\n")[10],"%H:%M"))
                coList.append(datetime.strptime(row.text.split("\n")[14],"%H:%M"))
            aprilPay=0.0
            mayPay=0
            junePay=0
            julyPay=0
            
            for i in range(len(shiftList)):
                if shiftList[i].split(" ")[2]=="Apr":
                    aprilPay+=((((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13)*.8
                elif shiftList[i].split(" ")[2]=="May":
                    mayPay+=((((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13)*.8
                elif shiftList[i].split(" ")[2]=="Jun":
                    junePay+=((((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13)*.8
                elif shiftList[i].split(" ")[2]=="Jul":
                    julyPay+=((((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13)*.8
    returnVal ={"username":payload.get("userId"),
                    "aprilPay": aprilPay,
                    "mayPay": mayPay,
                    "junePay":junePay,
                    "julyPay":julyPay}
    return returnVal
