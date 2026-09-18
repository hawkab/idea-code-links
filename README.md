EN | [RU](README_ru.md)

# IDEA code links

Open a local file at a specific line in IntelliJ IDEA from a browser.

## Where to use

Jira, Confluence, Test IT, Allure TestOps: paste a code link into a description or link field. If `jetbrains://` is blocked, use the [demo URL](https://hawkab.github.io/idea-code-links/#css-class) instead.

## Example

Open `.code-link` in `styles.css`, line 15:

```text
jetbrains://idea/navigate/reference?project=idea-code-links&path=styles.css:15:1
```

`project` is the local project name; `path` is relative to it. The last numbers are line and column. This link uses coordinates, not a CSS selector search.

## Install

```bash
git clone https://github.com/hawkab/idea-code-links.git
```

1. Open `idea-code-links` as a project in IDEA.
2. Open the [demo](https://hawkab.github.io/idea-code-links/) and click **Open .code-link**. Allow the browser to open IDEA if prompted.
3. If it works, nothing else is needed. Otherwise, install or start JetBrains Toolbox and retry.

Only if Linux still fails: with Python 3 and `xdg-utils` installed, run from the repository, replacing the launcher path:

```bash
python3 scripts/install-linux.py /path/to/idea/bin/idea
```

This registers a user-level handler that sends IDEA navigation URLs directly to IDEA. Rerun if the launcher path changes.
