i = 3
x = "even" if i % 2 == 0 else "odd"  # if文を式として使う
print(x)


def fail():
    raise Exception("Oops")


x = fail() if False else 20
print(x)  # 20

result = [x / 4 for x in range(10) if x % 2 == 0]
print(result)

