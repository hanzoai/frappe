from contextvars import ContextVar
from typing import Any

from werkzeug.local import Local, LocalProxy

_contextvar = ContextVar("frappe_local")
_local_attributes = frozenset(dir(Local))
_local_proxy_attributes = frozenset(dir(LocalProxy))


class FrappeLocal(Local):
	"""
	For internal use only. Do not use this class directly.
	"""

	__slots__ = ()

	def __init__(self):
		super().__init__(_contextvar)

	def __getattribute__(self, name: str) -> Any:
		if name in _local_attributes:
			return object.__getattribute__(self, name)

		obj = _contextvar.get(None)
		if obj is not None and name in obj:
			return obj[name]

		return object.__getattribute__(self, name)

	def __setattr__(self, name: str, value: Any) -> None:
		obj = _contextvar.get(None)
		if obj is None:
			obj = {}
			_contextvar.set(obj)

		obj[name] = value

	def __delattr__(self, name: str) -> None:
		obj = _contextvar.get(None)
		if obj is not None and name in obj:
			del obj[name]
			return

		raise AttributeError(name)

	def __call__(self, name: str) -> LocalProxy:
		def _get_current_object() -> Any:
			obj = _contextvar.get(None)
			if obj is not None and name in obj:
				return obj[name]

			raise RuntimeError("object is not bound") from None

		lp = FrappeLocalProxy(_get_current_object)
		object.__setattr__(lp, "_get_current_object", _get_current_object)
		return lp


class FrappeLocalProxy(LocalProxy):
	__slots__ = ()

	def __getattribute__(self, name: str) -> Any:
		if name in _local_proxy_attributes:
			return object.__getattribute__(self, name)

		return getattr(object.__getattribute__(self, "_get_current_object")(), name)
