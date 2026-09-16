# Boston Bunnies Sail Team

Boat designs of the Boston Bunnies Sail Team — small, printable, self-steering sailing
models. Each boat is a parametric FreeCAD macro plus the spec and renders that go with
it.

## Fleet

| Boat | Current | What it is |
|---|---|---|
| [**Lahar**](boats/lahar/) | v2 one-piece prototype | Rounded deck-down body with attached amas, beams and skeg. 220 mm, approximately 318 g all-up, solid vane, four-bolt yard clamps, keyed steering mounts and MK4S files. |

[![Lahar v2](boats/lahar/v2/renders/hero.png)](boats/lahar/v2/)

## Repository layout

```
boats/<name>/
  README.md          current-version entry point and version history
  v2/                all assets for the current prototype
    cad/             parametric macro, FreeCAD/STEP files and generation scripts
    docs/            design and assembly guide
    print/           STLs, self-contained 3MFs and printer-specific G-code
    renders/         CAD-derived reference views
    reports/         software checks and engineering estimates
  versions/v1/       frozen previous assets, including their original print jobs
```

The boat README points to the current version. Starting with Lahar v2, current
assets live in an explicit version directory, as requested for this prototype.
The source is [boats/lahar/v2/cad/lahar.FCMacro](boats/lahar/v2/cad/lahar.FCMacro).
Superseded assets remain under `versions/`; never rebuild or overwrite the archive.

## Working on a design

The macro is the single source of truth. Everything else — the dimensions in the spec,
the figures printed on the renders — is a snapshot derived from it. To change a design,
edit the parameter constants at the top of the macro and regenerate, rather than
hand-editing the derived numbers downstream. Numbers that get hand-patched in one place
and not another are how a spec and a render end up disagreeing about the same boat.

See [boats/lahar/versions/README.md](boats/lahar/versions/README.md) for preservation
rules. A valid model and completed slice do not prove watertightness or sailing
performance; each version records its outstanding physical tests.
