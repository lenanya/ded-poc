import requests
from sys import argv

if len(argv) < 2:
    raise ValueError("Supply your discord token to run");

discord_token: str = argv[1]

discord_api_link: str = "https://discord.com/api/v10/"

current_channel: str|None = None;

command: str = "";

def send_message(message: str) -> bool:
    post_url: str = discord_api_link + f"channels/{current_channel}/messages"
    headers: dict = {"Authorization": discord_token}
    json_payload: dict = {"content": message}
    response = requests.post(url=post_url, headers=headers, json=json_payload)
    if response.status_code != 200:
        return False
    return True

def get_channel_messages() -> dict|None:
    get_url: str = discord_api_link + f"channels/{current_channel}/messages"
    headers: dict = {"Authorization": discord_token}
    response = requests.get(url=get_url, headers=headers)
    if response.status_code != 200:
        return None
    return response.json()

def print_messages(messages: dict) -> None:
    for m in messages[::-1]:
        author: dict|None = m.get("author")
        if not author:
            raise ValueError("Something went wrong...")
        username: str|None = author.get("username")
        if not username:
            raise ValueError("Something went wrong...")
        content: str|None = m.get("content")
        if not content:
            if not m.get("attachments"):
                raise ValueError("Something went wrong...")
            else:
                content = "{attachment}"
        print(f"{username}:")
        msg_parts: list[str] = [f"  {p}" for p in content.split("\n") if p]
        for p in msg_parts:
            print(p)

while True:
    command = input();
    if command == "c":
        current_channel = input();
    elif command == "m":
        if not current_channel:
            print("no channel");
            continue
        message: str = input();
        if len(message) > 1999:
            print("message cant be more than 1999 characters")
            continue
        if send_message(message) == False:
            raise ValueError("failed sending :(")
    elif command == "p":
        if not current_channel:
            print("no channel")
            continue
        messages: dict|None = get_channel_messages()
        if not messages:
            raise ValueError("failed getting messages :(")
        print_messages(messages)
    elif command == "q":
        break;
    else:
        print("?")        
        
