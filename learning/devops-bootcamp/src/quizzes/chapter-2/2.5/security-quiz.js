const rawQuizdown= `

---
shuffleQuestions: true
---

# Which tool is most effective for automatically upgrading libraries to reduce security vulnerabilities?

1. [x] Dependabot
1. [ ] Code scanning
1. [ ] Secret Scanning

# SOS!!! Your SQL database just got dropped by maliscious data injection! Which of the tools mentioned above can you apply to help prevent this in the future?

1. [ ] Dependabot
1. [x] Code scanning
	> Good. Code Scanning can be added to your pipeline to track down security risks such as SQL injection vulnerabilities. So long, Johnny Drop Tables :)
1. [ ] Secret Scanning

# Which tool would stop you from committing a token to a GitHub repo?

1. [ ] Dependabot
1. [ ] Code scanning
1. [x] Secret Scanning
	> Most of us, at one point or another, have accidentally pushed a token to a GitHub repo. It's a simple mistake, but can easily get you into a serious mess. You'll thank yourself later if you turn this on
`;

export { rawQuizdown }