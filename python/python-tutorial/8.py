class B(Exception):
    pass


class C(B):
    pass


class D(C):
    pass


for cls in [B, C, D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")

try:
    raise Exception("spam", "eggs")  # 例外には引数を持たせることができる
except Exception as inst:
    print(type(inst))
    print(inst.args)  # 引数は.argsに格納される
    print(inst)  # 組み込み例外には__str__()が実装されている

    x, y = inst.args
    print("x = ", x)
    print("y = ", y)

import sys

try:
    f = open("workfile.txt")
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS Error", err)
except ValueError:
    print("Failed to convert to type: int")
except Exception as err:
    # Exceptionサブクラスに対しては例外を表示してから再度送出
    print(f"Unexpected error {err=}, {type(err)=}")
    raise

for arg in sys.argv[1:]:
    try:
        f = open(arg, "r")
    except OSError:
        print(arg, "が開けません")
    else:  # 例外が起きなかった場合のみ実行される
        print(arg, "は", len(f.readlines()), "行です")
        f.close()


def this_fails():
    x = 1 / 0


try:
    this_fails()  # try中で発生した外部の例外も拾う
except ZeroDivisionError as err:
    print("実行時エラーを処理", err)

try:
    raise NameError("Hi there")
except NameError:
    print("例外が通り過ぎました")
    # raise  # 例外を送出するにはraiseを使う

#####################
# 例外の連鎖

try:
    open("database.sqlite")
except OSError as exc:
    # except説中で未処理の例外が発生すると処理された例外中に未処理例外のエラーメッセージも含まれる
    # 送出しているのはRuntimeErrorだがFileNotFoundErrorが含まれて表示される
    raise RuntimeError(
        "unable to handle error"
    ) from exc  # fromで連鎖関係を明示的に示せる
finally:  # 例外が発生しても実行される。finallyが実行された後未処理例外が表示される
    # file, connectionなどをcloseするのに便利
    print("Goodbye, world")
