def f():
    raise OSError("operation failed")


excs = []
for i in range(3):
    try:
        f()
    except Exception as e:
        e.add_note(
            f"Happend in Iteration {i + 1}"
        )  # add_noteで例外送出時にコンテキスト情報を付加することができる
        excs.append(e)
raise ExceptionGroup("We have some problem", excs)


# + Exception Group Traceback (most recent call last):
# |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 12, in <module>
# |     raise ExceptionGroup("We have some problem", excs)
# | ExceptionGroup: We have some problem (3 sub-exceptions)
# +-+---------------- 1 ----------------
#   | Traceback (most recent call last):
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 8, in <module>
#   |     f()
#   |     ~^^
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 2, in f
#   |     raise OSError("operation failed")
#   | OSError: operation failed
#   | Happend in Iteration 1
#   +---------------- 2 ----------------
#   | Traceback (most recent call last):
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 8, in <module>
#   |     f()
#   |     ~^^
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 2, in f
#   |     raise OSError("operation failed")
#   | OSError: operation failed
#   | Happend in Iteration 2
#   +---------------- 3 ----------------
#   | Traceback (most recent call last):
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 8, in <module>
#   |     f()
#   |     ~^^
#   |   File "/Users/ken702/ghq/github.com/frinfo702/playground/python-tutorial/8.10.py", line 2, in f
#   |     raise OSError("operation failed")
#   | OSError: operation failed
#   | Happend in Iteration 3
#   +------------------------------------
