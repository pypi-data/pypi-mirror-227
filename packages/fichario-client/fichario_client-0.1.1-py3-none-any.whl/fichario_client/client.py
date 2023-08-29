import requests

import asyncio
import httpx

import json



class FicharioClient:
    _BASEURL: str = "https://api.roncloud.dev/"

    def __init__(self, email:str, password:str) -> None:
        self.USER_CREDENTIALS: dict = {email: email, password: password}
        self._JWT: str = None
        self._login(email=email, password=password)

    def _login(self, email:str, password:str):
        configs={
            'login':email,
            'password':password
        }
        try:
            request = requests.post(self._BASEURL + 'auth',json=configs)
            response = request.json()
            if (request.status_code == 200 or request.status_code == 201) and ('token' in response):
                self._JWT = response['token']
                return True
            else:
                return False
        except Exception as error:
            raise error

    def _make_request(self, path: str, http_method: str = 'GET'):
        if self._JWT is None:
            self._login(email=self.USER_CREDENTIALS.email, password=self.USER_CREDENTIALS.password)
            # return False
        head={'Authorization':'Bearer '+ self._JWT}
        try:
            if(http_method=='GET'):
                request = requests.get(self._BASEURL + path, headers=head)
                response = request.json()
                print(">> ", request.status_code)
                if (request.status_code == 200 or request.status_code == 201):
                    return response
                else:
                    return False
            else:
                return False
        except Exception as error:
            raise error

    def get_user_credentials(self):
        try:
            response = self._make_request(path='users/me', http_method='GET')
            return response
        except Exception as error:
            raise error


    def get_my_company(self):
        """
        Retrieve a list of companies.

        Returns:
            list: A list of companies in JSON format if successful, False otherwise.
        """
        try:
            response = self._make_request(path='companies/myCompany', http_method='GET')
            return response
        except Exception as error:
            raise error


    def list_my_devices(self):
        try:
            response = self._make_request(path='devices', http_method='GET')
            return response
        except Exception as error:
            raise error

    def get_device(self, deviceId:str = None):
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='devices/' + deviceId, http_method='GET')
            return response
        except Exception as error:
            raise error


    def get_payload(self, deviceId: str = None):
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='data/payloads/' + deviceId, http_method='GET')
            return response
        except Exception as error:
            raise error

    def get_device_info(self, deviceId: str = None):
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='data/deviceInfos/' + deviceId, http_method='GET')
            return response
        except Exception as error:
            raise error