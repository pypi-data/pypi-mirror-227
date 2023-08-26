"""
an open source key value store in Python.

persist records to the disk and we dont lose all of the data in a crash.

it will support 4 operations :
    1. GET 
    2. SET 
    3. DEL 
    4. QUIT 

author : sagnikc395<sagnikchatterjee607@gmail.com>    
"""

import os
import pickle
import hashlib
from rich.console import Console

console = Console()


class OpenKV:
    def __init__(self, path: str, shard_count: int) -> None:
        self.path = path
        self.shard_count = shard_count
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _get_shard_id(self, key: str) -> int:
        hashVal = hashlib.sha256(key.encode()).hexdigest()
        return int(hashVal, 16) % self.shard_count

    def _get_filename(self, key) -> str:
        return os.path.join(self.path, f"{key}.kv")

    def put(self, key, value) -> None:
        filename = self._get_filename(key)
        with open(filename, "wb") as f:
            pickle.dump(value, f)

    def get(self, key, default=None) -> str:
        filename = self._get_filename(key)
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return pickle.load(f)
        return default

    def delete(self, key) -> None:
        filename = self._get_filename(key)
        if os.path.exists(filename):
            os.remove(filename)

    def keys(self) -> list:
        return [os.path.splitext(entry)[0] for entry in os.listdir(self.path)]

    def delall(self) -> None:
        for key in self.keys():
            self.delete(key)


def shell():
    store = OpenKV("data")
    console.print("Starting OpenKV v.0.0.1", style="bold purple")
    console.print("Commands list  : GET,PUT,KEYS,DELALL,QUIT", style="yellow")
    status: bool = True
    while status:
        arg = input("openKV> ")
        if arg.upper() == "GET":
            key = input()
            console.print(store.get(key), style="bold green")
        elif arg.upper() == "PUT":
            key, value = input().split(",")
            store.put(key, value)
        elif arg.upper() == "KEYS":
            console.print(store.keys(), style="bold yellow")
        elif arg.upper() == "DELALL":
            key = input()
            store.delete(key)
        elif arg.upper() == "QUIT":
            console.print("exiting.", style="bold red")
            status = False


if __name__ == "__main__":
    shell()
