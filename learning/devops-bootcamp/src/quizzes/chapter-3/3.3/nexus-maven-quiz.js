const rawQuizdown = `
---
shuffleQuestions: true
shuffleAnswers: true
---

# Order the following components into a pipeline that correctly utilizes the tools you have been working with in this section:

1. Checkout code from repo
2. Build artifact using ____ (place answer in the next slot) 
3. Maven
3. Run automated testing
4. Deploy to ____ (place answer in the next slot)
5. Nexus

# Suppose you were to tear down your VM that contains your self-hosted runner. Would your pipeline still work?

1. [x] No, because the runner has to be actively running in order to handle requests from the workflow
	> Good. One of the tradeoffs with self-hosted runners is that you are responsible for their hosting and ensuring that they are up and running
1. [ ] No, because once the machine shuts down GitHub will forget about and remove the runner
	> This isn't the case, thankfully. GitHub repos will remember the runners that have been created for them
1. [ ] Yes, because GitHub will cache the runner and use it itself if its machine shuts down
	> GitHub *will* remember your runner, but it will never operate it for you
1. [ ] Yes, because the pipeline we created doesn't actually utilize a runner
	> This will never be the case. GitHub actions by nature need a runner to execute them
`;

export { rawQuizdown }