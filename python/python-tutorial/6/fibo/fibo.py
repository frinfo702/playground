# このファイルのあるディレクトリで import fiboを行うことでmoduleを読み込める
# import <filename>
# from <filename> import <classname/funcname>
def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=" ")
        (
            a,
            b,
        ) = b, a + b
    print()


def fib2(n):
    """nまでのフィボナッチ数を返す"""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


# e.g. python3 fibo.py <arguments>
# importされた場合は実行されない
if __name__ == "__main__":
    # このモジュールがmainファイルとして起動されたときだけ実行される
    import sys

    fib(int(sys.argv[1]))

# __name__はpythonが自動設定するモジュールの名前でこのファイルがどうやって読み込まれたかを持つ
# module全体に対して割り当てられる特殊な変数
