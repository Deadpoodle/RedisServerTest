from unittest.mock import MagicMock, patch

import protocol


@patch("protocol.db", {"foo": "bar"})
def test_handle_get_valid():
    key = "foo"
    expected = "+bar\r\n".encode()

    response = protocol.RedisServerProtocol.handle_get(None, key)

    assert response == expected


@patch("protocol.db", {"foo": "bar"})
def test_handle_get_invalid():
    key = "foobar"
    expected = "$-1\r\n".encode()

    response = protocol.RedisServerProtocol.handle_get(None, key)

    assert response == expected


@patch("protocol.db", {})
def test_handle_set_valid():
    key = "foo"
    val = "bar"
    expected = b"+OK\r\n"

    response = protocol.RedisServerProtocol.handle_set(None, key, val)

    assert response == expected


@patch("protocol.db", {})
def test_handle_set_invalid():
    key = ["foo"]
    val = "uh oh"
    expected = b"-ERR error saving key value pair\r\n"

    response = protocol.RedisServerProtocol.handle_set(None, key, val)

    assert response == expected


@patch("protocol.db", {"foo": "bar"})
def test_handle_del_valid():
    key = "foo"
    expected = b"+OK\r\n"

    response = protocol.RedisServerProtocol.handle_del(None, key)

    assert response == expected


@patch("protocol.db", {"foo": "bar"})
def test_handle_del_invalid():
    key = ["foo"]
    expected = b"-ERR Invalid key\r\n"

    response = protocol.RedisServerProtocol.handle_del(None, key)

    assert response == expected


def test_parse_command_set_int():
    data = "*3\r\n$3\r\nset\r\n$4\r\ntest\r\n$1\r\n1\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "SET"
    assert key == "test"
    assert val == 1


def test_parse_command_set_float():
    data = "*3\r\n$3\r\nset\r\n$4\r\ntest\r\n$1\r\n1.5\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "SET"
    assert key == "test"
    assert val == 1.5


def test_parse_command_set_string():
    data = "*3\r\n$3\r\nset\r\n$4\r\ntest\r\n$1\r\nfoobar\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "SET"
    assert key == "test"
    assert val == "foobar"


def test_parse_command_set_bool():
    data = "*3\r\n$3\r\nset\r\n$4\r\ntest\r\n$1\r\ntrue\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "SET"
    assert key == "test"
    assert val == True


def test_parse_command_set_invalid_set_args_amount():
    data = "*3\r\n$3\r\nset\r\n$4\r\ntest\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "nil"
    assert key == "nil"
    assert val == "nil"


def test_parse_command_set_invalid_args_amount():
    data = "*2\r\n$3\r\ndel\r\n"

    cmd, key, val = protocol.RedisServerProtocol.parse_command(None, data)

    assert cmd == "nil"
    assert key == "nil"
    assert val == "nil"


def test_data_received_valid():
    # Not sure how valuable this test is
    data = b"*1\r\n$7\r\nCOMMAND\r\n"
    expected = ""
    protocol_mock = protocol.RedisServerProtocol()
    protocol_mock.data_received = MagicMock()

    response = protocol_mock.data_received(None, data)

    protocol_mock.data_received.assert_called_once_with(
        None, b"*1\r\n$7\r\nCOMMAND\r\n"
    )
