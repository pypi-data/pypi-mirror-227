import binascii

import base64
import hashlib

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.PublicKey.RSA import RsaKey

from collections.abc import MutableMapping
from importlib.metadata import version
import ssl
from typing import Any, Iterable, Union, Optional, Dict

import requests
from urllib3.poolmanager import PoolManager  # type: ignore
from urllib3.util import ssl_

class __utils__:
    
    @staticmethod
    def bytes_to_int(bytes_seq: bytes) -> int:
        return int.from_bytes(bytes_seq, "big")
    
    @staticmethod
    def int_to_bytes(num: int, pad_multiple: int = 1) -> bytes:
        if num == 0:
            return b"\0" * pad_multiple
        if num < 0:
            raise ValueError("Can only convert non-negative numbers.")
        value = hex(num)[2:]
        value = value.rstrip("L")
        if len(value) & 1:
            value = "0" + value
        result = binascii.unhexlify(value)
        if pad_multiple not in [0, 1]:
            filled_so_far = len(result) % pad_multiple
            if filled_so_far != 0:
                result = b"\0" * (pad_multiple - filled_so_far) + result
        return result

class __google__:
    
    def key_from_b64(b64_key: bytes) -> RsaKey:
        """Extract key from base64."""
        binary_key = base64.b64decode(b64_key)

        i = __utils__.bytes_to_int(binary_key[:4])
        mod = __utils__.bytes_to_int(binary_key[4 : 4 + i])

        j = __utils__.bytes_to_int(binary_key[i + 4 : i + 4 + 4])
        exponent = __utils__.bytes_to_int(binary_key[i + 8 : i + 8 + j])

        key = RSA.construct((mod, exponent))

        return key


    def key_to_struct(key: RsaKey) -> bytes:
        """Convert key to struct."""
        mod = __utils__.int_to_bytes(key.n)
        exponent = __utils__.int_to_bytes(key.e)

        return b"\x00\x00\x00\x80" + mod + b"\x00\x00\x00\x03" + exponent


    def parse_auth_response(text: str) -> Dict[str, str]:
        """Parse received auth response."""
        response_data = {}
        for line in text.split("\n"):
            if not line:
                continue

            key, _, val = line.partition("=")
            response_data[key] = val

        return response_data


    def construct_signature(email: str, password: str, key: RsaKey) -> bytes:
        """Construct signature."""
        signature = bytearray(b"\x00")

        struct = __google__.key_to_struct(key)
        signature.extend(hashlib.sha1(struct).digest()[:4])

        cipher = PKCS1_OAEP.new(key)
        encrypted_login = cipher.encrypt((email + "\x00" + password).encode("utf-8"))

        signature.extend(encrypted_login)

        return base64.urlsafe_b64encode(signature)

