# 複数の例外の送出
# ExceptionGroupを使う


from logging import exception


def f():
    excs = [OSError("error 1"), SystemError("error 2")]
    raise ExceptionGroup("there were problems", excs)


f()

# + Exception Group Traceback (most recent call last):
# |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.9.py", line 10, in <module>
# |     f()
# |     ~^^
# |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.9.py", line 7, in f
# |     raise ExceptionGroup("there were problems", excs)
# | ExceptionGroup: there were problems (2 sub-exceptions)
# +-+---------------- 1 ----------------
#   | OSError: error 1
#   +---------------- 2 ----------------
#   | SystemError: error 2
#   +------------------------------------


try:
    f()
except Exception as e:
    print(f"caught {type(e)}: {e}")

# caught <class 'ExceptionGroup'>: there were problems (2 sub-exceptions)


def f():
    raise ExceptionGroup(
        "group1",
        [
            OSError(1),
            SystemError(2),
            ExceptionGroup("group2", [OSError(3), RecursionError(4)]),
        ],
    )


try:
    f()
except* OSError:  # except* とすることでグループ内の特定の例外のみを選択して処理できる
    print("There were OSErrors")
except* SystemError:
    print("There were SystemErrors")

# There were OSErrors
# There were SystemErrors
#   + Exception Group Traceback (most recent call last):
#   |   File "<stdin>", line 2, in <module>
#   |     f()
#   |     ~^^
#   |   File "<stdin>", line 2, in f
#   |     raise ExceptionGroup(
#   |     ...<12 lines>...
#   |     )
#   | ExceptionGroup: group1 (1 sub-exception)
#   +-+---------------- 1 ----------------
#     | ExceptionGroup: group2 (1 sub-exception)
#     +-+---------------- 1 ----------------
#       | RecursionError: 4
#       +------------------------------------
