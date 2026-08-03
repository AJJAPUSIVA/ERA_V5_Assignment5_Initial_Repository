# Repository Rename Guide

## Recommended identity

- Project name: **IndicMix Lab**
- Repository slug: **`indicmix-lab`**
- Repository path: **`AJJAPUSIVA/indicmix-lab`**
- Suggested description:
  `Reproducible QLoRA experiments for Hindi/Hinglish data-mixture optimization on Qwen2.5-1.5B.`

Suggested topics:

```text
qlora
multilingual-llm
hindi
hinglish
data-mixture
reproducible-ml
qwen2
machine-learning
```

## Scientific identifiers that remain unchanged

M0, M1, model revision hashes, evidence filenames, config filenames and schema
versions remain unchanged. They are experiment provenance, not project
branding.

## Rename on GitHub

1. Open the repository.
2. Select **Settings**.
3. Under **General**, find **Repository name**.
4. Change the current name to `indicmix-lab`.
5. Confirm the rename.

## Update the local remote

```bash
git remote set-url origin https://github.com/AJJAPUSIVA/indicmix-lab.git
git remote -v
git fetch origin
```

## Preserve a historical snapshot

Before applying the rebrand:

```bash
git tag -a pre-open-source-rebrand -m "Snapshot before IndicMix Lab rebrand"
git push origin pre-open-source-rebrand
```

## Versioning

When `v1.0.0` has not been published, use it for this release.

When `v1.0.0` already exists remotely, do not rewrite the tag. Publish the
rebrand as `v1.1.0`.
