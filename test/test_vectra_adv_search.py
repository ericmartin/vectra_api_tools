'''
Excercise the Advanced Search Features
'''
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

def test_critical_quad_host_count(vc_v2):
    '''
    Verify get_hosts and advanced_search return the same results to verify each call
    '''
    basic_count = vc_v2.get_hosts(certainty_gte=50, threat_gte=50).json()['count']
    adv_generator = vc_v2.advanced_search(stype='hosts',
        query='host.certainty:>=50 and host.threat:>=50')
    results = next(adv_generator)

    assert results.json()['count'] == basic_count


def test_ip_search(vc_v2):
    '''
    Verify get_hosts and advanced search return the same results for IPs
    '''
    test_ip = vc_v2.get_hosts().json()['results'][-1]['last_source']
    basic_host_id = vc_v2.get_hosts(last_source=test_ip).json()['results'][0]['id']
    adv_host_gen = vc_v2.advanced_search(
                            stype='hosts',
                            query=f'host.last_source:{test_ip}'
                        )
    adv_host_id = next(adv_host_gen)
    returned_ids = []
    for host in adv_host_id.json()['results']:
        returned_ids.append(host['id'])
    assert basic_host_id in returned_ids


def test_page_size(vc_v2):
    '''
    Check the page size is returned properly
    Default = 50
    '''

    ret_objects = vc_v2.advanced_search(
                        stype='hosts',
                        query='host.state:"active" OR host.state:"inactive"')
    results = next(ret_objects).json()['results']

    assert  len(results) == 50, "Default Page Size is 50"

    ret_objects = vc_v2.advanced_search(
                        stype='hosts', page_size=100,
                        query='host.state:"active" OR host.state:"inactive"')
    results = next(ret_objects).json()['results']
    assert len(results) == 100

    ret_objects = vc_v2.advanced_search(
                        stype='hosts', page_size=17,
                        query='host.state:"active" OR host.state:"inactive"')
    results = next(ret_objects).json()['results']

    assert len(results) == 17


def test_medium_and_critical_detection_count(vc_v2):
    '''
    Verify we are reciving the proper counts for Certainty >= 50 (Medium / Critical)
    '''
    basic_count = vc_v2.get_detections(certainty_gte=50).json()['count']
    adv_gen = vc_v2.advanced_search(
                    stype='detections',
                    page_size=5000,
                    query='detection.certainty:>=50'
                )
    adv_count = next(adv_gen)

    # basic search returns triaged detections
    assert adv_count.json()['count'] <= basic_count
