# PyCrypto-based authenticated symetric encryption
import cPickle as pickle
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Util.randpool import RandomPool

AES_BLOCK_SIZE = 16
SIG_SIZE = hashlib.sha256().digest_size

class AuthenticationError(Exception): pass

class Crypticle(object):
    """Authenticated encryption class
    
    Encryption algorithm: AES-CBC
    Signing algorithm: HMAC-SHA256
    """

    PICKLE_PAD = "pickle::"

    def __init__(self, key_string, key_size=256):
        self.keys = self.extract_keys(key_string, key_size)
        self.key_size = key_size

    @classmethod
    def generate_key_string(cls, key_size=256):
        key = RandomPool(512).get_bytes(key_size / 8 + SIG_SIZE)
        return key.encode("base64").replace("\n", "")

    @classmethod
    def extract_keys(cls, key_string, key_size):
        key = key_string.decode("base64")
        assert len(key) == key_size / 8 + SIG_SIZE, "invalid key"
        return key[:-SIG_SIZE], key[-SIG_SIZE:]

    def encrypt(self, data):
        """encrypt data with AES-CBC and sign it with HMAC-SHA256"""
        aes_key, hmac_key = self.keys
        pad = AES_BLOCK_SIZE - len(data) % AES_BLOCK_SIZE
        data = data + pad * chr(pad)
        iv_bytes = RandomPool(512).get_bytes(AES_BLOCK_SIZE)
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = iv_bytes + cypher.encrypt(data)
        sig = hmac.new(hmac_key, data, hashlib.sha256).digest()
        return data + sig

    def decrypt(self, data):
        """verify HMAC-SHA256 signature and decrypt data with AES-CBC"""
        aes_key, hmac_key = self.keys
        sig = data[-SIG_SIZE:]
        data = data[:-SIG_SIZE]
        if hmac.new(hmac_key, data, hashlib.sha256).digest() != sig:
            raise AuthenticationError("message authentication failed")
        iv_bytes = data[:AES_BLOCK_SIZE]
        data = data[AES_BLOCK_SIZE:]
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = cypher.decrypt(data)
        return data[:-ord(data[-1])]

    def dumps(self, obj, pickler=pickle):
        """pickle and encrypt a python object"""
        return self.encrypt(self.PICKLE_PAD + pickler.dumps(obj))

    def loads(self, data, pickler=pickle):
        """decrypt and unpickle a python object"""
        data = self.decrypt(data)
        # simple integrity check to verify that we got meaningful data
        assert data.startswith(self.PICKLE_PAD), "unexpected header"
        return pickler.loads(data[len(self.PICKLE_PAD):])
