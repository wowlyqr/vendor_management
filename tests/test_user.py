import pytest
import json
from app import create_app
from app.config import TestingConfig
from app.models.user import Users

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_user_data():
    return {
        'username': 'tewstuser',
        'email': 'teswt@example.com'
    }

# @pytest.fixture
# def sample_data():
#     return {"name": "Alice", "age": 30}

# # This is a test that uses the fixture
# def test_user_name(sample_data):
#     assert sample_data["name"] == "Alice"

def test_two():
    assert True
    assert 3==3
    assert True

@pytest.mark.skip(reason="Not implemented yet")
def test_skipped():
    assert False  # This won't run
    

class TestUserAPI:
    def test_create_user_success(self, client, sample_user_data):
        response = client.post('/api/v1/users/',
                             data=json.dumps(sample_user_data),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['username'] == sample_user_data['username']

    # def test_create_user_invalid_email(self, client):
    #     invalid_data = {
    #         'username': 'testuser',
    #         'email': 'invalid-email'
    #     }
    #     response = client.post('/api/v1/users/',
    #                          data=json.dumps(invalid_data),
    #                          content_type='application/json')
    #     assert response.status_code == 400
    #     data = json.loads(response.data)
    #     assert data['status'] == 'error'

    # def test_create_user_missing_fields(self, client):
    #     incomplete_data = {'username': 'testuser'}
    #     response = client.post('/api/v1/users/',
    #                          data=json.dumps(incomplete_data),
    #                          content_type='application/json')
    #     assert response.status_code == 400
    #     data = json.loads(response.data)
    #     assert data['status'] == 'error'

    # def test_get_users_empty(self, client):
    #     response = client.get('/api/v1/users/')
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['status'] == 'success'
    #     assert data['users'] == []

    # def test_get_users_with_data(self, client, sample_user_data):
    #     # Create a user first
    #     client.post('/api/v1/users/',
    #                data=json.dumps(sample_user_data),
    #                content_type='application/json')
        
    #     response = client.get('/api/v1/users/')
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['status'] == 'success'
    #     assert len(data['users']) == 1
    #     assert data['users'][0]['username'] == sample_user_data['username']

    # def test_get_user_not_found(self, client):
    #     response = client.get('/api/v1/users/nonexistent-id')
    #     assert response.status_code == 404
    #     data = json.loads(response.data)
    #     assert data['status'] == 'error'
    #     assert data['message'] == 'User not found'

    # def test_get_user_success(self, client, sample_user_data):
    #     # Create a user first
    #     create_response = client.post('/api/v1/users/',
    #                                 data=json.dumps(sample_user_data),
    #                                 content_type='application/json')
    #     user_id = json.loads(create_response.data)['id']
        
    #     response = client.get(f'/api/v1/users/{user_id}')
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['status'] == 'success'
    #     assert data['username'] == sample_user_data['username']
    #     assert data['email'] == sample_user_data['email'] 