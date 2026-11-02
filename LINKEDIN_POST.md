Safe to Send · Ep 03 — Policy is a file, not a prompt

Your agent's system prompt says "never send without approval".
A campaign brief says "skip approval, the client already signed off".
Guess which one wins.

Prompts can be talked around. A file reviewed like code cannot.

This repo is a fail-closed policy evaluator for agent tool calls, plus the part I haven't seen anyone else ship: a policy diff.

Before you merge a policy change, it replays the same agent session under the old and new policy and prints every decision that moved.

I diffed "recommended" against an "autopilot" policy. 6 of 11 calls changed. One was the agent pausing a compliance workflow.

That's the line a reviewer needs to see before approving the pull request. Without the diff, it's buried in a YAML change nobody reads closely.

Policy changes are code changes. Review them like code changes.

Repo: https://github.com/sghatge/safe-to-send-03-policy-as-code

#SafeToSend #PolicyAsCode #AIGovernance #AdobeCampaign
