# Concept Crafter Backend (Node.js & Express)

This document provides a technical explanation of the Node.js and Express-based backend project located in the `backend` folder. This server serves as the core API for creating, storing, and managing mind maps and flowcharts.

## 🚀 Core Technology Stack
- **Runtime**: Node.js
- **Framework**: Express.js (TypeScript)
- **Database**: MongoDB (via Mongoose)
- **Authentication**: Passport.js (Local Strategy) & bcrypt
- **Validation**: Zod (Data schema and request validation)
- **AI Integration**: OpenRouter / Google Gemini / OpenAI (Automated diagram generation)

## 📂 Project Structure
- `index.ts`: Entry point of the server. Responsible for middleware setup, route registration, and server execution.
- `routes.ts`: Main API route definitions (Project CRUD, Templates, AI Generation).
- `db.ts`: MongoDB connection setup and Mongoose model definitions.
- `storage.ts` & `mongoStorage.ts`: Data storage layer abstraction. Provides interfaces for both in-memory and MongoDB storage.
- `src/routes/auth.ts`: Authentication-related routes (Register, Login, Logout).
- `src/shared/schema.ts`: Shared Zod data models and TypeScript type definitions for both frontend and backend.

## 🛠 Key Features & API Endpoints

### 1. Authentication
- `POST /api/auth/register`: Create a new user account (with hashed password storage).
- `POST /api/auth/login`: User authentication and session management.
- `POST /api/auth/logout`: Terminate the user session.
- `GET /api/auth/user`: Retrieve information about the currently logged-in user.

### 2. Project Management (Project CRUD)
- `GET /api/projects`: List all projects (mind maps, flowcharts) for the user.
- `GET /api/projects/:id`: Retrieve detailed data for a specific project.
- `POST /api/projects`: Create a new project.
- `PUT /api/projects/:id`: Update a project (name, data, thumbnail, etc.).
- `DELETE /api/projects/:id`: Delete a project.

### 3. AI Diagram Generation
- `POST /api/generate`: Automatically generates mind map or flowchart structures in JSON format based on user prompts.
- Internally calls LLMs (Large Language Models) to construct diagram nodes and edges.

### 4. Templates
- `GET /api/templates`: Provides a list of pre-defined diagram templates.

## 🔐 Security & Data Validation
- **Password Hashing**: Uses `bcrypt` to securely hash and store user passwords.
- **Zod Validation**: All API request data is strictly validated through `Zod` schemas to ensure data integrity.

## 📡 How to Run
1. Run `npm install` in the `backend` folder to install dependencies.
2. Set the necessary environment variables (e.g., `OPENROUTER_API_KEY`, `MONGODB_URI`) in a `.env` file.
3. Run the development server with the `npm run dev` command (Default port: 5000).
