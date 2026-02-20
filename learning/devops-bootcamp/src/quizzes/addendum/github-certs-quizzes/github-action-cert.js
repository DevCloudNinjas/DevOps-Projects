const rawQuizdown = `
# Which statement is correct regarding passing permissions to reusable workflows?
> https://docs.github.com/en/actions/using-workflows/reusing-workflows#access-and-permissions
1. [x] The \`GITHUB_TOKEN\` permissions passed from the caller workflow can be only downgraded by the called workflow.
1. [ ] The \`GITHUB_TOKEN\` permissions passed from the caller workflow can be only elevated by the called workflow.
1. [ ] The \`GITHUB_TOKEN\` permissions passed from the caller workflow can be both downgraded and elevated by the called workflow.
1. [ ] The \`GITHUB_TOKEN\` permissions passed from the caller workflow can be neither downgraded or elevated by the called workflow.

# What are the different permission levels You can assign to \`GITHUB_TOKEN\` in the \`permissions\` block?
> https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
1. [x] none, write, read
1. [ ] read, write, delete
1. [ ] read, write

# You can use \`permissions\` to modify the \`GITHUB_TOKEN\` permissions on:
- [x] Workflow level
- [x] Job level
- [ ] Step level

# Are Github Actions free for public repositories?
1. [x] Yes
1. [ ] No

# Which of these is not a valid event that could trigger a workflow?
> https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#about-events-that-trigger-workflows
1. [x] Cloning the repository
1. [ ] Commiting a file to master branch
1. [ ] A branch is created
1. [ ] Adding a label to a pull request

# Which is true about workflows?
> https://docs.github.com/en/actions/using-workflows/about-workflows
> Actions (not workflows) can be shared in Github Marketplace
- [x] Workflows can run one or multiple jobs at a time
- [x] Workflows can be triggered manually, by an event or run on a schedule
- [x] Workflows have to be defined in the \`.github/workflows\` directory
- [ ] Workflows can only be run on a schedule
- [ ] Workflow can run only one job at a time
- [ ] Workflows are written in any of \`.yaml\`, \`.json\` or \`.toml\` formats
- [ ] Workflows can be shared in Github Marketplace

# Which components are required for a workflow?
> https://docs.github.com/en/actions/using-workflows/about-workflows#workflow-basics
- [x] One or more events that will trigger the workflow
- [x] One or more jobs
- [ ] Workflow name
- [ ] Defined branches on which the workflow will run

# Which event is triggered by a webhook action from outside of the repository?
> https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
1. [x] repository_dispatch
1. [ ] webhook_dispatch
1. [ ] workflow_dispatch
1. [ ] remote_dispatch
1. [ ] api_dispatch

# Workflows are defined in which format
1. [x] yaml
1. [ ] toml
1. [ ] json
1. [ ] xml

# Where should you store sensitive data such as passwords or certificates that will be used in workflows
1. [x] secrets
1. [ ] config variables
1. [ ] vault
1. [ ] environment variables

# In a workflow with multiple jobs the default behaviour is:
> https://docs.github.com/en/actions/using-workflows/about-workflows#creating-dependent-jobs
1. [x] All jobs run in parallel
1. [ ] Jobs run in sequence

# If job B requires job A to be finished you have to:
> https://docs.github.com/en/actions/using-workflows/about-workflows#creating-dependent-jobs
1. [x] use the \`needs\` keyword in job B to create this dependency
1. [ ] use the \`needs\` keyword in job A to create this dependency
1. [ ] use the \`requires\` keyword in job B to create this dependency
1. [ ] use the \`requires\` keyword in job A to create this dependency

# In a workflow with multiple jobs, if job A fails then:
> https://docs.github.com/en/actions/using-workflows/about-workflows#creating-dependent-jobs
1. [x] the jobs that are dependent on job A are skipped
1. [ ] the jobs that are dependent on job A fail
1. [ ] the workflow immediately cancels all other jobs

# This code will launch 6 different jobs in parallel using the matrix strategy. Can You use the matrix strategy to parallelize entire workflows?
\`\`\`yaml
jobs:
  example_matrix:
    strategy:
      matrix:
        version: [10, 12, 14]
        os: [ubuntu-latest, windows-latest]
\`\`\`
> https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-a-matrix-strategy-with-a-reusable-workflow
1. [ ] No
1. [x] Yes

# Which matrix job definition is syntactically correct?
> https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#using-a-matrix-strategy
1. [x] 1
\`\`\`yaml
  jobs:
    example_matrix:
      strategy:
        matrix:
          version: [10, 12, 14]
          os: [ubuntu-latest, windows-latest]
\`\`\`
1. [ ] 2
\`\`\`yaml
  jobs:
    example_matrix:
      matrix:
        strategy:
          version: [10, 12, 14]
          os: [ubuntu-latest, windows-latest]
\`\`\`
1. [ ] 3
\`\`\`yaml
  jobs:
    example_matrix:
      matrix:
        version: [10, 12, 14]
        os: [ubuntu-latest, windows-latest]
\`\`\`
1. [ ] 4
\`\`\`yaml
  jobs:
    matrix:
      version: [10, 12, 14]
      os: [ubuntu-latest, windows-latest]
\`\`\`

# How do You access matrix variables in a matrix strategy job?
> https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#using-a-matrix-strategy
1. [ ] Using the \`vars\` context
1. [x] Using the \`matrix\` context
1. [ ] Using the \`job\` context
1. [ ] Using the \`jobs\` context

# When using the \`pull_request\` and \`pull_request_target\` events, how do You configure the workflow to run only when targeting the \`prod\` branch?
> https://docs.github.com/en/actions/using-workflows/triggering-a-workflow#using-filters-to-target-specific-branches-for-pull-request-events
1. [x] Using \`branches\` filter
1. [ ] Using \`branch\` filter
1. [ ] You create the workflow only on \`prod\` branch
1. [ ] Using glob patterns

# This workflow will run on all pull requests where:
\`\`\`yaml
on:
  pull_request:
    branches:
      - 'releases/**'
      - '!releases/**-alpha'
\`\`\`
> https://docs.github.com/en/actions/using-workflows/triggering-a-workflow#example-including-and-excluding-branches
1. [x] the target branch name starts with \`release\` but does not end with \`-alpha\`
1. [ ] the target branch name starts with \`release\`
1. [ ] the source branch name starts with \`release\` but does not end with \`-alpha\`
1. [ ] the source branch name starts with \`release\`

# Fill in the blank: When using \`push\` event trigger filters You can use <____> patterns to target multiple branches
> https://docs.github.com/en/actions/using-workflows/triggering-a-workflow#using-filters-to-target-specific-branches-or-tags-for-push-events
1. [x] glob
1. [ ] regex
1. [ ] scheme
1. [ ] action

# Which event allows You to manually trigger a workflow from the GitHub UI?
> https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow
1. [x] workflow_dispatch
1. [ ] manual_dispatch
1. [ ] workflow_trigger
1. [ ] manual_trigger

# What are the possible types of an input variable for a manually triggered workflow?
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_dispatchinputs
- [x] choice
- [x] boolean
- [x] string
- [x] environment
- [ ] number
- [ ] dropdown
- [ ] select

# A workflow that has only \`workflow_dispatch\` event trigger can be triggered using GitHub's REST API
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_dispatchinputs
1. [x] True
1. [ ] False

# To stop a workflow from running temporarily without modyfing the source code You should
> https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow
1. [x] Use the \`Disable workflow\` option in GitHub Actions
1. [ ] Remove secrets that are required for this workflow
1. [ ] Delete environment that is required for this workflow
1. [ ] Prevent any new commits to main branch

# What are \`activity types\` of an event used for ?
> https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#about-events-that-trigger-workflows
1. [x] Limiting workflow runs to specific activity types using the \`types\` filter
1. [ ] Checking if the activity comes from an user or a bot
1. [ ] Reacting to new activity on a repository (e.g new contributor)

# You want to create a reusable workflow \`CI\` that runs some quality checks, linting and tests on code changes. What event trigger should the \`CI\` workflow define to allow reusing it in other workflows?
> https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
1. [x] workflow_call
1. [ ] workflow_trigger
> There is no such event trigger
1. [ ] workflow_dispatch
> This is used for manual triggers
1. [ ] workflow_run
> https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run

# A reusable workflow named \`build\` creates zip file artifacts. How do You pass the zip file location to the caller workflow that is calling the \`build\` workflow?
> https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-outputs-from-a-reusable-workflow
- [x] You define an output on workflow level in the \`build\` workflow
- [x] You define an output on job level in the \`build\` workflow
- [x] In the \`build\` workflow You write the output into \`$GITHUB_OUTPUT\` in one of the steps
- [ ] All outputs are automatically passed to the caller workflows

# What are the valid use cases for using **defaults**?
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#defaults
- [x] Using defaults.run on workflow level to set default shell (e.g bash) for an entire workflow
- [x]  Using defaults.run on job level to set default working-directory for all steps in a single job
- [ ] Using defaults.run on step level to set default shell (e.g bash) for that single step
> defaults.run can only be set on workflow or job level
- [ ] Using defaults.env on workflow level to set default environment variables for an entire workflow
> There is no such thing as defaults.env
- [ ] Using defaults.env on job level to set default environment variables for all steps in a single job
> There is no such thing as defaults.env

# How can You ensure that a workflow called \`Deploy Prod\` is always running at most one at a time?
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#concurrency
1. [x] Use \`concurrency\` on workflow level
\`\`\`yaml
concurrency: \$\{\{ github.workflow \}\}
\`\`\`
1. [ ] Use \`queue\` on workflow level
\`\`\`yaml
queue: \$\{\{ github.workflow \}\}
\`\`\`
1. [ ] Use \`order\` on workflow level
\`\`\`yaml
order: \$\{\{ github.workflow \}\}
\`\`\`
1. [ ] Use \`parallel\` on workflow level
\`\`\`yaml
parallel: \$\{\{ github.workflow \}\}
\`\`\`

# Your Pull Request analysis workflow uses multiple code analysis tools and takes about 20minutes to fully complete. It is triggered on \`pull_request\` event with \`branches\` filter set to \`master\`. Therefore if a developer pushes multiple commits within few minutes multiple workflows are running in parallel. How can You stop all previous workflow runs and only run the one with latest changes?
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-concurrency-to-cancel-any-in-progress-job-or-run
1. [x] Use concurrency with cancel-in-progress
\`\`\`yaml
  concurrency:
    group: \$\{\{ github.workflow }}-\$\{\{ github.ref \}\}
    cancel-in-progress: true
\`\`\`
1. [ ] Use concurrency
\`\`\`yaml
  concurrency:
    group: \$\{\{ github.ref \}\}
\`\`\`
> This would queue runs on that github ref. It will not stop previous runs

1. [ ] Use activity types filter
\`\`\`yaml
  on:
    pull_request:
      branches:
        - master
      types: [latest]
\`\`\`
> There is no such activity type as \`latest\` for pull_request event
1. [ ] Use cancel-in-progress flag for \`pull_request\` event
\`\`\`yaml
  on:
    pull_request:
      branches:
        - master
      cancel-in-progress: true
\`\`\`

# When will job3 run?
\`\`\`yaml
  jobs:
    job1:
    job2:
      needs: job1
    job3:
      if: \$\{\{ always() \}\}
      needs: [job1, job2]
\`\`\`
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-not-requiring-successful-dependent-jobs
1. [x] job3 will run after job1 and job2 have completed, regardless of whether they were successful
1. [ ] You cannot use \`if: \$\{\{ always() \}\}\` and \`needs\` together. The workflow will fail on startup.
1. [ ] job3 will run after job1 and job2 have been successfully completed
1. [ ] job3 will run after both job1 and job2 have failed

# What \`jobs.job_id.if\` conditional will make sure that job \`production-deploy\` is triggered only on \`my-org/my-repo\` repository?
\`\`\`yaml
  jobs:
    production-deploy:
      if: <CONDITION>
      runs-on: ubuntu-latest
      steps:
        ...
\`\`\`
> https://docs.github.com/en/actions/learn-github-actions/contexts#github-context
- [x] \`if: github.repository == 'my-org/my-repo'\`
- [x] \`if: \$\{\{ github.repository == 'my-org/my-repo' \}\}\`
- [ ] \`if: \$\{\{ github.organization == 'my-org' && github.repository == 'my-repo' \}\}\`
> https://docs.github.com/en/actions/learn-github-actions/contexts#github-context
- [ ] \`if: \$\{\{ github.org == 'my-org' && github.repository == 'my-repo' \}\}\`
> https://docs.github.com/en/actions/learn-github-actions/contexts#github-context

# What Github-hosted runner types are available to use?
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#choosing-github-hosted-runners
- [x] Windows Server
- [x] Ubuntu
- [x] macOS
- [ ] Android

# Is this statement true? \`Not all steps run actions, but all actions run as a step\`
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps
1. [x] True
1. [ ] False
> Steps can but don't have to run actions (e.g running a run command)

# For any action published in GitHub Marketplace, you can often use it in multiple versions, rank the different approaches from most to least stable and secure.
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-versioned-actions
1. Using the commit SHA
\`\`\`yaml
    uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3
\`\`\`
2. Using version tags
\`\`\`yaml
    uses: actions/checkout@v3
\`\`\`
3. Using the main branch
\`\`\`yaml
    uses: actions/checkout@main
\`\`\`

# To prevent a job from failure when one of the steps fails You can include:
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepscontinue-on-error
1. [x] \`continue-on-error\` flag in the failing step
\`\`\`yaml
  steps:
      - uses: my-org/failing-action@v1
        continue-on-error: true
\`\`\`
1. [ ] \`ignore-error\` flag in the failing step
\`\`\`yaml
  steps:
      - uses: my-org/failing-action@v1
        ignore-error: true
\`\`\`
1. [ ] \`failure()\` conditional in the failing step
\`\`\`yaml
  steps:
      - uses: my-org/failing-action@v1
        if: failure()
\`\`\`
1. [ ] \`always()\` conditional in the failing step
\`\`\`yaml
  steps:
      - uses: my-org/failing-action@v1
        if: always()
\`\`\`

# You defined a matrix job \`example_matrix\`. How can limit the matrix to run a maximum of 2 jobs at a time?
\`\`\`yaml
  jobs:
    example_matrix:
      strategy:
        matrix:
          version: [10, 12, 14]
          os: [ubuntu-latest, windows-latest]
\`\`\`
> https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategymax-parallel
1. [x] Set \`jobs.example_matrix.strategy.max-parallel\` to 2
1. [ ] Set \`jobs.example_matrix.strategy.concurrency\` to 2
1. [ ] Use Github's REST API to check if the job count is lesser than 2
1. [ ] It's not possible, a matrix will always run all of the jobs in parallel if there are runners available

# Which of these is a proper way of setting an output parameter \`PET\` with a value of \`DOG\` in a \`step\`.
> https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
1. [x] \`echo "PET=DOG" >> "$GITHUB_OUTPUT"\`
1. [ ] \`echo "DOG=PET" >> "$GITHUB_OUTPUT"\`
1. [ ] \`gh set-output "DOG=PET"\`
1. [ ] \`gh set-output "PET=DOG"\`

# Which of these is a way using \`action_state\` in \`step_two\`?
\`\`\`yaml
  steps:
    - name: Set the value
      id: step_one
      run: |
        echo "action_state=yellow" >> "$GITHUB_ENV"
    - name: Use the value
      id: step_two
      run: ?
\`\`\`
> https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable
1. [x] \`run: echo "$action_state"\`
1. [ ] \`run: echo "\$\{\{ steps.step_one.outputs.action_state \}\}"\`
> That would be the case if \`action_state\` was written to \`$GITHUB_OUTPUT\`
1. [ ] \`run: echo "$steps.step_one.outputs.action_state"\`
1. [ ] \`run: echo "\$\{\{ action_state \}\}"\`

# Is this statement true? \`Workflows can be reused, but a reusable workflow cannot call another reusable workflow.\`
> https://docs.github.com/en/actions/using-workflows/reusing-workflows#nesting-reusable-workflows
1. [x] False
1. [ ] True
> Reusable workflows can be nested, but there are limitations https://docs.github.com/en/actions/using-workflows/reusing-workflows#limitations

# In the following example, \`workflow A\` passes all of its secrets to \`workflow B\`, by using the inherit keyword. Then \`workflow B\` calls \`workflow C\`. Which statement regarding \`secrets\` is true for that example?
\`\`\`yaml
  jobs:
    workflowA-calls-workflowB:
      uses: octo-org/example-repo/.github/workflows/B.yml@main
      secrets: inherit
\`\`\`
\`\`\`yaml
  jobs:
    workflowB-calls-workflowC:
      uses: different-org/example-repo/.github/workflows/C.yml@main
\`\`\`
> https://docs.github.com/en/actions/using-workflows/reusing-workflows#passing-secrets-to-nested-workflows
1. [x] All secrets available to \`workflow A\`  will be also available to \`workflow B\`, but not to \`workflow C\`
1. [ ] All secrets from \`octo-org\` organization and \`octo-org/example-repo\` repository will be available to \`workflow B\`, but not to \`workflow C\`
> Not all secrets from \`octo-org\` organization have to be made available to \`octo-org/example-repo\`.
1. [ ] All secrets available to \`workflow A\` will be also available to \`workflow B\` and \`workflow C\`
> \`Workflow B\` would need to add \`secrets: inherit\` when calling \`workflow C\`
1. [ ] Only repository and environment secrets available to \`workflow A\` will be available to \`workflow B\`, but not to \`workflow C\`. Organization scoped secrets cannot be inherited

# When should You use \`caching\`?
> https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#comparing-artifacts-and-dependency-caching
1. [x] When you want to reuse files that don't change often between jobs or workflow runs, such as build dependencies from a package management system.
1. [ ] When you want to reuse files that do change often between jobs or workflow runs, such as build dependencies from a package management system.
1. [ ] When you want to save files produced by a job to view after a workflow run has ended, such as built binaries or build logs.
> Artifacts should be used for that https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
1. [ ] When you want to save binaries produced by a build job to use in a subsequent deploy job to deploy a new version of an application
> Artifacts should be used for that https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts

# When should You use \`artifacts\`?
> https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#about-workflow-artifacts
- [x] Use artifacts to save files produced by a job to view after a workflow run has ended, such as test results or build logs.
- [x] Use artifacts to save binaries produced by a build job to use in a subsequent deploy job to deploy a new version of an application
- [ ] Use artifacts to reuse files that don't change often between jobs or workflow runs, such as build dependencies from a package management system.
> Caching should be used for that https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#comparing-artifacts-and-dependency-caching
- [ ] Use artifacts to create new versions of Your application together with release notes, mentions and/or contributors
> That's a use case for releases, not artifacts

# If a workflow runs on a \`feature-a\` branch, can it restore \`caches\` created in the default \`main\` branch?
> https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#restrictions-for-accessing-a-cache
1. [x] Yes, all branches can restore caches created on the default branch
1. [ ] Yes, all caches can be accessed by workflows on any branch within the same repository
1. [ ] No, caches can only be restored from the same branch
1. [ ] Yes but only if no files were changed on \`feature-a\` branch

# To access an \`artifact\` that was created in another, previously triggered workflow run You can:
> https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#about-workflow-artifacts
1. [x] You cannot access \`artifacts\` that were created in a different workflow run
1. [ ] Use the \`actions/download-artifact\` action.
1. [ ] Use the \`actions/upload-artifact\` action.
1. [ ] Use the \`actions/download-artifact\` action and make sure the artifact is not expired

# What should You use to store coverage reports or screenshots generated during a workflow that runs automated testing for a repository?
> https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#comparing-artifacts-and-dependency-caching
1. [x] Artifacts
1. [ ] Caches
1. [ ] Packages
> https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages
1. [ ] Releases
> https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

# You can only upload a single file at a time when using \`actions/upload-artifact\` action
> https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#uploading-build-and-test-artifacts
1. [x] False
1. [ ] True

#  In job \`deploy\`, if You want to access binaries (containing Your application) that were created in job \`build\` You should
> https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#comparing-artifacts-and-dependency-caching

1. [x] upload the binaries as artifacts in \`build\` and download them in \`deploy\`
1. [ ] upload the binaries as artifacts in \`deploy\` and download them in \`build\`
1. [ ] cache the binaries in \`build\` and read the files from cache in \`deploy\`
1. [ ] cache the binaries in \`deploy\` and read the files from cache in \`build\`

# A job called \`job2\` is using artifacts created in \`job1\`. Therefore it's important to make sure \`job1\` finishes before \`job2\` starts looking for the artifacts. How should You create that dependency?
> https://github.com/sede-x/osdu-dpsolutions-gha-commons/pull/40/commits/f46cc3161059ec787afa78c3875b9f5288d3f73c
1. [x] create this dependency using the \`needs\` keyword in \`job2\`
1. [ ] this dependency is created implicitly when using \`actions/download-artifact\` to download artifact from \`job1\`
1. [ ] create this dependency by defining \`job2\` after \`job1\` in the workflow's \`.yaml\` definition
1. [ ] create this dependency using the \`concurrency\` keyword in \`job2\`

# Which is true about \`Starter Workflows\` ?
> https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization
- [x] They allow users to leverage ready-to-use (or requiring minimal changes) workflow templates
- [x] Github provides and maintains starter workflows for different categories, languages and tooling
- [x] Your organization can create custom starter workflows for users in Your organization
- [ ] Starter workflows cannot call reusable workflows
- [ ] Starter workflows are a paid Github feature
- [ ] Starter workflows are provided ready-to-use and cannot be modified or enhanced
> https://docs.github.com/en/actions/using-workflows/using-starter-workflows#using-starter-workflows

# Secrets and configuration variables can be scoped to
> https://docs.github.com/en/actions/using-workflows/sharing-workflows-secrets-and-runners-with-your-organization#sharing-secrets-and-variables-within-an-organization
- [x] The entire organization, or selected repositories in an organization
- [x] A single repository
- [x] An environment in a repository
- [ ] An environment shared across multiple repositories
> Environments cannot be shared across repositories
- [ ] Multiple repositories that do not share an organization/enterprise
- [ ] A specific workflow in a repository
> Environment variables can be scoped to a workflow, configuration variables cannot
- [ ] A specific job in a workflow
> Environment variables can be scoped to a workflow, configuration variables cannot

# What are the three types of Actions?
> https://docs.github.com/en/actions/creating-actions/about-custom-actions#types-of-actions
1. [x] \`Docker container actions\`, \`JavaScript Actions\`, \`Composite Actions\`
1. [ ] \`Python Actions\`, \`JavaScript Actions\`, \`Custom Actions\`
1. [ ] \`Docker container Actions\`, \`JavaScript Actions\`, \`Custom Actions\`
1. [ ] \`Docker container actions\`, \`Java Actions\`, \`Composite Actions\`

# Is this statement true? \`Docker container actions are usually slower than JavaScript actions\`
> Docker container actions are slower than JavaScript actions
1. [x] True
1. [ ] False
> Because of the latency to build and retrieve the container, Docker container actions are slower than JavaScript actions.

# When creating a custom Github Action You have to store the source code in \`.github/workflows\` directory
> https://docs.github.com/en/actions/creating-actions/about-custom-actions#choosing-a-location-for-your-action
1. [x] False
1. [ ] True
> That is true for \`workflows\`, not for \`actions\`

# When creating custom Github Actions - in what file all the action \`metadata\` has to be defined?
Metadata examples: name, description, outputs or required inputs
> https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
1. [x] In the \`action.yml\` or \`action.yaml\` file in the action repository
1. [ ] In the repository \`README\` file
> While it's good practice to do that, it's not a requirement for the action to work
1. [ ] It's edited in Github Marketplace UI when published for sharing
1. [ ] In the \`action.yml\` or \`action.yaml\` file in the action repository, but it is not required if the action is not meant to be shared and used by the public
> All actions require the metadata file.

# A workflow was initially run on \`commit A\` and failed. You fixed the workflow with the subsequent \`commit B\`. When You re-run that workflow it will run with code from which commit?
> https://docs.github.com/en/actions/managing-workflow-runs/re-running-workflows-and-jobs#about-re-running-workflows-and-jobs
1. [x] It will run with code from \`commit A\`
1. [ ] It will run with code from \`commit B\`
> Re-running a workflow uses the same commit SHA and Git ref of the original event that triggered the workflow run.
1. [ ] You cannot re-run workflows in GitHub Actions. You have to trigger a new workflow which will run with latest changes
1. [ ] It will trigger two workflows, one with code from \`commit A\` and one with code from \`commit B\`

# How can You require manual approvals by a maintainer if the workflow run is targeting the \`production\` environment?
> https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
1. [x] Using deployment protection rules
1. [ ] Setting the required required reviewers in the \`production\` workflow
1. [ ] Using branch protection rules
1. [ ] Manual approvals are not supported by Github Actions

# Which is true about environments?
> Each job in a workflow can reference a single environment.
1. [x] Each job in a workflow can reference a single environment.
1. [ ] Each workflow can reference a single environment.
1. [ ] Each job in a workflow can reference a maximum of two environments.
1. [ ] Each workflow can reference a maximum of two environments.

# When using Github Actions to access resources in one of the cloud providers (such as AWS, Azure or GCP) the safest and recommended way to authenticate is
> https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
1. [x] Using OIDC
1. [ ] Using Vault
1. [ ] Storing access keys in \`secrets\`
> Using long lasting access keys is not recommended in case of any security leaks or attacks such as [script injection](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections)
1. [ ] Storing access keys in \`variables\`
> No sensitive values should be stored in \`variables\`

# Your open-source publicly available repository contains a workflow with a \`pull_request\` event trigger. How can You require approvals for workflow runs triggered from forks of Your repository?
> https://docs.github.com/en/actions/managing-workflow-runs/approving-workflow-runs-from-public-forks#about-workflow-runs-from-public-forks
1. [x] Setup required approvals for fork runs in the repository
1. [ ] Setup deployment protection rules for the repository
> Deployment protection rules are used for protecting environments
1. [ ] Setup branch protection rules for the repository
1. [ ] The workflow will not trigger for forks if using \`pull_request\` event. If You want to do that You should use \`fork_pull_request\` event trigger with \`require-approval\` flag.

# Which of the following default environment variables contains the name of the person or app that initiated the workflow run?
> https://docs.github.com/en/actions/reference/environment-variables#default-environment-variables
1. [ ] \`GITHUB_USER\`
1. [ ] \`GITHUB_REPOSITORY\`
1. [ ] \`GITHUB_WORKFLOW\`
1. [x] \`GITHUB_ACTOR\`

# Which of the following are default environment variables in GitHub Actions? (Select three.)
> https://docs.github.com/en/actions/reference/environment-variables#default-environment-variables
- [x] \`GITHUB_REPOSITORY\`
- [x] \`GITHUB_WORKFLOW\`
- [x] \`GITHUB_ACTOR\`
- [ ] \`GITHUB_USER\`
- [ ] \`GITHUB_ORGANIZATION\`
- [ ] \`GITHUB_TOKEN\`

# Your organization defines a secret \`SomeSecret\`, however when You reference that secret in a workflow using \`\$\{\{ secrets.SomeSecret \}\}\` it provides a different value than expected. What may be the reason for that?
> https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#naming-your-secrets
1. [x] The secret \`SomeSecret\` is also declared in repository scope
1. [ ] The secret \`SomeSecret\` is also declared in enterprise scope
> If a secret with the same name exists at multiple levels, the secret at the lowest level takes precedence.
1. [ ] \`\$\{\{ secrets.SomeSecret \}\}\` expression is only used for repository scoped secrets
1. [ ] You need to use the GitHub API to access organization scoped secrets

# Which is a correct way to print a debug message?
> https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#example-setting-a-debug-message
1. [x] \`echo "::debug::Watch out here!"\`
1. [ ] \`echo ":debug:Watch out here!"\`
1. [ ] \`echo "::debug::message=Watch out here!"\`
1. [ ] \`echo "Watch out here!" >> $GITHUB_DEBUG\`
`;
export { rawQuizdown }