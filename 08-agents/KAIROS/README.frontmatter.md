# KAIROS · Frontmatter Validation quick start

## Install and run locally
```bash
cd 08-agents/KAIROS
make schema.check        # validate schema itself
make fm.validate         # good examples must PASS
make fm.validate.bad     # bad examples must FAIL (as expected)
```
