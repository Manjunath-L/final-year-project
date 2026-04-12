import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from projects.models import Project


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROJECTS_URL = '/api/projects/'


def make_client():
    return APIClient()


def create_user(username='testuser', email='test@example.com', password='testpass123'):
    return User.objects.create_user(username=username, email=email, password=password)


def auth_client_for(user):
    client = make_client()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client


def create_project(user, name='Test Project', project_type='mindmap'):
    return Project.objects.create(user=user, name=name, project_type=project_type)


# ---------------------------------------------------------------------------
# List projects
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_list_projects_with_valid_token_returns_200_with_user_projects():
    user = create_user()
    create_project(user, name='Project A')
    create_project(user, name='Project B')

    # Another user's project should not appear
    other = create_user(username='other', email='other@example.com')
    create_project(other, name='Other Project')

    client = auth_client_for(user)
    response = client.get(PROJECTS_URL)

    assert response.status_code == 200
    data = response.json()
    names = [p['name'] for p in data]
    assert 'Project A' in names
    assert 'Project B' in names
    assert 'Other Project' not in names


@pytest.mark.django_db
def test_list_projects_without_token_returns_401():
    client = make_client()
    response = client.get(PROJECTS_URL)

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Create project
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_create_project_with_valid_data_returns_201_with_type_field():
    user = create_user()
    client = auth_client_for(user)

    payload = {'name': 'New Mind Map', 'type': 'mindmap'}
    response = client.post(PROJECTS_URL, payload, format='json')

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'New Mind Map'
    assert data['type'] == 'mindmap'
    assert 'id' in data


@pytest.mark.django_db
def test_create_project_flowchart_type_returns_201():
    user = create_user()
    client = auth_client_for(user)

    payload = {'name': 'My Flowchart', 'type': 'flowchart'}
    response = client.post(PROJECTS_URL, payload, format='json')

    assert response.status_code == 201
    assert response.json()['type'] == 'flowchart'


# ---------------------------------------------------------------------------
# Retrieve project
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_get_own_project_returns_200():
    user = create_user()
    project = create_project(user)
    client = auth_client_for(user)

    response = client.get(f'{PROJECTS_URL}{project.id}/')

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == project.id
    assert data['name'] == project.name


@pytest.mark.django_db
def test_get_other_users_project_returns_404():
    user = create_user()
    other = create_user(username='other', email='other@example.com')
    project = create_project(other, name='Other Project')

    client = auth_client_for(user)
    response = client.get(f'{PROJECTS_URL}{project.id}/')

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Update project
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_update_project_returns_200_with_updated_data():
    user = create_user()
    project = create_project(user, name='Old Name')
    client = auth_client_for(user)

    payload = {'name': 'Updated Name', 'type': 'flowchart'}
    response = client.put(f'{PROJECTS_URL}{project.id}/', payload, format='json')

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Updated Name'
    assert data['type'] == 'flowchart'


# ---------------------------------------------------------------------------
# Delete project
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_delete_project_returns_204():
    user = create_user()
    project = create_project(user)
    client = auth_client_for(user)

    response = client.delete(f'{PROJECTS_URL}{project.id}/')

    assert response.status_code == 204
    assert not Project.objects.filter(id=project.id).exists()
