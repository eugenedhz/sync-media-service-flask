from typing import NamedTuple, Optional, Any


class QueryParametersDTO(NamedTuple):
	required_ids: Optional[tuple[int, ...]]
	filters: Optional[dict[str, Any]]