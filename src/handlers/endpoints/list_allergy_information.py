from jsonschema import ValidationError
from sushi_allergy_parser import Allergen

from ...api_service_base import APIServiceBase
from ...infrastructures.allergy_information_repository import (
    AllergyInformationRepository,
)


def handler(event, context):
    service = ListAllergyinformationService(event, context)
    return service.main()


class ListAllergyinformationService(APIServiceBase):
    def _get_schema(self):
        return {
            "type": "object",
            "properties": {
                "pathParameters": {
                    "type": "object",
                    "properties": {"sushiChainId": {"type": "string"}},
                    "required": ["sushiChainId"],
                },
                "queryStringParameters": {
                    "type": ["object", "null"],
                    "properties": {
                        "exclusionAllergens": {"type": "string"},
                        "excludesMayContain": {"type": "string"},
                        "nameLike": {"type": "string"},
                        "limit": {"type": "string", "pattern": "^[0-9]{1,3}$"},
                        "page": {"type": "string", "pattern": "^[0-9]{1,3}$"},
                    },
                },
            },
        }

    def service_main(self):

        sushi_chain_id = self._event["pathParameters"]["sushiChainId"]

        query_parameters = self._event.get("queryStringParameters") or {}
        exclude_allergens = (
            query_parameters.get("excludeAllergens").split(",")
            if query_parameters.get("excludeAllergens")
            else []
        )
        unknown_allergens = set(exclude_allergens) - set(Allergen.values())
        if unknown_allergens:
            raise ValidationError(f"Unknown allergens {unknown_allergens}")

        excludes_may_contain = query_parameters.get("excludesMayContain") == "1"
        name_like = query_parameters.get("nameLike") or ""
        limit = int(query_parameters.get("limit") or 50)
        page = int(query_parameters.get("page") or 1)

        items = AllergyInformationRepository.query_by(
            sushi_chain_id,
            exclude_allergens,
            excludes_may_contain,
            name_like,
            limit,
            page,
        )
        return self.make_response(200, items)


if __name__ == "__main__":
    handler({}, None)
