from typing import NamedTuple, Optional, Any


# ставим дефолты `None`, если ещё параметры будут, чтобы лишний раз не сетить None, если не юзаются.
class QueryParametersDTO(NamedTuple):
	filters: Optional[dict[str, Any]] = None