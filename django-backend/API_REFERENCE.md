# Concept Crafter API Reference

Base URL: `https://your-server.com`

All protected endpoints require:

```
Authorization: Bearer <access_token>
```

---

## Auth

### POST /api/auth/register/

**Input:**

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "yourpassword"
}
```

**Expected Output (201):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**Error (400) — duplicate username or email:**

```json
{
  "message": "username: A user with that username already exists.",
  "errors": {
    "username": ["A user with that username already exists."]
  }
}
```

---

### POST /api/auth/login/

**Input:**

```json
{
  "username": "testuser",
  "password": "yourpassword"
}
```

**Expected Output (200):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**Error (400) — wrong credentials:**

```json
{
  "message": "Invalid username or password"
}
```

---

### POST /api/auth/logout/

**Headers:** `Authorization: Bearer <token>`

**Input:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Expected Output (200):**

```json
{
  "message": "Logout successful"
}
```

**Error (400) — missing refresh token:**

```json
{
  "message": "Refresh token is required"
}
```

**Error (400) — invalid/expired refresh token:**

```json
{
  "message": "Token is invalid or expired"
}
```

---

### GET /api/auth/me/

**Headers:** `Authorization: Bearer <token>`

**Input:** none

**Expected Output (200):**

```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**Error (401) — missing or invalid token:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Projects

All project endpoints require `Authorization: Bearer <token>`.

---

### GET /api/projects/

List all projects for the authenticated user.

**Input:** none

**Expected Output (200):**

