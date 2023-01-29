from auth import User
from product import Product
from helpers.banner import print_banner
from helpers.messages import Message, PasswordErrors, UsernameErrors
from helpers.commands import Command
from helpers.colorama_funcs import blue, green, red, yellow
from helpers.help import print_help
from helpers.exceptions import (
    PasswordLengthError,
    RemoveProductError,
    TypeUsernameError,
    TypePasswordError
)
from helpers.functions import (
    clear_screen,
    price_after_discount,
    show_cart,
    show_products,
    add_product,
    remove_product,
    total_price,
    add_to_cart,
    remove_from_cart
)
import json
import time
import colorama
from random import randint

# Load JSON of products
with open("./product/products.json", mode='r') as f:
    products: dict = json.load(f)

cart = dict()  # cart of user

colorama.init(autoreset=True)  # setting of colorama

print_banner()  # print the banner of program

print(blue("* Welcome Page *"))
print(Message.HELP_MESSAGE)

# This variable declares that user is logged-in or logged-out.
logged_in = False

# get the initial input from user (create / login)
while logged_in is False:
    initial_command_input = input(Message.BEFORE_LOGIN).lower().strip()

    while True:
        if initial_command_input == 'login':
            clear_screen()
            print("Login to the app...\n")
            username = input('Username: ')
            password = input('Password: ')
            # if authenication is failed
            if not User.login(username, password):
                print(red(Message.AUTHENICATION_FAILED))
                time.sleep(1.25)
            else:
                # set the balance to new instance of User (readed from json)
                current_user_balance = User.read_balance_from_file(username)
                # create an instance of User class
                current_user = User(username, password, current_user_balance)
                current_user_role = current_user.get_role()
                clear_screen()
                print(f"Welcome Back {blue(username)}.")
                time.sleep(1)
                logged_in = True
                break
        if initial_command_input == 'create':
            clear_screen()
            print("Creating an new account...\n")
            username = input('Username: ')
            password = input('Password: ')

            # checking for username, password input correction
            try:
                # if account has been created successfuly
                if User.create_account(username, password, 30000):
                    print(Message.ACCOUNT_CREATED)
                    print(blue("Username: ") + green(username))
                    print(blue("Password: ") + green(password))
                    print("Redirecting to Login page... 4 Seconds.")
                    time.sleep(4)
                    initial_command_input = 'login'
                else:
                    print(red("Failed. Try again."))
            except TypeUsernameError:
                print(yellow(UsernameErrors.USERNAME_TYPE_ERROR))

            except TypePasswordError:
                print(yellow(PasswordErrors.PASSWORD_TYPE_ERROR))

            except PasswordLengthError:
                print(yellow(PasswordErrors.PASSWORD_LENGTH_ERROR))

            except TypeError:
                print(yellow("Balance must be int or float."))

            time.sleep(2)

    while logged_in is True:
        print(blue("* Home Page *"))
        print(f"({username})", end='')
        # if current user is an 'admin user' print like this
        if current_user_role == 'admin':
            print(green(f" ${str(current_user.get_balance())}"), end='')
            print(red(f" ({current_user_role})"))
        else:
            print(green(f" ${str(current_user.get_balance())}"))
        print(Message.HELP_MESSAGE+'\n')

        # get the input from user in home page (main input)
        user_input = input("Enter Command: ").strip().casefold()
        clear_screen()

        # < Help >
        if user_input in Command.HELP.value:
            print_help()

        # < Clear >
        elif user_input in Command.CLEAR.value:
            clear_screen()

        # < Balance >
        elif user_input in Command.BALANCE.value:
            clear_screen()
            print(f"Your balance: {green(str(current_user.get_balance()))} $")

        # < Charge >
        elif user_input in Command.CHARGE.value:
            clear_screen()
            # get the value of charge for wallet to increase
            charge_value = input('Value that you want to charge: ')
            try:
                charge_value = int(charge_value)
                # if casting to int was successful
                if isinstance(charge_value, int):
                    # add the charge to the instance of User and json database
                    current_user.add_balance(charge_value)
                    print("Your balance has been increased ", end='')
                    print(f"{green('+'+str(charge_value))} $")
                    print(f"Current balance: {current_user.get_balance()}")
            except ValueError:
                print(red("Wrong input. Value should be an number."))

        # < Change Password >
        elif user_input in Command.CHANGE_PASSWORD.value:
            clear_screen()
            # print some warnings and message
            print(red("WARNING!"))
            print(Message.TRY_CHANGE_PASS + {username})
            print("First, you need to authenicate again.")
            previous_password_input = input("Your current password: ")
            # if user is authenicated
            if User.login(username, previous_password_input):
                print(blue("OK! Now enter your new password."))
                # get the new password
                new_password_input = input("New Password: ")
                # if password changed successfuly
                if current_user.change_password(new_password_input):
                    print(green("OK!"))
                    print(blue("Password changed successfuly."))
                    print(blue("Your new password is now: "))
                    print(green(f" -> {new_password_input}"))
                else:
                    print("You can't set the same password. Try again.")
            # if authenication failed
            else:
                print(red("Authenication Failed."))

        # < Log-out >
        elif user_input == Command.LOGOUT.value:
            clear_screen()
            # get confirmation for logging-out
            log_out_confirm = input(red(Message.LOG_OUT_CONFIRM))
            # if confirmed
            if log_out_confirm.casefold().strip() == 'y':
                logged_in = False
                print("Logged Out.")
                break
            else:
                print(yellow("Canceled."))

        # < Exit >
        elif user_input in Command.EXIT.value:
            exit_confirm = input(red(Message.EXIT_CONFIRM))
            if exit_confirm.casefold().strip() == 'y':
                print()  # for set the color to default
                print("Hope to see you soon.")
                print("Quited.")
                exit()
            else:
                print(yellow("Canceled."))

        # < SHOW >
        elif user_input in Command.SHOW.value:
            clear_screen()
            if len(cart) <= 0:
                print(yellow("Your cart is empty."))
            else:
                print(blue("**    CART    **"))
                print()
                show_cart(cart, current_user_balance)

        # < Add >
        elif user_input in Command.ADD.value:
            clear_screen()
            print(blue("Adding to Cart..."))
            print(yellow("You can cancel adding item by entering 'cancel'."))
            product_category = input("Category: ").strip().casefold()
            if product_category.strip().lower() == 'cancel':
                print(yellow("Canceled."))
            else:
                product_name = input("Product Name: ").strip().casefold()
                product_amount = int(input("Amount: "))
                if not product_category.isalpha():
                    print(red("Category should be an string."))

                elif not product_name.isalpha():
                    print(red("Product Name should be an string."))

                elif not isinstance(product_amount, int):
                    print(red("Entered amount should be an integer."))

                else:
                    if Product.is_available(
                        product_category,
                        product_name,
                    ):
                        if remove_product(
                            product_name,
                            product_category,
                            product_amount,
                            products
                        ):
                            add_to_cart(
                                product_name,
                                product_category,
                                products[product_category][product_name]['price'],  # noqa E501
                                product_amount,
                                cart
                            )
                            print(green(f"+{product_name} x{product_amount}"))
                            print(green("Successfuly Added."))
                        else:
                            print(yellow(
                                f"Not enough amount of {product_name}."))
                    else:
                        print(yellow(
                            "Sorry. Product isn't available in stock."))

        # < Category >
        elif user_input in Command.CATEGORY.value:
            clear_screen()
            print(blue("** Categories of products **: \n"))
            for category in products.keys():
                print(blue(category.capitalize()))
                print(red("   |"))
                print(red("   -----"))
                print(red(f"         {len(products[category].keys())} items"))

        # < Remove >
        if user_input in Command.REMOVE.value:
            clear_screen()
            print(blue("Removing from Cart...\n"))
            print(yellow("You can cancel by entering 'cancel'."))
            product_category = input("Category of product: ")
            if product_category.lower().strip() == 'cancel':
                print("Canceled.")
            else:
                product_name = input("Product that you want to remove: ")\
                    .casefold().strip()
                product_amount = int(input("Amount: "))

                # remove product from cart
                remove_from_cart(
                    product_name,
                    product_category,
                    product_amount,
                    cart
                )
                # add removed products to dictionary of products
                add_product(
                    product_name,
                    cart[product_category][product_name]['price'],
                    product_category,
                    product_amount,
                    products
                )

        # < Prods >
        if user_input in Command.PRODS.value:
            clear_screen()
            print(blue("** Products of Store **"))
            show_products(current_user_role)

        # < Buy >
        if user_input in Command.BUY.value:
            print(blue("** Purchase Page **"))
            use_discount_confirm = input(Message.ASK_TO_USE_DISCOUNT)
            if use_discount_confirm.lower().strip() == 'y':
                discount_code = input("Enter your code: ").strip().lower()
                if not current_user.check_discount(discount_code):
                    print(red("Invalid Code!"))
                else:
                    percent = current_user.get_percent_of_discount(
                        discount_code)
                    final_price = price_after_discount(
                        total_price(cart),
                        percent
                        )
                    show_cart(cart, current_user_balance)
                    print(blue("You will get"), end='')
                    print(red(f"{percent}%"), end='')
                    print(blue("off on your cart."))
                    print("-----------------------")
                    print("Final Price: ", end='')
                    print(f"{final_price}")
                    purchase_confirm = input(Message.FINISH_PURCHASE)
                    # if user wants to finish the purchase
                    if purchase_confirm in Command.FINISH_PURCHASE.value:
                        purchase_no = randint(1000, 9999)
                        print(yellow(Message.PURCHASE_PROCESS))
                        time.sleep(1.5)
                        # decrease total price from user balance
                        if current_user.decrease_balance(final_price):
                            # removing products in the cart from products.json
                            for category in cart.keys():
                                for product in cart[category].keys():
                                    if not Product.remove_product(
                                        product,
                                        category,
                                        cart[category][product]['amount']
                                    ):
                                        raise RemoveProductError
                            # add purchase informations to users purchase
                            # history
                            current_user.add_purchase_history(
                                purchase_no,
                                cart
                            )
                            cart = dict()  # reset the cart
                            clear_screen()
                            print("\nYour purchase code is: ", end='')
                            print(f"{green(str(purchase_no))}")
                            print(green(Message.PURCHASE_SUCCESS))
                        # not enough balance
                        else:
                            print(red(Message.NOT_ENOUGH_BALANCE))
                    # Purchase canceled
                    else:
                        print(yellow(Message.PURCHASE_CANCEL))
            else:
                show_cart(cart, current_user_balance)
                purchase_confirm = input(Message.FINISH_PURCHASE)
                # if user wants to finish the purchase
                if purchase_confirm in Command.FINISH_PURCHASE.value:
                    purchase_no = randint(1000, 9999)
                    print(yellow(Message.PURCHASE_PROCESS))
                    time.sleep(1.5)
                    # decrease total price from user balance
                    if current_user.decrease_balance(total_price(cart)):
                        # removing products in the cart from products.json
                        for category in cart.keys():
                            for product in cart[category].keys():
                                if not Product.remove_product(
                                    product,
                                    category,
                                    cart[category][product]['amount']
                                ):
                                    raise RemoveProductError
                        # add purchase informations to users purchase
                        # history
                        current_user.add_purchase_history(
                            purchase_no,
                            cart
                        )
                        cart = dict()  # reset the cart
                        clear_screen()
                        print("\nYour purchase code is: ", end='')
                        print(f"{green(str(purchase_no))}")
                        print(green(Message.PURCHASE_SUCCESS))
                    # not enough balance
                    else:
                        print(red(Message.NOT_ENOUGH_BALANCE))

                # purchase cancel
                else:
                    print(yellow(Message.PURCHASE_CANCEL))
