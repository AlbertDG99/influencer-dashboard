def test_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'


def test_influencers_list(client):
    res = client.get('/api/influencers')
    assert res.status_code == 200
    data = res.get_json()
    assert 'items' in data
    assert data['page'] == 1


def test_influencer_detail(client):
    res = client.get('/api/influencers/1')
    assert res.status_code == 200
    item = res.get_json()
    assert item['id'] == '1'


def test_export_csv(client):
    res = client.get('/api/export/csv')
    assert res.status_code == 200
    assert res.mimetype == 'text/csv'


def test_export_xlsx(client):
    res = client.get('/api/export/xlsx')
    assert res.status_code == 200
    assert res.mimetype.startswith('application/vnd.openxmlformats-officedocument')
