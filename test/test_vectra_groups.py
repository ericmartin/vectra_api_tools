import pytest
import requests

requests.urllib3.disable_warnings()

test_vars = {}



@pytest.fixture()
def test_host(vc_v2):
    return vc_v2.get_hosts().json()['results'][-1]


@pytest.fixture()
def test_host2(vc_v2):
    return vc_v2.get_hosts().json()['results'][-2]


@pytest.fixture()
def test_host4(vc_v2_4):
    return vc_v2_4.get_hosts().json()['results'][-2]

# TODO Group tests into classes; host, ip, sensor_luid, all_hosts


def test_create_group_account(vc_v2_4, test_host):
    group_type = 'account'
    resp = vc_v2_4.create_group(name=f'pytest - {group_type}',
                              description=f'pytest test {group_type} group',
                              type=group_type)
    test_vars['host_rule_id'] = resp.json().get('id', None)
    assert resp.status_code == 201


def test_create_group_domain(vc_v2, test_host):
    group_type = 'domain'
    resp = vc_v2.create_group(name=f'pytest - {group_type}',
                              description=f'pytest test {group_type} group',
                              type=group_type,
                              members=['vectra.ai'])
    test_vars['host_rule_id'] = resp.json().get('id', None)
    assert resp.status_code == 201


def test_create_group_host(vc_v2, test_host):
    group_type = 'host'
    resp = vc_v2.create_group(name=f'pytest - {group_type}',
                              description=f'pytest test {group_type} group',
                              type=group_type)
    test_vars['host_rule_id'] = resp.json().get('id', None)
    assert resp.status_code == 201


def test_create_group_ip(vc_v2, test_host):
    group_type = 'ip'
    resp = vc_v2.create_group(name=f'pytest - {group_type}',
                              description=f'pytest test {group_type} group',
                              type=group_type)
    test_vars['host_rule_id'] = resp.json().get('id', None)
    assert resp.status_code == 201



def test_create_rule_sensor_luid(vc_v2):
    pass


def test_create_rule_all_hosts(vc_v2):
    resp = vc_v2.create_rule(detection_category='botnet activity', detection_type='outbound port sweep',
                             triage_category='misconfiguration', description='pytest_all', all_hosts=True,
                             remote1_port=['443'])
    test_vars['host_rule_all_hosts'] = resp.json().get('id', None)
    assert resp.status_code == 201


def test_get_rules(vc_v2):
    resp = vc_v2.get_rules().json()
    assert resp['count'] >= 3

    resp2 = vc_v2.get_rules(name='pytest_hostname')
    assert resp2['description'] == 'pytest_hostname'


def test_update_rule_replace(vc_v2, test_host2):
    host_url = test_host2['url']
    resp = vc_v2.update_rule(rule_id=test_vars['host_rule_id'], host=[host_url], remote1_dns=['foo.com'],
                             remote1_ip=['4.4.4.4'], remote1_port=['8443'])
    assert resp.status_code == 200

    resp2 = vc_v2.get_rules(rule_id=test_vars['host_rule_id']).json()
    assert [host_url] == resp2['host']
    assert ['foo.com'] == resp2['remote1_dns']
    assert ['4.4.4.4'] == resp2['remote1_ip']
    assert ['8443'] == resp2['remote1_port']


def test_update_rule_append(vc_v2, test_host):
    resp = vc_v2.update_rule(rule_id=test_vars['host_rule_ip'], append = True, ip=['254.254.254.254'],
                             remote1_dns=['foo.com'], remote1_ip=['4.4.4.4'], remote1_port=['8443'])
    assert resp.status_code == 200

    resp2 = vc_v2.get_rules(rule_id=test_vars['host_rule_ip']).json()
    assert all(ip in resp2['ip'] for ip in [test_host['last_source'], '254.254.254.254'])
    assert all(domain in resp2['remote1_dns'] for domain in ['google.com', 'foo.com'])
    assert all(ip in resp2['remote1_ip'] for ip in ['8.8.8.8', '4.4.4.4'])
    assert all(port in resp2['remote1_port'] for port in ['443', '8443'])


def test_delete_rule(vc_v2):
    resp1 = vc_v2.delete_rule(rule_id=test_vars['host_rule_id'])
    resp2 = vc_v2.delete_rule(rule_id=test_vars['host_rule_ip'])
    resp3 = vc_v2.delete_rule(rule_id=test_vars['host_rule_all_hosts'])

    assert all(resp.status_code == 204 for resp in [resp1, resp2, resp3])
