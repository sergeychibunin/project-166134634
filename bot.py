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


class Store:
    srv_uri: str
    users: List[Dict]


store = Store()


def cfg_srv_init(cfg: configparser.SectionProxy) -> None:
    """
    Save the server URI
    """
    store.srv_uri = f'http://{cfg["server_host"]}{cfg["server_port"]}'


def rand_user(number: int) -> Dict[str, str]:
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
    for number in amount:
        user = rand_user(number)
        store.users.append(user)
        signup(user)
        print(f'Welcome {user["username"]}')


def write_posts(post_limit: int) -> None:
    """
    Generate random posts
    """
    for user_number in range(len(store.users)):
        login(user_number)


def main() -> None:
    config = configparser.ConfigParser()
    config.read('bot.ini')
    cfg_srv_init(config['network'])
    add_users(int(config['behavior']['number_of_users']))
    # write_posts(config['behavior']['max_posts_per_user'])
    # add_likes(config['behavior']['max_likes_per_user'])


if __name__ == "__main__":
    main()
