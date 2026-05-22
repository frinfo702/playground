# Python 基礎力養成問題集

この問題集は、Pythonの基礎文法とプログラミングの基礎力を身につけるための100問から構成されています。特定のフレームワークに依存せず、標準的なPythonの知識とスキルを鍛えることを目的としています。

## 推奨ディレクトリ構成

```
python-practices-problems/
├── python-practice-problems.md  # この問題集
└── answers/                     # あなたの解答を置くディレクトリ
    ├── q01_hello_world/
    │   ├── solution.py          # 解答コード
    │   └── test_solution.py     # 自分で書くテスト
    ├── q02_add_numbers/
    │   ├── solution.py
    │   └── test_solution.py
    ...
```

## テストケースの書き方（基本形）

各問題では `solution.py` に解答を書き、`test_solution.py` に自分でテストを書く練習をします。以下は基本テンプレートです。

```python
# test_solution.py
from solution import solve  # 問題に応じて関数名を変更

def test_case_1():
    assert solve("入力1") == "期待する出力1"

def test_case_2():
    assert solve("入力2") == "期待する出力2"

# 実行方法: python -m pytest test_solution.py
# pytest がなくても、以下のように直接実行可能です
if __name__ == "__main__":
    test_case_1()
    test_case_2()
    print("All tests passed!")
```

pytest がインストールされていなくても、`if __name__ == "__main__":` ブロックで直接実行できるようにしておくと便利です。

---

## 第1章：入出力と基本構文（Q01〜Q10）

---

### Q01. Hello World

**問題文**
`hello()` という関数を定義し、実行すると文字列 `"Hello, World!"` を返すようにしてください。

**テストケースの書き方**

```python
# test_solution.py
from solution import hello

def test_hello():
    assert hello() == "Hello, World!"
```

**解答例**

```python
# solution.py
def hello():
    return "Hello, World!"
```

---

### Q02. 二つの数の足し算

**問題文**
`add(a, b)` という関数を定義してください。2つの整数 `a`, `b` を受け取り、それらの和を返します。

**テストケースの書き方**

```python
# test_solution.py
from solution import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_mixed():
    assert add(5, -3) == 2
```

**解答例**

```python
# solution.py
def add(a, b):
    return a + b
```

---

### Q03. 名前付き挨拶

**問題文**
`greet(name)` という関数を定義してください。文字列 `name` を受け取り、`"Hello, <name>!"` という形式の文字列を返します。

**テストケースの書き方**

```python
# test_solution.py
from solution import greet

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
```

**解答例**

```python
# solution.py
def greet(name):
    return f"Hello, {name}!"
```

---

### Q04. 標準入力から1行読み込む

**問題文**
`read_and_echo()` という関数を定義してください。標準入力から1行読み込み、読み込んだ文字列（末尾の改行を除く）を返します。

**テストケースの書き方**

標準入力のテストは `io.StringIO` を使ってモック化するとよいでしょう。

```python
# test_solution.py
import io
import sys
from solution import read_and_echo

def test_read_and_echo(monkeypatch):
    # pytest の monkeypatch を使う例
    monkeypatch.setattr(sys, "stdin", io.StringIO("test input\n"))
    assert read_and_echo() == "test input"
```

**解答例**

```python
# solution.py
import sys

def read_and_echo():
    return sys.stdin.readline().strip()
```

---

### Q05. 複数行の入力

**問題文**
`read_lines(n)` という関数を定義してください。標準入力から最初の1行を整数 `n` として読み込み、続く `n` 行を読み込んで、各行を要素とするリストを返します。各行の末尾の改行は取り除いてください。

**テストケースの書き方**

```python
# test_solution.py
import io
import sys
from solution import read_lines

def test_read_lines(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("3\napple\nbanana\ncherry\n"))
    assert read_lines(3) == ["apple", "banana", "cherry"]
```

**解答例**

```python
# solution.py
import sys

def read_lines(n):
    lines = []
    for _ in range(n):
        line = sys.stdin.readline().strip()
        lines.append(line)
    return lines
```

---

### Q06. スペース区切りの入力

**問題文**
`read_ints()` という関数を定義してください。標準入力から1行読み込み、スペース区切りの整数をリストとして返してください。

**テストケースの書き方**

```python
# test_solution.py
import io
import sys
from solution import read_ints

def test_read_ints(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("1 2 3 4 5\n"))
    assert read_ints() == [1, 2, 3, 4, 5]
```

**解答例**

```python
# solution.py
import sys

def read_ints():
    line = sys.stdin.readline().strip()
    return list(map(int, line.split()))
```

---

### Q07. 円周率を表示

**問題文**
`pi_string()` という関数を定義してください。円周率の値 `3.14159` を小数点以下2桁までの文字列（`"3.14"`）として返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import pi_string

def test_pi_string():
    assert pi_string() == "3.14"
```

**解答例**

```python
# solution.py
def pi_string():
    return f"{3.14159:.2f}"
```

---

### Q08. 現在時刻の表示

**問題文**
`current_year()` という関数を定義してください。`datetime` モジュールを使って、現在の西暦年（整数）を返してください。

**テストケースの書き方**

現在時刻に依存するテストは、モック化して固定値を返すようにするとよいでしょう。

```python
# test_solution.py
from unittest.mock import patch
from datetime import datetime
from solution import current_year

