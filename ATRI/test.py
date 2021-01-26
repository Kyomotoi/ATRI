a = [
    {'a': 1},
    {'a': 2}
]

from random import randint

print(a)
print(a[randint(0, len(a)) - 1])
print(len(a))