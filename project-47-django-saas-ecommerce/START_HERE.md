# Start Here: project-47-django-saas-ecommerce

**Learning focus:** Django multitenant SaaS e-commerce with local Docker, PostgreSQL/Redis/Celery, testing, and DevSecOps deployment concepts

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, create a local Python virtual environment, install the dependencies from `requirements.txt`, and review `.env.example` without filling in real credentials or running any cloud or deployment commands.

## Checkpoints

1. 1. `python manage.py check` completes locally with the environment configured from the example settings
2. 2. `python manage.py migrate` applies the Django migrations and `python manage.py test` reports the project tests
3. 3. `docker compose up --build` starts the local service stack and the app responds at the documented local address `http://127.0.0.1:8585/`.

## Hints if you are stuck

1. 1. If Django cannot start, compare the variable names and database/Redis settings you supplied with `.env.example` and the settings module referenced by the project
2. 2. If migrations or tests fail, identify whether the error names a missing dependency, an unapplied migration, or an unavailable local service before changing code
3. 3. If the browser cannot reach port 8585, inspect the Compose service logs and confirm which host port the container publishes rather than switching to an AWS or Kubernetes path.

## Evidence to capture

Terminal captures for `check`, migrations, and tests plus a local browser response at port 8585 and a brief note identifying the Django, Compose, PostgreSQL, Redis/Celery, and test components exercised

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
