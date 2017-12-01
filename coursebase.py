import os
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


class Professor(db.Model):
    __tablename__ = 'professors'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.string(64))
    about = db.Column(db.Text)
    classes = db.relationship('Class', backref='professor', cascade="delete")


class Class(db.model):
    __tablename__ = 'classes'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.string(256))
    about = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/professors')
def show_all_professors():
    professors = Professor.query.all()
    return render_template('professor-all.html', professors=professors)


@app.route('/professor/add', methods=['GET', 'POST'])
def add_professors():
    if request.method == 'GET':
        return render_template('professor-add.html')
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']

        professor = Professor(name=name, about=about)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))

@app.route('/professor/edit/<int:id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-edit.html' professor=professor)
    if request.method == 'POST':
        professor.name = request.form['name']
        professor.about = request.form['about']
        db.session.commit()
        return redirect(url_for('show_all_professors'))

@app.route('/classes')
def classes():
    classes = Class.query.all()
    return render_template('class-all.html', classes=classes)

@app.route('/class/add', methods=['GET', 'POST'])
def add_classes():
    if request.method == 'GET':
        professors = Professor.query.all()
        return render_template('class-add.html', professors=professors)
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        class = Class(name=name, about=about, professor=professor)

        db.session.add(class)
        db.session.commit()
        return redirect(url_for('show_all_classes'))

@app.route('/class/edit/<int:id>', methods=['GET', 'POST'])
def edit_class(id):
    class = Class.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('class-edit.html' class=class, professor=professor)
    if request.method == 'POST':
        class.name = request.form['name']
        class.about = request.form['about']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        class.professor = professor
        db.session.commit()
        return redirect(url_for('show_all_classes'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/users')
def show_all_users():
    return render_template('user-all.html')

@app.route('/form-demo', methods=['GET', 'POST'])
def form-demo():
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        return redirect(url_for('form-demo'))

@app.route('/user/<string:name>/')
def get_user_name(name):
    return render_template('user.html', name=name)

@app.route('/class.<int:id>/')
def get_class_id(id):
    return "Hi, this is %s and the class' id is %d" % ('administrator', id)

if __name__ == '__main__':
    app.run()
