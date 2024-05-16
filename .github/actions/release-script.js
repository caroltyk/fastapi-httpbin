//import { Octokit } from "@octokit/action";
const { Octokit } = require("@octokit/action");

const octokit = new Octokit();

const response = await octokit.request('POST /repos/caroltyk/tyk-apiops-demo/dispatches', {
    owner: context.repo.owner,
    repo: context.repo.repo,
    event_type: 'trigger',
    client_payload: {
        key: 'value'  // Payload data if needed
    }
});

console.log("dispatch status", response.status);