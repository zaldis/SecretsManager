import sqlite3
from dataclasses import asdict

import pyperclip
import webview

from app.utils import create_password
from app.src.storages import DBStorageManager
from app import settings
from app.src.managers import SecretManager


pyperclip.set_clipboard(settings.CLIP_MODULE)


class API:

    def __init__(self):
        storage_manager = DBStorageManager(sqlite3)
        self._manager = SecretManager(storage_manager)

    @property
    def secrets(self):
        return self._manager.secrets

    def get_secrets(self):
        return [asdict(secret) for secret in self.secrets]

    def create_secret(self, name='secret', extra=''):
        password = ''.join(
            create_password(symbols=settings.ALPHABET,
                            size=settings.PASSWORD_SIZE)
        )
        name = name.lower()

        try:
            self._manager.add_secret(name, extra, password)
        except ValueError as err:
            return {
                'ok': False,
                'message': str(err)
            }

        pyperclip.copy(password)
        return {
            'ok': True,
            'message': f'New secret was successfuly added for <{name}>'
        }

    def save_to_clipboard(self, secret_id: str):
        secret_id = int(secret_id)
        allowed_secrets = (
            secret
            for secret in self.secrets
            if secret.id == secret_id
        )
        secret = next(allowed_secrets, None)

        if secret:
            pyperclip.copy(secret.password)
            return {
                'ok': True,
                'message': f'Secret <{secret.name}> is saved to clipboard'
            }
        return {
            'ok': False,
            'message': f'Secret with ID {secret_id} does not exist'
        }

    def remove_secret(self, secret_id):
        is_ok = self._manager.remove_secret(secret_id)
        return {
            'ok': is_ok,
            'message': f'Secret with ID <{secret_id}> was removed'
        }

    def make_backup(self):
        self._manager.make_backup()


def run():
    webview.create_window(title='Zaldis Secrets',
                          url='app/assets/index.html',
                          js_api=API(),
                          confirm_close=True)
    webview.start(debug=True)


if __name__ == '__main__':
    run()
