
users = [
    ("10001", "李四", "13212151258", "朋友"),
    ("10002", "张三", "13212151259", "基友")
]

with open("book.txt", "w", encoding="utf-8") as file:
    for user in users:
        file.write(",".join(user) + "\n")
