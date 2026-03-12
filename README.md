## FastAPI Agent Streaming

Interactive, streaming chat assistant built with FastAPI, OpenAI Agents, and SQLModel. It exposes a simple web UI and HTTP APIs for creating chat sessions and streaming AI responses (via Server-Sent Events).

### Features

- **Streaming AI responses**: `/chat/` endpoint returns incremental text chunks using SSE, rendered live in the bundled `chat.html` UI.
- **Session-aware memory**: Chats are associated with persistent sessions stored via SQLModel and Alembic-managed migrations.
- **Tool-augmented agent**: The agent can call tools such as web search (`tavily-python`) and weather lookup, using `openai-agents` with the `litellm` backend.
- **Simple web UI**: A minimal, modern HTML UI at `/` for trying the agent in the browser.
- **API documentation**: Scalar UI is available at `/scalar` for exploring the OpenAPI schema.

### Tech Stack

- **Backend**: FastAPI
- **Agent runtime**: `openai-agents[litellm]`
- **Database/ORM**: SQLModel + SQLAlchemy + Alembic
- **Async database driver**: `aiosqlite` (default SQLite URL)
- **Docs**: `scalar-fastapi`
- **Utilities**: `python-dotenv`, `tavily-python`
- **Server**: Uvicorn

### Prerequisites

- **Python**: >= 3.13
- **Package manager**: `uv` (recommended) or `pip`

Optional but recommended:

- A **virtual environment** for isolation.

### Getting Started

#### 1. Clone the repository

```bash
git clone <your-repo-url>.git
cd fastapi-agent-streaming
```

#### 2. Create and activate a virtual environment

Using `uv` (recommended):

```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# On Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

Or with the built-in `venv` module:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# On Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

#### 3. Install dependencies

With `uv`:

```bash
uv pip install -e .
```

Or with `pip`:

```bash
pip install -e .
```

This uses `pyproject.toml` to install the `fastapi-agent-streaming` project and its dependencies.

#### 4. Configure environment variables

Configuration is defined in `app/core/settings.py` and loaded via `.env`:

- **`OPENROUTER_API_KEY`**: API key for OpenRouter (used by `openai-agents`).
- **`OPENROUTER_BASE_URL`** (optional): Defaults to `https://openrouter.ai/api/v1`.
- **`TAVILY_API_KEY`**: API key for Tavily web search.
- **`DATABASE_URL`** (optional): Defaults to `sqlite+aiosqlite:///./database.db`.

Create a `.env` file in the project root:

```bash
cp .env.example .env  # if you add an example file
```

Or create it manually:

```bash
echo "OPENROUTER_API_KEY=your-openrouter-key" >> .env
echo "TAVILY_API_KEY=your-tavily-key" >> .env
echo "DATABASE_URL=sqlite+aiosqlite:///./database.db" >> .env
```

### Database Migrations

This project uses Alembic with SQLModel. The generated migration scripts live under `alembic/versions/`.

Common commands (from the project root):

```bash
# Initialize / upgrade database to latest migration
alembic upgrade head

# Generate a new migration after changing models
alembic revision --autogenerate -m "describe changes"
```

Make sure your `DATABASE_URL` in `.env` matches the database you want to migrate.

### Running the Application

Start the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

By default, the server will run on `http://127.0.0.1:8000`.

### Endpoints Overview

- **`GET /`**
  - Serves the `app/static/chat.html` web UI.
  - Use this to interact with the assistant from your browser.

- **`POST /chat/`**
  - Body: JSON matching `ChatRequest` (e.g. `{"session_id": "your-session-id", "message": "Hello"}`).
  - Response: `text/event-stream` (SSE) streaming events of two types:
    - `{"type": "text", "content": "<delta>"}` – incremental text chunks.
    - `{"type": "tool_call", "tool_name": "<name>", "arguments": {...}}` – when tools are invoked.

- **`POST /chat-sessions/`**
  - Creates a new `ChatSession` row in the database and returns it.
  - Use the returned `id` as `session_id` for subsequent `/chat/` requests.

- **`GET /scalar`**
  - Returns the Scalar API reference UI for this FastAPI app.

### Using the Web UI

1. Start the server with `uvicorn app.main:app --reload`.
2. Open `http://127.0.0.1:8000` in your browser.
3. (Optional) Call `POST /chat-sessions/` via Scalar or another client to create a session and copy its `id`.
4. Enter the session ID and your message in the form and click **Send**.
5. Watch the response stream into the UI, along with any tool calls displayed below.

### Development

- **Formatting / Linting**: The project uses `ruff` (see `pyproject.toml`), with basic rules enabled and `alembic` excluded.
- **Local changes**:
  - Update models in `app/models` and module routers in `app/modules/**`.
  - Regenerate and apply Alembic migrations for schema changes.

### Project Structure (High Level)

- `app/main.py` – FastAPI app, router registration, root route, Scalar docs.
- `app/static/chat.html` – Browser-based chat UI with SSE streaming.
- `app/modules/chats/router.py` – `/chat/` endpoint implementing streaming agent responses.
- `app/modules/chats/schema.py` – Pydantic models for chat requests.
- `app/modules/sessions/router.py` – `/chat-sessions/` endpoints for session management.
- `app/modules/agents/*` – Agent configuration, tools, prompts, and models.
- `app/models/*` – Database engine and models (SQLModel).
- `app/core/settings.py` – Application settings loaded from environment.
- `alembic/*` – Alembic configuration and migrations.

