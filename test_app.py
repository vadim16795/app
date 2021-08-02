from app import app
def test_smth():
    1 + 1 == 2

def test_more():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
