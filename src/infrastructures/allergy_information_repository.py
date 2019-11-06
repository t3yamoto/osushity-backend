import json
import os
from typing import Dict, List

import boto3
from botocore.errorfactory import ClientError
from sushi_allergy_parser import AllergenState
from ..exceptions import NotFoundError

s3 = boto3.resource("s3")
BUCKET_NAME = os.environ["BUCKET_NAME_DATA"]
ENCODING = "utf-8"


class AllergyInformationRepository:
    @classmethod
    def query_by(
        cls,
        sushi_chain_id: str,
        exclude_allergens: List[str],
        excludes_may_contain: bool,
        name_like: str,
        limit: int,
        page: int,
    ) -> List[Dict]:

        body = cls._read_data(sushi_chain_id + ".json")
        items = json.loads(body, encoding=ENCODING)

        filterd_items = [
            item
            for item in items
            if cls._filter_item(
                item, exclude_allergens, excludes_may_contain, name_like
            )
        ]

        return cls._pagenate_items(filterd_items, limit, page)

    @classmethod
    def _filter_item(
        cls,
        item: dict,
        exclude_allergens: List[str],
        excludes_may_contain: bool,
        name_like: str,
    ) -> bool:
        if name_like not in item["name"]:
            return False

        for exclude_allergen in exclude_allergens:
            if item[exclude_allergen] == "CONTAIN" or (
                item[exclude_allergen] == "MAY_CONTAIN" and excludes_may_contain
            ):
                return False
        return True

    @classmethod
    def _pagenate_items(cls, items: List[Dict], limit: int, page: int) -> List[Dict]:
        start = limit * (page - 1)
        end = start + limit
        return items[start:end]

    @classmethod
    def save_all(cls, sushi_chain: str, items: List[Dict]):
        body = json.dumps(items, default=cls.default, ensure_ascii=False, indent=4)
        cls._write_data(sushi_chain + ".json", body)

    @classmethod
    def default(cls, v):
        if isinstance(v, AllergenState):
            return str(v)
        raise TypeError("Not serializable")

    @classmethod
    def _read_data(cls, key: str) -> str:
        try:
            object = s3.Object(BUCKET_NAME, key)
            object.load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise NotFoundError
            else:
                raise e
        body = object.get()["Body"].read().decode(ENCODING)
        return body

    @classmethod
    def _write_data(cls, key: str, body: str):
        object = s3.Object(BUCKET_NAME, key)
        _ = object.put(Body=body, ContentEncoding=ENCODING)
