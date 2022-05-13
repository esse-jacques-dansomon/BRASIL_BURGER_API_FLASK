from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .Address import Address
from .Order import Order
from .OrderItem import OrderItem
from .Product import Product
from .Address import Address
from .Complement import Complement
from .ComplementType import ComplementType
from .Payment import Payment
from .Menu import Menu
from .Client import Client
from .Burger import Burger
