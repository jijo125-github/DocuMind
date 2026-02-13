Conversations folder

This folder contains saved conversation exports and summaries for the DocuMind project.

Suggested workflow:

1. Commit the folder to git:

```bash
git add conversations
git commit -m "chore: add chat export and summary for DocuMind"
```

2. If you want the raw JSON inside this folder, move it:

```bash
git mv ../documind_export.json conversations/
```

3. Use these files as reference when resuming work, writing the README, or preparing interview materials.

If you'd like, I can:
- Move the raw export into this folder.
- Create a markdown conversion of the full conversation (large) for easier reading.
- Open a PR with these changes.