def test_current_year():
    fixed_now = datetime(2024, 6, 15, 12, 0, 0)
    with patch("solution.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_now
        assert current_year() == 2024
```

**解答例**

```python
# solution.py
from datetime import datetime

def current_year():
    return datetime.now().year
```

---

### Q09. コマンドライン引数の合計

**問題文**
`sum_args(args)` という関数を定義してください。文字列のリスト `args` を受け取り、各要素を整数に変換して合計を返してください。`args` はコマンドライン引数（プログラム名を除く）を想定しています。

**テストケースの書き方**

```python
# test_solution.py
from solution import sum_args

def test_sum_args():
    assert sum_args(["10", "20", "30"]) == 60
    assert sum_args(["5"]) == 5
    assert sum_args([]) == 0
```

**解答例**

```python
# solution.py
def sum_args(args):
    total = 0
    for arg in args:
        total += int(arg)
    return total
```

---

### Q10. 改行を含む出力

**問題文**
`print_rectangle(width, height)` という関数を定義してください。`*` を並べた `width` × `height` の長方形を標準出力に出力してください。戻り値は不要です。

例：`print_rectangle(3, 2)` の場合、以下のように出力します。

```
***
***
```

**テストケースの書き方**

```python
# test_solution.py
import io
import sys
from solution import print_rectangle

def test_print_rectangle(capsys):
    print_rectangle(3, 2)
    captured = capsys.readouterr()
    assert captured.out == "***\n***\n"
```

**解答例**

```python
# solution.py
def print_rectangle(width, height):
    for _ in range(height):
        print("*" * width)
```

---

## 第2章：変数とデータ型（Q11〜Q20）

---

### Q11. 型の確認

**問題文**
`get_type(value)` という関数を定義してください。受け取った値の型名（`int`, `str`, `float`, `list`, `dict`, `bool` など）を文字列として返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import get_type

def test_get_type():
    assert get_type(10) == "int"
    assert get_type("hello") == "str"
    assert get_type(3.14) == "float"
    assert get_type([1, 2]) == "list"
    assert get_type({"a": 1}) == "dict"
    assert get_type(True) == "bool"
```

**解答例**

```python
# solution.py
def get_type(value):
    return type(value).__name__
```

---

### Q12. 型変換（整数→文字列）

**問題文**
`int_to_str(n)` という関数を定義してください。整数 `n` を受け取り、文字列に変換して返してください。組み込み関数 `str()` は使わずに実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import int_to_str

def test_int_to_str():
    assert int_to_str(123) == "123"
    assert int_to_str(-456) == "-456"
    assert int_to_str(0) == "0"
```

**解答例**

```python
# solution.py
def int_to_str(n):
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    result = ""
    while n > 0:
        result = chr(ord("0") + n % 10) + result
        n //= 10
    return "-" + result if negative else result
```

---

### Q13. 型変換（文字列→整数）

**問題文**
`str_to_int(s)` という関数を定義してください。数字だけからなる文字列 `s` を受け取り、整数に変換して返してください。負の数も考慮してください。組み込み関数 `int()` は使わずに実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import str_to_int

def test_str_to_int():
    assert str_to_int("123") == 123
    assert str_to_int("-456") == -456
    assert str_to_int("0") == 0
```

**解答例**

```python
# solution.py
def str_to_int(s):
    negative = s.startswith("-")
    start = 1 if negative else 0
    result = 0
    for i in range(start, len(s)):
        result = result * 10 + (ord(s[i]) - ord("0"))
    return -result if negative else result
```

---

### Q14. 入れ子リストの合計

**問題文**
`sum_nested(data)` という関数を定義してください。入れ子になったリスト `data` に含まれるすべての整数の合計を返してください。リストは任意の深さで入れ子になっている可能性があります。

**テストケースの書き方**

```python
# test_solution.py
from solution import sum_nested

def test_sum_nested():
    assert sum_nested([1, 2, [3, 4], 5]) == 15
    assert sum_nested([1, [2, [3, [4]]]]) == 10
    assert sum_nested([]) == 0
    assert sum_nested([[], [[]]]) == 0
```

**解答例**

```python
# solution.py
def sum_nested(data):
    total = 0
    for item in data:
        if isinstance(item, list):
            total += sum_nested(item)
        elif isinstance(item, int):
            total += item
    return total
```

---

### Q15. タプルの入れ替え

**問題文**
`swap_tuple(t)` という関数を定義してください。2要素のタプル `t` を受け取り、要素を入れ替えたタプルを返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import swap_tuple

def test_swap_tuple():
    assert swap_tuple((1, 2)) == (2, 1)
    assert swap_tuple(("a", "b")) == ("b", "a")
```

**解答例**

```python
# solution.py
def swap_tuple(t):
    return (t[1], t[0])
```

---

### Q16. 三つの値の中央値

**問題文**
`median_of_three(a, b, c)` という関数を定義してください。3つの整数を受け取り、中央値（大きさの順で真ん中の値）を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import median_of_three

def test_median_of_three():
    assert median_of_three(1, 2, 3) == 2
    assert median_of_three(5, 1, 3) == 3
    assert median_of_three(10, 10, 5) == 10
```

**解答例**

```python
# solution.py
def median_of_three(a, b, c):
    return sorted([a, b, c])[1]
```

---

### Q17. 真偽値の反転

**問題文**
`negate(value)` という関数を定義してください。真偽値 `value` を受け取り、その反転値を返してください。ただし、`not` 演算子は使わずに実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import negate

def test_negate():
    assert negate(True) is False
    assert negate(False) is True
```

**解答例**

```python
# solution.py
def negate(value):
    return not value
```

---

### Q18. ビット演算

**問題文**
`is_even_bitwise(n)` という関数を定義してください。整数 `n` が偶数かどうかをビット演算のみで判定して、偶数なら `True`、奇数なら `False` を返してください。`%` や `//` による剰余計算は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import is_even_bitwise

def test_is_even_bitwise():
    assert is_even_bitwise(4) is True
    assert is_even_bitwise(7) is False
    assert is_even_bitwise(0) is True
    assert is_even_bitwise(-3) is False
```

**解答例**

```python
# solution.py
def is_even_bitwise(n):
    return (n & 1) == 0
```

---

### Q19. 浮動小数点数の比較

**問題文**
`float_equal(a, b, eps=1e-9)` という関数を定義してください。2つの浮動小数点数 `a`, `b` が、絶対誤差 `eps` 以内で等しいかどうかを判定してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import float_equal

def test_float_equal():
    assert float_equal(0.1 + 0.2, 0.3) is True
    assert float_equal(1.0, 1.0000000001) is True
    assert float_equal(1.0, 1.1) is False
```

**解答例**

```python
# solution.py
def float_equal(a, b, eps=1e-9):
    return abs(a - b) < eps
```

---

### Q20. 複素数の絶対値

**問題文**
`complex_abs(real, imag)` という関数を定義してください。実部 `real`、虚部 `imag` の複素数の絶対値を返してください。組み込み関数 `abs()` や `cmath` は使わず、`math.hypot()` も使わずに実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import complex_abs

def test_complex_abs():
    assert complex_abs(3, 4) == 5.0
    assert complex_abs(5, 12) == 13.0
    assert complex_abs(0, 0) == 0.0
```

**解答例**

```python
# solution.py
import math

def complex_abs(real, imag):
    return math.sqrt(real ** 2 + imag ** 2)
```

---

## 第3章：条件分岐（Q21〜Q30）

---

### Q21. 絶対値

**問題文**
`my_abs(n)` という関数を定義してください。整数 `n` の絶対値を返してください。組み込み関数 `abs()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import my_abs

def test_my_abs():
    assert my_abs(5) == 5
    assert my_abs(-5) == 5
    assert my_abs(0) == 0
```

**解答例**

```python
# solution.py
def my_abs(n):
    return n if n >= 0 else -n
```

---

### Q22. 成績評価

**問題文**
`grade(score)` という関数を定義してください。0〜100の整数 `score` を受け取り、以下のルールで成績を返してください。

- 90〜100: `"A"`
- 80〜89: `"B"`
- 70〜79: `"C"`
- 60〜69: `"D"`
- 0〜59: `"F"`
- それ以外: `"Invalid"`

**テストケースの書き方**

```python
# test_solution.py
from solution import grade

def test_grade():
    assert grade(95) == "A"
    assert grade(85) == "B"
    assert grade(75) == "C"
    assert grade(65) == "D"
    assert grade(55) == "F"
    assert grade(101) == "Invalid"
    assert grade(-1) == "Invalid"
```

**解答例**

```python
# solution.py
def grade(score):
    if 90 <= score <= 100:
        return "A"
    elif 80 <= score <= 89:
        return "B"
    elif 70 <= score <= 79:
        return "C"
    elif 60 <= score <= 69:
        return "D"
    elif 0 <= score <= 59:
        return "F"
    else:
        return "Invalid"
```

---

### Q23. うるう年判定

**問題文**
`is_leap_year(year)` という関数を定義してください。西暦年 `year` がうるう年なら `True`、そうでなければ `False` を返してください。うるう年の定義は以下の通りです。

- 4で割り切れる年はうるう年
- ただし、100で割り切れる年はうるう年ではない
- ただし、400で割り切れる年はうるう年

**テストケースの書き方**

```python
# test_solution.py
from solution import is_leap_year

def test_is_leap_year():
    assert is_leap_year(2000) is True
    assert is_leap_year(1900) is False
    assert is_leap_year(2024) is True
    assert is_leap_year(2023) is False
```

**解答例**

```python
# solution.py
def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
```

---

### Q24. 最大値を求める

**問題文**
`max_of_two(a, b)` という関数を定義してください。2つの整数 `a`, `b` のうち大きい方を返してください。組み込み関数 `max()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import max_of_two

def test_max_of_two():
    assert max_of_two(3, 5) == 5
    assert max_of_two(10, 2) == 10
    assert max_of_two(7, 7) == 7
```

**解答例**

```python
# solution.py
def max_of_two(a, b):
    return a if a >= b else b
```

---

### Q25. 符号判定

**問題文**
`sign(n)` という関数を定義してください。整数 `n` が正なら `1`、負なら `-1`、ゼロなら `0` を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import sign

def test_sign():
    assert sign(10) == 1
    assert sign(-5) == -1
    assert sign(0) == 0
```

**解答例**

```python
# solution.py
def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0
```

---

### Q26. 三角形の成立条件

**問題文**
`is_triangle(a, b, c)` という関数を定義してください。3つの正の整数 `a`, `b`, `c` を3辺の長さとする三角形が成立するかどうかを判定してください。三角形が成立する条件は「任意の2辺の和が残りの1辺より大きいこと」です。

**テストケースの書き方**

```python
# test_solution.py
from solution import is_triangle

def test_is_triangle():
    assert is_triangle(3, 4, 5) is True
    assert is_triangle(1, 2, 3) is False
    assert is_triangle(5, 5, 5) is True
    assert is_triangle(2, 3, 6) is False
```

**解答例**

```python
# solution.py
def is_triangle(a, b, c):
    return a + b > c and b + c > a and c + a > b
```

---

### Q27. 文字列の長さ判定

**問題文**
`check_length(s, min_len, max_len)` という関数を定義してください。文字列 `s` の長さが `min_len` 以上 `max_len` 以下なら `"OK"`、短すぎれば `"Too short"`、長すぎれば `"Too long"` を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import check_length

def test_check_length():
    assert check_length("hello", 3, 10) == "OK"
    assert check_length("hi", 3, 10) == "Too short"
    assert check_length("hello world", 3, 10) == "Too long"
```

**解答例**

```python
# solution.py
def check_length(s, min_len, max_len):
    length = len(s)
    if length < min_len:
        return "Too short"
    elif length > max_len:
        return "Too long"
    else:
        return "OK"
```

---

### Q28. 文字列のパリンドローム判定

**問題文**
`is_palindrome(s)` という関数を定義してください。文字列 `s` が回文（前から読んでも後ろから読んでも同じ）なら `True`、そうでなければ `False` を返してください。大文字小文字は区別せず、空白や記号は無視してください（英字のみ考慮）。

**テストケースの書き方**

```python
# test_solution.py
from solution import is_palindrome

def test_is_palindrome():
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
```

**解答例**

```python
# solution.py
def is_palindrome(s):
    filtered = "".join(ch.lower() for ch in s if ch.isalpha())
    return filtered == filtered[::-1]
```

---

### Q29. FizzBuzz

**問題文**
`fizzbuzz(n)` という関数を定義してください。1から `n` までの整数に対して、3で割り切れるなら `"Fizz"`、5で割り切れるなら `"Buzz"`、両方で割り切れるなら `"FizzBuzz"`、いずれでもないならその数字の文字列を、要素とするリストを返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import fizzbuzz

def test_fizzbuzz():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[14] == "FizzBuzz"
    assert fizzbuzz(1) == ["1"]
```

**解答例**

```python
# solution.py
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
```

---

### Q30. 範囲内かつ倍数判定

**問題文**
`count_multiples_in_range(start, end, divisor)` という関数を定義してください。`start` 以上 `end` 以下の整数の中で、`divisor` の倍数であるものの個数を返してください。`divisor` は正の整数とします。

**テストケースの書き方**

```python
# test_solution.py
from solution import count_multiples_in_range

def test_count_multiples_in_range():
    assert count_multiples_in_range(1, 10, 2) == 5
    assert count_multiples_in_range(5, 15, 5) == 3
    assert count_multiples_in_range(1, 100, 7) == 14
```

**解答例**

```python
# solution.py
def count_multiples_in_range(start, end, divisor):
    count = 0
    for i in range(start, end + 1):
        if i % divisor == 0:
            count += 1
    return count
```

---

## 第4章：繰り返し処理（Q31〜Q40）

---

### Q31. 階乗

**問題文**
`factorial(n)` という関数を定義してください。非負整数 `n` の階乗を返してください。0の階乗は1とします。再帰を使わずに実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import factorial

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800
```

**解答例**

```python
# solution.py
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

---

### Q32. フィボナッチ数列

**問題文**
`fibonacci(n)` という関数を定義してください。非負整数 `n` に対して、フィボナッチ数列の第 `n` 項（0始まり）を返してください。

- fib(0) = 0
- fib(1) = 1
- fib(n) = fib(n-1) + fib(n-2)

**テストケースの書き方**

```python
# test_solution.py
from solution import fibonacci

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(20) == 6765
```

**解答例**

```python
# solution.py
def fibonacci(n):
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

---

### Q33. 約数の列挙

**問題文**
`divisors(n)` という関数を定義してください。正の整数 `n` の正の約数をすべて昇順でリストにして返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import divisors

def test_divisors():
    assert divisors(12) == [1, 2, 3, 4, 6, 12]
    assert divisors(13) == [1, 13]
    assert divisors(1) == [1]
```

**解答例**

```python
# solution.py
def divisors(n):
    result = []
    for i in range(1, n + 1):
        if n % i == 0:
            result.append(i)
    return result
```

---

### Q34. 素数判定

**問題文**
`is_prime(n)` という関数を定義してください。整数 `n` が素数なら `True`、そうでなければ `False` を返してください。1以下は素数ではありません。

**テストケースの書き方**

```python
# test_solution.py
from solution import is_prime

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(17) is True
    assert is_prime(18) is False
    assert is_prime(1) is False
    assert is_prime(0) is False
```

**解答例**

```python
# solution.py
import math

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True
```

---

### Q35. 九九の表

**問題文**
`multiplication_table()` という関数を定義してください。1から9までの九九の表を、各行がスペース区切りの文字列となったリストとして返してください。1行目は `1×1` から `1×9` まで、9行目は `9×1` から `9×9` までとします。

**テストケースの書き方**

```python
# test_solution.py
from solution import multiplication_table

def test_multiplication_table():
    table = multiplication_table()
    assert len(table) == 9
    assert table[0] == "1 2 3 4 5 6 7 8 9"
    assert table[1] == "2 4 6 8 10 12 14 16 18"
    assert table[8] == "9 18 27 36 45 54 63 72 81"
```

**解答例**

```python
# solution.py
def multiplication_table():
    table = []
    for i in range(1, 10):
        row = " ".join(str(i * j) for j in range(1, 10))
        table.append(row)
    return table
```

---

### Q36. 数字の反転

**問題文**
`reverse_number(n)` という関数を定義してください。正の整数 `n` を受け取り、各位の数字を逆順に並べ替えた整数を返してください。先頭のゼロは無視されます（例：`1200` → `21`）。

**テストケースの書き方**

```python
# test_solution.py
from solution import reverse_number

def test_reverse_number():
    assert reverse_number(123) == 321
    assert reverse_number(1200) == 21
    assert reverse_number(5) == 5
```

**解答例**

```python
# solution.py
def reverse_number(n):
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    return reversed_num
```

---

### Q37. 2進数表示

**問題文**
`to_binary(n)` という関数を定義してください。非負整数 `n` を2進数表記の文字列に変換して返してください。組み込み関数 `bin()` は使わないでください。ただし `0` の場合は `"0"` を返します。

**テストケースの書き方**

```python
# test_solution.py
from solution import to_binary

def test_to_binary():
    assert to_binary(0) == "0"
    assert to_binary(5) == "101"
    assert to_binary(255) == "11111111"
```

**解答例**

```python
# solution.py
def to_binary(n):
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = str(n % 2) + result
        n //= 2
    return result
```

---

### Q38. 桁数の和

**問題文**
`digit_sum(n)` という関数を定義してください。非負整数 `n` の各位の数字の和を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import digit_sum

def test_digit_sum():
    assert digit_sum(123) == 6
    assert digit_sum(9999) == 36
    assert digit_sum(0) == 0
```

**解答例**

```python
# solution.py
def digit_sum(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total
```

---

### Q39. パスカルの三角形

**問題文**
`pascal_triangle(n)` という関数を定義してください。パスカルの三角形の上から `n` 行目（1始まり）のリストを返してください。各行の両端は1で、内側の数値は上の行の隣り合う2数の和です。

**テストケースの書き方**

```python
# test_solution.py
from solution import pascal_triangle

def test_pascal_triangle():
    assert pascal_triangle(1) == [1]
    assert pascal_triangle(2) == [1, 1]
    assert pascal_triangle(5) == [1, 4, 6, 4, 1]
    assert pascal_triangle(6) == [1, 5, 10, 10, 5, 1]
```

**解答例**

```python
# solution.py
def pascal_triangle(n):
    row = [1]
    for _ in range(1, n):
        new_row = [1]
        for i in range(len(row) - 1):
            new_row.append(row[i] + row[i + 1])
        new_row.append(1)
        row = new_row
    return row
```

---

### Q40. コラッツ数列

**問題文**
`collatz_length(n)` という関数を定義してください。正の整数 `n` に対して、コラッツ数列（偶数なら2で割る、奇数なら3倍して1足す、を1になるまで繰り返す）の長さ（1を含む項数）を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import collatz_length

def test_collatz_length():
    assert collatz_length(1) == 1
    assert collatz_length(6) == 9  # 6,3,10,5,16,8,4,2,1
    assert collatz_length(7) == 17
```

**解答例**

```python
# solution.py
def collatz_length(n):
    length = 1
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        length += 1
    return length
```

---

## 第5章：リストとタプル（Q41〜Q50）

---

### Q41. 最大値のインデックス

**問題文**
`argmax(numbers)` という関数を定義してください。数値のリスト `numbers` の中で最大値のインデックス（先頭からの0始まり）を返してください。最大値が複数ある場合は、最も先頭に近いものを返してください。組み込み関数 `max()` や `index()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import argmax

def test_argmax():
    assert argmax([3, 1, 4, 1, 5]) == 4
    assert argmax([10, 10, 5]) == 0
    assert argmax([-5, -2, -10]) == 1
```

**解答例**

```python
# solution.py
def argmax(numbers):
    if not numbers:
        return None
    max_idx = 0
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[max_idx]:
            max_idx = i
    return max_idx
```

---

### Q42. リストの反転

**問題文**
`my_reverse(lst)` という関数を定義してください。リスト `lst` を反転した新しいリストを返してください。組み込み関数 `reversed()` やメソッド `reverse()`、`[::-1]` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import my_reverse

def test_my_reverse():
    assert my_reverse([1, 2, 3]) == [3, 2, 1]
    assert my_reverse(["a"]) == ["a"]
    assert my_reverse([]) == []
```

**解答例**

```python
# solution.py
def my_reverse(lst):
    result = []
    for i in range(len(lst) - 1, -1, -1):
        result.append(lst[i])
    return result
```

---

### Q43. 重複削除

**問題文**
`unique_ordered(lst)` という関数を定義してください。リスト `lst` から重複する要素を削除し、元の順序を保ったリストを返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import unique_ordered

def test_unique_ordered():
    assert unique_ordered([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
    assert unique_ordered(["a", "b", "a", "c"]) == ["a", "b", "c"]
    assert unique_ordered([]) == []
```

**解答例**

```python
# solution.py
def unique_ordered(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

---

### Q44. リストの回転

**問題文**
`rotate_left(lst, k)` という関数を定義してください。リスト `lst` を左に `k` 回転させた新しいリストを返してください。`k` は非負整数とします。例えば `[1, 2, 3, 4]` を1回左に回転すると `[2, 3, 4, 1]` になります。

**テストケースの書き方**

```python
# test_solution.py
from solution import rotate_left

def test_rotate_left():
    assert rotate_left([1, 2, 3, 4], 1) == [2, 3, 4, 1]
    assert rotate_left([1, 2, 3, 4], 2) == [3, 4, 1, 2]
    assert rotate_left([1, 2, 3, 4], 5) == [2, 3, 4, 1]
```

**解答例**

```python
# solution.py
def rotate_left(lst, k):
    if not lst:
        return []
    k = k % len(lst)
    return lst[k:] + lst[:k]
```

---

### Q45. 2つのリストの共通要素

**問題文**
`common_elements(a, b)` という関数を定義してください。2つのリスト `a`, `b` に共通して含まれる要素を、重複なく、昇順にソートしたリストとして返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import common_elements

def test_common_elements():
    assert common_elements([1, 2, 3, 4], [3, 4, 5, 6]) == [3, 4]
    assert common_elements(["a", "b"], ["c", "d"]) == []
    assert common_elements([1, 1, 1], [1, 1]) == [1]
```

**解答例**

```python
# solution.py
def common_elements(a, b):
    return sorted(list(set(a) & set(b)))
```

---

### Q46. 部分リストの和の最大値

**問題文**
`max_subarray_sum(numbers)` という関数を定義してください。数値のリスト `numbers` の連続する部分リストの和の最大値を返してください。リストが空の場合は `0` を返してください。（Kadaneのアルゴリズムを使って解いてください）

**テストケースの書き方**

```python
# test_solution.py
from solution import max_subarray_sum

def test_max_subarray_sum():
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_sum([1]) == 1
    assert max_subarray_sum([5, 4, -1, 7, 8]) == 23
    assert max_subarray_sum([]) == 0
```

**解答例**

```python
# solution.py
def max_subarray_sum(numbers):
    max_sum = 0
    current_sum = 0
    for num in numbers:
        current_sum = max(0, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
```

---

### Q47. バブルソート

**問題文**
`bubble_sort(lst)` という関数を定義してください。リスト `lst` を昇順にソートした新しいリストを返してください。組み込み関数 `sorted()` やメソッド `sort()` は使わず、バブルソートの手法を実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import bubble_sort

def test_bubble_sort():
    assert bubble_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert bubble_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert bubble_sort([]) == []
```

**解答例**

```python
# solution.py
def bubble_sort(lst):
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

---

### Q48. 行列の転置

**問題文**
`transpose(matrix)` という関数を定義してください。2次元リスト `matrix`（行列）を転置した新しい行列を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import transpose

def test_transpose():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
    assert transpose([]) == []
```

**解答例**

```python
# solution.py
def transpose(matrix):
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]
```

---

### Q49. 二次元リストの初期化

**問題文**
`create_matrix(rows, cols, value)` という関数を定義してください。`rows` 行 `cols` 列の2次元リストを作成し、すべての要素を `value` で初期化して返してください。ただし、各行が同じリストオブジェクトを参照してはいけません（独立した行リストである必要があります）。

**テストケースの書き方**

```python
# test_solution.py
from solution import create_matrix

def test_create_matrix():
    m = create_matrix(2, 3, 0)
    assert m == [[0, 0, 0], [0, 0, 0]]
    m[0][0] = 1
    assert m[1][0] == 0  # 各行が独立であることを確認
```

**解答例**

```python
# solution.py
def create_matrix(rows, cols, value):
    return [[value for _ in range(cols)] for _ in range(rows)]
```

---

### Q50. タプルのリストを辞書に変換

**問題文**
`pairs_to_dict(pairs)` という関数を定義してください。`(key, value)` のタプルのリスト `pairs` を辞書に変換して返してください。同じキーが複数回出現する場合は、最後に登場した値を採用してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import pairs_to_dict

def test_pairs_to_dict():
    assert pairs_to_dict([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}
    assert pairs_to_dict([("a", 1), ("a", 2)]) == {"a": 2}
    assert pairs_to_dict([]) == {}
```

**解答例**

```python
# solution.py
def pairs_to_dict(pairs):
    result = {}
    for key, value in pairs:
        result[key] = value
    return result
```

---

## 第6章：辞書と集合（Q51〜Q60）

---

### Q51. 文字の出現回数

**問題文**
`char_frequency(s)` という関数を定義してください。文字列 `s` に含まれる各文字の出現回数を辞書として返してください。大文字小文字は区別します。

**テストケースの書き方**

```python
# test_solution.py
from solution import char_frequency

def test_char_frequency():
    assert char_frequency("hello") == {"h": 1, "e": 1, "l": 2, "o": 1}
    assert char_frequency("") == {}
```

**解答例**

```python
# solution.py
def char_frequency(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq
```

---

### Q52. 値で辞書をソート

**問題文**
`sort_dict_by_value(d, ascending=True)` という関数を定義してください。辞書 `d` のキーを、対応する値でソートしたタプル `(key, value)` のリストを返してください。`ascending` が `True` なら昇順、`False` なら降順とします。

**テストケースの書き方**

```python
# test_solution.py
from solution import sort_dict_by_value

def test_sort_dict_by_value():
    d = {"a": 3, "b": 1, "c": 2}
    assert sort_dict_by_value(d) == [("b", 1), ("c", 2), ("a", 3)]
    assert sort_dict_by_value(d, False) == [("a", 3), ("c", 2), ("b", 1)]
```

**解答例**

```python
# solution.py
def sort_dict_by_value(d, ascending=True):
    return sorted(d.items(), key=lambda x: x[1], reverse=not ascending)
```

---

### Q53. 2つの辞書のマージ

**問題文**
`merge_dicts(a, b)` という関数を定義してください。2つの辞書 `a`, `b` をマージした新しい辞書を返してください。同じキーが両方に存在する場合は、値を足し合わせてください（数値を想定）。

**テストケースの書き方**

```python
# test_solution.py
from solution import merge_dicts

def test_merge_dicts():
    assert merge_dicts({"x": 1, "y": 2}, {"y": 3, "z": 4}) == {"x": 1, "y": 5, "z": 4}
    assert merge_dicts({}, {"a": 10}) == {"a": 10}
```

**解答例**

```python
# solution.py
def merge_dicts(a, b):
    result = dict(a)
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    return result
```

---

### Q54. 辞書の値の反転

**問題文**
`invert_dict(d)` という関数を定義してください。辞書 `d` のキーと値を入れ替えた新しい辞書を返してください。ただし、値が重複している場合は、そのうちの1つだけを保持します（最後に処理したもの）。

**テストケースの書き方**

```python
# test_solution.py
from solution import invert_dict

def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert_dict({"a": 1, "b": 1}) == {1: "b"}
```

**解答例**

```python
# solution.py
def invert_dict(d):
    return {v: k for k, v in d.items()}
```

---

### Q55. 集合の対称差

**問題文**
`symmetric_difference(a, b)` という関数を定義してください。2つのリスト `a`, `b` を集合として扱い、どちらか一方にだけ含まれる要素のリスト（ソート済み）を返してください。組み込みの `symmetric_difference` メソッドは使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import symmetric_difference

def test_symmetric_difference():
    assert symmetric_difference([1, 2, 3], [2, 3, 4]) == [1, 4]
    assert symmetric_difference(["a", "b"], ["b", "c"]) == ["a", "c"]
```

**解答例**

```python
# solution.py
def symmetric_difference(a, b):
    set_a = set(a)
    set_b = set(b)
    result = []
    for item in set_a:
        if item not in set_b:
            result.append(item)
    for item in set_b:
        if item not in set_a:
            result.append(item)
    return sorted(result)
```

---

### Q56. 重複する要素の抽出

**問題文**
`find_duplicates(lst)` という関数を定義してください。リスト `lst` の中で2回以上出現する要素を、重複なく昇順にソートしたリストとして返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import find_duplicates

def test_find_duplicates():
    assert find_duplicates([1, 2, 2, 3, 3, 3, 4]) == [2, 3]
    assert find_duplicates(["a", "b", "a", "c", "b"]) == ["a", "b"]
    assert find_duplicates([1, 2, 3]) == []
```

**解答例**

```python
# solution.py
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(list(duplicates))
```

---

### Q57. グループ化

**問題文**
`group_by_length(words)` という関数を定義してください。文字列のリスト `words` を、文字列の長さごとにグループ化した辞書を返してください。キーは長さ（整数）、値はその長さの文字列のリストです。

**テストケースの書き方**

```python
# test_solution.py
from solution import group_by_length

def test_group_by_length():
    words = ["a", "bb", "ccc", "dd", "e"]
    result = group_by_length(words)
    assert result[1] == ["a", "e"]
    assert result[2] == ["bb", "dd"]
    assert result[3] == ["ccc"]
```

**解答例**

```python
# solution.py
def group_by_length(words):
    groups = {}
    for word in words:
        length = len(word)
        if length not in groups:
            groups[length] = []
        groups[length].append(word)
    return groups
```

---

### Q58. デフォルト値付き辞書アクセス

**問題文**
`get_with_default(d, key, default)` という関数を定義してください。辞書 `d` からキー `key` に対応する値を取得して返します。キーが存在しない場合は `default` を返してください。組み込みの `dict.get()` メソッドは使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import get_with_default

def test_get_with_default():
    assert get_with_default({"a": 1}, "a", 0) == 1
    assert get_with_default({"a": 1}, "b", 0) == 0
    assert get_with_default({}, "x", "default") == "default"
```

**解答例**

```python
# solution.py
def get_with_default(d, key, default):
    for k in d:
        if k == key:
            return d[k]
    return default
```

---

### Q59. リスト内の出現回数トップN

**問題文**
`top_n_frequent(lst, n)` という関数を定義してください。リスト `lst` の要素の出現回数が多い順に `n` 個の要素を返してください。同じ回数の場合は値の小さい方（文字列なら辞書順）を優先します。

**テストケースの書き方**

```python
# test_solution.py
from solution import top_n_frequent

def test_top_n_frequent():
    assert top_n_frequent([1, 2, 2, 3, 3, 3], 2) == [3, 2]
    assert top_n_frequent(["a", "b", "a", "b", "c"], 2) == ["a", "b"]
```

**解答例**

```python
# solution.py
def top_n_frequent(lst, n):
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [item for item, count in sorted_items[:n]]
```

---

### Q60. 辞書の深いコピー（1段階のみ）

**問題文**
`shallow_copy_dict(d)` という関数を定義してください。辞書 `d` の浅いコピーを返してください。組み込みモジュール `copy` は使わず、`dict.copy()` メソッドも使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import shallow_copy_dict

def test_shallow_copy_dict():
    original = {"a": [1, 2], "b": 3}
    copied = shallow_copy_dict(original)
    assert copied == original
    copied["b"] = 100
    assert original["b"] == 3
    copied["a"].append(3)
    assert original["a"] == [1, 2, 3]  # 浅いコピーなのでリストは共有
```

**解答例**

```python
# solution.py
def shallow_copy_dict(d):
    return {k: v for k, v in d.items()}
```

## 第7章：関数（Q61〜Q75）

---

### Q61. 可変長引数の合計

**問題文**
`sum_all(*args)` という関数を定義してください。可変長の数値引数を受け取り、その合計を返してください。引数がない場合は `0` を返します。

**テストケースの書き方**

```python
# test_solution.py
from solution import sum_all

def test_sum_all():
    assert sum_all(1, 2, 3) == 6
    assert sum_all() == 0
    assert sum_all(10) == 10
```

**解答例**

```python
# solution.py
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total
```

---

### Q62. 高階関数：mapの実装

**問題文**
`my_map(func, lst)` という関数を定義してください。リスト `lst` の各要素に関数 `func` を適用した結果を新しいリストとして返してください。組み込み関数 `map()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import my_map

def test_my_map():
    assert my_map(lambda x: x * 2, [1, 2, 3]) == [2, 4, 6]
    assert my_map(str, [1, 2, 3]) == ["1", "2", "3"]
    assert my_map(len, []) == []
```

**解答例**

```python
# solution.py
def my_map(func, lst):
    return [func(item) for item in lst]
```

---

### Q63. 高階関数：filterの実装

**問題文**
`my_filter(func, lst)` という関数を定義してください。リスト `lst` の各要素に対して関数 `func` を適用し、その結果が真となる要素だけを集めた新しいリストを返してください。組み込み関数 `filter()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import my_filter

def test_my_filter():
    assert my_filter(lambda x: x > 0, [-1, 0, 1, 2]) == [1, 2]
    assert my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4]) == [2, 4]
    assert my_filter(bool, []) == []
```

**解答例**

```python
# solution.py
def my_filter(func, lst):
    return [item for item in lst if func(item)]
```

---

### Q64. クロージャ

**問題文**
`make_multiplier(n)` という関数を定義してください。整数 `n` を受け取り、`x` を受け取って `n * x` を返す関数（クロージャ）を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import make_multiplier

def test_make_multiplier():
    double = make_multiplier(2)
    triple = make_multiplier(3)
    assert double(5) == 10
    assert triple(4) == 12
```

**解答例**

```python
# solution.py
def make_multiplier(n):
    def multiplier(x):
        return n * x
    return multiplier
```

---

### Q65. デコレータ：実行時間計測

**問題文**
`timer(func)` というデコレータを定義してください。デコレートされた関数の実行時間（秒）を `print` で出力し、元の関数の結果を返してください。ただし、この問題では `time` モジュールを使って実装してください。

**テストケースの書き方**

```python
# test_solution.py
import time
from solution import timer

@timer
def slow_add(a, b):
    time.sleep(0.01)
    return a + b

def test_timer(capsys):
    result = slow_add(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    assert "seconds" in captured.out
```

**解答例**

```python
# solution.py
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.6f} seconds")
        return result
    return wrapper
```

---

### Q66. 再帰：階乗

**問題文**
`factorial_recursive(n)` という関数を定義してください。非負整数 `n` の階乗を再帰を使って計算して返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import factorial_recursive

def test_factorial_recursive():
    assert factorial_recursive(0) == 1
    assert factorial_recursive(5) == 120
    assert factorial_recursive(1) == 1
```

**解答例**

```python
# solution.py
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
```

---

### Q67. 再帰：ユークリッドの互除法

**問題文**
`gcd(a, b)` という関数を定義してください。2つの非負整数 `a`, `b` の最大公約数を、ユークリッドの互除法を再帰で実装して返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import gcd

def test_gcd():
    assert gcd(48, 18) == 6
    assert gcd(100, 25) == 25
    assert gcd(7, 3) == 1
    assert gcd(0, 5) == 5
```

**解答例**

```python
# solution.py
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)
```

---

### Q68. 再帰：リストの長さ

**問題文**
`length_recursive(lst)` という関数を定義してください。リスト `lst` の長さを再帰を使って計算して返してください。組み込み関数 `len()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import length_recursive

