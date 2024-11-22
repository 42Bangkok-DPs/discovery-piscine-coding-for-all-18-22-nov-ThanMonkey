#!/usr/bin/env python3
import math

num = input("Give me a number: ")
try:
    num_float = float(num)
    print(math.ceil(num_float))    
except ValueError:
    print("That's not a valid number.")
