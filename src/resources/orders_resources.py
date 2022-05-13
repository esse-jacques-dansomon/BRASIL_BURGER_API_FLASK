from datetime import datetime

from flask import Blueprint, jsonify, request


from src.constantes import http_status_code
from src.constantes.url_prefix import PREFIX_URL
from src.models.Client import Client
from src.models.Order import Order
from src.models.OrderItem import OrderItem
from src.models.Payment import Payment
from src.models.Product import Product
from src.services.lib import is_granted, getUser

orders = Blueprint('orders', __name__, url_prefix=PREFIX_URL + '/orders')


@orders.get('')
def get_all_orders():
    orders = Order.query.order_by(Order.id.desc()).all()
    return jsonify([order.serialize() for order in orders]), http_status_code.HTTP_200_OK


@orders.get('/filter/user/<customer_id>')
def get_orders_by_customer(customer_id):
    orders = Order.query.filter_by(client_id=customer_id).order_by(Order.id.desc()).all()
    return jsonify([order.serialize() for order in orders]), http_status_code.HTTP_200_OK


@orders.get('/filter/date/<date1>/<date2>')
def get_orders_by_date(date1, date2):
    orders = Order.query.filter(Order.created_at.between(date1, date2)).all()
    return jsonify([order.serialize() for order in orders]), http_status_code.HTTP_200_OK


@orders.get('/filter/status/<status>')
def get_orders_by_status(status):
    orders = Order.query.filter_by(status=status).all()
    return jsonify([order.serialize() for order in orders]), http_status_code.HTTP_200_OK

@orders.get('/filter/product/<name>')
def get_orders_by_product(name):
    orders = Order.query.filter(OrderItem.product_id == Product.id, Product.name.like('%' + name + '%')).all()
    #orders = Order.query.join(OrderItem).join(Product).filter(Product.name == name).all()
    return jsonify([order.serialize() for order in orders]), http_status_code.HTTP_200_OK


@orders.get('/<int:id>')
def get_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({
            'status': http_status_code.HTTP_404_NOT_FOUND,
            'message': 'Order not found',
            'error': True
        }), http_status_code.HTTP_404_NOT_FOUND
    return order.serialize(), http_status_code.HTTP_200_OK


@orders.post('')
@is_granted('ROLE_USER')
def create_order():
    user = getUser()
    user = Client.query.get(user.id)
    if user is None or user.id is None:
        return jsonify({
            'status': http_status_code.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorized',
            'error': True
        }), http_status_code.HTTP_401_UNAUTHORIZED
    print(request.json)

    if request.json is None or request.json == {} or 'order_items' not in request.json:
        return jsonify({
            'status': http_status_code.HTTP_400_BAD_REQUEST,
            'message': 'Bad request',
            'error': True
        }), http_status_code.HTTP_400_BAD_REQUEST
    order = Order(customer_id=user.id, total=0, more_information=request.json.get('more_information', ''))
    total = 0
    # creating order item
    item_count = 0
    for item in request.json.get('order_items'):
        product = Product.query.get(item.get('product_id'))
        if product is not None:
            quantity = item.get('quantity', 1)
            price = item.get('price', product.price)
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=price)
            total += int(price) * int(quantity)
            order.order_items.append(order_item)
            item_count += 1
    order.total = total
    if item_count == 0:
        return http_status_code.is_client_error()
    # creating payment
    payment = Payment(is_paid=False)
    if request.json.get('payment') is not None:
        is_paid = request.json.get('payment').get('is_paid', False)
        type = request.json.get('payment').get('type', '')
        if is_paid == True and type != '':
            payment = Payment(is_paid=is_paid, type=type)
            order.payment = payment
    order.payment = payment
    order.client_id = user.id
    order.client = user
    order.save()
    print(order.serialize())
    return order.serialize(), http_status_code.HTTP_201_CREATED


@orders.patch('/edit-status')
@is_granted('ROLE_ADMIN')
def edit_status():
    if request.json is None or request.json == {} or 'id' not in request.json or 'status' not in request.json:
        return http_status_code.is_client_error()
    order = Order.query.get(request.json.get('id'))
    if order is None:
        return http_status_code.is_client_error()
    if order.status == request.json.get('status'):
        return http_status_code.is_client_error()
    order.status = request.json.get('status')
    order.save()
    return order.serialize(), http_status_code.HTTP_200_OK


@orders.patch('/edit-payment')
@is_granted('ROLE_USER')
def edit_payment():
    if request.json is None or request.json == {} or 'id' not in request.json:
        return http_status_code.is_client_error()
    order = Order.query.get(request.json.get('id'))
    if order is None:
        return http_status_code.is_client_error()
    order.payment.paid_at = datetime.utcnow()
    order.payment.is_paid = True
    order.payment.type = request.json.get('type', 'cash')
    order.save()
    return order.serialize(), http_status_code.HTTP_200_OK
