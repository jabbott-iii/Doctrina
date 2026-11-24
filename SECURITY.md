# Security policy

Report a security vulnerability in Doctrina privately, through GitHub, and never in a public
issue, discussion, or pull request.

## Supported versions

Doctrina has no releases. Fixes go to the `main` branch only, so report what you find against the
latest commit on `main`.

## Report a vulnerability

1. Open the repository's **Security and quality** tab.
2. Select **Report a vulnerability**. The form is also at
   <https://github.com/jabbott-iii/Doctrina/security/advisories/new>.
3. Fill in the form and submit it. The report stays private: only you and the repository's
   maintainers can see it.

Include:

- the file and the commit you found the problem in;
- the steps or the proof of concept that show it;
- what an attacker could do with it, and to whom;
- how to reach you, if not through the report.

Test only on your own systems and data, never against someone else's repository or deployment.

## What's in scope

- **The rules and skills** in `rules/`, `skills/`, and `.claude/`: any text that would lead a
  coding agent that follows it to leak secrets or personal data, run commands the user didn't ask
  for, weaken a security control, or obey instructions hidden in the text it reads.
- **The code** in the courses, such as `courses/lua101/lualab/` and `courses/lua101/tools/`.
- **The GitHub Actions workflows** in `.github/workflows/`.

These are out of scope:

- The answer keys in each course's `solutions/` folder, which are public on purpose.
- A vulnerability in a dependency, such as JupyterLab, nbgrader, or lupa. Report it to that
  project, through its own security policy.
- A repository that copied a Doctrina rule or skill. Report it to that repository's maintainers.

## What happens next

The maintainer reads each report and replies through it. A confirmed vulnerability is fixed in
private and then disclosed in a GitHub security advisory on this repository, which credits you
unless you'd rather not be named. Doctrina doesn't promise a response time.
