from src.models.Product import Product


def get_product_from_json(json_product):
    return Product(
        json_product['id'],
        json_product['name'],
        json_product['price'],
        json_product['quantity']
    )