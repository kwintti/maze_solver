import random

hello = [(0,1), (1,0), (12, 7)]
hello.append((2, 4))
hello.append((3,5))
new_i, new_j = hello[random.randrange(0, len(hello))]
print(hello)

print(new_i, new_j)
