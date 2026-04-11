import json
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


MINDMAP_SYSTEM = """Create a mind map structure based on the user's input topic.
Output MUST be valid JSON with exactly this structure:
{
  "rootId": "1",
  "nodes": {
    "1": { "id": "1", "text": "Central Topic", "children": ["2", "3"], "color": "#4CAF50" },
    "2": { "id": "2", "text": "Main Branch 1", "children": ["4", "5"], "color": "#2196F3" }
  }
}
Requirements:
1. rootId must be "1"
2. Each node MUST have id, text, children, color
3. Respond ONLY with valid JSON, no other text"""

FLOWCHART_SYSTEM = """Create a flowchart structure based on the user's input process.
Output MUST be valid JSON with exactly this structure:
{
  "nodes": [
    {"id":"1","type":"terminal","data":{"label":"Start","color":"#90EE90"},"position":{"x":250,"y":0}},
    {"id":"2","type":"process","data":{"label":"Process Step","color":"#ADD8E6"},"position":{"x":250,"y":100}}
  ],
  "edges": [
    {"id":"e1-2","source":"1","target":"2","label":null,"animated":false,"markerEnd":{"type":"arrowclosed"}}
  ]
}
Requirements:
1. Use terminal/process/decision/input/output node types
2. Always start with terminal "Start" and end with terminal "End"
3. Decision nodes must have Yes/No edges with sourceHandle left/right
4. Respond ONLY with valid JSON, no other text"""


class GenerateView(APIView):
    def post(self, request):
        diagram_type = request.data.get('type')
        prompt = request.data.get('prompt')
        options = request.data.get('options', {})

        if not diagram_type or not prompt:
            return Response({'message': 'Type and prompt are required'}, status=400)
        if diagram_type not in ('mindmap', 'flowchart'):
            return Response({'message': "Type must be either 'mindmap' or 'flowchart'"}, status=400)

        complexity = options.get('complexity', 'medium')
        node_count = {'simple': 5, 'medium': 8, 'complex': 15, 'comprehensive': 20}.get(complexity, 8)

        system_prompt = MINDMAP_SYSTEM if diagram_type == 'mindmap' else FLOWCHART_SYSTEM
        api_key = settings.OPENROUTER_API_KEY

        try:
            resp = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                    'HTTP-Referer': 'http://localhost:8000',
                    'X-Title': 'Diagram Generator',
                },
                json={
                    'model': 'google/gemma-3-27b-it:free',
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': f'Create a {diagram_type} with approximately {node_count} nodes that represents: {prompt}\n\nRespond ONLY with valid JSON, nothing else.'},
                    ],
                    'temperature': 0.1,
                    'max_tokens': 8192,
                },
                timeout=60,
            )
            resp.raise_for_status()
        except Exception as e:
            return Response({'message': f'Failed to communicate with AI service: {str(e)}'}, status=500)

        content = resp.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        if not content:
            return Response({'message': 'AI generation failed. Invalid response structure.'}, status=500)

        # Strip markdown code fences
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            return Response({'message': 'AI generation produced invalid JSON response.', 'error': str(e)}, status=500)

        if diagram_type == 'mindmap' and ('rootId' not in result or 'nodes' not in result):
            return Response({'message': 'Invalid mind map structure'}, status=500)
        if diagram_type == 'flowchart' and (not isinstance(result.get('nodes'), list) or not isinstance(result.get('edges'), list)):
            return Response({'message': 'Invalid flowchart structure'}, status=500)

        return Response(result)
