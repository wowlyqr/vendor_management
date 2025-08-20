import pytest
import json
from app import create_app
from app.config import TestingConfig
from app.models.user import Users

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDA1MDUyOCwianRpIjoiNDc4NjM5MjgtMDVlMi00MTU5LTg3NGQtYWU1N2JmNTAwYTNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZhOGFiZWZjLTdmOTEtNDE4Mi04YjQ1LTdkNTJmNWM5YjFjZiIsIm5iZiI6MTc1NDA1MDUyOCwiY3NyZiI6Ijc1YzEwZTJjLWVmNzEtNDE2MC1iMmIyLTU4NTEyOGI4NTVlMCIsImV4cCI6MTc1NDA1NzcyOCwicm9sZXMiOiJ2ZW5kb3Jfb3duZXIifQ.5VsPdxsx6I7XDMwDnVKGdysuyVfWGIDHdwhXPOx26wk'
headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_user_data():
    return {
        "name": "test",
        "email": "vendorll20@gmail.com",
        "password": "Test@123",
        "user_type": "users",
        "mobile": 7771000000,
        "country_code": 91,
        "gender":"Male",
        "brand_name":"unit test",
        "address":"unit test",
        "pincode":852147
    }

#
@pytest.mark.skip(reason="Not implemented yet")
def test_skipped():
    assert False  # This won't run
    

class TestVendorOwnerAPI:
    def test_create_user_success(self, client, sample_user_data):
        response = client.post('/api/v1/vendor_owner/create_vendor_owner',
                             data=json.dumps(sample_user_data),
                             headers=headers
                             )
        import pdb;pdb.set_trace()
        assert response.status == '201 CREATED'
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['username'] == sample_user_data['username']
