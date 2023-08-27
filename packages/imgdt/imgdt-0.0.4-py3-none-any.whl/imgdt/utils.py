# utils.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of ImageDatasetTools and is released under
# the MIT License: https://opensource.org/license/mit/

class _STDOFormat:
    TEXT = '\33[37m'
    SUCCESS = '\33[92m'
    WARNING = '\33[93m'
    LOADING = '\33[94m'
    INFO = '\33[0m'
    ERROR = '\33[91m'

class _Logger:
    def classic(message) -> None:
        print(f"{message}")

    def text(message) -> None:
        print(f"\n{_STDOFormat.TEXT}>> {message}{_STDOFormat.TEXT}")

    def warning(message) -> None:
        print(f"\n{_STDOFormat.WARNING}[WARNING] | {message}{_STDOFormat.TEXT}")

    def success(message) -> None:
        print(f"{_STDOFormat.SUCCESS}[COMPLETED] | {message}{_STDOFormat.TEXT}")

    def error(message) -> None:
        print(f"{_STDOFormat.ERROR}[ERROR] | {message}{_STDOFormat.TEXT}")

    def loading(message) -> None:
        print(f"{_STDOFormat.LOADING}[LOADING] | {message}{_STDOFormat.TEXT}", end='\r')

    def info(message) -> None:
        print(f"{_STDOFormat.INFO} - {message}{_STDOFormat.TEXT}")