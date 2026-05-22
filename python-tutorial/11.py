# 大きなコンテナや深くネストしたコンテナを省略して表示するバージョンを提供
import reprlib
from typing import override

print(reprlib.repr(set("supercalifragilisticexpialidocious")))

# 組込み型やユーザ定義型をわかりやすく表示するための洗練された制御手段を提供
import pprint

t = [[[["black", "cyan"], "white", ["green", "red"]], [["magenta", "yellow"], "blue"]]]

pprint.pprint(t, width=30)


import textwrap

doc = """The wrap() method is just like fill() except that it returns
a list of strings instead of one big string with newlines to separate
the wrapped lines."""

print(textwrap.fill(doc, width=40))
# The wrap() method is just like fill()
# except that it returns a list of strings
# instead of one big string with newlines
# to separate the wrapped lines.

import locale

print(locale.setlocale(locale.LC_ALL, "de_DE.UTF-8"))
conv = locale.localeconv()  # get a mapping of conventions
x = 1234567.8
print(locale.format_string("%d", x, grouping=True))
print(
    locale.format_string(
        "%s%.*f", (conv["currency_symbol"], conv["frac_digits"], x), grouping=True
    )
)

from string import Template

t = Template("${village}folk send $$10 to $cause.")
print(t.substitute(village="Nottingham", cause="the ditch fund"))

t = Template("Return the $item to $owner.")
# d = dict(item="unladen swallow") KeyErrorになる
d = dict(item="unladen swallow", owner="owner")
print(t.substitute(d))

import os.path
import time

photofiles = ["img_1074.jpg", "img_1076.jpg", "img_1077.jpg"]


class BatchRename(Template):
    delimiter = "%"


# fmt = input("Enter rename style (%d-date %n-seqnum %f-format):  ")
fmt = "Ashley_%n%f"

t = BatchRename(fmt)
date = time.strftime("%d%b%y")
for i, filename in enumerate(photofiles):
    base, ext = os.path.splitext(filename)
    newname = t.substitute(d=date, n=i, f=ext)
    print(f"{filename} --> {newname}")

########################


import logging

logging.debug("Debugging information")
logging.info("Informational message")
logging.warning("Warning:config file %s not found", "server.conf")
logging.error("Error occured")
logging.critical("Critical error -- shutting down")

###############

# 弱参照を作れる
# 作成コストの大きいオブジェクトのキャッシュ時など
import gc
import weakref


class A:
    def __init__(self, value):
        self.value = value

    @override
    def __repr__(self) -> str:
        return str(self.value)


a = A(10)  # create a reference
d = weakref.WeakValueDictionary()
d["primary"] = a  # does not create a reference
print(d["primary"])  # fetch the object if it is still alive

del a  # remove the one reference
print(gc.collect())  # run garbage collection right away
try:
    print(d["primary"])
except KeyError:
    print("entry was automatically removed")

#########################
# array module は同種のデータのみを格納する

from array import array

a = array("H", [4000, 10, 700, 22222])  # type code: "H"の配列
print(sum(a))  # 26392

print(a[1:])

#########################
from collections import deque

d = deque(["task1", "task2", "task3"])
d.append("task4")
print("Hndling", d.popleft())

import bisect

scores = [(100, "perl"), (200, "tcl"), (400, "lua"), (500, "python")]
bisect.insort(scores, (300, "ruby"))
print(scores)

# 常に小さい値が先頭に来る
from heapq import heapify, heappop, heappush

data = [1, 3, 4, 7, 9, 2, 4, 6, 8, 0]
heapify(data)  # list into heap
heappush(data, -5)
print([heappop(data) for _ in range(3)])

#########################
# 手で計算した場合の結果と同じになる
# 浮動小数点計算による意図しない丸めなどを回避できる
from decimal import *

print(Decimal("1.00") % Decimal(".10"))
print(1.00 % 0.10)

print(sum([Decimal("0.1")] * 10) == Decimal("1.0"))
print(0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 == 1.0)