def test_length_recursive():
    assert length_recursive([1, 2, 3]) == 3
    assert length_recursive([]) == 0
    assert length_recursive(["a"]) == 1
```

**解答例**

```python
# solution.py
def length_recursive(lst):
    if not lst:
        return 0
    return 1 + length_recursive(lst[1:])
```

---

### Q69. 部分適用

**問題文**
`partial(func, *fixed_args)` という関数を定義してください。関数 `func` と固定する引数 `fixed_args` を受け取り、残りの引数を受け取って `func` を呼び出す新しい関数を返してください。`functools.partial` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import partial

def test_partial():
    def add(a, b, c):
        return a + b + c
    add_5 = partial(add, 5)
    assert add_5(3, 2) == 10
    add_5_3 = partial(add, 5, 3)
    assert add_5_3(2) == 10
```

**解答例**

```python
# solution.py
def partial(func, *fixed_args):
    def wrapper(*args):
        return func(*fixed_args, *args)
    return wrapper
```

---

### Q70. キーワード引数の辞書化

**問題文**
`kwargs_to_dict(**kwargs)` という関数を定義してください。受け取ったすべてのキーワード引数を辞書として返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import kwargs_to_dict

def test_kwargs_to_dict():
    assert kwargs_to_dict(a=1, b=2) == {"a": 1, "b": 2}
    assert kwargs_to_dict() == {}
