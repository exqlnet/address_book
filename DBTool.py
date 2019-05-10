import os
import copy


class User:

    def __init__(self, user_id, name, phone, remark):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.remark = remark

    def to_tuple(self):
        return self.user_id, self.name, self.phone, self.remark


class UserTool:

    users = []
    increment = "10000"

    def __init__(self):
        if os.path.exists("book.txt"):
            with open("book.txt", "r", encoding="utf-8") as file:
                for line in file.readlines():
                    user = User(*line.strip("\n").split(","))
                    self.increment = str(int(user.user_id) + 1)
                    self.users.append(user)

    def add(self, **kwargs):
        self.users.append(User(user_id=self.increment, **kwargs))
        self.increment = str(int(self.increment) + 1)
        self.save()

    def get_all(self):
        return self.users

    def get_by_id(self, user_id):
        """通信录编号获取用户"""
        for user in self.users:
            if user.user_id == str(user_id):
                return user
        return None

    def get_by_name(self, name):
        """姓名获取用户"""
        res_users = []
        for user in self.users:
            if user.name == name:
                res_users.append(user)
        return res_users

    def delete(self, user_id):
        for i in range(len(self.users)):
            if str(self.users[i].user_id) == str(user_id):
                self.users.pop(i)
                break
        self.save()

    def batch_delete(self, *user_ids):
        self.users = list(filter(lambda u: int(u.user_id) not in user_ids, self.users))
        self.save()

    def save(self):
        with open("book.txt", "w+", encoding="utf-8") as file:
            for user in self.users:
                file.write(",".join(user.to_tuple()) + "\n")

    def modify(self, user_id, **kwargs):
        for user in self.users:
            if user.user_id == str(user_id):
                for k, v in kwargs.items():
                    setattr(user, k, v)
                break
        self.save()
