# Archived Lahar versions

## v1

[v1](v1/) preserves the complete previous design: its original README, printing
instructions, macro, export and slicing scripts, design specification, renders,
STLs, two 3MF projects and two CORE One+ G-code files. All original files were
compared byte-for-byte before the root-level duplicates were removed.

[FIELD-NOTES.md](v1/FIELD-NOTES.md) records the owner's 2026-09-15 observations
and why v2 replaces it. The archived original README and instructions are
historical snapshots; their older "not yet printed" wording and root-relative
rebuild examples have deliberately not been rewritten.

**Do not rebuild inside this archive.** Its scripts overwrite generated files
beside themselves. Copy a version to a separate work area before investigating
or rebuilding it. Never run these CORE One+ jobs on the MK4S.

## Current-version layout

The current design is [../v2](../v2/). Starting with v2, each active iteration
has its own explicit directory containing all its assets, and the boat README
points to it. This replaces v1's convention of putting active CAD and print
folders directly at the boat root.

## Preserve a future version

1. Record the physical observations, measured mass, water uptake, hardware
   dimensions and steering tests before changing anything.
2. Preserve the complete previous directory, including instructions, reports
   and printer files, under `versions/vN`. Do not copy only CAD and renders.
3. Verify every original file against the archive before removing a duplicate.
4. Create the next active directory, update the macro/document version, and
   regenerate its CAD, meshes, projects, G-code, reports and renders together.
5. Update the boat README and fleet entry. Clearly distinguish software checks
   from physical validation, and identify the exact printer/nozzle/material.

An archive's original assets are immutable. Add a separate field-notes file for
later observations instead of rewriting old evidence or hand-patching old G-code.
