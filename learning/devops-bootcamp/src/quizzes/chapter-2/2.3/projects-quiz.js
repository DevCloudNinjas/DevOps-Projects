const rawQuizdown = `

# Assume a ticket is converted to an issue. Given the following project workflow, select the true statement:
![](../../../../img/github-projects.png)

1. [x] When the issue is closed, the ticket will automatically be moved to the "Done" column
1. [ ] When the ticket is moved to the "Done" column, the issue will automatically be closed
	> Not quite. Typically the issue *would* close (if the repo settings were configured right and the PR referenced it), but not because of this workflow
1. [ ] Both are true
1. [ ] Neither are true
`;

export { rawQuizdown }