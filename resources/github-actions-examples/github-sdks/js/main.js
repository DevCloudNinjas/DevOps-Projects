const { Octokit, App } = require("octokit");

console.log(`TOKEN: ${process.env.GH_TOKEN}`)

const octokit = new Octokit({
    auth: process.env.GH_TOKEN
  })
  
octokit.request('POST /repos/{owner}/{repo}/git/refs', {
    owner: 'andrew-wc-brown',
    repo: 'Github-Examples',
    ref: 'refs/heads/sdksjs',
    sha: '3a652b86905ca4e7888f4898e1b6f5d957b2c926',
    headers: {
      'X-GitHub-Api-Version': '2022-11-28'
    }
  })