class GAuth:
    
    def __init__(self) -> None:
        self.__B64_KEY_7_3_29__ = (
            b"AAAAgMom/1a/v0lblO2Ubrt60J2gcuXSljGFQXgcyZWveWLEwo6prwgi3"
            b"iJIZdodyhKZQrNWp5nKJ3srRXcUW+F1BD3baEVGcmEgqaLZUNBjm057pK"
            b"RI16kB0YppeGx5qIQ5QjKzsR8ETQbKLNWgRY0QRNVz34kMJR3P/LgHax/"
            b"6rmf5AAAAAwEAAQ=="
        )

        self.__ANDROID_KEY_7_3_29__ = __google__.key_from_b64(self.__B64_KEY_7_3_29__)

        self.__AUTH_URL__ = "https://android.clients.google.com/auth"
        self.__USER_AGENT__ = "GoogleAuth/1.4"
        
        self.__CIPHERS__ = [
            "ECDHE+AESGCM",
            "ECDHE+CHACHA20",
            "DHE+AESGCM",
            "DHE+CHACHA20",
            "ECDH+AES",
            "DH+AES",
            "RSA+AESGCM",
            "RSA+AES",
            "!aNULL",
            "!eNULL",
            "!MD5",
            "!DSS",
        ]

    class SSLContext(ssl.SSLContext):

        def set_alpn_protocols(self, alpn_protocols: Iterable[str]) -> None:
            """
            ALPN headers cause Google to return 403 Bad Authentication.
            """


    class AuthHTTPAdapter(requests.adapters.HTTPAdapter):

        def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
            context = GAuth.SSLContext()
            context.set_ciphers(ssl_.DEFAULT_CIPHERS)
            context.verify_mode = ssl.CERT_REQUIRED
            context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
            self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)


    def _perform_auth_request(self, data: dict, proxies: Optional[MutableMapping[str, str]] = None) -> Dict[str, str]:
        session = requests.session()
        session.mount(self.__AUTH_URL__, GAuth.AuthHTTPAdapter())
        if proxies:
            session.proxies = proxies
        session.headers = {
            "User-Agent": self.__USER_AGENT__,
            "Content-type": "application/x-www-form-urlencoded",
        }

        res = session.post(self.__AUTH_URL__, data=data, verify=True)

        return __google__.parse_auth_response(res.text)

    def Login(
        self,
        email: str,
        password: str,
        android_id: str,
        service: str = "ac2dm",
        device_country: str = "us",
        operator_country: str = "us",
        lang: str = "en",
        sdk_version: int = 17,
        proxy: Optional[MutableMapping[str, str]] = None,
        client_sig: str = "38918a453d07199354f8b19af05ec6562ced5788",
    ) -> Dict[str, str]:
        """
        Perform a master login, which is what Android does when you first add
        a Google account.
        Return a dict, eg::
            {
                'Auth': '...',
                'Email': 'email@gmail.com',
                'GooglePlusUpgrade': '1',
                'LSID': '...',
                'PicasaUser': 'My Name',
                'RopRevision': '1',
                'RopText': ' ',
                'SID': '...',
                'Token': 'oauth2rt_1/...',
                'firstName': 'My',
                'lastName': 'Name',
                'services': 'hist,mail,googleme,...'
            }
        """

        data: dict = {
            "accountType": "HOSTED_OR_GOOGLE",
            "Email": email,
            "has_permission": 1,
            "add_account": 1,
            "EncryptedPasswd": __google__.construct_signature(
                email, password, self.__ANDROID_KEY_7_3_29__
            ),
            "service": service,
            "source": "android",
            "androidId": android_id,
            "device_country": device_country,
            "operatorCountry": operator_country,
            "lang": lang,
            "sdk_version": sdk_version,
            "client_sig": client_sig,
            "callerSig": client_sig,
            "droidguard_results": "dummy123",
        }

        return self._perform_auth_request(data, proxy)
    
    def oAuth(
        self,
        email: str,
        master_token: str,
        android_id: str,
        service: str,
        app: str,
        client_sig: str,
        device_country: str = "us",
        operator_country: str = "us",
        lang: str = "en",
        sdk_version: int = 17,
        proxy: Optional[MutableMapping[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Use a master token from master_login to perform OAuth to a specific Google service.

        Return a dict, eg::

            {
                'Auth': '...',
                'LSID': '...',
                'SID': '..',
                'issueAdvice': 'auto',
                'services': 'hist,mail,googleme,...'
            }

        To authenticate requests to this service, include a header
        ``Authorization: GoogleLogin auth=res['Auth']``.
        """

        data: dict = {
            "accountType": "HOSTED_OR_GOOGLE",
            "Email": email,
            "has_permission": 1,
            "EncryptedPasswd": master_token,
            "service": service,
            "source": "android",
            "androidId": android_id,
            "app": app,
            "client_sig": client_sig,
            "device_country": device_country,
            "operatorCountry": operator_country,
            "lang": lang,
            "sdk_version": sdk_version,
        }

        return self._perform_auth_request(data, proxy)
    
    def verifyAssertion(self, token: str, app: str, Cert: str, Key: str) -> Dict[str, str]:
        URL     = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyAssertion?key={Key}'
        HEADERS = {
            'Content-Type': 'application/json',
            'X-Android-Package': app,
            'X-Android-Cert': Cert.upper(),
            'Accept-Language': 'in-ID, en-US',
            'X-Client-Version': 'Android/Fallback/X22001000/FirebaseCore-Android'
        }
        return requests.post(URL, json={"autoCreate":True,"returnSecureToken":True,"postBody":f"id_token={token}&providerId=google.com","requestUri":"http://localhost","returnIdpCredential":True}, headers=HEADERS).json()
    
    def getAccountInfo(self, idToken: str, app: str, Cert: str, Key: str):
        URL     = f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={Key}'
        HEADERS = {
            'Content-Type': 'application/json',
            'X-Android-Package': app,
            'X-Android-Cert': Cert.upper(),
            'Accept-Language': 'in-ID, en-US',
            'X-Client-Version': 'Android/Fallback/X22001000/FirebaseCore-Android'
        }
        return requests.post(URL, json={"idToken":idToken}, headers=HEADERS).json()
    
