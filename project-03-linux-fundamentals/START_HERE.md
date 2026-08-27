# Start Here: project-03-linux-fundamentals

**Learning focus:** Linux administration fundamentals: users, groups, permissions, filesystem navigation, file
management, and mounting

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

On a disposable local Linux environment, make a temporary practice directory and record the starting user and
current working directory before attempting any account, ownership, or deletion exercise.

## Checkpoints

1. 1. The learner can show the intended users and groups in a local practice setup and explain which accounts use primary versus secondary group membership
2. 1. The learner can reproduce the specified /dir* and /opt/dir14 paths and demonstrate file creation, movement, renaming, and relative-path use without touching real system data
3. 1. The learner can provide command output showing the requested text substitutions/searches, filesystem listing checks, and a simulated /data mount-verification plan, while reserving actual EBS, mount, and cleanup operations for instructor-controlled material.

## Hints if you are stuck

1. 1. Before each step, verify the active account, working directory, and target path
2. many failures here come from confusing an absolute path such as /f3 with a path relative to the current directory
3. 1. When an operation is denied, inspect the target's owner, group, and permission bits and compare them with the account currently logged in rather than immediately escalating privileges
4. 1. For move, delete, and text-edit tasks, first confirm the source exists and preview the affected names or lines, then use a reversible copy or disposable workspace to isolate whether the issue is path selection, permissions, or command syntax.

## Evidence to capture

A local command transcript plus a before/after directory tree, account/group membership summary, file-content
transformation evidence, search/count outputs, and a clearly labeled instructor-only plan for the
EBS/filesystem portion

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