```

**解答例**

```python
# solution.py
def kwargs_to_dict(**kwargs):
    return kwargs
```

---

### Q71. デフォルト引数の罠を回避

**問題文**
`append_item_safe(item, lst=None)` という関数を定義してください。リスト `lst` に `item` を追加して返します。`lst` が指定されない場合は新しい空リストを作成して使用してください。可変オブジェクトをデフォルト引数にしない形で実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import append_item_safe

def test_append_item_safe():
    assert append_item_safe(1) == [1]
    assert append_item_safe(2) == [2]  # 前回の呼び出しと共有されていないことを確認
    assert append_item_safe(3, [0]) == [0, 3]
```

**解答例**

```python
# solution.py
def append_item_safe(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

### Q72. 関数の合成

**問題文**
`compose(f, g)` という関数を定義してください。2つの関数 `f`, `g` を受け取り、`compose(f, g)(x) = f(g(x))` となる新しい関数を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import compose

def test_compose():
    double = lambda x: x * 2
    increment = lambda x: x + 1
    h = compose(double, increment)
    assert h(3) == 8  # double(increment(3)) = double(4) = 8
```

**解答例**

```python
# solution.py
def compose(f, g):
    def h(x):
        return f(g(x))
    return h
```

---

### Q73. メモ化

**問題文**
`memoize(func)` というデコレータを定義してください。デコレートされた関数の結果をキャッシュし、同じ引数で再度呼び出されたときはキャッシュから結果を返すようにしてください。引数は位置引数のみで、ハッシュ可能なものとします。

