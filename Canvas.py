import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

DISCORD_AUTH = os.getenv("DISCORD_AUTH")
CANVAS_API_KEY = os.getenv("CANVAS_API_KEY")

def send_message(mesg, channel):
    url = f'https://discord.com/api/v10/channels/{channel}/messages'
    payload = {
        "content": mesg
    }
    headers = {
        'Authorization': f"Bot {DISCORD_AUTH}",
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Message sent successfully to channel", channel)
    else:
        print("Failed to send message to channel", channel, ". Status code:", response.text)

def canvas_dlsu(class_code, channel):
    url = f"https://dlsu.instructure.com/api/v1/courses/{class_code}/discussion_topics?only_announcements=true"
    headers = {
        'Authorization': f'Bearer {CANVAS_API_KEY}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch Canvas announcements. Status code:", response.text)
        return

    posts = response.json()

    post_ids_file = "post_ids.txt"
    with open(post_ids_file, "r+") as f:
        post_ids = f.read().splitlines()

    for post in reversed(posts):
        if str(post['id']) not in post_ids:
            with open(post_ids_file, "a") as f:
                f.write(f"{post['id']}\n")

            clean_text = re.sub(r'<.*?>', '', post['message'])  # Remove all HTML tags
            urls = re.findall(r'https?://\S+', clean_text)

            message = f"```\nPost:\nID: {post['id']}\nTitle: {post['title']}\nMessage:\n{clean_text}\n```\nCanvas Link: https://dlsu.instructure.com/courses/{class_code}/discussion_topics/{post['id']}"
            if urls:
                message += f"\nLinks:\n{' '.join(urls)}"

            send_message(message, channel)

while True:
    canvas_dlsu(169360, 1235601784785997935)
    canvas_dlsu(169351, 1235601763198046270)
    canvas_dlsu(169489, 1235601808655646841)
    canvas_dlsu(169794, 1235601834756804669)
    canvas_dlsu(170148, 1235601860279271435)
    canvas_dlsu(170593, 1235601889714896896)
    canvas_dlsu(172878, 1235601911470751908)
    canvas_dlsu(173586, 1235601930567417866)
