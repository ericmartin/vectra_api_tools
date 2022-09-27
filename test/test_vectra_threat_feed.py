'''
Test Threat Feeds
'''
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

test_vars = {}


def test_create_feed(vc_v2):
    '''
    Create Threat Feeds
    '''
    resp = vc_v2.create_feed(
                name='pytest',
                category='cnc',
                certainty='Medium',
                itype='Watchlist',
                duration=14
    )
    test_vars['threatFeed'] = resp.json()['threatFeed']['id']
    assert resp.status_code == 201


def test_get_feeds(vc_v2):
    '''
    Get the list of feeds; should be > 0
    '''
    feeds = vc_v2.get_feeds()
    assert len(feeds.json()['threatFeeds']) > 0


def test_get_feed_by_name(vc_v2):
    '''
    Get the first Threat Feed, then obtain that feed by name and verify they are the same
    '''
    feed = vc_v2.get_feeds().json()['threatFeeds'][0]
    name = feed['name']
    feed_id = feed['id']
    assert vc_v2.get_feed_by_name(name=name) == feed_id


def test_post_stix_file(vc_v2):
    '''
    Post a STIX file
    '''
    resp = vc_v2.post_stix_file(feed_id=test_vars['threatFeed'], stix_file='test/stix.xml')
    assert resp.status_code == 200


def test_delete_feed(vc_v2):
    '''
    Delete a STIX feed that we created
    '''
    resp = vc_v2.delete_feed(feed_id=test_vars['threatFeed'])
    assert resp.status_code == 200
