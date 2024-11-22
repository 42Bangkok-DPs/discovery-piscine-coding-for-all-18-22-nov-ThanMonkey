#!/usr/bin/env python3

num = input("Give me a number: ")
try:
    num_float = float(num)
    if num_float.is_integer():
        print("This number is an integer.")
    else:
        print("This number is a decimal.")
except ValueError:
    print("That's not a valid number.")
