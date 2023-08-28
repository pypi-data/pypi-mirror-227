# protection.py

import os
from typing import Optional
import base64

from attrs import define

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from represent import represent

__all__ = [
    "Cryptographer",
    "encrypt",
    "decrypt"
]

@define(repr=False)
@represent
class Cryptographer:
    """A class for cryptography encryption and decryption of data."""

    key: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    data: Optional[bytes] = None

    def _validate_key(self, key: Optional[str] = None) -> str:
        """
        Defines the attribute's value.

        :param key: The string to convert to a valid key.

        :return: The string to convert to a valid key.
        """

        if (key, self.key) == (None, None):
            raise ValueError(f"A key must be defined.")

        elif key is None:
            key = self.key

        elif self.key is None:
            self.key = key
        # end if

        return key
    # end _validate_key

    def _validate_source(self, source: Optional[str] = None) -> str:
        """
        Defines the attribute's value.

        :param source: The source file.

        :return: The source file.
        """

        if source is None:
            source = self.source

        elif self.source is None:
            self.source = source
        # end if

        return source
    # end _validate_source

    def _validate_destination(self, destination: Optional[str] = None) -> str:
        """
        Defines the attribute's value.

        :param destination: The destination file.

        :return: The destination file.
        """

        if destination is None:
            destination = self.destination

        elif self.destination is None:
            self.destination = destination
        # end if

        return destination
    # end _validate_destination

    def _validate_data(self, data: Optional[bytes] = None) -> bytes:
        """
        Defines the attribute's value.

        :param data: The data to process.

        :return: The data to process.
        """

        if data is None:
            data = self.data

        elif self.data is None:
            self.data = data
        # end if

        return data
    # end _validate_data

    def digest_key(self, key: Optional[str] = None) -> bytes:
        """
        Digests the key to a valid hashing key.

        :param key: The string to convert to a valid key.

        :return: A valid url safe 64-bit hash key.
        """

        key = self._validate_key(key)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32,
            salt=b'9\x89\nt\x9d\xf6E\xb70B\x93s\xc7@[)',
            iterations=1000, backend=default_backend()
        )

        return base64.urlsafe_b64encode(kdf.derive(key.encode()))
    # end __digest_key

    def encrypt(
            self,
            key: str,
            source: Optional[str] = None,
            destination: Optional[str] = None,
            data: Optional[bytes] = None
    ) -> bytes:
        """
        Encrypts the data with an encryption key.

        :param data: The data to encrypt.
        :param key: The encryption key.
        :param source: The data source file.
        :param destination: The encrypted data destination file.

        :return: The encrypted data.
        """

        source = self._validate_source(source)
        destination = self._validate_destination(destination)
        data = self._validate_data(data)

        if (data, source) == (None, None):
            raise ValueError(
                "Both 'data' and 'source' parameters were not given, "
                "while at least one must be. When both are, "
                "the 'source' parameter will be disregarded."
            )
        # end if

        if data is None:
            with open(source, 'rb') as file:
                data = file.read()
            # end open
        # end if

        encrypted_key = self.digest_key(key)

        fernet = Fernet(encrypted_key)

        encrypted_data = fernet.encrypt(data)

        if destination is not None:
            if location := os.path.split(destination)[0]:
                os.makedirs(location, exist_ok=True)
            # end if

            with open(destination, 'wb') as file:
                file.write(encrypted_data)
            # end open
        # end if

        return encrypted_data
    # end encrypt

    def decrypt(
            self,
            key: str,
            data: Optional[bytes] = None,
            source: Optional[str] = None,
            destination: Optional[str] = None
    ) -> bytes:
        """
        Decrypts the data with a decryption key.

        :param data: The data to encrypt.
        :param key: The decryption key.
        :param source: The data source file.
        :param destination: The decrypted data destination file.

        :return: The decrypted data.
        """

        source = self._validate_source(source)
        destination = self._validate_destination(destination)
        data = self._validate_data(data)

        if (data, source) == (None, None):
            raise ValueError(
                "Both 'data' and 'source' parameters were not given, "
                "while at least one must be. When both are, "
                "the 'source' parameter will be disregarded."
            )
        # end if

        if data is None:
            with open(source, 'rb') as file:
                data = file.read()
            # end open
        # end if

        encrypted_key = self.digest_key(key)

        fernet = Fernet(encrypted_key)

        decrypted_data = fernet.decrypt(data)

        if destination is not None:
            if location := os.path.split(destination)[0]:
                os.makedirs(location, exist_ok=True)
            # end if

            with open(destination, 'wb') as file:
                file.write(decrypted_data)
            # end open
        # end if

        return decrypted_data
    # end decrypt
# end Cryptographer

def encrypt(
        key: str,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        data: Optional[bytes] = None
) -> bytes:
    """
    Encrypts the data with an encryption key.

    :param data: The data to encrypt.
    :param key: The encryption key.
    :param source: The data source file.
    :param destination: The encrypted data destination file.

    :return: The encrypted data.
    """

    return Cryptographer().encrypt(
        key=key, data=data, source=source,
        destination=destination
    )
# end encrypt

def decrypt(
        key: str,
        data: Optional[bytes] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None
) -> bytes:
    """
    Decrypts the data with a decryption key.

    :param data: The data to encrypt.
    :param key: The decryption key.
    :param source: The data source file.
    :param destination: The decrypted data destination file.

    :return: The decrypted data.
    """

    return Cryptographer().decrypt(
        key=key, data=data, source=source,
        destination=destination
    )
# end decrypt