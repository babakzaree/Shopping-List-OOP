import os
import json
from helpers.colorama_funcs import red


def clear_screen():
    '''Clear the terminal.'''
    return os.system('clear')


def price_after_discount(total_price, percent):
    return (percent * total_price) / 100


def show_products(role: str):
    with open("./product/products.json", mode='r') as f:
        products_json: dict = json.load(f)
        for category in products_json.keys():
            print(f"{category} ".ljust(13, '_'))
            print("|".rjust(13))
            for product in products_json[category].keys():
                print("             ----------------------------------------------")  # noqa E501
                if role == 'admin':
                    print(f"            Name: {product}  x {products_json[category][product]['amount']}")  # noqa E501
                else:
                    print(f"            Name: {product}")
                print(f"            Price: {products_json[category][product]['price']} $") # noqa E501
                print("             ----------------------------------------------")  # noqa E501


def add_product(name: str, price: int, category: str, amount: int, products: dict):  # noqa E501
    if category in products.keys():
        if name not in products[category].keys():
            products[category][name] = {
                'price': price,
                'amount': amount
            }
        else:
            products[category][name]['amount'] += amount


def remove_product(name: str, category: str, amount: int, products: dict):
    if amount < 0:
        amount = abs(amount)

    if amount == 0:
        raise ValueError("Amount can't be Zero.")

    if not isinstance(amount, int):
        raise TypeError("Amount type should be int.")

    result = False
    # Check if the product is available in database
    if name in products[category].keys():
        if products[category][name]['amount'] <= amount:
            # completely remove product from json
            del products[category][name]
        else:
            products[category][name]['amount'] -= amount
            result = True
    return result


def total_price(cart: dict):

    total_price = int()

    for category in cart.keys():
        for product in cart[category].keys():
            # multiplication of each product price in amount
            product_total_price = (cart[category][product]['price']) * \
                (cart[category][product]['amount'])
            total_price += product_total_price
    # return the total price of items in the cart
    return total_price


def show_cart(cart: dict, user_balance):
    for category in cart.keys():
        print(f"{category} ".ljust(13, '_'))
        print("|".rjust(13))
        for product in cart[category].keys():
            print("             ----------------------------------------------")         # noqa E501
            print(f"            Name: {product}  x {cart[category][product]['amount']}") # noqa E501
            print(f"            Price: {cart[category][product]['price']} $")
            print("             ----------------------------------------------")         # noqa E501
    if (user_balance - total_price(cart)) < 0:
        # print total balance in red color if user money isn't enough
        print(f"Total Price of Cart: {red(str(total_price(cart)))} $")
    else:
        print(f"Total Price of Cart: {total_price(cart)} $")


def add_to_cart(product_name: str, category: str, price: int, amount: int, cart: dict):  # noqa E501
    # if category is available
    if category in cart.keys():
        # if product is available in category
        if product_name in cart[category].keys():
            # add specified amount of product to cart
            cart[category][product_name]['amount'] += amount
            # add new product to available category
        else:
            cart[category].update({product_name: {
                'amount': amount,
                'price': price
            }})
    else:
        # add product to cart with specified amount, price and category
        cart[category] = {
            product_name: {
                'amount': amount,
                'price': price
            }
        }


def remove_from_cart(product_name: str, category: str, amount: int, cart: dict) -> bool:  # noqa E501
    result = False
    # if product is available in cart
    if product_name in cart[category].keys():
        # if specified amount is more than or equal to amount of product
        # in cart
        if cart[category][product_name]['amount'] <= amount:
            # if there is only one product in specified category
            if len(cart[category]) == 1:
                # completely remove category from cart
                del cart[category]
            else:
                # completely remove product from cart
                del cart[category][product_name]
            result = True
        else:
            # remove specified amount from cart
            cart[category][product_name]['amount'] -= amount
            result = True
    return result
