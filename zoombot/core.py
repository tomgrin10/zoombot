from __future__ import annotations

import base64
from pprint import pprint
from typing import Dict

import aiohttp
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse

from zoombot.utils import nullcontext


class Bot:
    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        bot_jid: str,
        verification_token: str,
        auth_route: str = "authorize",
        command_route: str = "",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bot_jid = bot_jid
        self.verification_token = verification_token
        self.auth_route = auth_route
        self.command_route = command_route

        self.api = Starlette()
        self._init_routes()

    def _init_routes(self):
        self.api.add_route(f"/{self.auth_route}", self._authorize, methods=["GET"])
        self.api.add_route(f"/{self.command_route}", self._message, methods=["POST"])

    async def _authorize(self, request: Request):
        return RedirectResponse(f"https://zoom.us/launch/chat?jid=robot_{self.bot_jid}")

    async def _message(self, request: Request):
        body = await request.json()
        message = Message.from_zoom_json(self, body)
        await self.on_message(message)

        return PlainTextResponse("ok")

    async def _get_chatbot_token(
        self, *, session: aiohttp.ClientSession() = None
    ) -> str:
        session = nullcontext(session) if session else aiohttp.ClientSession()

        url = "https://zoom.us/oauth/token?grant_type=client_credentials"
        secret = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {"Authorization": f"Basic {secret}"}
        async with session as session:
            async with session.post(url, headers=headers) as response:
                body = await response.json()
                return body["access_token"]

    async def send_chat_message(
        self, head: str = None, body: str = None, *, to_jid: str, account_id: str,
    ):
        async with aiohttp.ClientSession() as session:
            access_token = await self._get_chatbot_token(session=session)

            url = "https://api.zoom.us/v2/im/chat/messages"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            json_body = {
                "robot_jid": self.bot_jid,
                "to_jid": to_jid,
                "account_id": account_id,
                "content": {},
            }
            if head:
                json_body["content"]["head"] = {"text": head}
            if body:
                json_body["content"]["body"] = [{"type": "message", "text": body}]

            async with session.post(url, json=json_body, headers=headers) as response:
                pass

    async def on_message(self, message: Message):
        raise NotImplementedError()

    def run(self, *, host: str = "0.0.0.0", port: int = 3000):
        uvicorn.run(self.api, host=host, port=port)


class Message:
    def __init__(self, *, bot: Bot, to_jid: str, account_id: str, content: str):
        self.to_jid = to_jid
        self.account_id = account_id
        self.bot = bot
        self.content = content

    @classmethod
    def from_zoom_json(cls, bot: Bot, json: Dict):
        return cls(
            bot=bot,
            to_jid=json["payload"]["toJid"],
            account_id=json["payload"]["accountId"],
            content=json["payload"]["cmd"],
        )

    async def reply(self, head: str = None, body: str = None):
        await self.bot.send_chat_message(
            head=head, body=body, to_jid=self.to_jid, account_id=self.account_id
        )
