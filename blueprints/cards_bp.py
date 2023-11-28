from flask import Blueprint,request,abort
from flask_jwt_extended import jwt_required
from setup import db
from models.card import CardSchema, Card
from auth import admin_required


cards_blueprint = Blueprint('cards',__name__, url_prefix = '/cards')

@cards_blueprint.route("/")
@jwt_required()
def all_cards():
    admin_required()

    # select * from cards;
    stmt = db.select(
        Card
    )  # .where(db.or_(Card.status != 'Done', Card.id > 2)).order_by(Card.title.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

# get one card

@cards_blueprint.route('/<int:id>')
@jwt_required()
def one_card(id):
    stmt = db.select(Card).filter_by(id=id) # .where (Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return { 'error' : 'card not found' }, 404

# create

@cards_blueprint.route('/', methods=['POST'])
def new_card():
    card_info = CardSchema(exclude =["date_created","id"]).load(request.json)
    card  = Card(
        title =card_info['title'],
        description =card_info['description'],
        status = card_info.get('status', 'To do')
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201


#update card

@cards_blueprint.route('/<int:id>', methods = ['PUT', 'PATCH'])
def update_card(id):
    card_info = CardSchema(exclude =["date_created","id"]).load(request.json)
    stmt = db.select(Card).filter_by(id=id) # .where (Card.id == id)
    card = db.session.scalar(stmt)
    
    if card:
        card.title = card_info.get('title', card.title)
        card.description = card_info.get('description', card.description)
        card.status =card_info.get('status', card.status)
        db.session.commit()
        return CardSchema().dump(card),200
    else:
        return { 'error' : 'card not found' }, 404


#delete

@cards_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_card(id):
    # admin_required()
    stmt = db.select(Card).filter_by(id=id) # .where(Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {f'Card status : {id}': 'Deleted'}, 200
    else:
        return {'error': 'Card not found'}, 404


