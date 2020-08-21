# zoombot

[![PyPI](https://img.shields.io/pypi/v/zoombot)](https://pypi.org/project/zoombot/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoombot)](https://pypi.org/project/zoombot/)
[![PyPI License](https://img.shields.io/pypi/l/zoombot)](https://pypi.org/project/zoombot/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)

Python wrapper for Zoom Chatbot API

### Usage
```python
from zoombot.core import Bot, Message


class MyBot(Bot):
    async def on_message(self, message: Message):
        await message.reply("Hello", f"You sent {message.content}")


if __name__ == "__main__":
    bot = MyBot(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        bot_jid="BOT_JID",
        verification_token="VERIFICATION_TOKEN",
    )

    bot.run()
```
