import json
import requests
import os
from ...worker_service_base import WorkerServiceBase

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def handler(event, context):
    service = NotifyUpdateService(event, context)
    return service.main()


class NotifyUpdateService(WorkerServiceBase):
    def _get_schema(self):
        return None

    def service_main(self):
        key = self._event["Records"][0]["s3"]["object"]["key"]
        sushi_chain_id = key.split(".")[0]
        res = requests.post(
            SLACK_WEBHOOK_URL,
            json.dumps({"text": f"Updated {sushi_chain_id} document"}),
            headers={"content-type": "application/json"},
        )
        print(res)