**テストケースの書き方**

```python
# test_solution.py
from solution import memoize

call_count = 0

@memoize
def slow_fib(n):
    global call_count
    call_count += 1
    if n <= 1:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)

def test_memoize():
    global call_count
    call_count = 0
    assert slow_fib(10) == 55
    assert call_count <= 20  # メモ化により呼び出し回数が抑えられている
```

**解答例**

```python
# solution.py
import functools

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

---

### Q74. カリー化

**問題文**
`curry(func)` という関数を定義してください。2引数の関数 `func` を、1引数ずつ受け取るカリー化された関数に変換して返してください。例：`curry(add)(1)(2) == 3`

**テストケースの書き方**

```python
# test_solution.py
from solution import curry

def test_curry():
    def add(a, b):
        return a + b
    curried_add = curry(add)
    assert curried_add(1)(2) == 3
```

**解答例**

```python
# solution.py
def curry(func):
    def inner_a(a):
        def inner_b(b):
            return func(a, b)
        return inner_b
    return inner_a
```

---

### Q75. コールバック付き処理

**問題文**
`process_and_callback(data, callback)` という関数を定義してください。リスト `data` の各要素を2倍にした新しいリストを作成し、その結果を `callback` 関数に渡して呼び出してください。最後に変換後のリストを返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import process_and_callback

def test_process_and_callback():
    called_with = []
    def callback(result):
        called_with.append(result)
    result = process_and_callback([1, 2, 3], callback)
    assert result == [2, 4, 6]
    assert called_with == [[2, 4, 6]]
```

