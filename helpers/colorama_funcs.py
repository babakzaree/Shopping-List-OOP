from colorama import Fore


def blue(string: str) -> str:
    '''Return colored in blue text by using colorama module.'''
    return (Fore.BLUE + string)


def green(string: str) -> str:
    '''Return colored in green text by using colorama module.'''
    return (Fore.GREEN + string)

def red(string: str) -> str:
    '''Return colored in red text by using colorama module.'''
    return (Fore.RED + string)

def yellow(string: str) -> str:
    '''Return colored in yellow text by using colorama module.'''
    return (Fore.LIGHTYELLOW_EX + string)

def white(string: str) -> str:
    '''Return colored in white text by using colorama module.'''
    return (Fore.WHITE + string)