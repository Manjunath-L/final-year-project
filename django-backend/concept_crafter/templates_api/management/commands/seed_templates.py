from django.core.management.base import BaseCommand
from templates_api.models import Template

TEMPLATES = [
    {
        "name": "Process Flowchart",
        "type": "flowchart",
        "description": "A simple process flowchart with start, steps, and end nodes.",
        "data": {
            "nodes": [
                {"id": "1", "type": "terminal", "data": {"label": "Start", "color": "#90EE90"}, "position": {"x": 250, "y": 0}},
                {"id": "2", "type": "process",  "data": {"label": "Step 1", "color": "#ADD8E6"}, "position": {"x": 250, "y": 100}},
                {"id": "3", "type": "process",  "data": {"label": "Step 2", "color": "#ADD8E6"}, "position": {"x": 250, "y": 200}},
                {"id": "4", "type": "terminal", "data": {"label": "End",   "color": "#FFB6C1"}, "position": {"x": 250, "y": 300}},
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2", "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e2-3", "source": "2", "target": "3", "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e3-4", "source": "3", "target": "4", "animated": False, "markerEnd": {"type": "arrowclosed"}},
            ],
        },
    },
    {
        "name": "Brainstorming Map",
        "type": "mindmap",
        "description": "A mindmap with a central idea and four branches for brainstorming.",
        "data": {
            "rootId": "root",
            "nodes": {
                "root":    {"id": "root",    "text": "Central Idea", "children": ["b1", "b2", "b3", "b4"], "color": "#4CAF50"},
                "b1":      {"id": "b1",      "text": "Branch 1",     "children": [], "color": "#2196F3"},
                "b2":      {"id": "b2",      "text": "Branch 2",     "children": [], "color": "#FF9800"},
                "b3":      {"id": "b3",      "text": "Branch 3",     "children": [], "color": "#9C27B0"},
                "b4":      {"id": "b4",      "text": "Branch 4",     "children": [], "color": "#F44336"},
            },
        },
    },
    {
        "name": "Decision Tree",
        "type": "flowchart",
        "description": "A decision tree with a decision diamond and yes/no branches.",
        "data": {
            "nodes": [
                {"id": "1", "type": "terminal", "data": {"label": "Start",       "color": "#90EE90"}, "position": {"x": 250, "y": 0}},
                {"id": "2", "type": "decision",  "data": {"label": "Decision?",  "color": "#FFFACD"}, "position": {"x": 250, "y": 100}},
                {"id": "3", "type": "process",   "data": {"label": "Yes Path",   "color": "#ADD8E6"}, "position": {"x": 100, "y": 200}},
                {"id": "4", "type": "process",   "data": {"label": "No Path",    "color": "#ADD8E6"}, "position": {"x": 400, "y": 200}},
                {"id": "5", "type": "terminal",  "data": {"label": "End",        "color": "#FFB6C1"}, "position": {"x": 250, "y": 300}},
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2", "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e2-3", "source": "2", "target": "3", "label": "Yes", "sourceHandle": "left",  "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e2-4", "source": "2", "target": "4", "label": "No",  "sourceHandle": "right", "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e3-5", "source": "3", "target": "5", "animated": False, "markerEnd": {"type": "arrowclosed"}},
                {"id": "e4-5", "source": "4", "target": "5", "animated": False, "markerEnd": {"type": "arrowclosed"}},
            ],
        },
    },
    {
        "name": "Concept Map",
        "type": "mindmap",
        "description": "A concept map with a main concept and related concepts.",
        "data": {
            "rootId": "root",
            "nodes": {
                "root": {"id": "root", "text": "Main Concept",     "children": ["c1", "c2", "c3"], "color": "#4CAF50"},
                "c1":   {"id": "c1",   "text": "Related Concept 1","children": [], "color": "#2196F3"},
                "c2":   {"id": "c2",   "text": "Related Concept 2","children": [], "color": "#FF9800"},
                "c3":   {"id": "c3",   "text": "Related Concept 3","children": [], "color": "#9C27B0"},
            },
        },
    },
]


class Command(BaseCommand):
    help = "Seed the database with default diagram templates."

    def handle(self, *args, **options):
        created_count = 0
        for tpl in TEMPLATES:
            name = tpl["name"]
            _, created = Template.objects.get_or_create(
                name=name,
                defaults={
                    "type":        tpl["type"],
                    "data":        tpl["data"],
                    "description": tpl["description"],
                    "thumbnail":   "",
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {name}"))
            else:
                self.stdout.write(f"  Already exists: {name}")

        self.stdout.write(self.style.SUCCESS(
            f"Done. {created_count} template(s) created, {len(TEMPLATES) - created_count} already existed."
        ))
