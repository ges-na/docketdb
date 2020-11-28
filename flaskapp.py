from flask import Flask
from flask import render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import ipdb


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docketdb:docketdb@localhost:5432/docketdb'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def homepage():
    dockets = Docket.query.all()
    return render_template('homepage.html', dockets=dockets)
#@app.route('/officer/<officer_id>')
#def officer(officer_id):
#    return render_template('officer.html', officer=Officer.query.get(officer_id))
@app.route('/judge/<judge_id>')
def judge(judge_id):
    judge = Judge.query.filter_by(id=judge_id).first()
    return render_template('judge.html', judge=judge)


class Judge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    district = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Judge %r>' % self.id

class PoliceDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


    def __repr__(self):
        return '<PoliceDepartment %r>' % self.id


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Officer %r>' % self.id


class Docket(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    defendant = db.Column(db.String(80), unique=True, nullable=False)
    #birthdate may well be nullable
    birthdate = db.Column(db.String(80), unique=False, nullable=False)
    race = db.Column(db.String(80), unique=False, nullable=True)
    sex = db.Column(db.String(80), unique=False, nullable=False)
    complaint = db.Column(db.Integer, unique=True, nullable=False) 

    hearing_judge = db.Column(db.Integer, db.ForeignKey('judge.id'), nullable=True)
    judge = db.relationship('Judge', backref=db.backref('dockets', lazy=True))

    arresting_officer = db.Column(db.Integer, db.ForeignKey('officer.id'), nullable=True)
    officer = db.relationship('Officer', backref=db.backref('dockets', lazy=True))

    def __repr__(self):
        return '<Docket %r>' % self.id
