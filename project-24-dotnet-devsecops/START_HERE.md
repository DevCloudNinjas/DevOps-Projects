# Start Here: project-24-dotnet-devsecops

**Learning focus:** Local .NET web application DevSecOps pipeline and container/Kubernetes delivery

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the packet’s project root, inspect `DotNet-monitoring/README.md`, `makefile`, and
`.github/workflows/ci-build.yaml`, then run only the local application’s documented build/test targets rather
than any cloud deployment target.

## Checkpoints

1. 1. The .NET project restores/builds locally and the xUnit test target completes, with the result recorded
2. 1. The application runs locally on its documented Kestrel port and the Info, Tools, and Monitoring pages are observable without optional cloud/API configuration
3. 1. A local review of the CI workflow and container/Kubernetes manifests identifies the build, Trivy security-scan, dependency-check, image, and deployment stages, with a brief mapping of each stage to its evidence.

## Hints if you are stuck

1. 1. If the first local command fails, verify that the available .NET SDK matches the README’s .NET 6 prerequisite and that you are invoking commands from the directory containing `src/dotnet-demoapp.csproj`
2. 1. If an expected page or feature is absent, check the README’s optional-configuration section before treating it as an application defect
3. 1. If CI/security review results differ from expectations, compare the workflow’s stage names and scan thresholds with the active YAML and distinguish static inspection from actually running cloud-dependent steps.

## Evidence to capture

Local build/test output, a localhost screenshot or notes for Info/Tools/Monitoring, and a short
stage-to-artifact security/CI mapping

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
