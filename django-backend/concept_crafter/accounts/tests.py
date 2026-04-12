import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REGISTER_URL = '/api/auth/register/'
LOGIN_URL = '/api/auth/login/'
LOGOUT_URL = '/api/auth/logout/'
ME_URL = '/api/auth/me/'

VALID_REGISTER_PAYLOAD = {
    'username': 'newuser',
    'email': 'newuser@example.com',
    'password': 'securepass123',
}


def make_client():
    return APIClient()


def create_user(username='testuser', email='test@example.com', password='testpass123'):
    return User.objects.create_user(username=username, email=email, password=password)


def auth_client_for(user):
    client = make_client()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client, str(refresh)


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_register_valid_data_returns_201_with_token_refresh_user():
    client = make_client()
    response = client.post(REGISTER_URL, VALID_REGISTER_PAYLOAD, format='json')

    assert response.status_code == 201
    data = response.json()
    assert 'token' in data
    assert 'refresh' in data
    assert 'user' in data
    assert data['user']['username'] == VALID_REGISTER_PAYLOAD['username']
    assert data['user']['email'] == VALID_REGISTER_PAYLOAD['email']


@pytest.mark.django_db
def test_register_duplicate_username_returns_400():
    create_user(username='existinguser', email='existing@example.com')
    client = make_client()
    response = client.post(REGISTER_URL, {
        'username': 'existinguser',
        'email': 'other@example.com',
        'password': 'somepass123',
    }, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_missing_fields_returns_400():
    client = make_client()
    # Missing password
    response = client.post(REGISTER_URL, {
        'username': 'someuser',
        'email': 'someuser@example.com',
    }, format='json')

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_login_valid_credentials_returns_200_with_token_refresh_user():
    create_user(username='loginuser', email='login@example.com', password='mypassword')
    client = make_client()
    response = client.post(LOGIN_URL, {
        'username': 'loginuser',
        'password': 'mypassword',
    }, format='json')

    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    assert 'refresh' in data
    assert 'user' in data
    assert data['user']['username'] == 'loginuser'


@pytest.mark.django_db
def test_login_wrong_password_returns_400_with_message():
    create_user(username='loginuser2', email='login2@example.com', password='correctpass')
    client = make_client()
    response = client.post(LOGIN_URL, {
        'username': 'loginuser2',
        'password': 'wrongpass',
    }, format='json')

    assert response.status_code == 400
    data = response.json()
    assert data.get('message') == 'Invalid username or password'


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_logout_with_valid_refresh_token_returns_200():
    user = create_user(username='logoutuser', email='logout@example.com', password='pass123')
    client, refresh_token = auth_client_for(user)

    response = client.post(LOGOUT_URL, {'refresh': refresh_token}, format='json')

    assert response.status_code == 200
    assert response.json().get('message') == 'Logout successful'


# ---------------------------------------------------------------------------
# Me
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_me_with_valid_token_returns_200_with_user():
    user = create_user(username='meuser', email='me@example.com', password='pass123')
    client, _ = auth_client_for(user)

    response = client.get(ME_URL)

    assert response.status_code == 200
    data = response.json()
    assert 'user' in data
    assert data['user']['username'] == 'meuser'
    assert data['user']['email'] == 'me@example.com'


@pytest.mark.django_db
def test_me_without_token_returns_401():
    client = make_client()
    response = client.get(ME_URL)

    assert response.status_code == 401
