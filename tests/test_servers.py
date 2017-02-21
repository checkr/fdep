import json
import time

import pytest
import requests
from fdep.servers.jsonrpc import JSONRPCServer
from fdep.servers.xmlrpc import XMLRPCServer

from six.moves import xmlrpc_client


def setup_test_server(driver, **kwargs):
    server = driver()
    server.register_functions({
        'test': lambda: True
    }.items())
    return server


def test_basic_jsonrpc_server(fdep_serve):
    server = setup_test_server(JSONRPCServer)
    th = fdep_serve(server, port=14244)
    th.start()
    time.sleep(1)

    payload = {
        "method": "test",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0
    }
    headers = {
        'content-type': 'application/json'
    }

    res = requests.post(
        'http://127.0.0.1:14244/', data=json.dumps(payload),
        headers=headers
    ).json()

    assert res['result'] is True
    assert res['jsonrpc']
    assert res['id'] == 0

    th.stop()
    th.join()


def test_jsonrpc_server_auth(fdep_serve):
    server = setup_test_server(JSONRPCServer)
    th = fdep_serve(
        server, port=14244, username='test', password='pass')
    th.start()
    time.sleep(1)

    payload = {
        "method": "test",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0
    }
    headers = {
        'content-type': 'application/json'
    }

    res = requests.post(
        'http://127.0.0.1:14244/', data=json.dumps(payload),
        headers=headers
    )

    # Without credentials, it should error
    assert res.status_code == 401

    res = requests.post(
        'http://127.0.0.1:14244', data=json.dumps(payload),
        headers=headers, auth=('test', 'pass')
    ).json()

    # With credentials, it should function properly.
    assert res['result'] is True
    assert res['jsonrpc']
    assert res['id'] == 0

    th.stop()
    th.join()


def test_basic_xmlrpc_server(fdep_serve):
    server = setup_test_server(XMLRPCServer)
    th = fdep_serve(server, port=14243)
    th.start()
    time.sleep(1)

    s = xmlrpc_client.Server("http://127.0.0.1:14243")
    assert s.test() is True

    th.stop()
    th.join()


def test_xmlrpc_server_auth(fdep_serve):
    server = setup_test_server(XMLRPCServer)
    th = fdep_serve(server, port=14243, username='test', password='pass')
    th.start()
    time.sleep(1)

    s = xmlrpc_client.Server('http://127.0.0.1:14243')
    with pytest.raises(xmlrpc_client.ProtocolError):
        s.test()

    s = xmlrpc_client.Server('http://test:pass@127.0.0.1:14243')
    assert s.test() is True

    th.stop()
    th.join()


def test_serve(load_fixture, fdep):
    load_fixture('serve')
    # Should return 1 with a help message.
    assert fdep('serve') == 1


def test_console_server(load_fixture, fdep):
    load_fixture('serve')
    assert fdep('serve', 'app', '--func', 'classify', '--text', 'hello') == 0
    assert fdep('serve', 'app', '--func', 'wrong_func') == 1


def test_wrong_port(load_fixture, fdep):
    load_fixture('serve')
    assert fdep('serve', '--port', 'ERROR', '--driver', 'xmlrpc', 'app') == 1


def test_wrong_driver(load_fixture, fdep):
    load_fixture('serve')
    assert fdep('serve', '--driver', 'test_some_wrong_driver_name', 'app') == 1
    assert fdep(
        'serve', '--driver', 'test_some_wrong_driver_name.driver', 'app') == 1
    assert fdep('serve', '--driver', 'app.test_driver', 'app') == 1