**解答例**

```python
# solution.py
def process_and_callback(data, callback):
    result = [x * 2 for x in data]
    callback(result)
    return result
```

## 第8章：文字列操作（Q76〜Q85）

---

### Q76. アナグラム判定

**問題文**
`is_anagram(s1, s2)` という関数を定義してください。2つの文字列 `s1`, `s2` がアナグラム（同じ文字を同じ数だけ含む並び替え）なら `True`、そうでなければ `False` を返してください。大文字小文字は区別せず、空白は無視してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import is_anagram

def test_is_anagram():
    assert is_anagram("listen", "silent") is True
    assert is_anagram("Hello", "olleh") is True
    assert is_anagram("abc", "def") is False
```

**解答例**

```python
# solution.py
def is_anagram(s1, s2):
    def normalize(s):
        return sorted(ch.lower() for ch in s if ch.isalpha())
    return normalize(s1) == normalize(s2)
```

---

### Q77. 単語数カウント

**問題文**
`count_words(s)` という関数を定義してください。文字列 `s` に含まれる単語の数を返してください。単語は空白（スペース、タブ、改行）で区切られた文字列とします。連続する空白は1つの区切りとみなします。

**テストケースの書き方**

```python
# test_solution.py
from solution import count_words

def test_count_words():
    assert count_words("hello world") == 2
    assert count_words("  a   b  c ") == 3
    assert count_words("") == 0
    assert count_words("one") == 1
```

**解答例**

```python
# solution.py
def count_words(s):
    words = s.split()
    return len(words)
```

---

### Q78. スネークケース→キャメルケース

**問題文**
`snake_to_camel(s)` という関数を定義してください。スネークケース（`snake_case_string`）の文字列を受け取り、キャメルケース（`snakeCaseString`）に変換して返してください。ただし先頭の単語は小文字のままとします。

**テストケースの書き方**

```python
# test_solution.py
from solution import snake_to_camel

def test_snake_to_camel():
    assert snake_to_camel("hello_world") == "helloWorld"
    assert snake_to_camel("get_user_name") == "getUserName"
    assert snake_to_camel("single") == "single"
```

**解答例**

```python
# solution.py
def snake_to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])
```

---

### Q79. 文字列の圧縮（Run-length encoding）

**問題文**
`run_length_encode(s)` という関数を定義してください。文字列 `s` をランレングス圧縮して返してください。例：`"aaabbc"` → `"a3b2c1"`

**テストケースの書き方**

```python
# test_solution.py
from solution import run_length_encode

def test_run_length_encode():
    assert run_length_encode("aaabbc") == "a3b2c1"
    assert run_length_encode("a") == "a1"
    assert run_length_encode("aabbaa") == "a2b2a2"
```

**解答例**

```python
# solution.py
def run_length_encode(s):
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(s[i - 1] + str(count))
            count = 1
    result.append(s[-1] + str(count))
    return "".join(result)
```

---

### Q80. 文字列の展開（Run-length decoding）

**問題文**
`run_length_decode(s)` という関数を定義してください。ランレングス圧縮された文字列 `s` を元に戻して返してください。例：`"a3b2c1"` → `"aaabbc"`

**テストケースの書き方**

```python
# test_solution.py
from solution import run_length_decode

def test_run_length_decode():
    assert run_length_decode("a3b2c1") == "aaabbc"
    assert run_length_decode("a1") == "a"
    assert run_length_decode("a2b2a2") == "aabbaa"
```

**解答例**

```python
# solution.py
def run_length_decode(s):
    result = []
    i = 0
    while i < len(s):
        ch = s[i]
        i += 1
        count = 0
        while i < len(s) and s[i].isdigit():
            count = count * 10 + int(s[i])
            i += 1
        result.append(ch * count)
    return "".join(result)
