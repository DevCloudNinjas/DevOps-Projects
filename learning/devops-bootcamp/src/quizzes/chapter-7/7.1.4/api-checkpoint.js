const rawQuizdown = `
---
shuffleAnswers: true
---
# What would the following request do?

\`\`\`bash
curl http://localhost:8080/engineers \

    		--include \

    		--header "Content-Type: application/json" \

    		--request "POST" \

    		--data '{"name": "Ryan","email": "ryan@ferrets.com"}'
\`\`\`

- [x] Create an engineer with the name Ryan.
    > Correct! The request type "POST" will cause a new resource to be created.
- [ ] Update an engineer with the name Ryan.
    > Take a closer look at the request type. What does "POST" do?
- [ ] Delete an engineer with the name Ryan.
    > Take a closer look at the request type. What does "POST" do?
`;

export { rawQuizdown }