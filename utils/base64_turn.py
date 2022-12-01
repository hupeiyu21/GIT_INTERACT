import base64

def str2base64str(sentence):
    return base64.b64encode(sentence.encode('utf8')).decode('utf8')

def base64str2str(b64str):
    return base64.b64decode(b64str).decode('utf8')