```

---

### Q81. ゼロ埋め

**問題文**
`zero_pad(n, width)` という関数を定義してください。整数 `n` を受け取り、桁数が `width` になるように先頭にゼロを埋めた文字列を返してください。組み込みの `zfill()` は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import zero_pad

def test_zero_pad():
    assert zero_pad(42, 5) == "00042"
    assert zero_pad(42, 2) == "42"
    assert zero_pad(0, 3) == "000"
```

**解答例**

```python
# solution.py
def zero_pad(n, width):
    s = str(n)
    zeros_needed = width - len(s)
    if zeros_needed > 0:
        return "0" * zeros_needed + s
    return s
```

---

### Q82. カンマ区切りの数字

**問題文**
`format_number(n)` という関数を定義してください。整数 `n` を3桁ごとにカンマで区切った文字列にして返してください。負の数も考慮してください。組み込みの `format()` や f-string のカンマ書式指定は使わないでください。

**テストケースの書き方**

```python
# test_solution.py
from solution import format_number

def test_format_number():
    assert format_number(1234567) == "1,234,567"
    assert format_number(1000) == "1,000"
    assert format_number(100) == "100"
    assert format_number(-1234567) == "-1,234,567"
```

**解答例**

```python
# solution.py
def format_number(n):
    negative = n < 0
    s = str(abs(n))
    result = []
    for i, ch in enumerate(reversed(s)):
        if i > 0 and i % 3 == 0:
            result.append(",")
        result.append(ch)
    formatted = "".join(reversed(result))
    return "-" + formatted if negative else formatted
```

---

### Q83. テンプレート文字列の置換

**問題文**
`simple_template(template, mapping)` という関数を定義してください。テンプレート文字列 `template` の中の `{key}` を `mapping` 辞書の対応する値に置換して返してください。正規表現は使わず、`str.replace()` も使わないでください（手動で `{` と `}` を探して置換してください）。

**テストケースの書き方**

```python
# test_solution.py
from solution import simple_template

def test_simple_template():
    assert simple_template("Hello, {name}!", {"name": "Alice"}) == "Hello, Alice!"
    assert simple_template("{x} + {y} = {z}", {"x": "1", "y": "2", "z": "3"}) == "1 + 2 = 3"
```

**解答例**

```python
# solution.py
def simple_template(template, mapping):
    result = []
    i = 0
    while i < len(template):
        if template[i] == "{":
            j = template.find("}", i)
            if j != -1:
                key = template[i + 1:j]
                result.append(mapping.get(key, ""))
                i = j + 1
                continue
        result.append(template[i])
        i += 1
    return "".join(result)
```

---

### Q84. ローマ数字→整数

**問題文**
`roman_to_int(s)` という関数を定義してください。ローマ数字の文字列 `s` を整数に変換して返してください。`I=1, V=5, X=10, L=50, C=100, D=500, M=1000` とします。減算記法（IV=4, IX=9 など）も考慮してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import roman_to_int

def test_roman_to_int():
    assert roman_to_int("III") == 3
    assert roman_to_int("IV") == 4
    assert roman_to_int("IX") == 9
    assert roman_to_int("LVIII") == 58
    assert roman_to_int("MCMXCIV") == 1994
```

**解答例**

```python
# solution.py
def roman_to_int(s):
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        curr = values[ch]
        if curr < prev:
            total -= curr
        else:
            total += curr
        prev = curr
    return total
```

---

### Q85. 文字列の差分（1文字のみ）

**問題文**
`is_one_edit_away(s1, s2)` という関数を定義してください。2つの文字列 `s1`, `s2` が「1文字だけ異なる（または長さが1だけ異なる）」かどうかを判定してください。具体的には、以下のいずれか1回で `s1` を `s2` に変換できる場合に `True` を返します。

- 1文字挿入
- 1文字削除
- 1文字置換

**テストケースの書き方**

```python
# test_solution.py
from solution import is_one_edit_away

def test_is_one_edit_away():
    assert is_one_edit_away("pale", "ple") is True
    assert is_one_edit_away("pales", "pale") is True
    assert is_one_edit_away("pale", "bale") is True
    assert is_one_edit_away("pale", "bake") is False
```

**解答例**

```python
# solution.py
def is_one_edit_away(s1, s2):
    len1, len2 = len(s1), len(s2)
    if abs(len1 - len2) > 1:
        return False
    i = j = diff = 0
    while i < len1 and j < len2:
        if s1[i] != s2[j]:
            if diff == 1:
                return False
            diff += 1
            if len1 > len2:
                i += 1
            elif len1 < len2:
                j += 1
            else:
                i += 1
                j += 1
        else:
            i += 1
            j += 1
    if i < len1 or j < len2:
        diff += 1
    return diff == 1
```

## 第9章：ファイル操作（Q86〜Q92）

---

### Q86. ファイルの行数カウント

**問題文**
`count_lines(filepath)` という関数を定義してください。ファイルの行数を返してください。空のファイルの場合は `0` を返します。

**テストケースの書き方**

テスト用に一時ファイルを作成して使います。

```python
# test_solution.py
import tempfile
import os
from solution import count_lines

def test_count_lines():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("line1\nline2\nline3\n")
        path = f.name
    assert count_lines(path) == 3
    os.unlink(path)
```

**解答例**

```python
# solution.py
def count_lines(filepath):
    count = 0
    with open(filepath, "r") as f:
        for _ in f:
            count += 1
    return count
```

---

### Q87. ファイルの内容をリストで取得

**問題文**
`read_lines_from_file(filepath)` という関数を定義してください。ファイルの各行を要素とするリストを返してください。各行の末尾の改行文字 `\n` は取り除いてください。

**テストケースの書き方**

```python
# test_solution.py
import tempfile
import os
from solution import read_lines_from_file

def test_read_lines_from_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("apple\nbanana\ncherry\n")
        path = f.name
    assert read_lines_from_file(path) == ["apple", "banana", "cherry"]
    os.unlink(path)
```

**解答例**

```python
# solution.py
def read_lines_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f]
```

---

### Q88. ファイルへの書き込み

**問題文**
`write_numbers(filepath, numbers)` という関数を定義してください。数値のリスト `numbers` を、1行に1つずつファイル `filepath` に書き込んでください。ファイルが既に存在する場合は上書きしてください。

**テストケースの書き方**

```python
# test_solution.py
import tempfile
import os
from solution import write_numbers

def test_write_numbers():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "nums.txt")
        write_numbers(path, [1, 2, 3])
        with open(path, "r") as f:
            assert f.read() == "1\n2\n3\n"
```

**解答例**

```python
# solution.py
def write_numbers(filepath, numbers):
    with open(filepath, "w") as f:
        for num in numbers:
            f.write(str(num) + "\n")
```

---

### Q89. CSV風テキストのパース

**問題文**
`parse_csv_line(line)` という関数を定義してください。カンマ区切りの1行 `line` を受け取り、各フィールドを要素とするリストを返してください。`csv` モジュールは使わず、自力でパースしてください。

**テストケースの書き方**

```python
# test_solution.py
from solution import parse_csv_line

def test_parse_csv_line():
    assert parse_csv_line("a,b,c") == ["a", "b", "c"]
    assert parse_csv_line("1,2,3,4") == ["1", "2", "3", "4"]
    assert parse_csv_line("single") == ["single"]
```

**解答例**

```python
# solution.py
def parse_csv_line(line):
    return line.split(",")
```

---

### Q90. ファイルのコピー

**問題文**
`copy_file(src, dst)` という関数を定義してください。ファイル `src` の内容をファイル `dst` にコピーしてください。`shutil` モジュールは使わず、1行ずつ読み書きしてください。

**テストケースの書き方**

```python
# test_solution.py
import tempfile
import os
from solution import copy_file

def test_copy_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        with open(src, "w") as f:
            f.write("hello\nworld\n")
        copy_file(src, dst)
        with open(dst, "r") as f:
            assert f.read() == "hello\nworld\n"
```

**解答例**

```python
# solution.py
def copy_file(src, dst):
    with open(src, "r") as f_src, open(dst, "w") as f_dst:
        for line in f_src:
            f_dst.write(line)
