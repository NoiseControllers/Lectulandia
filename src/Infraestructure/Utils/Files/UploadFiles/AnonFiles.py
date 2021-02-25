import requests
import os
import json


class AnonFiles:
    def __init__(self):
        self._path = os.getcwd() + '\\temp\\'

    def upload(self, file_name):
        try:
            with open(self._path + file_name, 'rb') as f:
                r = requests.post('https://api.anonfile.com/upload', files={'file': f})
                data_json = json.loads(r.content)

                if data_json['status']:
                    return data_json['data']['file']['url']['short']
                else:
                    print('[-] El fichero no se ha podido subir.')
                    return None
        except FileNotFoundError:
            print(f'[-] El fichero "{file_name}" no existe.')

        return None
