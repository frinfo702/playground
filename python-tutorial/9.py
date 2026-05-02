def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment", spam)
    do_nonlocal()
    print("After nonlocal assignment", spam)
    do_global()
    print("After global assignment", spam)


scope_test()
print("In global scope", spam)


class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


x = Complex(3.0, -4.5)
print(x.r, x.i)


class MyClass:
    """A simple example class"""

    i = 12345

    def f(self):
        return "hello, world"


x = MyClass()
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter

xf = x.f
# x.f()という呼び出しは MyClass.f(x)と厳密に等価
# selfはインスタンス自体が入る（今回はx）
for _ in range(3):
    print(xf())


class Dog:
    tricks = []

    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)


d = Dog("Fido")
e = Dog("Buddy")
d.add_trick("roll over")
e.add_trick("play dead")
print(d.tricks)  # tricksが]共有されてしまっている


class Dog:
    def __init__(self, name):
        self.name = name
        self.tricks = []  # クラスインスタンスごとに新しいリストを作る

    def add_trick(self, trick):
        self.tricks.append(trick)


d = Dog("Fido")
e = Dog("Buddy")
d.add_trick("roll over")
e.add_trick("play dead")
print(d.tricks)
print(e.tricks)


class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)  # 同じクラス内の別のメソッドを使うこともできる
        self.add(x)


from dataclasses import dataclass


# 構造体を使いたい時はdataclassesを使う
@dataclass
class Employee:
    name: str
    dept: str
    salary: int


######################
# for文にコンテナオブジェクトが渡される時iter()が呼ばれている
# iter() はコンテナの中の要素に一つずつアクセスする__next__()が
# 定義されているイテレータオブジェクトを返す
# ループの最後では__next__()メソッドがStopIteration例外を送出して終了する

s = "abc"
it = iter(s)
print(it)

print(next(it))  # イテレータオブジェクトには__next__()が定義されている
print(next(it))
print(next(it))
# print(next(it))  # StopIteration例外が発生


class Reverse:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


rev = Reverse("spam")
iter(rev)
for char in rev:
    print(char)

#######################
# generator


# ジェネレータはイテレータを作成できる
# 自動的に__iter()__, __next()__が実装される
def reverse(data):
    for index in range(len(data) - 1, -1, -1):
        yield data[index]


for char in reverse("golf"):
    print(char)

# ジェネレータ式
# 内包表記と似ているが[]ではなく()を使う
square_sum = sum(i * i for i in range(10))
print(square_sum)

xvec = [10, 20, 30]
yvec = [7, 5, 3]
dot_mul = sum(x * y for x, y in zip(xvec, yvec))
print(dot_mul)
