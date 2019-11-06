import json
import logging
from abc import ABCMeta, abstractmethod

from jsonschema import ValidationError, validate

from .exceptions import NotFoundError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class APIServiceBase(metaclass=ABCMeta):
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

    def make_response(self, status_code: int, body):
        return {
            "statusCode": status_code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps(body, ensure_ascii=False, indent=4),
        }

    def main(self):
        try:
            if self._get_schema():
                validate(self._event, self._get_schema())
            return self.service_main()
        except ValidationError as e:
            logger.info(e)
            return self.make_response(400, {"message": e.message})
        except NotFoundError as e:
            logger.info(e)
            return self.make_response(404, {"message": "Resource not found"})
        except Exception as e:
            logger.exception(e)
            return self.make_response(500, {"message": "Internal server error"})
