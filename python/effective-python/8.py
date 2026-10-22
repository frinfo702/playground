fresh_fruit = {"apple": 10, "banana": 8, "lemon": 5}


def out_of_stock():
    print("out of stock!")


def OutOfBananas(Exception):
    pass


def slice_bananas(count): ...


def make_cider(count): ...


def make_smoothies(count): ...


# countはif文の条件比較のみに用いるのでif文のスコープの中でのみ定義したい
# := を使うことでできる
if count := fresh_fruit.get("apple", 0) >= 0:
    print(count)
else:
    out_of_stock()

# 代入式を使ってswitch文相当を書ける
if count := fresh_fruit.get("banana", 0) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif count := fresh_fruit.get("apple", 0) >= 4:
    to_enjoy = make_smoothies(count)
elif count := fresh_fruit.get("lemon", 0):
    to_enjoy = make_smoothies(count)
else:
    to_enjoy = "nothing"

# 新しい果物が追加されるたび、果物がなくなるまでジュースをボトル詰めする


def pick_fruit(): ...


def make_juice(fruit, count): ...


bottles = []
fresh_fruit = pick_fruit()  # first
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()  # second

# 代入式を使うと
bottles = []
while fresh_fruit := pick_fruit():  # only once
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
