# Imali

> Brief one-line description of what this project does.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- PostgreSQL (via [Neon](https://neon.tech))

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com//Imali.git
cd Imali
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

```bash
cp .env.example.dev .env
```

Open `.env` and fill in all required values. See [Environment Variables](#environment-variables) below.

### 4. Create the accounts app

The `accounts` app must exist before running any migrations.
See [Custom User Model](#custom-user-model) below.

### 5. Run migrations

```bash
uv run python manage.py migrate
```

### 6. Create a superuser

```bash
uv run python manage.py createsuperuser
```

### 7. Run the development server

```bash
uv run python manage.py runserver
```

---

## Environment Variables

Copy the appropriate example file and fill in the values:

| File | Purpose |
|---|---|
| `.env.example.dev` | Local development |
| `.env.example.production` | Production deployment |

All required variables are marked `REQUIRED` inside the example files.

---

## Custom User Model

This project uses a custom user model (`accounts.CustomUser`). Django requires
this to be in place before the first migration is run — it cannot be swapped in
later without resetting the migration graph.

Before running `migrate` on a fresh project:

```bash
uv run python manage.py startapp accounts
```

Define `CustomUser` in `accounts/models.py`, register it in `accounts/admin.py`,
and ensure `accounts.apps.AccountsConfig` is in `LOCAL_APPS` in `base.py`.

---

## Settings

Settings are split into a package under `Imali/settings/`:

| File | Purpose |
|---|---|
| `base.py` | Production-safe defaults shared across all environments |
| `dev.py` | Local development overrides |
| `production.py` | Production-specific configuration |

Select the active settings file via:

```bash
DJANGO_SETTINGS_MODULE=Imali.settings.dev
```

---

## Running Tests

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov
```

---

## Project Structure

```
Imali/
├── Imali/       # Project configuration package
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # Custom user model (required first app)
├── static/                 # Source static files
├── staticfiles/            # Collected static files (generated, not committed)
├── templates/              # Project-level templates
├── .env.example.dev
├── .env.example.production
├── manage.py
└── pyproject.toml
```

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