```

---

### Q91. ディレクトリ内のファイル一覧（拡張子指定）

**問題文**
`list_files_with_extension(directory, ext)` という関数を定義してください。ディレクトリ `directory` の中から、拡張子が `ext`（例：`.txt`）のファイル名のみをリストとして返してください。サブディレクトリは探索しません。`glob` モジュールは使わず、`os.listdir()` を使ってください。

**テストケースの書き方**

```python
# test_solution.py
import tempfile
import os
from solution import list_files_with_extension

def test_list_files_with_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, "a.txt"), "w").close()
        open(os.path.join(tmpdir, "b.py"), "w").close()
        open(os.path.join(tmpdir, "c.txt"), "w").close()
        result = list_files_with_extension(tmpdir, ".txt")
        assert sorted(result) == ["a.txt", "c.txt"]
```

**解答例**

```python
# solution.py
import os

def list_files_with_extension(directory, ext):
    return [name for name in os.listdir(directory) if name.endswith(ext)]
```

---

### Q92. 大きなファイルの行頭フィルタ

**問題文**
`filter_lines_by_prefix(src, dst, prefix)` という関数を定義してください。ファイル `src` から `prefix` で始まる行だけを抽出して、ファイル `dst` に書き込んでください。メモリにファイル全体を読み込まず、1行ずつ処理してください。

**テストケースの書き方**

```python
# test_solution.py
import tempfile
import os
from solution import filter_lines_by_prefix

def test_filter_lines_by_prefix():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = os.path.join(tmpdir, "src.txt")
        dst = os.path.join(tmpdir, "dst.txt")
        with open(src, "w") as f:
            f.write("INFO: start\nDEBUG: detail\nINFO: end\n")
        filter_lines_by_prefix(src, dst, "INFO")
        with open(dst, "r") as f:
            assert f.read() == "INFO: start\nINFO: end\n"
```

**解答例**

```python
# solution.py
def filter_lines_by_prefix(src, dst, prefix):
    with open(src, "r") as f_src, open(dst, "w") as f_dst:
        for line in f_src:
            if line.startswith(prefix):
                f_dst.write(line)
```

---

## 第10章：エラー処理と総合問題（Q93〜Q100）

---

### Q93. 安全な整数変換

**問題文**
`safe_int(s, default=0)` という関数を定義してください。文字列 `s` を整数に変換して返します。変換できない場合は `default` を返してください。`try/except` を使って実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import safe_int

def test_safe_int():
    assert safe_int("123") == 123
    assert safe_int("abc") == 0
    assert safe_int("abc", -1) == -1
    assert safe_int("12.3") == 0
```

**解答例**

```python
# solution.py
def safe_int(s, default=0):
    try:
        return int(s)
    except ValueError:
        return default
```

---

### Q94. リストの安全なアクセス

**問題文**
`safe_get(lst, index, default=None)` という関数を定義してください。リスト `lst` の `index` 番目の要素を返します。インデックスが範囲外の場合は `default` を返してください。`try/except` を使って実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import safe_get

def test_safe_get():
    assert safe_get([1, 2, 3], 1) == 2
    assert safe_get([1, 2, 3], 5) is None
    assert safe_get([1, 2, 3], -1, "out") == "out"
```

**解答例**

```python
# solution.py
def safe_get(lst, index, default=None):
    try:
        return lst[index]
    except IndexError:
        return default
```

---

### Q95. 辞書の安全なネストアクセス

**問題文**
`safe_nested_get(d, keys, default=None)` という関数を定義してください。辞書 `d` に対して、キーのリスト `keys` を順番に辿って値を取得します。どこかでキーが存在しなければ `default` を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import safe_nested_get

def test_safe_nested_get():
    d = {"a": {"b": {"c": 42}}}
    assert safe_nested_get(d, ["a", "b", "c"]) == 42
    assert safe_nested_get(d, ["a", "x", "c"]) is None
    assert safe_nested_get(d, ["a", "b", "c", "d"]) is None
```

**解答例**

```python
# solution.py
def safe_nested_get(d, keys, default=None):
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
```

---

### Q96. カスタム例外

**問題文**
`validate_positive(n)` という関数を定義してください。整数 `n` が正の数であればその値を返します。そうでなければ `ValueError` を発生させてください。エラーメッセージは `"Value must be positive, got <n>"` としてください。

**テストケースの書き方**

```python
# test_solution.py
import pytest
from solution import validate_positive

def test_validate_positive():
    assert validate_positive(5) == 5
    assert validate_positive(1) == 1

def test_validate_positive_error():
    with pytest.raises(ValueError, match="Value must be positive"):
        validate_positive(0)
    with pytest.raises(ValueError, match="Value must be positive"):
        validate_positive(-3)
```

**解答例**

```python
# solution.py
def validate_positive(n):
    if n <= 0:
        raise ValueError(f"Value must be positive, got {n}")
    return n
```

---

### Q97. コンテキストマネージャ風の実装

**問題文**
`managed_resource()` というジェネレータ関数を定義してください。以下のように使えるようにしてください。

```python
with contextlib.closing(managed_resource()) as res:
    res.do_something()
```

ただし、この問題では `managed_resource` が以下を満たすクラスをyieldするように実装してください。

- `open()` で `"opened"` を表示
- `close()` で `"closed"` を表示
- `do_something()` で `"doing something"` を返す

`yield` の前後で `open()` と `close()` を呼び出すジェネレータ関数を書いてください。

**テストケースの書き方**

```python
# test_solution.py
import contextlib
from solution import managed_resource

def test_managed_resource(capsys):
    with contextlib.closing(managed_resource()) as res:
        assert res.do_something() == "doing something"
    captured = capsys.readouterr()
    assert "opened" in captured.out
    assert "closed" in captured.out
```

**解答例**

```python
# solution.py
class Resource:
    def open(self):
        print("opened")
    def close(self):
        print("closed")
    def do_something(self):
        return "doing something"

def managed_resource():
    res = Resource()
    res.open()
    try:
        yield res
    finally:
        res.close()
```

---

### Q98. イテレータの実装

**問題文**
`Countdown` クラスを定義してください。初期値 `start` から `0` まで1つずつ減らすイテレータとして動作するクラスです。`for` 文で使えるようにしてください。

**テストケースの書き方**

```python
# test_solution.py
from solution import Countdown

def test_countdown():
    assert list(Countdown(3)) == [3, 2, 1, 0]
    assert list(Countdown(0)) == [0]
```

**解答例**

```python
# solution.py
class Countdown:
    def __init__(self, start):
        self.start = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.start < 0:
            raise StopIteration
        current = self.start
        self.start -= 1
        return current
```

---

### Q99. ジェネレータ式でフィボナッチ

**問題文**
`fibonacci_generator(limit)` という関数を定義してください。フィボナッチ数列の値を `limit` 個だけ順番に `yield` するジェネレータ関数として実装してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import fibonacci_generator

def test_fibonacci_generator():
    assert list(fibonacci_generator(1)) == [0]
    assert list(fibonacci_generator(5)) == [0, 1, 1, 2, 3]
    assert list(fibonacci_generator(10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**解答例**

```python
# solution.py
def fibonacci_generator(limit):
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b
```

---

### Q100. 総合：簡易電卓

**問題文**
`calculate(expression)` という関数を定義してください。文字列 `expression` は `"<整数> <演算子> <整数>"` の形式です。演算子は `+`, `-`, `*`, `//` のいずれかとします。計算結果を整数で返してください。0除算の場合は `"Division by zero"` という文字列を返してください。不正な演算子の場合は `"Invalid operator"` を返してください。

**テストケースの書き方**

```python
# test_solution.py
from solution import calculate

def test_calculate():
    assert calculate("3 + 5") == 8
    assert calculate("10 - 2") == 8
    assert calculate("4 * 7") == 28
    assert calculate("10 // 3") == 3
    assert calculate("10 // 0") == "Division by zero"
    assert calculate("10 ^ 2") == "Invalid operator"
```

**解答例**

```python
# solution.py
def calculate(expression):
    parts = expression.split()
    if len(parts) != 3:
        return "Invalid operator"
    a, op, b = int(parts[0]), parts[1], int(parts[2])
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "//":
        if b == 0:
            return "Division by zero"
        return a // b
    else:
        return "Invalid operator"
```

---

## おわりに

100問すべてにチャレンジしてみましょう。各問題でテストケースを自分で書く練習をすることで、

- 仕様を正確に読み取る力
- 境界値を考える力
- コードの動作を検証する力

が身につきます。解答例を見る前に、必ず自分で考えて実装してみてください。
