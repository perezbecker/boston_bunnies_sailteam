# Superseded versions

Frozen copies of earlier iterations of this boat. Empty for now — v1 is the first
design and is still current, so it lives at the boat root.

## Why the current design is not in here

The design you want is always at the boat root: `cad/`, `docs/`, `renders/`. Older
iterations move down into this directory when they are replaced. That keeps one
obvious answer to "which macro do I print?" no matter how many versions accumulate.

## Cutting a new version

When a design has been printed, sailed, and you're ready to change it:

1. Copy the current design down here, frozen as-is:
   ```
   mkdir -p versions/v1
   cp -r cad docs renders versions/v1/
   ```
2. Write `versions/v1/README.md` recording what that version *was* and what sailing it
   taught you — see the template below. This is the part that's easy to skip and the
   part that's worth the most later.
3. Bump the version in the macro header, in the `App.newDocument("Lahar_vN")` call, and
   in the spec title.
4. Make your changes to the macro's `PARAMETERS` block at the boat root, regenerate the
   parts, and re-render.
5. Update the boat README: new principal dimensions, and a row in the version history
   table.

## Template for a frozen version's README

```markdown
# Lahar v1

Superseded by v2 on <date>.

## What it was
<principal dimensions — beam, weight, sail, anything that changed in v2>

## What sailing it taught us
<what worked, what didn't, and the measurement or observation behind each>

## What changed in v2, and why
<each change tied to the problem it solves>
```

The third section is the one that pays off. A frozen version whose README explains
*why* it was replaced stops a later iteration from re-introducing a problem that was
already solved and forgotten.
