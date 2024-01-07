import random

def generate_token():
    return "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(50)])

def user_is_owner(user1, user2):
    return user1.id == user2.id