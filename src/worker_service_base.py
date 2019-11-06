import logging
from abc import ABCMeta, abstractmethod

from jsonschema import ValidationError, validate


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WorkerServiceBase(metaclass=ABCMeta):
    def __init__(self, event: dict, context=None):
        logger.info(event)
        self._event = event
        self._context = context

    @abstractmethod
    def _get_schema(self):
        pass

    @abstractmethod
    def service_main(self):
        raise NotImplementedError

    def main(self):
        try:
            if self._get_schema():
                validate(self._event, self._get_schema())
            return self.service_main()
        except Exception as e:
            logger.exception(e)
            raise e
