## What changed

<!-- One or two sentences. Link the issue this closes, if any. -->

## Why

<!-- The problem this solves. "Because the linter said so" is not a reason. -->

## How it was checked

<!-- The commands you ran, and their result. "Not run" is an acceptable answer if explained. -->

```
python -m pytest tests/ -v --tb=short
```

## Checks

- [ ] The change is focused; unrelated cleanup is in a separate pull request
- [ ] Existing checks pass (or the failure is explained above)
- [ ] The `ci` status check is green
- [ ] New behaviour is covered by a test, or the reason it is not is stated
- [ ] No runtime dependency was added, or the reason it is unavoidable is stated
      (jaeger is standard-library-only)
- [ ] Documentation is updated if behaviour or usage changed

## If this touches learner-facing content

This repository currently has no learner-facing content, so this section does not
apply unless your change adds some. If it does:

- [ ] Keyboard-navigable, with visible focus
- [ ] Every image or canvas has a text alternative
- [ ] New terms are defined the first time they appear
- [ ] Reading level suits the intended age group
