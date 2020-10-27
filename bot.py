import time
import random
from typing import Dict, List
import configparser
import requests
import string


def rnd_word() -> str:
    """
    Make an undefined word
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(4))


def rnd_text() -> str:
    """
    Make a random text
    """
    return ' '.join(rnd_word() for _ in range(8))


class BreakExc(Exception):
    ...


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Store:
    srv_uri: str  # the server URI
    users: List[Dict] = []  # a container with usernames and passwords
    posts: List[int] = []  # a container with post's identifiers


store = Store()


def cfg_srv_init(cfg: configparser.SectionProxy) -> None:
    """
    Save the server URI
    """
    store.srv_uri = f'http://{cfg["server_host"]}:{cfg["server_port"]}'


def rand_user() -> Dict[str, str]:
    """
    Make a couple of a random username and a random password
    """
    return {
        'username': f'user{str(int(time.time()))}',
        'password': str(int(time.time()))}


def signup(user: Dict[str, str]) -> None:
    """
    Sign up a new user
    """
    requests.post(f'{store.srv_uri}/api/user/signup', data=user)


def login(user_number: int) -> None:
    """
    Log in an user
    """
    user = store.users[user_number]
    response = requests.post(f'{store.srv_uri}/api/token/', data=user)
    store.users[user_number]['token'] = response.json()['access']


def add_users(amount: int) -> None:
    """
    Generate and sign up a specified amount of users
    """
    for _ in range(amount):
        user = rand_user()
        store.users.append(user)
        signup(user)
        print(f'Welcome {user["username"]}')


def write_posts(post_limit: int) -> None:
    """
    Generate random posts
    """
    for user_number in range(len(store.users)):
        login(user_number)
        for _ in range(random.randint(0, post_limit)):
            post_body = rnd_text()
            response = requests.post(
                f'{store.srv_uri}/api/post/', 
                data={'body': post_body},
                auth=BearerAuth(store.users[user_number]['token']))
            store.posts.append(response.json()['id'])
            print(f"User {store.users[user_number]} has posted \"{post_body}\"")


def add_likes(likes_limit: int) -> None:
    """
    Add likes to anywhere
    """
    for user_number in range(store.users):
        liked_posts = []
        try:
            for _ in range(random.randint(0, likes_limit)):
                post_id = random.choice(store.posts)
                while post_id in likes_limit:
                    post_id = random.choice(store.posts)
                    if len(store.posts) == len(liked_posts):
                        raise BreakExc()

                urls = (
                    ('/api/post/like', 'like'),
                    ('/api/post/dislike', 'dislike')
                )
                rnd_int = random.randint(0, 1)
                requests.post(
                    f"{store.srv_uri}{urls[rnd_int][0]}", 
                    data={'post_id': post_id},
                    auth=BearerAuth(store.users[user_number]['token']))
                liked_posts.append(post_id)
                print(f"User a {urls[rnd_int][1]} to the post ID {post_id}")
        except BreakExc:
            continue


def main() -> None:
    config = configparser.ConfigParser()
    config.read('bot.ini')
    cfg_srv_init(config['network'])
    add_users(int(config['behavior']['number_of_users']))
    write_posts(config['behavior']['max_posts_per_user'])
    add_likes(config['behavior']['max_likes_per_user'])


if __name__ == "__main__":
    main()