```json
[
  {
    "id": 1,
    "type": "flowchart",
    "name": "My Flowchart",
    "data": {},
    "thumbnail": "",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

---

### POST /api/projects/

Create a new project.

**Input:**

```json
{
  "name": "My Flowchart",
  "type": "flowchart",
  "data": {},
  "thumbnail": ""
}
```

**Expected Output (201):**

```json
{
  "id": 1,
  "type": "flowchart",
  "name": "My Flowchart",
  "data": {},
  "thumbnail": "",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

---

### GET /api/projects/{id}/

Get a single project by ID.

**Input:** none

**Expected Output (200):**

```json
{
  "id": 1,
  "type": "flowchart",
  "name": "My Flowchart",
  "data": {},
  "thumbnail": "",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

**Error (404):**

```json
{
  "detail": "No Project matches the given query."
}
```

---

### PUT /api/projects/{id}/

Full update of a project (all fields required).

**Input:**

```json
{
  "name": "Updated Flowchart",
  "type": "flowchart",
  "data": { "nodes": [], "edges": [] },
  "thumbnail": "data:image/png;base64,..."
}
```

**Expected Output (200):**

```json
{
  "id": 1,
  "type": "flowchart",
  "name": "Updated Flowchart",
  "data": { "nodes": [], "edges": [] },
  "thumbnail": "data:image/png;base64,...",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z"
}
```

---

### PATCH /api/projects/{id}/

Partial update (only send fields you want to change).

**Input:**

```json
{
  "name": "Renamed Project"
}
```

**Expected Output (200):**

```json
{
  "id": 1,
  "type": "flowchart",
  "name": "Renamed Project",
  "data": {},
  "thumbnail": "",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:30:00Z"
}
```

---

### DELETE /api/projects/{id}/

**Input:** none

**Expected Output (204):** no body

---

## Templates

### GET /api/templates/

List all available templates.

**Input:** none

**Expected Output (200):**

```json
[
  {
    "id": 1,
    "name": "Basic Flowchart",
    "type": "flowchart",
    "data": {},
    "thumbnail": ""
  }
]
```

---

## AI Generator

### POST /api/generate/

**Headers:** `Authorization: Bearer <token>`

**Input:**

```json
{
  "type": "flowchart",
  "prompt": "user login process",
  "options": {
    "complexity": "medium"
  }
}
```

- `type`: `"flowchart"` or `"mindmap"`
- `complexity`: `"simple"` (5 nodes) | `"medium"` (8 nodes) | `"complex"` (15 nodes) | `"comprehensive"` (20 nodes)

---

**Expected Output (200) — flowchart:**

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "terminal",
      "data": { "label": "Start", "color": "#90EE90" },
      "position": { "x": 250, "y": 0 }
    },
    {
      "id": "2",
      "type": "process",
      "data": { "label": "Enter Credentials", "color": "#ADD8E6" },
      "position": { "x": 250, "y": 100 }
    },
    {
      "id": "3",
      "type": "decision",
      "data": { "label": "Valid credentials?", "color": "#FFFACD" },
      "position": { "x": 250, "y": 200 }
    },
    {
      "id": "4",
      "type": "terminal",
      "data": { "label": "End", "color": "#FFB6C1" },
      "position": { "x": 250, "y": 400 }
    }
  ],
  "edges": [
    {
      "id": "e1-2",
      "source": "1",
      "target": "2",
      "label": null,
      "animated": false,
      "markerEnd": { "type": "arrowclosed" }
    },
    {
      "id": "e2-3",
      "source": "2",
      "target": "3",
      "label": null,
      "animated": false,
      "markerEnd": { "type": "arrowclosed" }
    },
    {
      "id": "e3-4-yes",
      "source": "3",
      "target": "4",
      "label": "Yes",
      "sourceHandle": "left",
      "animated": false,
      "markerEnd": { "type": "arrowclosed" }
    }
  ]
}
```

**Expected Output (200) — mindmap:**

```json
{
  "rootId": "1",
  "nodes": {
    "1": {
      "id": "1",
      "text": "User Login",
      "children": ["2", "3"],
      "color": "#4CAF50"
    },
    "2": {
      "id": "2",
      "text": "Authentication",
      "children": ["4", "5"],
      "color": "#2196F3"
    },
    "3": {
      "id": "3",
      "text": "Security",
      "children": [],
      "color": "#FF5722"
    }
  }
}
```

**Error (400) — missing fields:**

```json
{
  "message": "Type and prompt are required"
}
```

**Error (400) — invalid type:**

```json
{
  "message": "Type must be either 'mindmap' or 'flowchart'"
}
```

**Error (500) — AI service not configured:**

```json
{
  "message": "OPENROUTER_API_KEY is not configured."
}
```

**Error (500) — AI returned bad JSON:**

```json
{
  "message": "AI generation produced invalid JSON response."
}
```

**Error (502) — AI service unreachable:**

```json
{
  "message": "Failed to communicate with AI service: ..."
}
```

{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2MTgxNTY2LCJpYXQiOjE3NzYwOTUxNjYsImp0aSI6ImY0NDg4YjcxZDY3ODQ0ODJhNzI3MGQ2ODI4MDA0NjVjIiwidXNlcl9pZCI6IjEifQ.RQuW5aLsqaD2WH2T6OgCQbSeWURjpeSx33doCC1-7N4",
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjY5OTk2NiwiaWF0IjoxNzc2MDk1MTY2LCJqdGkiOiIxNTgzNzZmNDNiMGQ0NDRkOGNjYjJkYjNkNDk1YzIwMCIsInVzZXJfaWQiOiIxIn0.S4UHAHc36GQxCzCjSOlwgYkTVm9_gMoTa97wzFQ2POU",
"user": {
"id": 1,
"username": "testuser",
"email": "test@example.com"
}
}

{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2MTgxNjIwLCJpYXQiOjE3NzYwOTUyMjAsImp0aSI6IjYyOTZiNGY1MjhhZDQ2Y2M4YmE4NTMwZTk4N2EyNTRlIiwidXNlcl9pZCI6IjEifQ.zIzwqd3Db1FJd-lQ0vLZAu3Ja6O_4Pn-RBM5NXXT8k0",
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NjcwMDAyMCwiaWF0IjoxNzc2MDk1MjIwLCJqdGkiOiJjMDliNjExNTBjZGY0ZTQ2OTgxMGEwMGVjMTAyOTNkNiIsInVzZXJfaWQiOiIxIn0.Nse2sAIm4NTHAUhu845MPodnbpA6rk1f3rAkmTqc_IA",
"user": {
"id": 1,
"username": "testuser",
"email": "test@example.com"
}
}
