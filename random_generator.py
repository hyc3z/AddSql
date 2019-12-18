
import random
from limits import *


def randomChar(charType="all"):
    if charType.lower() == "all":
        return randomCharAll()
    elif charType.lower() == "numeric":
        return randomNumeric()
    elif charType.lower() == "lowercase":
        return randomLower()
    elif charType.lower() == "uppercase":
        return randomUpper()
    elif charType.lower() == "alphanumeric":
        return randomAlphanumeric()
    else:
        return randomCharAll()


def randomCharAll():
    return chr(random.randint(33, 126))


def randomNumeric():
    return chr(random.randint(48, 57))


def randomUpper():
    return chr(random.randint(65, 90))


def randomLower():
    return chr(random.randint(97, 122))


def randomAlphanumeric():
    choice = random.randint(1, 3)
    if choice == 1:
        return randomUpper()
    elif choice == 2:
        return randomLower()
    else:
        return randomNumeric()


def randomTinyint(length, unsigned=False):
    return random.randint(0, min(U_TINY_INT_MAX, 10 ** length)) if unsigned else random.randint(max(TINY_INT_MIN, -10 ** length), min(TINY_INT_MAX, 10 ** length))


def randomSmallint(length, unsigned=False):
    return random.randint(0, min(U_SMALL_INT_MAX, 10 ** length)) if unsigned else random.randint(max(SMALL_INT_MIN, -10 ** length), min(SMALL_INT_MAX, 10 ** length))


def randomMediumint(length, unsigned=False):
    return random.randint(0, min(U_MEDIUM_INT_MAX, 10 ** length)) if unsigned else random.randint(max(MEDIUM_INT_MIN, -10 ** length), min(MEDIUM_INT_MAX, 10 ** length))


def randomInt(length, unsigned=False):
    return random.randint(0, min(U_INT_MAX, 10 ** length)) if unsigned else random.randint(max(INT_MIN, -10 ** length), min(INT_MAX, 10 ** length))


def randomBigint(length, unsigned=False):
    return random.randint(0, min(U_BIG_INT_MAX, 10 ** length)) if unsigned else random.randint(max(BIG_INT_MIN, -10 ** length), min(BIG_INT_MAX, 10 ** length))


def randomBit(length):
    string = ""
    for _ in range(length):
        string += str(random.randint(0, 1))
    return string


def randomFloat(unsigned=False):
    return random.random() if unsigned else (random.random() if random.randint(0,1) else -random.random())


def randomVarchar(length, charType):
    string = ""
    for _ in range(length):
        string += randomChar(charType)
    return string


if __name__ == '__main__':
    for _ in range(10):
        print(randomFloat())
