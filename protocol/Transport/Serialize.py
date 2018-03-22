import json

def serialize(data):
    return json.dumps(data)

def deserialize(string):
    return json.loads(string)

def encode(data):
    return data.encode('utf-8')

def decode(bytes):
    return bytes.decode('utf-8')