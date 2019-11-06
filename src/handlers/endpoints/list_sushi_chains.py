from ...api_service_base import APIServiceBase
from ...infrastructures.sushi_chain_repository import SushiChainRepository


def handler(event, context):
    service = ListSushiChainsService(event, context)
    return service.main()


class ListSushiChainsService(APIServiceBase):
    def _get_schema(self):
        return None

    def service_main(self):

        items = SushiChainRepository.scan_all()
        return self.make_response(
            200, [SushiChainRepository.to_item(model) for model in items]
        )
