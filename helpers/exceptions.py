from .messages import PasswordErrors, UsernameErrors, ProductErrors


class WrongUsernameError(ValueError):
    pass


class TypeUsernameError(WrongUsernameError):
    def __str__(self) -> str:
        return UsernameErrors.USERNAME_TYPE_ERROR


class UserNotExist(WrongUsernameError):
    def __str__(self) -> str:
        return UsernameErrors.USERNAME_NOT_EXIST


class WrongPasswordError(ValueError):
    pass


class TypePasswordError(WrongPasswordError):
    def __str__(self) -> str:
        return PasswordErrors.PASSWORD_TYPE_ERROR


class PasswordLengthError(WrongPasswordError):
    def __str__(self) -> str:
        return PasswordErrors.PASSWORD_LENGTH_ERROR


class RemoveProductError(RuntimeError):
    def __str__(self) -> str:
        return ProductErrors.REMOVE_ERROR
