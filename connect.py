import requests
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def login_and_get_token():
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    payload = {"identifier": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Login successful!")
        return response.json().get("accessJwt")
    else:
        print("Login failed:", response.status_code, response.text)
        return None

def get_user_posts(user_id, token):
    url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={user_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        posts = response.json().get('feed', [])
        post_contents = [post.get('post', {}).get('record', {}).get('text', 'No content') for post in posts]
        print("User Posts:", post_contents)
    else:
        print("Failed to get user posts:", response.status_code, response.text)

def get_user_comments(user_id, token):
    url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={user_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        posts = response.json().get('feed', [])
        comment_contents = [
            post.get('post', {}).get('record', {}).get('text', 'No content')
            for post in posts if post.get('post', {}).get('record', {}).get('$type') == 'app.bsky.feed.post'
        ]
        print("User Comments:", comment_contents)
    else:
        print("Failed to get user comments:", response.status_code, response.text)

def main():
    token = login_and_get_token()
    if not token:
        return

    user_id = USERNAME

    print("\nUser Posts Content:")
    get_user_posts(user_id, token)

    print("\nUser Comments Content:")
    get_user_comments(user_id, token)

if __name__ == '__main__':
    main()
