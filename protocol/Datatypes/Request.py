import datetime
from protocol.Transport.Serialize import serialize, encode

class ClientCommands:
    def __init__(self):
        self.token = ''

    def _base_request(self, command, data):
        return encode(serialize({
            'token': self.token,
            'commands': {
                command: data
            }
        }))

    def login_req(self, username, password):
        data = {'username': username,
                'password': password}
        return self._base_request('login', data)

    def upload_req(self, filename, filesize):
        data = {'filename': filename,
                'filesize': filesize}
        return self._base_request('upload', data)

    def download_req(self, RID):
        return self._base_request('download', {'id': RID})

class ServerCommands:

    def _base_response(self, code, data, msg=''):
        return encode(serialize({
            'timestamp':int(datetime.datetime.utcnow().timestamp()),
            'status':code,
            'detail':msg,
            'data':data
        }))

    def unauthorized(self):
        return self._base_response(401, {}, msg='Unauthorized!')

    def internal_error(self):
        return self._base_response(500, {}, msg='Internal Server Error')

    def accepted(self):
        return self._base_response(202, {}, msg='Accepted!')

    def token(self, token, expired):
        data = {
            'token': token,
            'expired': expired
        }
        return self._base_response(200, data, 'Login success')

