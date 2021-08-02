from app import app
#def test_smth():
#    1 + 1 == 2

#def test_home():
#    client = app.test_client()
#    response = client.get('/')
#    assert response.status_code == 200

def test_characters():
    client = app.test_client()
    response = client.get('/characters')
    assert response.status_code == 200

#def test_planets():
#    client = app.test_client()
#    response = client.get('/planets')
#    assert response.status_code == 200

#def test_updatedb():
#    client = app.test_client()
#    response = client.get('/updatedb')
#    assert response.status_code == 200