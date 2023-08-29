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

    def _make_request(self, path: str, http_method: str = 'GET', query: str = None, body: dict = None):
        if self._JWT is None:
            self._login(email=self.USER_CREDENTIALS.email, password=self.USER_CREDENTIALS.password)
            # return False
        head={'Authorization':'Bearer '+ self._JWT}
        try:
            destiny = self._BASEURL + path if query == None or query =='?' else self._BASEURL + path + query
            if(http_method=='GET'):
                request = requests.get(destiny, headers=head)
                response = request.json()
                # print("PATH >> ", path)
                # print(">> ", request.status_code)
                # print(">> ", response)
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


    def get_payload(self, deviceId: str = None, get_all: bool = False, str_date: str = None, end_date: str = None ):
        '''

        :param deviceId: Device ID
        :param get_all: If TRUE return all the data from the current device. If FALSE return the last 1000 reads.
        :param str_date: Filter the data to start listing from the respective date
        :param end_date: Filter the data to end listing from the respective date
        :return: Return List os collected data from the device.
        '''
        if deviceId is None:
            return False
        try:
            query = '?'
            if get_all:
                query= query + 'complete=true&'
            if str_date != None:
                query= query + f'strDate={str_date}&'
            if end_date != None:
                query= query + f'endDate={end_date}&'

            response = self._make_request(path='data/payloads/' + deviceId, http_method='GET', query=query)
            return response
        except Exception as error:
            raise error
    def get_raw_payload(self, deviceId: str = None):
        '''

        :param deviceId: Device ID
        :return: Return RAW List of collected data from the device.
        '''
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='data/' + deviceId, http_method='GET')
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

    def get_device_alarms(self, deviceId:str = None):
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='devices/' + deviceId + '/alarms', http_method='GET')
            return response
        except Exception as error:
            raise error

    def get_device_alarms_history(self, deviceId:str = None):
        if deviceId is None:
            return False
        try:
            response = self._make_request(path='devices/' + deviceId + '/alarms/history', http_method='GET')
            return response
        except Exception as error:
            raise error
