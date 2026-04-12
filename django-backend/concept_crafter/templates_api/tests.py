import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from templates_api.models import Template


TEMPLATES_URL = '/api/templates/'

EXPECTED_TEMPLATE_NAMES = [
    'Process Flowchart',
    'Brainstorming Map',
    'Decision Tree',
    'Concept Map',
]


# ---------------------------------------------------------------------------
# seed_templates management command
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_seed_templates_creates_exactly_4_templates():
    call_command('seed_templates', verbosity=0)
    assert Template.objects.count() == 4


@pytest.mark.django_db
def test_seed_templates_creates_correct_names():
    call_command('seed_templates', verbosity=0)
    names = list(Template.objects.values_list('name', flat=True))
    for expected in EXPECTED_TEMPLATE_NAMES:
        assert expected in names


@pytest.mark.django_db
def test_seed_templates_creates_correct_types():
    call_command('seed_templates', verbosity=0)
    flowcharts = Template.objects.filter(type='flowchart').count()
    mindmaps = Template.objects.filter(type='mindmap').count()
    assert flowcharts == 2
    assert mindmaps == 2


@pytest.mark.django_db
def test_seed_templates_is_idempotent():
    """Running seed_templates twice should not create duplicates."""
    call_command('seed_templates', verbosity=0)
    call_command('seed_templates', verbosity=0)
    assert Template.objects.count() == 4


# ---------------------------------------------------------------------------
# GET /api/templates/
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_get_templates_returns_200():
    call_command('seed_templates', verbosity=0)
    client = APIClient()
    response = client.get(TEMPLATES_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_templates_returns_all_seeded_templates():
    call_command('seed_templates', verbosity=0)
    client = APIClient()
    response = client.get(TEMPLATES_URL)
    data = response.json()
    assert len(data) == 4


@pytest.mark.django_db
def test_get_templates_returns_correct_fields():
    call_command('seed_templates', verbosity=0)
    client = APIClient()
    response = client.get(TEMPLATES_URL)
    data = response.json()
    for template in data:
        assert 'id' in template
        assert 'name' in template
        assert 'type' in template
        assert 'data' in template
        assert 'thumbnail' in template
        assert 'description' in template


@pytest.mark.django_db
def test_get_templates_returns_correct_names():
    call_command('seed_templates', verbosity=0)
    client = APIClient()
    response = client.get(TEMPLATES_URL)
    names = [t['name'] for t in response.json()]
    for expected in EXPECTED_TEMPLATE_NAMES:
        assert expected in names


@pytest.mark.django_db
def test_get_templates_accessible_without_auth():
    """Templates endpoint is public (AllowAny)."""
    call_command('seed_templates', verbosity=0)
    client = APIClient()
    response = client.get(TEMPLATES_URL)
    assert response.status_code == 200
