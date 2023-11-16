from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

ma = Marshmallow(app)
db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(100))
    date_created = db.Column(db.Date())

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description','date, status')

# card_schema = CardSchema()

# cards_schema = CardSchema(many = True)

@app.cli.command('db_create')
def db_create():
    db.drop_all()
    print("Tables dropped")
    db.create_all()
    print ('Created Tables')

@app.cli.command('db_seed')
def db_seed():
    
    cards = [

    Card(
        title = 'Start the project',
        description = 'Stage 1 - Creation ERD',
        status = 'done',
        date_created = date.today()
    ),

    Card(
        title = "ORM Queries",
        description = "Stage 2, Implement CRUD",
        status = 'In progress',
        date_created = date.today()
    ),

    Card(
        title = "SQLAlchemy and Marshmallow",
        description = "Stage 3, integrate modules",
        status ='In progress',
        date_created = date.today()
    ),

    ]
    
    db.session.add_all(cards)



    db.session.commit()
    print('Database seeded')



@app.route('/cards')
def all_cards():
    # select * from cards;
    stmt = db.select(Card).where(db.or_(Card.status != 'done', Card.id > 2)).order_by(Card.title)
    print (stmt)
    cards = db.session.scalars(stmt).all()
    return CardSchema(many = True).dump(cards)



@app.route('/')
def index():
    return 'MAIN PAGE'