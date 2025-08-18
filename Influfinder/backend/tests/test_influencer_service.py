from backend.domain.services.influencer_service import InfluencerService
from backend.infrastructure.repositories.memory_influencer_repository import InMemoryInfluencerRepository


def make_service():
    return InfluencerService(repository=InMemoryInfluencerRepository())


def test_search_by_category():
    svc = make_service()
    result = svc.search_influencers(query=None, category='fitness', language=None, page=1, page_size=50)
    assert result['items']
    assert all('fitness' in [c.lower() for c in i['categories']] for i in result['items'])


def test_hashtag_search():
    svc = make_service()
    result = svc.search_by_hashtag(hashtag='gaming', page=1, page_size=50)
    assert result['items']


def test_not_found():
    svc = make_service()
    try:
        svc.get_by_id('nope')
        assert False, 'should raise'
    except Exception as e:
        assert 'no encontrado' in str(e) or 'not' in str(e).lower()

