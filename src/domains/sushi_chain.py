from dataclasses import dataclass
from datetime import datetime


@dataclass
class SushiChain:
    id: str
    name: str
    parser: str
    document_url: str
    last_modified_at: datetime
