from protocol.Transport.Serialize import decode, deserialize

class ServerResponse:
    def __init__(self, bytes):
        self.bytes = bytes
        self.dataframe = deserialize(decode(bytes))
        self.timestamp = self.dataframe['timestamp']
        self.status = self.dataframe['status']
        self.detail = self.dataframe['detail']
        self.data = self.dataframe['data']

class ClientResponse:
    def __init__(self, bytes):
        self.bytes = bytes
        self.dataframe = deserialize(decode(bytes))
        self.commands = self.dataframe['commands']
        self.token = self.dataframe['token']