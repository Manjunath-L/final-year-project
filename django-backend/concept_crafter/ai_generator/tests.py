import json
from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


GENERATE_URL = '/api/generate/'

VALID_MINDMAP_JSON = {
    'rootId': '1',
    'nodes': {
        '1': {'id': '1', 'text': 'Central Topic', 'children': ['2', '3'], 'color': '#4CAF50'},
        '2': {'id': '2', 'text': 'Branch 1', 'children': [], 'color': '#2196F3'},
        '3': {'id': '3', 'text': 'Branch 2', 'children': [], 'color': '#FF9800'},
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_client():
    return APIClient()


def create_user(username='genuser', email='gen@example.com', password='pass123'):
    return User.objects.create_user(username=username, email=email, password=password)


def auth_client_for(user):
    client = make_client()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client


def mock_openrouter_response(content):
    """Build a mock requests.Response that returns the given content string."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {
        'choices': [{'message': {'content': content}}]
    }
    return mock_resp


# ---------------------------------------------------------------------------
# Validation errors (no auth needed to hit 400, but auth is required first)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_generate_without_type_returns_400():
    user = create_user()
    client = auth_client_for(user)
    response = client.post(GENERATE_URL, {'prompt': 'solar system'}, format='json')
    assert response.status_code == 400
    assert response.json().get('message') == 'Type and prompt are required'


@pytest.mark.django_db
def test_generate_without_prompt_returns_400():
    user = create_user()
    client = auth_client_for(user)
    response = client.post(GENERATE_URL, {'type': 'mindmap'}, format='json')
    assert response.status_code == 400
    assert response.json().get('message') == 'Type and prompt are required'


@pytest.mark.django_db
def test_generate_with_invalid_type_returns_400():
    user = create_user()
    client = auth_client_for(user)
    response = client.post(GENERATE_URL, {'type': 'invalid', 'prompt': 'test'}, format='json')
    assert response.status_code == 400
    assert response.json().get('message') == "Type must be either 'mindmap' or 'flowchart'"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_generate_without_auth_returns_401():
    client = make_client()
    response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'test'}, format='json')
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# OpenRouter error handling
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_generate_openrouter_request_error_returns_500():
    import requests as req_lib
    user = create_user()
    client = auth_client_for(user)

    with patch('ai_generator.views.requests.post', side_effect=req_lib.RequestException('connection error')):
        response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'test'}, format='json')

    assert response.status_code == 500
    assert 'Failed to communicate with AI service' in response.json().get('message', '')


@pytest.mark.django_db
def test_generate_openrouter_returns_non_json_content_returns_500():
    user = create_user()
    client = auth_client_for(user)

    mock_resp = mock_openrouter_response('this is not json at all !!!')

    with patch('ai_generator.views.requests.post', return_value=mock_resp):
        response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'test'}, format='json')

    assert response.status_code == 500
    assert 'invalid JSON' in response.json().get('message', '')


# ---------------------------------------------------------------------------
# Successful generation
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_generate_mindmap_with_valid_json_returns_200():
    user = create_user()
    client = auth_client_for(user)

    mock_resp = mock_openrouter_response(json.dumps(VALID_MINDMAP_JSON))

    with patch('ai_generator.views.requests.post', return_value=mock_resp):
        response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'solar system'}, format='json')

    assert response.status_code == 200
    data = response.json()
    assert 'rootId' in data
    assert 'nodes' in data


@pytest.mark.django_db
def test_generate_mindmap_with_json_wrapped_in_markdown_fences_returns_200():
    user = create_user()
    client = auth_client_for(user)

    wrapped = f'```json\n{json.dumps(VALID_MINDMAP_JSON)}\n```'
    mock_resp = mock_openrouter_response(wrapped)

    with patch('ai_generator.views.requests.post', return_value=mock_resp):
        response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'solar system'}, format='json')

    assert response.status_code == 200
    data = response.json()
    assert 'rootId' in data
    assert 'nodes' in data


@pytest.mark.django_db
def test_generate_mindmap_with_plain_markdown_fences_returns_200():
    """Handles ``` fences without the 'json' language tag."""
    user = create_user()
    client = auth_client_for(user)

    wrapped = f'```\n{json.dumps(VALID_MINDMAP_JSON)}\n```'
    mock_resp = mock_openrouter_response(wrapped)

    with patch('ai_generator.views.requests.post', return_value=mock_resp):
        response = client.post(GENERATE_URL, {'type': 'mindmap', 'prompt': 'solar system'}, format='json')

    assert response.status_code == 200
    data = response.json()
    assert 'rootId' in data
