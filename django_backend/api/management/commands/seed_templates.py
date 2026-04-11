from django.core.management.base import BaseCommand
from api.models import Template


TEMPLATES = [
    {
        'name': 'Process Flowchart',
        'type': 'flowchart',
        'description': 'Standard template for process documentation',
        'data': {
            'nodes': [
                {'id': '1', 'type': 'terminal', 'data': {'label': 'Start', 'color': '#90EE90'}, 'position': {'x': 250, 'y': 0}},
                {'id': '2', 'type': 'process', 'data': {'label': 'Process Step 1', 'color': '#ADD8E6'}, 'position': {'x': 250, 'y': 100}},
                {'id': '3', 'type': 'process', 'data': {'label': 'Process Step 2', 'color': '#ADD8E6'}, 'position': {'x': 250, 'y': 200}},
                {'id': '4', 'type': 'terminal', 'data': {'label': 'End', 'color': '#FFB6C1'}, 'position': {'x': 250, 'y': 300}},
            ],
            'edges': [
                {'id': 'e1-2', 'source': '1', 'target': '2', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e2-3', 'source': '2', 'target': '3', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e3-4', 'source': '3', 'target': '4', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
            ],
        },
    },
    {
        'name': 'Brainstorming Map',
        'type': 'mindmap',
        'description': 'Ideal for creative thinking sessions',
        'data': {
            'rootId': '1',
            'nodes': {
                '1': {'id': '1', 'text': 'Central Topic', 'children': ['2', '3', '4'], 'color': '#4CAF50'},
                '2': {'id': '2', 'text': 'Idea 1', 'children': ['5', '6'], 'color': '#2196F3'},
                '3': {'id': '3', 'text': 'Idea 2', 'children': ['7', '8'], 'color': '#FF9800'},
                '4': {'id': '4', 'text': 'Idea 3', 'children': ['9', '10'], 'color': '#9C27B0'},
                '5': {'id': '5', 'text': 'Detail 1.1', 'children': [], 'color': '#2196F3'},
                '6': {'id': '6', 'text': 'Detail 1.2', 'children': [], 'color': '#2196F3'},
                '7': {'id': '7', 'text': 'Detail 2.1', 'children': [], 'color': '#FF9800'},
                '8': {'id': '8', 'text': 'Detail 2.2', 'children': [], 'color': '#FF9800'},
                '9': {'id': '9', 'text': 'Detail 3.1', 'children': [], 'color': '#9C27B0'},
                '10': {'id': '10', 'text': 'Detail 3.2', 'children': [], 'color': '#9C27B0'},
            },
        },
    },
    {
        'name': 'Decision Tree',
        'type': 'flowchart',
        'description': 'For mapping out decision points',
        'data': {
            'nodes': [
                {'id': '1', 'type': 'terminal', 'data': {'label': 'Start', 'color': '#90EE90'}, 'position': {'x': 250, 'y': 0}},
                {'id': '2', 'type': 'decision', 'data': {'label': 'Decision?', 'color': '#FFFACD'}, 'position': {'x': 250, 'y': 100}},
                {'id': '3', 'type': 'process', 'data': {'label': 'Option A', 'color': '#ADD8E6'}, 'position': {'x': 100, 'y': 200}},
                {'id': '4', 'type': 'process', 'data': {'label': 'Option B', 'color': '#ADD8E6'}, 'position': {'x': 400, 'y': 200}},
                {'id': '5', 'type': 'terminal', 'data': {'label': 'End A', 'color': '#FFB6C1'}, 'position': {'x': 100, 'y': 300}},
                {'id': '6', 'type': 'terminal', 'data': {'label': 'End B', 'color': '#FFB6C1'}, 'position': {'x': 400, 'y': 300}},
            ],
            'edges': [
                {'id': 'e1-2', 'source': '1', 'target': '2', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e2-3', 'source': '2', 'target': '3', 'label': 'Yes', 'sourceHandle': 'left', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e2-4', 'source': '2', 'target': '4', 'label': 'No', 'sourceHandle': 'right', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e3-5', 'source': '3', 'target': '5', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
                {'id': 'e4-6', 'source': '4', 'target': '6', 'animated': False, 'markerEnd': {'type': 'arrowclosed'}},
            ],
        },
    },
    {
        'name': 'Concept Map',
        'type': 'mindmap',
        'description': 'Connect complex ideas and concepts',
        'data': {
            'rootId': '1',
            'nodes': {
                '1': {'id': '1', 'text': 'Main Concept', 'children': ['2', '3', '4'], 'color': '#4CAF50'},
                '2': {'id': '2', 'text': 'Concept 1', 'children': ['5', '6'], 'color': '#2196F3'},
                '3': {'id': '3', 'text': 'Concept 2', 'children': ['7', '8'], 'color': '#FF9800'},
                '4': {'id': '4', 'text': 'Concept 3', 'children': ['9', '10'], 'color': '#9C27B0'},
                '5': {'id': '5', 'text': 'Detail 1.1', 'children': [], 'color': '#2196F3'},
                '6': {'id': '6', 'text': 'Detail 1.2', 'children': [], 'color': '#2196F3'},
                '7': {'id': '7', 'text': 'Detail 2.1', 'children': [], 'color': '#FF9800'},
                '8': {'id': '8', 'text': 'Detail 2.2', 'children': [], 'color': '#FF9800'},
                '9': {'id': '9', 'text': 'Detail 3.1', 'children': [], 'color': '#9C27B0'},
                '10': {'id': '10', 'text': 'Detail 3.2', 'children': [], 'color': '#9C27B0'},
            },
        },
    },
]


class Command(BaseCommand):
    help = 'Seed default templates'

    def handle(self, *args, **kwargs):
        for t in TEMPLATES:
            Template.objects.get_or_create(name=t['name'], defaults=t)
            self.stdout.write(f"  Seeded: {t['name']}")
        self.stdout.write(self.style.SUCCESS('Templates seeded successfully.'))
