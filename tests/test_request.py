from __future__ import annotations

import json

import pytest

from slapshot.request import cayenne_build, cayenne_build_value, request_build, sort_build


def test_request_build_defaults_to_empty() -> None:
    assert request_build('https://example.com').params == {}


def test_request_build_drops_none() -> None:
    assert request_build('https://example.com', {'a': 1, 'b': None}).params == {'a': 1}


def test_request_build_keeps_falsy_non_none() -> None:
    assert request_build(
        'https://example.com', {'a': 0, 'b': '', 'c': False, 'd': None}
    ).params == {'a': 0, 'b': '', 'c': False}


def test_cayenne_build_value_int() -> None:
    assert cayenne_build_value(5) == '5'


def test_cayenne_build_value_float() -> None:
    assert cayenne_build_value(1.5) == '1.5'


def test_cayenne_build_value_true() -> None:
    assert cayenne_build_value(value=True) == 'true'


def test_cayenne_build_value_false() -> None:
    assert cayenne_build_value(value=False) == 'false'


def test_cayenne_build_value_quotes_string() -> None:
    assert cayenne_build_value('x') == '"x"'


def test_cayenne_build_value_rejects_embedded_quote() -> None:
    with pytest.raises(ValueError, match='double quote'):
        cayenne_build_value('a"b')


def test_cayenne_build_joins_with_and() -> None:
    assert cayenne_build({'a': 1, 'b': 2}) == 'a=1 and b=2'


def test_cayenne_build_preserves_order() -> None:
    assert cayenne_build({'b': 2, 'a': 1}) == 'b=2 and a=1'


def test_cayenne_build_mixed_types() -> None:
    assert cayenne_build({'a': 1, 'b': 'x', 'c': True}) == 'a=1 and b="x" and c=true'


def test_cayenne_build_drops_none_members() -> None:
    assert cayenne_build({'a': 1, 'b': None}) == 'a=1'


def test_cayenne_build_all_none_returns_none() -> None:
    assert cayenne_build({'a': None, 'b': None}) is None


def test_cayenne_build_empty_returns_none() -> None:
    assert cayenne_build({}) is None


def test_cayenne_build_lowercases_true() -> None:
    assert cayenne_build({'active': True}) == 'active=true'


def test_cayenne_build_lowercases_false() -> None:
    assert cayenne_build({'active': False}) == 'active=false'


def test_cayenne_build_quotes_strings() -> None:
    assert cayenne_build({'name': 'x'}) == 'name="x"'


def test_sort_build_passes_string_through() -> None:
    assert sort_build('points') == 'points'


def test_sort_build_encodes_sequence() -> None:
    sort = ({'property': 'points', 'direction': 'DESC'},)
    assert sort_build(sort) == json.dumps([{'property': 'points', 'direction': 'DESC'}])


def test_sort_build_encodes_list() -> None:
    sort = [{'property': 'points', 'direction': 'DESC'}]
    assert sort_build(sort) == json.dumps(sort)


def test_sort_build_empty_sequence_is_empty_json_array() -> None:
    assert sort_build(()) == '[]'


def test_sort_build_none_returns_none() -> None:
    assert sort_build(None) is None
