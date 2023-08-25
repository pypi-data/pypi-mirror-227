from nonebot import on_command, get_app
from fastapi import FastAPI
from .ddns.dnspod import DnsPod, BaseDDNS
from .web import app as ddns_app

a = on_command("测试")
app: FastAPI = get_app()

app.mount("/ddns", ddns_app, name="ddns")


@a.handle()
async def _():
    c = DnsPod()
    data = {
        "Domain": "alnthy.cn",
    }
    await c.test(json=data)
