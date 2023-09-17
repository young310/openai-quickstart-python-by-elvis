import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



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
        file_content = open(os.getcwd() + "\\transaction.txt").readlines()
        response = response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "以下都用繁體中文跟html語法回答，越短越好"},
                {"role": "system", "content": "你是一個具備十年經驗的會計師，專精審計與洗錢防制，我明天要開始當審計員了，可以幫我看一下資料?"},
                {"role": "user", "content": "用html畫成表格回答，只要<table>到</table>的內容，其他不要"},
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
        return redirect(url_for("tax_index", result=response.choices[0].message.content[response.choices[0].message.content.index('<table>'):response.choices[0].message.content.index('</table>')]))
    result = request.args.get("result")
    return render_template("tax_index.html", result=result)
