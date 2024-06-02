from typing import NamedTuple, Optional, Any

from pkg.query_params.filter_by.parse import Filter


# ставим дефолты `None`, если ещё параметры будут, чтобы лишний раз не сетить None, если не юзаются.
class QueryParametersDTO(NamedTuple):
	filters: Optional[list[Filter]] = None