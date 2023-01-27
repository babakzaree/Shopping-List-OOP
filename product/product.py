import json


class Product:

    # Constructor

    def __init__(self, name, price, category, amount) -> None:
        self.name = name
        self.price = price
        self.category = category
        self.amount = amount

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Product Name must be string.")
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Product Price must be int or float.")
        if value < 0:
            raise ValueError("Product Price must be at least Zero or greater.")
        self.__price = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Product Category must be string.")
        self.__category = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, (int)):
            raise TypeError("Product amount must be integer.")
        if value < 0:
            raise ValueError("Product amount must be at least Zero or greater.") # noqa E501
        self.__amount = value

    # Class methods

    @classmethod
    def add_product(cls, name, price, category, amount) -> bool:
        """
        ### Add new product to database.
        - Return True if adding was successful.
        - otherwise Return False."""

        if price < 0:
            raise ValueError("Price can't be less than Zero.")

        if not isinstance(price, (int, float)):
            raise TypeError("Price should be int or float.")

        if amount <= 0:
            raise ValueError("Amount can't be Zero or less.")

        if not isinstance(amount, int):
            raise TypeError("Amount should be int.")

        result = False

        with open("./product/products.json", mode='r') as f:
            products_json: dict = json.load(f)

            # if the given category is new
            if category not in products_json.keys():
                result = True
                # add the product to the database
                products_json[category] = {
                    name: {
                        'price': price,
                        'amount': amount
                    }
                }
            # if this product is not available in database
            # but the category is available
            if name not in products_json[category].keys():
                result = True
                selected_category: dict = products_json[category]
                # add the product to the category
                selected_category[name] = {
                    'price': price,
                    'amount': amount
                }
            with open("./product/products.json", mode='w') as f:
                json.dump(products_json, f, indent=4, separators=(', ', ': '))
            return result

    @classmethod
    def remove_product(cls, name, category, amount):
        """
        ### Remove specified amount of Product from database.
        - Return True if removing was successfuly.
        - otherwise False
        """
        if amount < 0:
            amount = abs(amount)

        if amount == 0:
            raise ValueError("Amount can't be Zero.")

        if not isinstance(amount, int):
            raise TypeError("Amount type should be int.")

        result = False
        # Check if the product is available in database
        products_json = cls.load_products()
        if name in products_json[category].keys():
            if products_json[category][name]['amount'] <= amount:
                # completely remove product from json
                del products_json[category][name]
            else:
                products_json[category][name]['amount'] -= amount
            if cls.dump_products(products_json):
                result = True
        return result

    @classmethod
    def change_price(cls, name, category, specified_price):
        """
        ### Changing price of product available in products database.
        - Return True if changing price was successfuly.
        - otherwise False
        """
        if not isinstance(specified_price, (int, float)):
            raise TypeError("Price must be int or float.")
        if specified_price < 0:
            raise ValueError("Price must be at least Zero or greater.")

        result = False
        products_json = cls.load_products()
        # Check if given category is correct.
        if category in products_json.keys():
            # Check if the product name is correct.
            if name in products_json[category].keys():
                # Changing the price of product
                products_json[category][name]['price'] = specified_price
                if cls.dump_products(products_json):
                    result = True
        return result

    @classmethod
    def change_category(cls, name: str, category: str, new_category: str) -> bool: # noqa E501
        """ ### Change the category of item.
        if new_category wasn't available in database,
        create an new category.

        Return
        ------
        - True if it was Successful.
        - otherwise False."""
        result = False
        products_json = cls.load_products()
        # Check if given category is correct.
        if category in products_json.keys():
            # Check if the product name is correct.
            if name in products_json[category].keys():
                # catch the product info
                selected_product = products_json[category][name]
                # delete the product from previous category
                del products_json[category][name]
                products_json[new_category][name] = selected_product
            if cls.dump_products(products_json):
                result = True
        return result

    @classmethod
    def is_available(cls, category: str, product_name: str) -> bool:
        result = False
        products_json = cls.load_products()
        if product_name in products_json[category].keys():
            result = True
        return result

    # Static methods

    @staticmethod
    def load_products() -> dict:
        """ ### Load the 'products.json' database.
        Return
        ------
        - True if loading the json file was successful.
        - otherwise False"""

        with open("./product/products.json", mode='r') as f:
            result: dict = json.load(f)
        return result

    @staticmethod
    def dump_products(dicionary: dict) -> bool:
        """ ### Dump the dicitonary to the 'products.json' database.
        Return
        ------
        - True if dump to json was successful.
        - otherwise False"""

        result = False
        with open("./product/products.json", mode='w') as f:
            json.dump(dicionary, f, indent=4, separators=(', ', ': '))
            result = True
        return result
