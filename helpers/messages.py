from enum import StrEnum


class PasswordErrors(StrEnum):

    PASSWORD_LENGTH_ERROR = 'Your password is too short.'

    PASSWORD_TYPE_ERROR = '\
Password must have at least one integer,\
Password must have at least one character,\
Password must have at least one sign'


class UsernameErrors(StrEnum):

    USERNAME_NOT_EXIST = 'Username dosn\'t exist.'

    USERNAME_TYPE_ERROR = 'Username must start with characters not numbers'


class ProductErrors(StrEnum):
    REMOVE_ERROR = 'Error in Removing Products (Something weird happened!)'


class Message(StrEnum):

    HELP_MESSAGE = "For more information's about the app, Enter 'help' command." # noqa E501

    AUTHENICATION_FAILED = 'Authenication Failed. Try Again.'

    ACCOUNT_CREATED = "Your account has been created successfuly.\n\
NOTE** Please do not forget your account information."

    LOG_OUT_CONFIRM = "Are you sure you want to logout? (Y / Any) : "

    EXIT_CONFIRM = "If you quit, Everything will be leave unsaved.\n\
Are you sure you want to quit? (Y / Any) : "

    TRY_CHANGE_PASS = "You are trying to change your password for User: "

    BEFORE_LOGIN = """
Please Login by 'login'.
if you haven't an account yet, Create an account by Entering 'Create' command.
You'll get '30,000 Tomans welcome bonus' if you create an account today!

( Create / Login ): """

    ASK_TO_USE_DISCOUNT = 'Do you want to use discount code? (Y / Any)'

    FINISH_PURCHASE = "If you agree to finish the purchase, enter ('finish' or 'y'): " # noqa E501
    PURCHASE_PROCESS = 'Purchase in process. Please wait...'
    NOT_ENOUGH_BALANCE = "Not enough balance.\nTry ('addmoney', 'charge') commands for recharge." # noqa E501
    PURCHASE_SUCCESS = "Purchase has been done successfuly. Thank you!"
    PURCHASE_CANCEL = 'Purchase has been canceled.'
