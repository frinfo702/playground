year = 2016
event = "poll"
print(f"{year}'s {event}")

yes_votes = 42_572_654
total_votes = 85_705_149
percentage = yes_votes / total_votes
print("{:-9} yes. {:2.2}".format(yes_votes, percentage))

import math

text = f"πの値は大体{math.pi:.3f}です"
print(text)

table = {"Sjoerd": 4127, "Jack": 4098, "Dcab": 7678}
for name, phone in table.items():
    print(f"{name:10} ==> {phone:10}")


animals = "うなぎ"
print(f"私のホバークラフトは{animals}でいっぱいです")
print(f"私のホバークラフトは{animals!r}でいっぱいです")

print('We are the {} who say "{}!"'.format("knights", "Ni"))
print("{0} and {1}".format("spam", "eggs"))
print(
    "This {food} is {adjective}.".format(food="spam", adjective="absolutely horrible")
)


table = {"Sjoerd": 4127, "Jack": 4098, "Dcab": 7678}
print("Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; Dcab: {0[Dcab]:d}".format(table))

# **は辞書をキーワード引数の集まりに展開する
# format(Jack=4098, Sjoerd=4127, Dcab=8637678)
print("Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}".format(**table))

table = {k: str(v) for k, v in vars().items()}
message = " ".join([f"{k}: " + "{" + k + "};" for k in table.keys()])
print(message.format(**table))

for x in range(20):
    print("{0:2d} {1:3d} {2:4d}".format(x, x**2, x**3))

for x in range(1, 11):
    # rjustは右寄せ
    print(repr(x).rjust(2), repr(x * x).rjust(3), end=" ")
    print(repr(x**3).rjust(4))

print("12".zfill(5))  # 00012

# withを使うことを癖づける。自動でcloseをしてくれる
with open("6.py", encoding="utf-8") as f:
    read_data = f.read()

print(f.closed)  # closeされているかを確認

with open("workfile.txt", encoding="utf-8") as f:
    print(f.read())  # file全文を読み出す
    print("-----------------------")
    print(f.read())

with open("workfile.txt") as f:
    print(f.readline())  # 1行だけを読み取る
    print("-----------------------")
    print(f.readline())

with open("workfile.txt", "r+") as f:
    f.write("This is a test line \n")
    for line in f:
        print(line, end="")

f = open("workfile.txt", "rb+")
print(f.write(b"0123456789abcdef"))
print(f.seek(5))  # ファイル内の6番目のバイトまで移動
print(f.read(1))
print(f.seek(-3, 2))  # 末尾から3番目のバイトに移動
print(f.read(1))

import json

x = [1, "simple", "list"]
print(json.dumps(x))

f = open("workfile.txt", "r+")
print(json.dump(x, f))
x = json.load(f)
print(x)
f.close()
