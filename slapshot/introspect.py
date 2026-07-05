from __future__ import annotations

import msgspec

from typing_extensions import Any


class UnknownFieldWarning(UserWarning):
    """The warning issued when a decoded payload has fields absent from its model."""


def unknown_fields(payload: Any, model: Any) -> list[str]:
    """It returns the dotted paths of fields in a payload absent from a model.

    It walks the model's type tree and collects keys present in the payload but
    not defined on the corresponding struct. It recurses into nested structs and
    lists, and skips freeform blocks (Any and dict fields) that are
    intentionally left undecoded.

    Args:
        payload: The decoded JSON payload, as returned by a raw request.
        model: The model type the payload was decoded into.

    Returns:
        The undefined field paths, in first-seen order and de-duplicated.
    """

    found: list[str] = []
    _walk(payload, msgspec.inspect.type_info(model), '', found)

    return list(dict.fromkeys(found))


def _walk(payload: Any, info: Any, path: str, found: list[str]) -> None:
    if isinstance(info, msgspec.inspect.StructType):
        if not isinstance(payload, dict):
            return

        known = {field.encode_name: field for field in info.fields}

        found.extend(_join(path, key) for key in payload if key not in known)

        for name, field in known.items():
            if name in payload:
                _walk(payload[name], field.type, _join(path, name), found)

        return

    if isinstance(info, msgspec.inspect.ListType):
        if not isinstance(payload, list):
            return

        for item in payload:
            _walk(item, info.item_type, f'{path}[]', found)

        return

    if isinstance(info, msgspec.inspect.UnionType):
        for member in info.types:
            if isinstance(member, (msgspec.inspect.StructType, msgspec.inspect.ListType)):
                _walk(payload, member, path, found)

        return


def _join(path: str, key: str) -> str:
    if not path:
        return key

    return f'{path}.{key}'
