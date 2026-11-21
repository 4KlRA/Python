import sys

class Jar:
    def __init__(self, capacity=12):
        self.capacity = capacity
        self._amt = 0


    def __str__(self):
        return "🍪" * self._amt

    def deposit(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Invalid deposit amount")
        if(self._amt + n > self.capacity):
            raise ValueError("Overflow")
        self._amt += n

    def withdraw(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Invalid deposit amount")
        if(n > self._amt):
            raise ValueError("Underflow")
        self._amt -= n

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("Invalid capacity")
        self._capacity = capacity

    @property
    def size(self):
        return self._amt