from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand, JoinedEvent
import asyncio
import json
from datetime import datetime, timedelta

def main(config):
    """
    Pull relevent values from config file, and initialize the Twitch bot.
    """
    CHANNELS = [config["twitch_channel_name"]]  # List (of type list) of channels to join
    APP_ID = config["twitch_app_id"]
    APP_SECRET = config["twitch_app_secret"]
    USER_SCOPE = [AuthScope.CHAT_READ]
    last_message_time = None  # Initialize state for tracking messages
    cooldown_period = timedelta(seconds=config["twitch_command_cooldown"])

    async def on_ready(ready_event: EventData):
        """
        Join Twitch channel(s), or fail with error.
        """
        # TODO handle with logging module
        print(f'Bot joining twitch channels: {config["twitch_channel_name"]}')
        failed_channels = await ready_event.chat.join_room(*CHANNELS)
        for channel in failed_channels:
            print(f'Unable to join {channel}. Reason: Bad Request')

    async def on_message(msg: ChatMessage):
        """
        Detects keywords in chat messages and changes the pngtuber model state accordingly
        """
        nonlocal last_message_time
        if "beer" in msg.text.lower():
            # TODO handle with logging module
            print(f"Beer detected in message: {msg.text}")
            last_message_time = datetime.now()
        elif "pizza" in msg.text.lower():
            # TODO handle with logging module
            print(f"Pizza detected in message: {msg.text}")
            last_message_time = datetime.now()

    async def run():
        twitch = await Twitch(APP_ID, APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

        chat = await Chat(twitch)
        chat.register_event(ChatEvent.READY, on_ready)
        chat.register_event(ChatEvent.MESSAGE, on_message)
        chat.start()

        try:
            await asyncio.sleep(999999)  # Keep the event loop running
        finally:
            chat.stop()
            await twitch.close()

    asyncio.run(run())  # Run the asyncio loop within main

if __name__ == '__main__':
    # load config file from current working directory
    with open("config.json", "r") as file:
        config = json.load(file)

    main(config)
