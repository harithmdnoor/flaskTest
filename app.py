from flask import Flask , render_template, request
from datetime import datetime, timedelta
from selenium import webdriver
import time 
import re
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    username = request.form['username']
    password = request.form['password']
    data = checkPay(username,password)
    return render_template('hello_there.html',data = data)

def checkPay(userInput,passInput):
    browser = webdriver.Chrome(executable_path="C:/Users/harith/Downloads/chromedriver_win32 (3)/chromedriver.exe")
    todayDate = datetime.today()
    yesterdayDate = todayDate - timedelta(days=1)
    url1 = "https://abs.rafflesmedical.com.sg/eroster/Account/Logout"

    url2 ="https://abs.rafflesmedical.com.sg/eroster/Attendance/History?DateFrom={}&DateTo={}".format("01-March-2021",yesterdayDate.strftime("%d-%B-%Y"))
    browser.get(url1)

    usernameInput = browser.find_element_by_id('editorUserName')
    usernameInput.send_keys(userInput)
    passwordInput= browser.find_element_by_id("password")
    passwordInput.send_keys(passInput)
    locationInput = browser.find_element_by_id('ddlClusters')
    for option in locationInput.find_elements_by_tag_name('option'):
        if option.text == "Pasir Ris Elias (PRE)":
            option.click()
    submitBtn = browser.find_element_by_class_name("btn-info")
    submitBtn.click()
    time.sleep(1)
    browser.get(url2)
    workHistory = browser.find_element_by_class_name("list-group")
    shiftList =[]
    ciList =[]
    coList=[]

    for row in workHistory.find_elements_by_xpath('li'):
        if row.text.split("\n")[1] == "Pasir Ris Elias":

            shiftList.append(row.text.split("\n")[0])
            ciList.append(datetime.strptime(row.text.split("\n")[2][4:],"%H:%M"))
            coList.append(datetime.strptime(row.text.split("\n")[-1][4:],"%H:%M"))
        aprilPay=0.0
        mayPay=0
        junePay=0
        julyPay=0
        for i in range(len(shiftList)):
            if shiftList[i].split(" ")[2]=="Apr":
                aprilPay+=(((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13
            elif shiftList[i].split(" ")[2]=="May":
                mayPay+=(((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13
            elif shiftList[i].split(" ")[2]=="Jun":
                junePay+=(((coList[i]-ciList[i])-timedelta(hours=1)).total_seconds()/3600)*13
    browser.close()
    returnVal ={"username":userInput,
                "aprilPay": aprilPay,
                "mayPay": mayPay,
                "junePay":junePay}

    return returnVal