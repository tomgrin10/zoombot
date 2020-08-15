# zoombot
Python wrapper for Zoom Chatbot API

### Usage
```python
from zoombot.core import Bot, Message


class MyBot(Bot):
    async def on_message(self, message: Message):
        await message.reply('Shlomo', "AAAAAAAAAAA")


if __name__ == "__main__":
    bot = MyBot(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        bot_jid="BOT_JID",
        verification_token="VERIFICATION_TOKEN",
    )

    bot.run()
```
