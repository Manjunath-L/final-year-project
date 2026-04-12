import json
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

COMPLEXITY_MAP = {
    'simple': 5,
    'medium': 8,
    'complex': 15,
    'comprehensive': 20,
}

MINDMAP_SYSTEM_PROMPT = '''Create a mind map structure based on the user's input topic: "{prompt}".
Output MUST be valid JSON with exactly this structure:
{{
  "rootId": "1",
  "nodes": {{
    "1": {{ 
      "id": "1", 
      "text": "Central Topic",  
      "children": ["2", "3"],
      "color": "#4CAF50"
    }},
    "2": {{
      "id": "2", 
      "text": "Main Branch 1", 
      "children": ["4", "5"],
      "color": "#2196F3"
    }}
  }}
}}

Requirements:
1. The "rootId" must be "1" and point to the central topic node
2. Each node MUST have "id", "text", and "children" properties
3. Node IDs must be unique strings (can be numbers as strings)
4. Use descriptive, short text for each node
5. Include "color" property with hex color values for each node
6. Create a hierarchical structure with meaningful branches
7. Respond ONLY with valid JSON, no other text'''

FLOWCHART_SYSTEM_PROMPT = '''Create a flowchart structure based on the user's input process: "{prompt}".
Output MUST be valid JSON with exactly this structure:
{{
  "nodes": [
    {{
      "id": "1",
      "type": "terminal",
      "data": {{ "label": "Start", "color": "#90EE90" }},
      "position": {{ "x": 250, "y": 0 }}
    }},
    {{
      "id": "2",
      "type": "process", 
      "data": {{ "label": "Process Step", "color": "#ADD8E6" }},
      "position": {{ "x": 250, "y": 100 }}
    }}
  ],
  "edges": [
    {{ 
      "id": "e1-2", 
      "source": "1", 
      "target": "2",
      "label": null,
      "animated": false,
      "markerEnd": {{ "type": "arrowclosed" }}
    }}
  ]
}}

Requirements:
1. Use these node types correctly:
   - "terminal" for start/end nodes (oval shaped, for "Start" and "End" nodes only)
   - "process" for process steps (rectangle)
   - "decision" for yes/no decisions (diamond)
   - "input" for input operations (parallelogram)
   - "output" for output operations (parallelogram)
   - "document" for document outputs
   - "manual_input" for manual input operations
   - "display" for information display
   - "preparation" for initialization steps
   - "connector" for flow connections
   - "data_storage" for data storage operations
   - "database" for database operations
   - "merge" for combining flows
   - "delay" for waiting periods
   - "alternate_process" for alternative steps

2. Node color coding is mandatory:
   - For terminal "Start" nodes, use color: "#90EE90" (light green)
   - For terminal "End" nodes, use color: "#FFB6C1" (light red)
   - For decision nodes, use color: "#FFFACD" (light yellow)
   - For process nodes, use color: "#ADD8E6" (light blue)
   - For input nodes, use color: "#F0E68C" (light gold)
   - For output nodes, use color: "#D8BFD8" (light purple)
   - For document nodes, use color: "#FFE4B5" (light orange)

3. Each node MUST have id, type, data.label, data.color, and position properties
4. Each edge MUST have id, source, target, animated:false, and markerEnd:{{"type":"arrowclosed"}}
5. Label all edges between decision nodes and their targets. Decision nodes MUST have TWO outgoing edges:
   - Edge from decision to Yes path must have label: "Yes" 
   - Edge from decision to No path must have label: "No"
   - Yes path should be on the LEFT side of the decision (lower x position)
   - No path should be on the RIGHT side of the decision (higher x position)
   - For edges from decision nodes, include sourceHandle:"left" or sourceHandle:"right"

6. Position nodes precisely:
   - First node (Start) at x:250, y:0
   - Vertical distance between primary flow nodes: 100px
   - Branching nodes (from decision Yes/No):
     * Yes branch: 150px to the left (x - 150)
     * No branch: 150px to the right (x + 150)
     * Place both at y + 100 from decision node\'s y position

7. Create a professional flowchart structure:
   - ALWAYS start with a terminal node labeled "Start"
   - ALWAYS end with at least one terminal node labeled "End"
   - Ensure all branches eventually connect back to the main flow or end node
   - For parallel processes, keep them properly aligned vertically
   - Ensure proper logical flow with no dead ends or disconnected nodes

8. For every decision node:
   - Make sure the question in the label ends with a question mark
   - Position its two branches at exactly opposite sides (left/right)
   - Label paths precisely as "Yes" and "No", not "True/False" or other variants
   - Connect both branches eventually to a merge point or to separate end nodes

9. Respond ONLY with valid JSON, no other text'''


def strip_markdown_fences(text):
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ``` fences
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()
    return text


def extract_json(text):
    """Try multiple strategies to extract valid JSON from model output."""
    # Strategy 1: strip fences and parse directly
    cleaned = strip_markdown_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Strategy 2: find the first { ... } block
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    # Strategy 3: find the first [ ... ] block (unlikely but safe)
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return None


class GenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        diagram_type = request.data.get('type')
        prompt = request.data.get('prompt')

        if not diagram_type or not prompt:
            return Response(
                {'message': 'Type and prompt are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if diagram_type not in ('mindmap', 'flowchart'):
            return Response(
                {'message': "Type must be either 'mindmap' or 'flowchart'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        options = request.data.get('options') or {}
        complexity = options.get('complexity', 'medium') if isinstance(options, dict) else 'medium'
        node_count = COMPLEXITY_MAP.get(complexity, COMPLEXITY_MAP['medium'])

        if diagram_type == 'mindmap':
            system_prompt = MINDMAP_SYSTEM_PROMPT.format(prompt=prompt)
        else:
            system_prompt = FLOWCHART_SYSTEM_PROMPT.format(prompt=prompt)

        user_message = (
            f"Create a {diagram_type} with approximately {node_count} nodes "
            f"that represents: {prompt}\n\n"
            f"Output ONLY a single valid JSON object. No explanation, no markdown, no extra text. "
            f"Start your response with {{ and end with }}."
        )

        try:
            response = requests.post(
                settings.AI_BASE_URL,
                json={
                    'model': settings.AI_MODEL,
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_message},
                    ],
                    'temperature': 0.1,
                    'max_tokens': 8192,
                },
                headers={'Content-Type': 'application/json'},
                timeout=120,
            )
            response.raise_for_status()
            raw_text = response.json()['choices'][0]['message']['content']
        except Exception as exc:
            return Response(
                {'message': f'Failed to communicate with AI service: {exc}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        diagram_data = extract_json(raw_text)
        if diagram_data is None:
            return Response(
                {'message': 'AI generation produced invalid JSON response.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if diagram_type == 'mindmap':
            if 'rootId' not in diagram_data or 'nodes' not in diagram_data:
                return Response(
                    {'message': 'AI generation produced invalid JSON response.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            if not isinstance(diagram_data.get('nodes'), list) or not isinstance(diagram_data.get('edges'), list):
                return Response(
                    {'message': 'AI generation produced invalid JSON response.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(diagram_data, status=status.HTTP_200_OK)
