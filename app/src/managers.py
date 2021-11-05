import csv
import datetime as dt
import os
from dataclasses import asdict
from pathlib import Path

from .storages import StorageManager, Secret


class SecretManager:

    def __init__(self, storage_manager: StorageManager):
        self._storage_manager = storage_manager
        self._secrets = list(self._storage_manager.get_secrets())

    @property
    def secrets(self):
        return self._secrets

    def add_secret(self, name: str, extra: str, password: str) -> None:
        if not name:
            raise ValueError('Secret name can not be empty')

        secret = Secret(None, name, extra, password)
        secret.id = self._storage_manager.save_secret(secret)
        self._secrets.append(secret)

    def remove_secret(self, secret_id: str) -> bool:
        self._storage_manager.remove_secret(secret_id)
        self._secrets = list(self._storage_manager.get_secrets())
        return True

    def make_backup(self):
        filename = dt.date.today().strftime('%d-%m-%Y')
        dir_path = 'backups'
        os.makedirs(dir_path, exist_ok=True)
        path = Path(dir_path)

        with open(path / f'{filename}.csv', 'w', newline='') as csvfile:
            fields = ['id', 'name', 'extra', 'password']
            writer = csv.DictWriter(csvfile, fields)
            writer.writeheader()

            writer.writerows(
                asdict(secret)
                for secret in self._storage_manager.get_secrets(decoded=False)
            )
