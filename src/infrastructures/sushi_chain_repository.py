import os
from datetime import datetime
from typing import Optional, List

import boto3
from boto3_type_annotations.dynamodb import Table

from ..domains.sushi_chain import SushiChain

db = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME_SUSHI_CHAINS"]
ISO_FORMAT = "%Y-%m-%d %H:%M:%S%z"


class SushiChainRepository:
    table: Table = db.Table(TABLE_NAME)

    @classmethod
    def scan_all(cls) -> List[SushiChain]:
        res = cls.table.scan()
        return [cls.to_model(item) for item in res["Items"]] if "Items" in res else []

    @classmethod
    def get_sushi_chain_by_id(cls, id: str) -> Optional[SushiChain]:
        res = cls.table.get_item(Key={"id": id})
        return cls.to_model(res["Item"]) if "Item" in res else None

    @classmethod
    def save(cls, sushi_chain: SushiChain) -> SushiChain:
        _ = cls.table.put_item(Item=cls.to_item(sushi_chain))
        return sushi_chain

    @classmethod
    def to_model(cls, item: dict) -> SushiChain:
        return SushiChain(
            id=item["id"],
            name=item["name"],
            parser=item["parser"],
            document_url=item["document_url"],
            last_modified_at=datetime.strptime(item["last_modified_at"], ISO_FORMAT),
        )

    @classmethod
    def to_item(cls, sushi_chain: SushiChain) -> dict:
        return {
            "id": sushi_chain.id,
            "name": sushi_chain.name,
            "parser": sushi_chain.parser,
            "document_url": sushi_chain.document_url,
            "last_modified_at": sushi_chain.last_modified_at.strftime(ISO_FORMAT),
        }
