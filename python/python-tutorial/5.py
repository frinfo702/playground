fruits = ["orange", "apple", "pear", "banana", "kiwi", "apple", "banana"]

print(fruits.count("apple"))  # 2
print(fruits.index("banana"))  # 3
print(fruits.index("banana", 4))  # 6

fruits.reverse()
print(fruits)

fruits.sort()
print(fruits)  # ['apple', 'apple', 'banana', 'banana', 'kiwi', 'orange', 'pear']

print(fruits.pop())  # pear

###############
# listはデフォルトでstack

stack = [3, 4, 5]
stack.append(6)
stack.append(7)

print(stack)  # [3, 4, 5, 6, 7]
print(stack.pop())  # 7
print(stack)  # [3, 4, 5, 6]
print(stack.pop())  # 6
print(stack)  # [3, 4, 5]

###############
# listをqueueとして使う
# 先頭要素をpopしたりすると全要素のシフトが発生して効率が悪い
# collections.dequeを使う方がいい

from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")
print(queue)  # deque(['Eric', 'John', 'Michael', 'Terry'])
print(queue.popleft())  # Eric
print(queue.popleft())  # John
print(queue)


############
# 内包表記でリストを作成する

squares = []
# xはループ終了後も残り続ける
for x in range(10):
    squares.append(x**2)
print(squares)

# イテラブルの各要素に関数を適用
squares = list(map(lambda x: x**2, range(10)))
print(squares)

squares = [x**2 for x in range(10)]
print(squares)

# 内包表記は式、for、ifで構成される
print([(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y])

vec = [-4, -2, 0, 2, 4]
print([x**2 for x in vec])  # [16, 4, 0, 4, 16]
print([x for x in vec if x >= 0])  # [0, 2, 4]
print([abs(x) for x in vec])  # [4, 2, 0, 2, 4]
freshfruit = [
    "  banana",
    " loganberry  ",
    "passion fruit   ",
]  # ['banana', 'loganberry', 'passion fruit']
print([weapon.strip() for weapon in freshfruit])

print([(x, x**2) for x in range(5)])  # [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]

vec = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattend = [num for row in vec for num in row]  # 2重ループを思い起こせばわかる
print(flattend)

from math import pi

print([str(round(pi, ndigit)) for ndigit in range(1, 5)])
# >> ['3.1', '3.14', '3.142', '3.1416']

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

print([[row[i] for row in matrix] for i in range(4)])  # 外側から評価
# 次のコードと等価
transposed = []
for i in range(4):
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])

    transposed.append(transposed_row)
print(transposed)

print(list(zip(*matrix)))  # 実際はこの方が早い

########################
# delはpop()のように値を返したりしない
# del obj[key] は内部で__delitem__を呼ぶ

a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
print(a)

del a[2:4]
print(a)

del a[:]
print(a)

# 変数自体を削除
del a  # dunderは呼ばずに名前のバインド解除

#############################

t = (12345, 54321, "hello")
print(t[0])

u = (t, (1, 2, 3, 4, 5))
print(u)

try:
    t[0] = 8888
except TypeError:
    print("tuple object isn't imutable")

empty = ()
singleton = ("hello",)
print(len(empty))
print(len(singleton))

# 上記で定義したtはタプルのpackの例。そしてunpackが存在する
x, y, z = t  # sequece unpacking (シーケンス型で利用できる)

###################################
# Set オブジェクトは集合として解釈できる
# 集合としての演算ができる

basket = {"apple", "orange", "apple", "orange", "pear", "banana"}

print(basket)  # {'orange', 'pear', 'banana', 'apple'}

print("orange" in basket)
print("cragbrass" in basket)

a = set("abracadabra")
b = set("alacazam")
print(a - b)
print(a | b)  # a∨b
print(a & b)  # a∧b
print(a ^ b)  # XOR

a = {x for x in "abracadabra" if x not in "abc"}
print(a)

############################
# 辞書型でkeyに指定できるのはオブジェクトとして変更不可能なものだけ
# int, str, setはできるが、listはできない（listは操作でオブジェクトの型ごと変わる可能性があるため）

tel = {"jack": 4098, "sape": 4139}
tel["guido"] = 4127
print(tel)
print(tel["jack"])
try:
    print(tel["irv"])
except KeyError:
    print("invalid key indicated")

# get()を使えば安全にアクセスできる
print(tel.get("irv"))  # None

del tel["sape"]
tel["irv"] = 4127
print(tel)
print(list(tel))
print(sorted(tel))

# dict()コンストラクタはキーと値のペアのタプルを含むリストから辞書を生成する
print(dict([("sape", 4139), ("guido", 4127), ("jack", 4098)]))

print({x: x**2 for x in range(4)})

print(dict(sape=4139, guido=4127, jack=4098))

########################

# 辞書のitemではunpackしつつループを回せる
knights = {"gallahad": "the pure", "robin": "the brave"}
for k, v in knights.items():
    print(k, v)

# シーケンス型にenumerate()を使うと要素とインデックスを同時に取り出せる
for i, v in enumerate(["tic", "tac", "toe"]):
    print(i, v)

# zip()で複数のシーケンスを同時にループすることもできる
questions = ["name", "quest", "favorite color"]
answers = ["lancelot", "the holy grail", "blue"]
for q, a in zip(questions, answers):
    print(f"What is your {q}? It is {a}")

for i in reversed(range(1, 10, 2)):
    print(i)

import math

raw_data = [56.2, float("NaN"), 51.7, 55.3, 52.5, float("NaN"), 47.8]
filtered_data = []
for value in raw_data:
    if not math.isnan(value):
        filtered_data.append(value)

print(filtered_data)
