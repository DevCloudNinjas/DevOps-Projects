const rawQuizdown = `

# Assume you want to scrape a GitHub org for an entire list of its users and rich details about each of their repositories. Keeping rate limiting and efficiency in mind, which GitHub API would be preferable?

1. [x] REST
	> Good. You could achieve this in just one or two API calls
1. [ ] GraphQL
	> In order to find all this info, you'd need to make many more API calls than with REST
1. [ ] It doesn't make a difference
	> While both APIs could query for all this information, they do so in different amounts of API calls

# Assume you want to scrape a GitHub org for a specific repository's contributors list. Keeping rate limiting and efficiency in mind, which GitHub API would be preferable?

1. [ ] REST
	> REST does query for this pretty easily due to it having dedicated endpoints for certain things, but it's important to understand how GraphQL handles it, as well
1. [ ] GraphQL
	> GraphQL does do this very simply, but there is something else to keep in mind. While much of the time GraphQL *is* optimal for finer tuned examples, REST has something put in place for certain specific queries
1. [x] It doesn't make a difference
	> While you might think that GraphQL is optimal for this because REST typically returns more data than necessary, it's important to keep in mind REST's API endpoints. For example, REST has a **GET /repos/{owner}/{repo}/contributors** dedicated endpoint to retrieve exactly what is needed here. Because GraphQL can also perform this rather simply, it doesn't make much of a difference for this example

# Which of the following statements are true? Select all that apply

- [x] REST uses a uniform interface and a set of predefined endpoints to interact with resources
- [ ] REST allows clients to specify the exact structure of the response and fetch only the required data
- [ ] GraphQL uses a uniform interface and a set of predefined endpoints to interact with resources
- [x] GraphQL allows clients to specify the exact structure of the response and fetch only the required data

`;

export { rawQuizdown }