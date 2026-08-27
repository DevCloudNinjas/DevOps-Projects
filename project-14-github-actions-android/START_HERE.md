# Start Here: project-14-github-actions-android

**Learning focus:** Android Gradle CI/CD with GitHub Actions

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, open `project.yaml` and then inspect `android-demo-app/.github/workflows/android.yml`
alongside the local validation command `./android-demo-app/gradlew -p android-demo-app tasks`, without
changing any student files or contacting GitHub.

## Checkpoints

1. 1. You can identify the Android project root, Gradle wrapper, and the three workflow files under `android-demo-app/.github/workflows/`
2. 1. The local Gradle validation completes or reports a concrete, locally reproducible error for `./android-demo-app/gradlew -p android-demo-app tasks`
3. 1. You can explain, from the YAML, which workflow step builds/tests or handles APK/artifact output and distinguish the cache-cleanup and artifact-deletion workflows from the main Android CI flow.

## Hints if you are stuck

1. 1. If the Gradle command is not found, verify that you are at the directory containing `android-demo-app` and that the wrapper path matches the one recorded in `project.yaml`
2. 1. If validation fails during setup, inspect the wrapper and Gradle configuration files before changing application code
3. 1. If the workflow roles are unclear, compare the filenames and triggers/steps in `android.yml`, `clear-caches.yml`, and `delete-artifacts.yml`, then trace referenced scripts under `android-demo-app/scripts/`.

## Evidence to capture

Annotated workflow-role map plus the unedited local Gradle validation output or captured error diagnosis

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
