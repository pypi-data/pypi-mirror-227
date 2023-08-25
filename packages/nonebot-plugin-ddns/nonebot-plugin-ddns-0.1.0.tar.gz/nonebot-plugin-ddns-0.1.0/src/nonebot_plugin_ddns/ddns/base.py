from abc import ABC, abstractmethod


class DDNS(ABC):

    @abstractmethod
    def _signature(self, *args, **kwargs):
        """
        获取签名
        """
        raise NotImplementedError

    @abstractmethod
    async def _request(self, *args, **kwargs):
        """
        发送请求
        """
        raise NotImplementedError

    @abstractmethod
    async def _create_record(self, *args, **kwargs):
        """
        创建
        """
        raise NotImplementedError

    @abstractmethod
    async def _modify_record(self, *args, **kwargs):
        """
        修改
        """
        raise NotImplementedError

    @abstractmethod
    async def _describe_record_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def ddns(self, *args, **kwargs):
        """
        运行
        """
        raise NotImplementedError
