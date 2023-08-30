from typing import List

import requests
import json
import asyncio


class MikogptAPI:
    """
    An object that allows you to make requests to the "mikogpt.ru" API by methods: `chat_completion`
    """

    def __init__(self, key, api_version=1):
        """
        Create new MikogptAPI Object

        :param key: private api key
        :param api_version: version of api (didn't require to change)
        """
        self._key = key
        self._api_version = api_version
        self._base_url = "http://api.mikogpt.ru"

    def _build_request_object(self, data):
        return {"key": self._key, "version": self._api_version, "data": data}

    @staticmethod
    def _from_chat_completion(response):
        txt = response.text
        jsonResponse = json.loads(txt)
        if jsonResponse["status"] != "Success":
            raise MikogptAPIResponseException(jsonResponse["status"])
        return jsonResponse

    async def chat_completion(self, messages: list[[str, str]], callback=lambda r: None):
        """
        Make chat completion request

        :param callback: Callback
        :param messages: A list of `[author, message]` objects pairs
        :return: MikogptAPIResponse object with response data
        :raise MikogptAPIResponse:
        """
        result = MikogptAPI._from_chat_completion(
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: requests.post(
                    self._base_url + "/chat",
                    json=self._build_request_object(messages)
                )
            )
        )
        callback(result)
        return result


class MikogptAPIResponseException(Exception):
    """
    Raises when api response with exception
    """
    def __init__(self, error_code):
        self.error_code = error_code
        super().__init__(f"MikogptAPI response with exception: \"{error_code}\"")


