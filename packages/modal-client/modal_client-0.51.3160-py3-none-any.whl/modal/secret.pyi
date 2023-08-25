import modal.object
import typing

class _SecretHandle(modal.object._Handle):
    ...

class SecretHandle(modal.object.Handle):
    def __init__(self, /, *args, **kwargs):
        ...


class _Secret(modal.object._Provider):
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, str] = {}, template_type=''):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...


class Secret(modal.object.Provider):
    def __init__(self):
        ...

    @staticmethod
    def from_dict(env_dict: typing.Dict[str, str] = {}, template_type=''):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...
