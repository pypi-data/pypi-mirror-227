from httpx import AsyncClient
from pydantic import BaseModel, Field
from tencentcloud.common import credential
from .utlis import DnsPodClient, Record, get_domain
from .base import DDNS as BaseDDNS
from enum import Enum


class Action(str, Enum):
    CreateRecord = "CreateRecord"
    DescribeRecordList = "DescribeRecordList"
    ModifyRecord = "ModifyRecord"


class Params(BaseModel):
    Domain: str = Field(None)
    RecordType: Record = Field(None)
    RecordLine: str = Field(None)
    Value: str = Field(None)
    RecordId: int = Field(None)
    SubDomain: str = Field(None)


class DnsPod(BaseDDNS):
    # API 配置
    API = "dnspod.tencentcloudapi.com"  # API endpoint

    id = "AKID450vgP1YxCH9vX5VxHSTPGLLHC7MTRPw"
    secret = "Up03wgJqGVYPZdZKvPipkU4Th9Zs28GI"

    def __init__(self):
        ...

    async def _request(self, data, action: Action, *args, **kwargs):
        headers = self._signature(action, data)
        async with AsyncClient(base_url=f"https://{self.API}", headers=headers) as client:
            res = await client.post("/", json=data)

        return res.json()

    def _signature(self, action: Action, params, header=None, *args, **kwargs) -> dict:
        if header is None:
            header = {}
        cred = credential.Credential("AKID450vgP1YxCH9vX5VxHSTPGLLHC7MTRPw", "Up03wgJqGVYPZdZKvPipkU4Th9Zs28GI")
        c = DnsPodClient(cred, "")
        return c.call(action, params, header)

    async def _create_record(self, params: Params, *args, **kwargs):
        res = await self._request(data=params.dict(exclude_none=True), action=Action.CreateRecord)
        return res

    async def _modify_record(self, params: Params, *args, **kwargs):
        res = await self._request(data=params.dict(exclude_none=True), action=Action.ModifyRecord)
        return res

    async def _describe_record_list(self, domain: str, *args, **kwargs) -> list:
        res = await self._request({"Domain": domain}, action=Action.DescribeRecordList)
        print(res)
        return res.get("Response").get("RecordList")

    async def test(self, **kwargs):
        res = await self.ddns("test.alnthy.cn", Record.AAAA, "240e:380:b51c:9801:e1a7:3241:41d6:7cc")
        print(res)

    async def ddns(self, domain: str, record_type: Record, value: str, *args, **kwargs):
        params = Params(**{"Domain": domain, "RecordType": record_type, "Value": value})
        name, belongs_domain = get_domain(domain)
        params.Domain = belongs_domain
        params.SubDomain = "@" if name is None else name
        record_list = await self._describe_record_list(belongs_domain)
        for i in record_list:
            if name == i.get("Name"):
                params.RecordLine = "默认"
                params.RecordId = i.get("RecordId")
                if i.get("Value") == value:
                    return f"你的IP {value} 没有变化, 域名 {domain}"
                await self._modify_record(params)
                return f"更新域名解析 {domain} 成功！IP: {value}"
        else:
            params.RecordLine = "默认"
            await self._create_record(params)
            return f"更新域名解析 {domain} 成功！IP: {value}"
