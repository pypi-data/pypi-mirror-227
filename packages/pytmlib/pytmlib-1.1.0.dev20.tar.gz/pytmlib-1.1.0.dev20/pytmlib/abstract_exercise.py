import abc
import logging
import os
import sys
import uuid
from typing import Iterable
from typing import Tuple

from flask import Flask

from .context import Context
from .create_app import create_app
from .decorators import ENTRYPOINT_MARKER
from .output import OutputBuilder as Output
from .types import Action

PYTM_UID_ENV = 'PYTM_UID'
PYTM_SECRET_ENV = 'PYTM_SECRET'
HOSTNAME_ENV = 'HOSTNAME'


class AbstractExercise(abc.ABC):
    def __new__(cls, unique_id: str = None, static_folder_path: str = None, *args, **kwargs):
        exercise: AbstractExercise = super().__new__(cls, *args, **kwargs)

        unique_id = os.getenv(PYTM_UID_ENV, unique_id)
        secret, fallback = AbstractExercise._get_secret()
        context: Context = Context(unique_id, secret, exercise)

        exercise._context = context

        app: Flask = create_app(context, static_folder_path)

        skip_warnings = app.debug or 'unittest' in sys.modules.keys()

        if not skip_warnings and unique_id is None:
            logging.warning('missing %s environment variable', PYTM_UID_ENV)

        if not skip_warnings and fallback:
            logging.warning('missing %s environment variable', PYTM_SECRET_ENV)

        return app

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Get the `semantic version <https://semver.org/spec/v2.0.0.html>`_ of this exercise.

        :return: The version of this exercise.
        """
        raise NotImplemented

    @property
    def output(self) -> Output:
        """Get a new output builder instance.

        :return: A new instance of the output builder.
        """
        return self._context.output

    @abc.abstractmethod
    def start(self) -> Output:
        """This is the main entrypoint.

        :return: The output of this exercise action.
        """
        pass

    def get_entrypoints(self) -> Iterable[Action]:
        for name in dir(self):
            func = getattr(self, name)

            if hasattr(func, ENTRYPOINT_MARKER):
                yield func

    @staticmethod
    def _get_secret() -> Tuple[str, bool]:
        hostname: str = os.getenv(HOSTNAME_ENV, os.name)
        fallback: uuid = uuid.uuid5(uuid.NAMESPACE_DNS, hostname)
        secret: str = os.getenv(PYTM_SECRET_ENV)
        use_fallback: bool = secret is None

        return str(fallback) if use_fallback else secret, use_fallback
