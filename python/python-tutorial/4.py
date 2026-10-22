def ask_ok(prompt, retries=4, reminder="please retry"):
    while True:
        reply = input(prompt)
        if reply in {"y", "ye", "yes"}:  # set
            return True
        if reply in {"n", "no", "nop", "nope"}:
            return False

        retries = retries - 1
        if retries < 0:
            raise ValueError("Invalid User Input")

        print(reminder)


# 引数のデフォルト値は初回参照時しか評価されない
def f(a, myList=[]):
    myList.append(a)
    return myList


print(f(1))  # [1]
print(f(2))  # [1, 2]
print(f(3))  # [1, 3]


# デフォルト値を共有したくない場合
def f2(a, myList=None):
    if myList is None:
        myList = []
    myList.append(a)
    return myList


# *nameはタプルを受け取る
# **nameは辞書を受け取る
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we,re all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])


cheeseshop("Limburger", "arg1", "arg2", client="John", sketch="Cheese")


def standard_arg(arg):
    print(arg)


# / の前の引数は位置専用引数
def pos_only_arg(arg, /):
    print(arg)


# * のあとはキーワード専用引数
def kwd_only_arg(*, arg):
    print(arg)


def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)


standard_arg(2)
standard_arg(arg=2)

pos_only_arg(1)
# pos_only_arg(arg=1) # invalid

# kwd_only_arg(3) invalid
kwd_only_arg(arg=1)

# これらはおk
combined_example(1, 2, kwd_only=3)
combined_example(1, standard=2, kwd_only=3)

print(list(range(3, 6)))  # 通常の関数呼び出し

args = [3, 6]
print(list(range(*args)))  # 引数リストをアンパックして呼び出し


def parrot(voltage, state="a stiff", action="voom"):
    print("-- This parrot wouldn't", action, end=" ")
    print("if you put", voltage, "volts through it.", end=" ")
    print("E's", state, "!")


d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
print(parrot(**d))


# lambdaで無名関数
# 関数オブジェクトが要求される場所なら使用できる
def make_incrementor(n):
    return lambda x: x + n


f = make_incrementor(42)
print(f(1))
