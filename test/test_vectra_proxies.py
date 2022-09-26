'''
Test how Vectra API Toolkit handles Proxy operations
'''
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)


global_proxy = {}

def test_proxy_get(vc_v2):
    '''
    Get proxies and receive a HTTP/200 OK
    '''
    resp = vc_v2.get_proxies()

    assert resp.status_code == 200


def test_proxy_add(vc_v2):
    '''
    Add a proxy and delete it after to leave things how we found them
    '''
    resp = vc_v2.add_proxy(address='127.0.0.254', enable=True)
    proxy = resp.json()['proxy']
    global_proxy['id'] = proxy['id']

    assert resp.status_code == 200, 'Failed to create the proxy 127.0.0.254'
    assert proxy['ip'] == '127.0.0.254'
    assert proxy['considerProxy'] is True

    resp = vc_v2.delete_proxy(proxy_id=proxy['id'])
    assert resp.status_code == 204, 'Failed to delete the proxy 127.0.0.254'


def test_proxy_address_update(vc_v2):
    '''
    Update the proxy we created to a new IP address
    TODO: Create a proxy so test is self sufficient
    '''
    resp = vc_v2.update_proxy(proxy_id=global_proxy['id'], address='127.0.0.253')
    proxy = resp.json()['proxy']

    assert resp.status_code == 200
    assert proxy['ip'] == '127.0.0.253'
    assert proxy['considerProxy'] is True


def test_proxy_state_update(vc_v2):
    '''
    Create a proxy, then update it to false
    '''
    resp = vc_v2.update_proxy(proxy_id=global_proxy['id'], enable=False)
    proxy = resp.json()['proxy']

    assert resp.status_code == 200
    assert proxy['ip'] == '127.0.0.253'
    assert proxy['considerProxy'] is False
