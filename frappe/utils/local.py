from contextvars import ContextVar
from typing import Any

from werkzeug.local import Local, LocalProxy

_contextvar = ContextVar("frappe_local")
_local_attributes = frozenset(dir(Local))
_local_proxy_attributes = frozenset(dir(LocalProxy))


def get_local(name: str) -> Any:
	obj = _contextvar.get(None)
	if obj is not None and name in obj:
		return obj[name]

	raise AttributeError(name)


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

		return get_local(name)

	def __getattr__(self, name: str) -> Any:
		return get_local(name)

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

	def __release_local__(self):
		_contextvar.set({})

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

		return getattr(get_obj(self), name)

	def __getattr__(self, name: str) -> Any:
		return getattr(get_obj(self), name)

	def __setattr__(self, name: str, value: str) -> None:
		setattr(get_obj(self), name, value)

	def __delattr__(self, name: str) -> None:
		delattr(get_obj(self), name)

	def __getitem__(self, key: str) -> Any:
		return get_obj(self)[key]

	def __setitem__(self, key: str, value: str) -> None:
		get_obj(self)[key] = value

	def __delitem__(self, key: str) -> None:
		del get_obj(self)[key]

	def __bool__(self) -> bool:
		try:
			return bool(get_obj(self))
		except RuntimeError:
			return False

	def __contains__(self, key: str) -> bool:
		return key in get_obj(self)

	def __str__(self) -> str:
		return str(get_obj(self))


def get_obj(lp: FrappeLocalProxy) -> Any:
	return object.__getattribute__(lp, "_get_current_object")()
