# Software Factory (V4)

## Install the loop

- Create the workflow file at `.github/workflows/software-factory.yml` for dispatch and workers.

- Create the factory configuration at `.github/factory/factory.json` for provider, routing, labels, and gates.

- Create the deterministic router at `.github/factory/route.py` using standard library code only.

- Document the installed architecture in `.github/factory/ARCHITECTURE.md` so every installed file stays readable.

- Define the labels and their commands in `.github/factory/LABELS.md`.

## Route work with receipts

- Route only an issue that carries the ready label and an explicit agent label when routing needs a forced choice.

- Assign routed work to a code agent and open a pull request for its output.

- Require a receipt for every label transition with `observed_at` and `recorded_at` values.

- Keep the execution provider abstract and default to GitHub Actions with no lock-in.

- Use a minimal token for single repo work and a GitHub App for multi repo work, with no broad personal token.

- Treat the Codex worker as unvalidated until an official action is verified.

- Refuse dispatch when the R1 breaker has tripped and keep the fail-safe direction.

## Gate work by design authority

- Require a signed design from the design authority before execution starts.

- Treat design authority as the gate and not as a human approval queue.

- Stop work that lacks design sign-off and send it back to the design authority.

- Protect the main branch with a receipt check rather than with a human approval queue.

## Stop a blocked loop instead of redispatching

- Treat a blocked receipt as a stop signal for that issue.

- Do not redispatch the same blocked issue to another worker.

- Apply a reversible pause to the blocked issue instead of letting the loop retry it.

- Journal the pause with the time, the reason, and the condition that would allow a resume.

- Route the blocked issue to the design authority for an unblock decision or a recovery plan.

- Resume only when the journaled unblock condition is met and journal the resume.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Use manual triage for a one-off issue that does not justify the full factory loop.

- Add hold-out validation before merging factory output when the change touches a contract.

- Pilot the loop in a small repo before installing it in a production repo.
