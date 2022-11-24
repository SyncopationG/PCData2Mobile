import random

random_int = random.randint
random_float = random.random


class RandomData:
    @staticmethod
    def int_type(num, low, high):
        a = []
        for i in range(num):
            a.append(random_int(low, high))
        return a

    @staticmethod
    def float_type(num, low, high):
        a = []
        span = high - low
        for i in range(num):
            a.append(low + span * random_float())
        return a
