const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# What are primary benefits of using self-hosted runners in GitHub Actions? Select all that apply
For help on self-hosted runners, check out the [GitHub docs](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#differences-between-github-hosted-and-self-hosted-runners)

- [x] Improved security due to the isolation of workflows on dedicated infrastructure
	> Good. With self-hosted runners, you control where they are hosted and run from, which means you can fine-tune the security to your needs
- [x] Increased control over hardware resources, software environments and build tools
	> Good. You can modify self-hosted runners to have different package dependencies/versions and build tools than the standard GitHub runners. Sometimes this is required for a project's success if no GitHub runner offers the environment you need
- [ ] Increased reliability as GitHub manages and monitors self-hosted runners 24/7
	> GitHub does not manage self-hosted runners. They only offer these services for their own hosted runners, like ubuntu-latest for example
- [ ] They are quicker and simpler to use than GitHub hosted runners
	> The main tradeoff is that self-hosted runners are less simple to use and slower to setup, but offer an extra layer of configuration to fit your needs

# When the upload artifact action *uploads an artifact*, how can you access/use it? Select all that apply
For help with the upload/artifact actions, refer to [this article](https://earthly.dev/blog/github-action-artifacts/)

- [x] It produces an external file in the runner machine that can be downloaded or used elsewhere
	> Good. In case you missed this, you can find it in the output of a workflow run that uses the upload artifact action. It will be just below the workflow flow chart
- [x] It can be referenced in other jobs using the download artifact action 
	> Good. While the output method from exercise 1 does this as well, this is an easy way to transfer data across jobs in a workflow
- [ ] The artifact automatically persists across different workflow runs and can be accessed by referencing its URL within GitHub Actions
	> Unfortunately, upload/download artifact are scoped to a single workflow. There are alternative methods for using the upload output as an input for a separate workflow

# When is it appropriate to use a composite action? Select all that apply

- [x] When you want to encapsulate multiple actions into one to be called in other workflows or repositories
- [x] When you want to abstract away complexity by avoiding repetitive code
- [ ] When you want to speed up a workflow
	> Composite actions won't result in speedup, as they're still doing the same amount of work
- [ ] When you want to migrate one workflow into another
	> Composite actions are similar to reusable workflows, but only handle a subset of actions, not the entire workflow

# True or False: When you call a reusable workflow from another workflow, it inherits the runner from the calling workflow and overwrites the runner it previously had declared
If you'd like, you can try calling your getting-started workflow from exercise 1 (which you modified to use a self-hosted runner) from the final workflow that calls the others, and make sure *that* workflow is using a GitHub runner. Take a look at the behavior of each workflow to help this make sense.
1. [ ] True
1. [x] False
	> Good. When a workflow is called from another, it is the exact same as if it was called manually or by a push. It is simply a different trigger, and doesn't modify the workflow.
`;

export { rawQuizdown }