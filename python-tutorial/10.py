import os

print(os.getcwd())  # current directory
os.chdir("6")
print(os.getcwd())
os.system("mkdir today")  # run the command mkdir in the system shell
os.chdir("..")
print(os.getcwd())


print(dir(os))  # osモジュールの関数全てのリストを返す
# print(help(os))  # docstringから生成された詳細なマニュアルを返す

# print(shutil.copyfile("data.db", "archive.db"))
# print(shutil.move("./build/executables/", "installdir"))

# UNIXにおけるファイルを一気に展開する処理をglobという
# pythonではワイルドカード付きパターンでファイル名をまとめて拾う機能
import glob
import shutil

print(glob.glob("*.py"))

import sys

print(sys.argv)

import argparse

parser = argparse.ArgumentParser(
    prog="top", description="Show top lines from each file"
)
parser.add_argument("filenames", nargs="+")
