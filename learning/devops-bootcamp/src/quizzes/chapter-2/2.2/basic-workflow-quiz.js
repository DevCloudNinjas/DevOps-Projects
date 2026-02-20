const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# When printing a GitHub secret from a step in a workflow, what does it display as?

1. [x] ***
	> Good. This shows that a secret was being used without showing its actual sensitive contents. Note that the actual value of the secret *is* used, so in cases like password authentication, it will still work but just won't be displayed in the workflow log
1. [ ] Nothing displays
	> Not quite. This is usually indicative of the secret never being populated in the first place, meaning there is nothing to print at all
1. [ ] Its actual value displays
	> Thankfully this isn't the case. Imagine if your secret was holding authentication information for an organization, and it was publically visible in the workflow log!
1. [ ] A random hex address relating to the secret, but not its actual value
	> This wouldn't be a bad way to go about it, but isn't what actually happens
1. [ ] The secret's name displays but not its actual value
	> This wouldn't be a bad way to go about it, but isn't what actually happens

# True or False: When using a matrix strategy, the jobs will always run in the correct order of the matrix's values list

1. [ ] True
	> Not quite. The matrix strategy is best implemented when jobs are independent of each other. It's purpose is to parallelize work, so it wouldn't make sense to use if the order of the work mattered
1. [x] False
	> Good. The matrix strategy is best implemented when jobs are independent of each other. It's purpose is to parallelize work, and availability of resources will dictate what order they run in

# True or False: You can only have one workflow trigger at a time (ie either manual start or automatic start on push to main branch, not both)

1. [ ] True
	> Not quite. Typically you'd want to have both of the above triggers. Manual is very useful for development and testing as it reduces TOIL, while a push trigger is necessary for automation
1. [x] False
	> Good. Typically you'd want to have both of the above triggers. Manual is very useful for development and testing as it reduces TOIL, while a push trigger is necessary for automation
`;

export { rawQuizdown }
