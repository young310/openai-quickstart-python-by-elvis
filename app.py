import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

file_content = open(os.getcwd() + "\\journal1.txt").readlines()
print(file_content)

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下都用中文回答，越短越好"},
                {"role": "user", "content": generate_prompt(animal)}
                
            ]
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero. 用繁體中文
Animal: {}
Names:""".format(
        animal.capitalize()
    )

@app.route("/acc", methods=("GET","POST"))
def acc_index():
    if request.method == "POST":
        question = request.form["question"]
        if '彙總' in question:
            file_content = open(os.getcwd() + "\\journal1.txt").readlines()
        else:
            file_content = open(os.getcwd() + "\\transaction.txt").readlines()
        
        #請幫我彙總資料，把年度放在column，把費用類別放在row，內容放借項，根據你產生的表格幫我做異常的費用
        #請幫我彙總資料，把年度放在column，把費用類別放在row，內容放借項，使用<table>語法畫成表格
        response = response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下都用繁體中文跟html語法回答"},
                {"role": "system", "content": "你是一個具備十年經驗的會計師，專精審計與洗錢防制，我明天要開始當審計員了，可以幫我看一下資料並給一些建議?"},
                {"role": "user", "content": "用html畫成表格回答"},
                {"role": "user", "content": question + "------" + ' '.join(file_content)}
                
            ]
        )
        return redirect(url_for("acc_index", result=response.choices[0].message.content))
    result = request.args.get("result")
    return render_template("acc_index.html", result=result)

@app.route("/tax", methods=("GET","POST"))
def tax_index():
    if request.method == "POST":
        question = request.form["question"]
        response = response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下都用繁體中文回答，越短越好"},
                {"role": "system", "content": "你是一個具備十年經驗的律師，專精稅法"},
                {"role": "user", "content": question}
                
            ]
        )
        return redirect(url_for("tax_index", result=response.choices[0].message.content))
    result = request.args.get("result")
    return render_template("tax_index.html", result=result)
