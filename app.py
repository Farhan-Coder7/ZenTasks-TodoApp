from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Zen.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Zen(db.Model):
    No = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default = datetime.now(timezone.utc))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Zen(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    Todo = Zen.query.all()
    return render_template('index.html', Todo=Todo)

@app.route('/update/<int:no>', methods=['GET', 'POST'])
def update(no):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Zen.query.filter_by(No=no).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    todo = Zen.query.filter_by(No=no).first()
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:no>')
def delete(no):
    todo = Zen.query.filter_by(No=no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template ('about.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        results = Zen.query.filter(Zen.title.ilike(f'%{query}%')).all()
        return render_template('search_results.html', results=results, query=query)
    return render_template('search_results.html', results=[], query="")



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)