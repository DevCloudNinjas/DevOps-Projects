# Start Here: project-28-openai-chatbot-eks

**Learning focus:** DevSecOps deployment of a Next.js/TypeScript chatbot using Docker, Jenkins, Terraform, and Kubernetes EKS

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the repository root, open `Chatbot-UI/README.md` and inspect `package.json`, `.env.example`, and the local source/configuration files before touching any AWS, Jenkins, Terraform, or Kubernetes resources.

## Checkpoints

1. 1. You can identify the local app entry points (`pages/index.tsx`, `pages/api/chat.ts`), the package scripts, and the environment-variable template without changing student materials
2. 2. The Chatbot-UI dependencies install locally and `npm run dev` starts a development server without invoking Terraform, AWS CLI, Jenkins, or EKS
3. 3. The local interface loads in a browser and you can document the expected API-key configuration path and a test-chat observation, keeping credentials out of submitted evidence.

## Hints if you are stuck

1. 1. If the local start command fails, compare the command and working directory with `Chatbot-UI/README.md` and inspect the exact script names in `Chatbot-UI/package.json`
2. 2. If the interface loads but chat requests fail, check whether the environment variable names and server-key fallback setting match `.env.example` and the README, rather than changing application code first
3. 3. If you are tempted to begin with the EKS files, Jenkinsfiles, or Terraform variables, first verify the local app boundary and capture the error from the smallest local test so the failure is attributable.

## Evidence to capture

Annotated local file map; dependency/startup output; browser capture of the local Chatbot UI; redacted configuration note and one documented test-chat result

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
