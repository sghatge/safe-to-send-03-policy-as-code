"""Policy is a file, not a prompt.

A fail-closed policy evaluator for AI agent tool calls, plus a diff that replays the same
agent session under two policies and shows exactly which decisions change.
Standard library only. Policies are JSON so they can be reviewed in a pull request.
"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def matches(rule, call):
    for key, expected in rule.get("when", {}).items():
        value = call.get(key)
        if key.endswith("_over"):
            field = key[: -len("_over")]
            if not (call.get(field, 0) > expected):
                return False
        elif value != expected:
            return False
    return True


def evaluate(policy, call):
    """First matching rule for the call's tool wins. A tool with no rules is blocked."""
    rules = policy.get("tools", {}).get(call["tool"])
    if not rules:
        return "block", "fail-closed: tool not named in policy"
    for rule in rules:
        if matches(rule, call):
            return rule["decision"], rule.get("id", "unnamed rule")
    return "block", "fail-closed: no rule matched"


def replay(policy, session):
    return [(c["id"], c["tool"], *evaluate(policy, c)) for c in session]


def diff(old, new, session):
    a = {cid: (d, why) for cid, _, d, why in replay(old, session)}
    changed = []
    for cid, tool, d, why in replay(new, session):
        if a[cid][0] != d:
            changed.append({"call": cid, "tool": tool, "before": a[cid][0], "after": d, "rule": why})
    return changed


def counts(results):
    out = {}
    for _, _, d, _ in results:
        out[d] = out.get(d, 0) + 1
    return dict(sorted(out.items()))


def main(argv):
    if len(argv) == 3:
        old, new, session = load(argv[0]), load(argv[1]), load(argv[2])
        print(f"Before: {counts(replay(old, session))}")
        print(f"After:  {counts(replay(new, session))}\n")
        for c in diff(old, new, session):
            print(f"call {c['call']:>2} {c['tool']:<16} {c['before']:>15} -> {c['after']:<15} ({c['rule']})")
        return 0
    policy, session = load(argv[0]), load(argv[1])
    for cid, tool, d, why in replay(policy, session):
        print(f"call {cid:>2} {tool:<16} {d:<15} {why}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:] or ["policies/recommended.json", "policies/autopilot.json", "examples/session.json"]
    sys.exit(main(args))
