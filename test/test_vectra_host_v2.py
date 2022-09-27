'''
Excercise the APIv2
'''
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)


def test_get_hosts(vc_v2):
    '''
    Get hosts via APIv2, should return HTTP/200 OK
    '''
    resp = vc_v2.get_hosts()

    assert vc_v2.version == 2
    assert resp.status_code == 200


def test_get_hosts_note_modified(vc_v2):
    resp = vc_v2.get_hosts(note_modified_timestamp_gte=100)

    assert vc_v2.version == 2
    assert resp.status_code == 200


def test_host_generator(vc_v2):
    '''
    Pull a page of data via the generator to test the API
    '''
    host_gen = vc_v2.get_all_hosts(page_size=1)
    results = next(host_gen)

    assert len(results.json()['results']) == 1
    assert results.json()['count'] > 1


def test_get_hosts_id(vc_v2):
    '''
    Verify the Host IDs returned are the same for different methods of access
    '''
    host_id = vc_v2.get_hosts().json()['results'][0]['id']
    resp = vc_v2.get_host_by_id(host_id=host_id)

    assert resp.json()['id'] == host_id


def test_key_asset(vc_v2):
    '''
    Mark hosts as Key Assets and unmark them
    '''
    host = vc_v2.get_hosts().json()['results'][0]
    host_id = host['id']
    key_asset = host['is_key_asset']

    vc_v2.set_key_asset(host_id=host_id, set=False)

    vc_v2.set_key_asset(host_id=host_id, set=True)
    assert vc_v2.get_host_by_id(host_id=host_id).json()['is_key_asset'] is True

    vc_v2.set_key_asset(host_id=host_id, set=False)
    assert vc_v2.get_host_by_id(host_id=host_id).json()['is_key_asset'] is False

    vc_v2.set_key_asset(host_id=host_id, set=key_asset)


def test_host_tags(vc_v2):
    '''
    Verify Tag creation and appending works
    '''
    host = vc_v2.get_hosts().json()['results'][0]
    host_id = host['id']
    host_tags = host['tags']

    vc_v2.set_host_tags(host_id=host_id, tags=['pytest'])
    assert vc_v2.get_host_tags(host_id=host_id).json()['tags'] == ['pytest']

    vc_v2.set_host_tags(host_id=host_id, tags=['foo', 'bar'], append=True)
    tags = vc_v2.get_host_tags(host_id=host_id).json()['tags']
    tags.sort()
    assert tags == ['bar', 'foo', 'pytest']

    vc_v2.set_host_tags(host_id=host_id, tags=host_tags)
    assert vc_v2.get_host_tags(host_id=host_id).json()['tags'] == host_tags
