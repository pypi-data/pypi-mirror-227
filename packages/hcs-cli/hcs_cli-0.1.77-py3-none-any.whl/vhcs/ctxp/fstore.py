"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import logging
from os import path, listdir
from typing import Any
from collections.abc import Generator
from . import jsondot
from .jsondot import dotdict

log = logging.getLogger(__name__)


def _validate_key(key: str):
    # if key.find(os.pathsep) >= 0:
    if key.find("/") >= 0 or key.find("\\") >= 0:
        raise Exception("Invalid profile name: " + key)


def _load_yaml(file_name: str) -> dotdict | None:
    if not os.path.exists(file_name):
        return
    with open(file_name, "r") as stream:
        import yaml

        ret = yaml.safe_load(stream)
        return jsondot.dotify(ret)


def _load_text(file_name: str) -> str:
    if not os.path.exists(file_name):
        return
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def _load_file(file_path: str, format: str) -> dotdict | str:
    _, ext = path.splitext(file_path)

    if ext == ".json" or (ext == "" and format == "json"):
        return jsondot.load(file_path)
    if ext == ".yaml" or ext == ".yml" or (ext == "" and (format == "yaml" or format == "yml")):
        return _load_yaml(file_path)
    if ext == ".txt" or (ext == "" and format in ["text", "plain", "txt"]):
        return _load_text(file_path)

    if format != "auto":
        raise Exception(f"Invalid store format: {format}")

    # The specified path has no ext name, and format is auto.
    if os.path.exists(file_path):
        return jsondot.load(file_path)

    tmp = file_path + ".json"
    if os.path.exists(tmp):
        return jsondot.load(file_path + ".json")

    tmp = file_path + ".yaml"
    if os.path.exists(tmp):
        return _load_yaml(tmp)

    tmp = file_path + ".yml"
    if os.path.exists(tmp):
        return _load_yaml(tmp)

    # Not found


class fstore:
    """A key-value store, optionally backed by a file system directory and files in it."""

    def __init__(self, store_path: str = None, create: bool = True):
        """Initialize the store

        Args:
                store_path (str): The path to store state files. If None, state will not be stored.
        create (bool, optional): If store_path is specified, try creating it if not exist. Defaults to True.

        Raises:
                Exception: [description]
        """
        if store_path:
            store_path = path.realpath(store_path)
            if not path.exists(store_path):
                if create:
                    os.makedirs(store_path)
                else:
                    raise Exception(f"Store path does not exist: {store_path}")
            elif not os.path.isdir(store_path):
                raise Exception(f"Store path is not a directory: {store_path}")
            self._path = store_path
        else:
            self._path = None
        self._cache = {}

    def get(self, key: str, reload: bool = False, format: str = "auto", default=None) -> dotdict:
        _validate_key(key)
        if self._path and (reload or key not in self._cache):
            file_path = self._get_path(key)
            log.debug(f"Read {file_path}")
            data = _load_file(file_path, format)
            if data != None:
                self._cache[key] = data
        else:
            data = self._cache.get(key)

        if data is None and default is not None:
            return jsondot.dotify(default)
        return data

    def _get_path(self, key: str) -> str:
        if not self._path:
            return None
        return path.join(self._path, key)

    def save(self, key: str, data: Any, format: str = "auto") -> Any:
        _validate_key(key)

        if format == "auto":
            if isinstance(data, str):
                format = "text"
            else:
                format = "json"

        data = jsondot.dotify(data)

        self._cache[key] = data
        if self._path:
            file_path = self._get_path(key)
            log.debug(f"Write {file_path}")
            if format == "json":
                jsondot.save(data, file_path)
            elif format == "text":
                with open(file_path, "w", encoding="utf-8") as outfile:
                    outfile.write(str(data))
            elif format == "json-compact":
                jsondot.save(data, file_path, False)
            elif format == "yaml":
                raise Exception("TODO")
            else:
                raise Exception(f"Invalid format. key={key}, format={format}")

        return data

    def delete(self, key: str) -> None:
        _validate_key(key)
        self._cache.pop(key, None)
        if self._path:
            file_path = self._get_path(key)
            if os.path.exists(file_path):
                os.remove(file_path)

    def keys(self) -> list[str]:
        if self._path:
            return [f for f in listdir(self._path) if path.isfile(path.join(self._path, f))]
        return list(self._cache.keys())

    def values(self) -> Generator[Any, None, None]:
        for k in self.keys():
            yield self.get(k)

    def items(self) -> Generator[tuple[str, dict], None, None]:
        for k in self.keys():
            yield (k, self.get(k))

    def clear(self) -> None:
        for k in self.keys():
            self.delete(k)

    def destroy(self) -> None:
        self._cache.clear()
        if self._path:
            import shutil

            shutil.rmtree(self._path)

    def size(self) -> int:
        return len(self.keys())

    def contains(self, key: str) -> bool:
        if key in self._cache:
            return True
        return key in self.keys()

    # ----------------- Helpers -----------------

    def patch(self, key: str, data: dict) -> dotdict:
        existing_data = self.get(key)
        if existing_data is None:
            existing_data = jsondot.dotify({})
        existing_data |= data
        self.save(key, existing_data)
        return existing_data
