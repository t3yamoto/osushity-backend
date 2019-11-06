import os
import tempfile
import urllib
from datetime import datetime

from ...domains.sushi_chain import SushiChain
from ...infrastructures.allergy_information_repository import (
    AllergyInformationRepository,
)
from ...infrastructures.sushi_chain_repository import SushiChainRepository
from ...util import parse_last_modified
from ...worker_service_base import WorkerServiceBase

SUSHI_CHAIN_ID = os.environ["SUSHI_CHAIN_ID"]


def handler(event, context):
    service = CollectAllergyinformationervice(event, context)
    return service.main()


class CollectAllergyinformationervice(WorkerServiceBase):
    def _get_schema(self):
        return None

    def service_main(self):

        sushi_chain: SushiChain = SushiChainRepository.get_sushi_chain_by_id(
            SUSHI_CHAIN_ID
        )
        if not sushi_chain:
            raise Exception(f"Sushi chain '{SUSHI_CHAIN_ID}' is not defined")

        fetched_last_modified = self._fetch_last_modified(sushi_chain.document_url)
        if sushi_chain.last_modified_at >= fetched_last_modified:
            return

        # import sushi-allergy-parser
        mod = __import__("sushi_allergy_parser", fromlist=[sushi_chain.parser])
        parser_class = getattr(mod, sushi_chain.parser)

        with tempfile.TemporaryDirectory(dir="/tmp") as d:
            dst_path = os.path.join(d, "tmp.pdf")
            urllib.request.urlretrieve(sushi_chain.document_url, dst_path)

            df = parser_class().parse(dst_path)
            records = df.to_dict("records")  # dataframe -> list[dict]

            AllergyInformationRepository.save_all(sushi_chain.id, records)

        sushi_chain.last_modified_at = fetched_last_modified
        SushiChainRepository.save(sushi_chain)

    def _fetch_last_modified(self, url: str) -> datetime:
        req = urllib.request.Request(url, method="HEAD")
        res = urllib.request.urlopen(req)
        if res.status == 200:
            return parse_last_modified(res.getheader("Last-Modified"))

    def _document_is_modified(self, url: str, last_modified: datetime):
        req = urllib.request.Request(url, method="HEAD")
        res = urllib.request.urlopen(req)
        if res.status == 200:
            current_last_modified = parse_last_modified(res.getheader("Last-Modified"))
            if last_modified < current_last_modified:
                return True
        return False
