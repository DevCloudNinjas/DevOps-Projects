# Start Here: project-04-django-aws-ecs

**Learning focus:** Containerizing a Django application and understanding its ECS/ECR deployment architecture

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `python3 -m compileall .` and record whether the Django source files compile
without errors.

## Checkpoints

1. 1. `python3 -m compileall .` completes successfully and produces bytecode-cache output for the Django package
2. 1. The learner can trace, from `manage.py`, `hello_world_django_app/settings.py`, and `urls.py`, how the local Django application is configured and routed
3. 1. The learner can annotate the `Dockerfile` and `project.yaml` to identify the image-build inputs, non-root container execution, exposed application port, and the separate ECR-to-ECS concepts without attempting cloud access.

## Hints if you are stuck

1. 1. If compilation fails, start with the filename and line number in the error, then check syntax and indentation in that file
2. 1. If the application flow is unclear, follow the imports from `manage.py` into the project package and then inspect the URL pattern's target view
3. 1. If the container configuration is confusing, compare each Dockerfile instruction with the files it copies or installs and distinguish image construction from runtime configuration.

## Evidence to capture

Successful local compileall output, a short annotated request/configuration flow, and a
Dockerfile/project.yaml mapping that identifies build, runtime-user, port, and ECS/ECR roles

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
