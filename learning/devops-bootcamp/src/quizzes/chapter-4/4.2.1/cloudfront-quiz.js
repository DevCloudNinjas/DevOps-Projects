const rawQuizdown = `
---
shuffleAnswers: true
shuffleQuestions: true
---

# What is the main purpose of Amazon CloudFront?

1. [x] Faster delivery of content to end users
	> Good. It speeds up delivery by caching storage at physical locations around the world to reduce the distance it needs to travel to end users
1. [ ] More secure delivery of content to end users
	> While CloudFront is secure, security is not its main purpose. If you are confused, feel free to read the [CloudFront docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
1. [ ] Storing large amounts of data for long-term archival
	> Incorrect. This is a characteristic of S3. If you are confused, feel free to read the [CloudFront docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
1. [ ] Running virtual servers for compute-intensive applications
	> Incorrect. While AWS does have services that can do this (that you'll learn about later), CloudFront is not concerned with it. If you are confused, feel free to read the [CloudFront docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)

# When you created your CloudFront distribution in Step 1 of Exercise 2, you were told to keep track of the ETag, ID, ARN, and Domain Name for further use. What command(s) can you run to retrieve these values, should you lose them?

1. [x] **aws cloudfront list-distributions** AND **aws cloudfront get-distribution**
	> Good. You can run \`aws cloudfront list-distributions\` to retrieve metadata about ALL distributions, and then you can use the ID of the specific distribution you're interested in and run \`aws cloudfront get-distribution --id ID\` to show all metadata about ONLY that distribution, including its ETag<br>Feel free to check out more information and use-cases for [list-distribution](https://docs.aws.amazon.com/cli/latest/reference/cloudfront/list-distributions.html) and [get-distribution](https://docs.aws.amazon.com/cli/latest/reference/cloudfront/get-distribution.html)
1. [ ] **aws cloudfront list-distributions**
	> Almost. This command will show metadata about ALL distributions, but will not display the ETag of any of them. You need to inspect a specific dustribution to receive that info
1. [ ] **aws cloudfront get-distribution**
	> Almost there. This command is necessary, but it requires you to use the \`--id\` flag. Where could you possibly grab the ID from if you don't have it?
1. [ ] **aws distribution list** AND **aws distribution get-distribution**
	> **distribution** is not a valid option for the AWS CLI
1. [ ] **aws distribution list**
	> **distribution** is not a valid option for the AWS CLI
1. [ ] **aws distribution get-distribution**
	> **distribution** is not a valid option for the AWS CLI

`;

export { rawQuizdown }