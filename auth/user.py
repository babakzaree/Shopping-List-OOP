from helpers.exceptions import (
    TypeUsernameError,
    WrongUsernameError,
    PasswordLengthError,
    TypePasswordError
    )

import json


class BaseUser:

    # Constructor

    def __init__(self, username, password, balance) -> None:
        self.username = username
        self.password = password
        self.balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be int or float.")
        if value < 0:
            value = abs(value)
        self.__balance = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeUsernameError()
        if not value[0].isalpha():
            raise WrongUsernameError()
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypePasswordError()
        if len(value) < 8:
            raise PasswordLengthError()
        self.__password = value

    # Magic methods

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.username}>'


class User(BaseUser):

    # instance methods
    def add_purchase_history(self, purchase_no: int, cart: dict):
        result = False

        if not isinstance(purchase_no, int):
            raise TypeError("purchase_no should be an int.")

        if not isinstance(cart, dict):
            raise TypeError("cart should be an dict.")

        # load users.json in users_json dictionary
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)

        # add new key,value pairs to users.json
        users_json[self.username]['purchases'][purchase_no] = {
            'cart': cart
        }
        result = True

        # dump new dictionary to users.json
        with open("./auth/users.json", mode='w') as f:
            json.dump(users_json, f, indent=4, separators=(', ', ': '))

        return result

    def use_discount(self, discount: str):
        """Use (remove) discount code from users.json"""
        result = False

        if not isinstance(discount, str):
            raise TypeError("Discount code should be an string.")
        # load the users.json
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)
        # remove discount code
        del users_json[self.username]['discounts'][discount]
        # dump updated users.json
        with open("./auth/users.json", mode='w') as f:
            json.dump(users_json, f, indent=4, separators=(', ', ': '))
            result = True
        return result

    def get_percent_of_discount(self, discount: str):
        if not isinstance(discount, str):
            raise TypeError("Discount code should be an string.")
        # load the users.json
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)
        result: int = users_json[self.username]['discounts'][discount]

        return result

    def check_discount(self, discount: str):
        '''Check if given discount code is in instance user discount codes.
        Return True if it was available.'''
        result = False

        if not isinstance(discount, str):
            raise TypeError("Discount code should be an string.")
        # load the users.json
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)
        # if discount its in users discount codes
        if discount in users_json[self.username]['discounts'].keys():
            result = True

        return result

    def add_discount(self, discount: dict, percent: int):
        '''Add new discount code to instance user.
        Return True if adding new discount code to users.json was
        successfuly.'''
        result = False
        if not isinstance(discount, dict):
            raise TypeError("Discount code should be an dictionary.")
        if not isinstance(percent, int):
            raise TypeError("Percentage of discount should be an int.")
        # load the users.json
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)
        # add new discount code to 'discounts' dict in users.json
        users_json[self.username]['discounts'][discount] = percent
        # dump edited users.json to old users.json
        with open("./auth/users.json", mode='w') as f:
            json.dump(users_json, f, indent=4, separators=(', ', ': '))
            result = True
        return result

    def get_role(self) -> str:
        """Return the role of instance user."""
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)
        return users_json[self.username]['role']

    def set_role(self, role: str):
        """ ### set role (permission) of user. (admin or user)
        Return
        ------
        - True if changing role was successfuly.
        - otherwise False"""

        if role not in ('user', 'admin'):
            raise ValueError("role must be 'user' or 'admin'.")

        result = False
        with open("./auth/users.json", mode='r') as f:
            users_json: dict = json.load(f)

            if users_json[self.username]['role'] == role:
                return result

            else:
                users_json[self.username]['role'] = role
                with open("./auth/users.json", mode='w') as f:
                    json.dump(users_json, f, indent=4, separators=(', ', ': '))
                    result = True

        return result

    def check_password(self, value: str):
        if self.password != value:
            raise ValueError("Password not match to confirm password.")

    def add_balance(self, value: int):
        '''Add balance to instance of user, and to the users.json'''
        if value < 0:
            raise ValueError("Value must be greater than zero.")

        if not isinstance(value, (int, float)):
            raise TypeError('Value must be "int" or "float".')

        self.balance += value

        with open('./auth/users.json', mode='r') as f:
            users_json = json.load(f)
            if self.username in users_json.keys():
                with open('./auth/users.json', mode='w') as f:
                    users_json[self.username]['balance'] = self.balance
                    json.dump(users_json, f, indent=4, separators=(', ', ': '))

    def decrease_balance(self, value: int):
        '''decrease balance from instance of user, and from the users.json'''
        result = False
        if value < 0:
            raise ValueError("Value must be greater than zero.")
        if not isinstance(value, (int, float)):
            raise TypeError('Value must be "int" or "float".')

        if self.balance >= value:
            with open('./auth/users.json', mode='r') as f:
                users_json = json.load(f)
                if self.username in users_json.keys():
                    self.balance -= value
                    users_json[self.username]['balance'] = self.balance
                    with open('./auth/users.json', mode='w') as f:
                        json.dump(users_json, f, indent=4, separators=(', ', ': ')) # noqa E501
                        result = True
        return result

    def get_balance(self):
        '''get the balance of current user'''
        with open("./auth/users.json", mode='r') as f:
            users_json = json.load(f)
            return users_json[self.username]['balance']

    def change_password(self, password: str):
        ''' Changing the password of user in 'users.json' database.'''
        result = False
        if password != self.password:
            with open("./auth/users.json", mode='r') as f:
                users_json = json.load(f)
                users_json[self.username]['password'] = password
            with open('./auth/users.json', mode='w') as f:
                json.dump(users_json, f, indent=4, separators=(', ', ': '))
                result = True
        return result

    # Class methods

    @classmethod
    def login(cls, username, password):
        '''user authenication. Return True if authenicated.'''
        is_authenicated = False
        if cls.does_username_exist(username):
            if password == cls.read_password_from_file(username):
                is_authenicated = True
            return is_authenicated

    @classmethod
    def create_account(cls, username, password, balance):
        result = False
        with open('./auth/users.json', mode='r') as f:
            users_json = json.load(f)
            if not cls.does_username_exist(username):
                with open('./auth/users.json', mode='w') as f:
                    users_json[username] = {
                        'password': password,
                        'balance': balance,
                        'role': 'user',
                        'discounts': dict(),
                        'purchases': dict()
                    }
                    json.dump(users_json, f, indent=4, separators=(', ', ': '))
                    result = True
        return result

    # Static methods

    @staticmethod
    def read_password_from_file(username):
        '''Read the password of specified username from database'''

        with open('./auth/users.json', mode='r') as f:
            users_database = json.load(f)
            user_password = users_database[username]['password']
            return user_password

    @staticmethod
    def does_username_exist(username):
        '''Return True if username was exist in database.'''

        with open('./auth/users.json', mode='r') as f:
            result = False
            users_database = json.load(f)
            if username in users_database.keys():
                result = True
            return result

    @staticmethod
    def read_balance_from_file(username) -> float:
        '''read the balance from json.
        For usecases that you haven't created an instance of User class.'''
        with open("./auth/users.json", mode='r') as f:
            users_json = json.load(f)
            return users_json[username]['balance']
