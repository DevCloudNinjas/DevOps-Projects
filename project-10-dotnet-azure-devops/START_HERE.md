# Start Here: project-10-dotnet-azure-devops

**Learning focus:** .NET CI/CD pipeline analysis with Azure DevOps and App Service

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Open the readme locally and map the three exercises into a paper or local notes checklist, starting with the
ASP.NET Core repository path and pipeline objects without signing into or provisioning Azure.

## Checkpoints

1. 1. Identify and record the expected ASP.NET Core Index page path stated in the readme and the build, release, artifact, and trigger objects named in the packet
2. 1. In a local notes checklist, sequence the stated CI steps—source retrieval, dependency restore, compilation, tests, and published output—and distinguish them from release tasks
3. 1. Produce a mock change-and-observation record showing the edited heading, expected commit, build/release progression, and updated heading as evidence targets, without executing a cloud deployment.

## Hints if you are stuck

1. 1. If the pipeline stages seem mixed together, separate build activities from release tasks and match each task to the artifact or environment it consumes
2. 1. If a repository path is hard to locate in your notes, copy it exactly from the exercise and verify each folder name before interpreting the expected change
3. 1. If a trigger appears not to fire in the described flow, check whether the packet attributes it to a commit, a new build artifact, or an optional manual setting before diagnosing further.

## Evidence to capture

Annotated local exercise checklist plus a mock CI/CD trace linking the Index page heading change, commit,
build, artifact, release tasks, and resulting updated heading

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
