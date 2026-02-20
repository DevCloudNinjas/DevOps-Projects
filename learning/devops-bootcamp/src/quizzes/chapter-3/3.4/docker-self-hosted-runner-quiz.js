const rawQuizdown = `
---
shuffleAnswers: true
---

# 1/3 - Having gone through the above exercises, you likely ran into the following scenario:<br><br>After setting up your runner-install script, copying it into the image, and running it, your self-hosted runner was configured and started.<br>What happens when you stop the container and rerun? 

1. [x] The install script fails because a runner already exists with the same name
	> Good. Without modifying your image at all, it will attempt to use the same name and GitHub's API will error
1. [ ] The install script fails because the token it uses from GitHub has expired
	> This is the case if you allow the token's expiration window to pass (1 hour) but assuming you attempt to rerun shortly after creating the runner, the token will work just fine and there is a separate issue you'll encounter
1. [ ] The install script works and starts the runner back up
	> Without using any form of caching or volumes, this will not happen
1. [ ] The install script works and creates a new runner
	> Without making any modifications to the image, this will not happen

# 2/3 - What are the solutions to this?

- [x] Change the name of the runner to create a new one
	> This is a potential solution. The root issue is creating runners with duplicate names, so you can change the name in your install script to get around this
- [x] Delete the existing runner and rerun the container
	> This is a potential solution. If you remove the existing runner, the new one can be created without any issues
- [ ] Delete the Docker image and rebuild it
	> Not quite. Without making any modifications to the image itself, this won't change anything
- [ ] Retrieve a new token from GitHub and replace it in the install script
	> While this *is* a good idea because tokens will eventually expire, it is not always required and there is a different action that must be done

# 3/3 - After fixing the issue, what problem still exists?

1. [x] The same runner as before is no longer being used. It's now an entirely new one, which essentially makes it stateless
	> Good. In the next section, you'll learn how you can use Docker Compose to alleviate this issue altogether to always use the same runner
1. [ ] There is no further issue. The previous solution solved it all perfectly
	> The previous solution does solve the problem, but a new issue arises
1. [ ] The container fails and exits because it no longer can communicate with the repo
	> This depends. If the token from GitHub has expired (1 hour window) then this is true and you will need to replace it. However, if you're running these attempts back to back then this won't be the case
1. [ ] The container fails and exits because it lacks the permissions needed to execute the script
	> Not quite. If it had the right permissions to create the initial runner, then it'll be fine for this one too
`;

export { rawQuizdown }
