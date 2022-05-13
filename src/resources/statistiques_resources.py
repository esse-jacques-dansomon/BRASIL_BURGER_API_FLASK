import datetime

from flask import Blueprint, jsonify

from src.constantes.url_prefix import PREFIX_URL
from src.models.Order import Order

statistiques = Blueprint('statistiques', __name__, url_prefix=PREFIX_URL + '/statistiques')

@statistiques.get('')
def get_statistiques():
    #order_of_the_day
    orders_of_the_day = Order.query.filter(Order.created_at.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))).all()
    orders_of_the_day = len([order.serialize() for order in orders_of_the_day])
    #orders_accepted_of_the_day
    orders_accepted_of_the_day = Order.query.filter(Order.created_at.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))).filter(Order.status == 'Terminer').all()
    orders_accepted_of_the_day = len([order.serialize() for order in orders_accepted_of_the_day])
    #total_amount_of_orders_of_the_day
    orders_accepted_of_the_day_somme = Order.query.filter(Order.created_at.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))).filter(Order.status == 'Terminer').all()
    total_amount_of_orders_of_the_day = sum(order.total for order in orders_accepted_of_the_day_somme)

    #orders_of_the_day_by_status
    orders_of_the_day_by_status = Order.query.filter(Order.created_at.between(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1))).filter(Order.status == 'Annuler').all()
    orders_of_the_day_by_status = len([order.serialize() for order in orders_of_the_day_by_status])
    #burger_most_buy_of_the_day
    return jsonify({
        'orders_of_the_day': orders_of_the_day,
        'orders_accepted_of_the_day': orders_accepted_of_the_day,
        'total_amount_of_orders_of_the_day': total_amount_of_orders_of_the_day,
        'orders_of_the_day_by_status': orders_of_the_day_by_status

    })