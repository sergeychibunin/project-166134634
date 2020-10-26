import time
from typing import Dict
import configparser
from rest_framework.test import RequestsClient


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
    client = RequestsClient()
    client.post(f'{cfg_srv()}/api/user/signup', json=user)


def add_users(amount: int) -> None:
    """
    Generate and sign up a specified amount of users
    """
    for number in amount:
        user = rand_user(number)
        signup(user)


def main() -> None:
    config = configparser.ConfigParser()
    config.read('bot.ini')
    cfg_srv_init(config['network'])
    add_users(int(config['behavior']['number_of_users']))
    write_posts(config['behavior']['max_posts_per_user'])
    add_likes(config['behavior']['max_likes_per_user'])


if __name__ == "__main__":
    main()
