from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#連接資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TodoList.db'
db = SQLAlchemy(app)

#建立資料表
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.String(50), nullable=False)

#新增
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_level = request.form['level']
        new_task = TodoList(content = task_content, level = task_level, date_created = datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks = TodoList.query.all()
        return render_template("index.html", tasks=tasks)

#刪除
@app.route('/delete/<int:id>')
def delete(id):
    task_delete = TodoList.query.get_or_404(id)
    db.session.delete(task_delete)
    db.session.commit()
    return redirect('/')

#修改
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_update = TodoList.query.get_or_404(id)
    if request.method == 'POST':
        task_update.content = request.form['update_content']
        task_update.level = request.form['update_level']
        db.session.commit()
        return redirect('/')
    else:
        tasks = TodoList.query.all()
        return render_template("index.html", tasks = tasks)

if __name__ == '__main__':
    app.run(debug = False)