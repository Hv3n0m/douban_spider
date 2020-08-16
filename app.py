from flask import Flask, render_template, request
import datetime
import sqlite3

app = Flask(__name__)




@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return render_template("index.html")

@app.route('/movie')
def movie():
    movelist = []
    con = sqlite3.connect('movie250.db')
    cur = con.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        movelist.append(item)
    cur.close()
    con.close()
    return render_template("movie.html", movelist=movelist)

@app.route('/score')
def score():
    return render_template("score.html")

@app.route('/word')
def word():
    return render_template("word.html")

# 表单提交
@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('/result.html', result=result)

@app.route("/user/<name>")
def welcome(name):
    return "你好 %s" % name

@app.route("/user/<int:id>")
def welcome2(id):
    return "你好,%d号会员" %id

if __name__ == '__main__':
    app.run(debug=True)