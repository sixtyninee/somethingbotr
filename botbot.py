import os
import discord
import aiohttp
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


SERVER_ID = 1207148560970293328
MONITORED_CHANNEL_IDS = [1207148561427468309, 1234963404670898196]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if (
            message.guild and
            message.guild.id == SERVER_ID and
            message.channel.id in MONITORED_CHANNEL_IDS
        ):
        
            user_info = f"Message by ({message.author.id}) {message.author}"
            server_info = f"Server: ({message.guild.id}) {message.guild.name}"
            channel_info = f"Channel: ({message.channel.id}) {message.channel.name}"
            timestamp = f"Date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            if message.content:
                message_info = message.content
            elif message.attachments:
                attachment_urls = [attachment.url for attachment in message.attachments]
                message_info = message.content
            else:
                message_info = "[Unknown content type]"


            
            embed = {
                "title": "charmfoolious on top",
                "color": 3447003,  # Blue color
                "fields": [
                    {"name": "User", "value": user_info, "inline": False},
                    {"name": "Server", "value": server_info, "inline": False},
                    {"name": "Channel", "value": channel_info, "inline": False},
                    {"name": "Date and Time", "value": timestamp, "inline": False},
                ]
            }
            


            async with aiohttp.ClientSession() as session:
                payload = {
                    "embeds": [embed],
                    "content": message_info
                }
                async with session.post(WEBHOOK_URL, json=payload) as response:
                    if response.status != 204:  # 204 No Content is expected for success
                        print(f"Failed to send webhook: {response.status}")
                for attachment in message.attachments:
                    attachment_payload = {
                        "content": attachment.url  # Directly send the attachment URL in the content field
                    }
                    async with session.post(WEBHOOK_URL, json=attachment_payload) as response:
                        if response.status != 204:
                            print(f"Failed to send attachment: {response.status}")

client = MyClient()
client.run(DISCORD_TOKEN)
