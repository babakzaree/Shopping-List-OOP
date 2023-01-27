from enum import Enum


class Command(Enum):
    # NORMAL COMMANDS
    SHOW = ('show', 'list')
    PRODS = ('prods', 'product', 'products')
    HELP = ('help', 'helpme', 'h')
    CATEGORY = ('category', 'categories')
    ADD = ('add', 'additem')
    CHARGE = ('charge', 'addmoney')
    BALANCE = ('balance', 'wallet', 'mymoney', 'mywallet', 'mybalance')
    CHANGE_PASSWORD = ('changepass', 'changepassword')
    REMOVE = ('remove', 'delete', 'rm', 'del')
    MYDISCOUNT = ('mydiscount', 'mycoupon', 'discounts', 'coupons')
    CLEAR = 'clear'
    BUY = 'buy'
    EXIT = ('ex', 'exit', 'q', 'quit')
    LOGOUT = 'logout'
    # ADMIN USER COMMANDS
    ESCALATE = ('escalate', 'editstock', 'stock')
    RULE = ('changerule', 'rule', 'setrule')
    USERS_MANAGE = ('edituser', 'manageusers', 'manageuser')
    SHUTDOWN = ('shutdown', 'kill')
    FINISH_PURCHASE = ('finish', 'y')
