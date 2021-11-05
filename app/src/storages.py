import abc
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Optional

from cryptography.fernet import Fernet

from app import settings


@dataclass
class Secret:
    id: Optional[int]
    name: str
    extra: str
    password: str


class StorageManager(abc.ABC):
    db_name = 'secrets.db'

    def __init__(self):
        self._crypto = Fernet(settings.SECRET_KEY)

    def save_secret(self, secret: Secret):
        cyphers = (
            self._encrypt(text)
            for text in (secret.name, secret.extra, secret.password, )
        )

        return self._save(*cyphers)

    @abc.abstractmethod
    def remove_secret(self, secret_id: int): pass

    @abc.abstractmethod
    def get_secrets(self): pass

    def _encrypt(self, plain_text):
        return self._crypto.encrypt(
            bytes(plain_text.encode('utf-8'))
        )

    def _decrypt(self, encrypted_text):
        return self._crypto.decrypt(encrypted_text).decode()

    def _save(self, secret, encrypted_password) -> int:
        pass


class DBStorageManager(StorageManager):

    def __init__(self, provider):
        super().__init__()

        self._provider = provider
        self._init_db()

    @contextmanager
    def connector(self):
        connection = self._provider.connect(self.db_name)
        yield connection
        connection.close()

    def _init_db(self):
        with self.connector() as connection:
            sql = ''
            sql_file_path = (
                settings.CURRENT_DIR / 'sql' / 'create_tables.sql'
            )
            with open(sql_file_path, 'r') as f:
                sql = f.read()

            with connection:
                connection.execute(sql)

    def _save(self, name, extra, password):
        generated_id = None
        with self.connector() as connection:
            sql = '''
                INSERT INTO secrets(name, extra, password)
                VALUES (?, ?, ?)
            '''
            with connection:
                cursor = connection.cursor()
                cursor.execute(
                    sql,
                    (name, extra, password)
                )
                generated_id = cursor.lastrowid
        return generated_id

    def get_secrets(self, decoded=True):
        with self.connector() as connection:
            sql = '''
                SELECT id, name, extra, password
                FROM secrets;
            '''
            cursor = connection.cursor()

            for row in cursor.execute(sql):
                secret_id, name, extra, password = row
                if decoded:
                    name = self._decrypt(name)
                    password = self._decrypt(password)
                    extra = self._decrypt(extra)
                yield Secret(secret_id, name, extra, password)

    def remove_secret(self, secret_id):
        with self.connector() as connection:
            sql = '''
                DELETE FROM secrets WHERE id=?
            '''
            with connection:
                connection.execute(sql, (secret_id, ))
