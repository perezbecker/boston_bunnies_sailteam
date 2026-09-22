# Lahar

A small mechanical self-steering downwind trimaran. No electronics.

**Current design: [v2 one-piece prototype](v2/README.md), revised 2026-09-15.**
The enclosed main hull, amas, beams and skeg print together **deck-down**, with
continuous rounded bottoms and no glued lids or ama joints. The body is 220 mm
long, 199.4 mm wide, and the boat is approximately 319 g nominal all-up. A solid
printed vane, two four-bolt yard clamps and recessed steering-mount guides are
included. All assets are together in [v2](v2/).
The CORE One+ steering job was revised on 2026-09-22 after reported vane
detachment: the vane now prints directly on a flat face, with a wider brim and
slower motion. **The successfully printed hull is unchanged and can be reused.**

![Lahar v2](v2/renders/hero.png)

## Build v2

- [CORE One+ printing instructions](v2/instructions.md)
- [Steering retry and bed-contact view](v2/renders/vane-print-contact.png)
- [Design, material reuse and assembly](v2/docs/design-spec.md)
- [Clamp and keyed-mount details](v2/renders/assembly-details.png)
- [FreeCAD assembly](v2/cad/Lahar_v2.FCStd) and [source macro](v2/cad/lahar.FCMacro)
- [USB G-code](v2/print/usb/) and [PrusaSlicer projects](v2/print/projects/)
- [Renders](v2/renders/) and [validation reports](v2/reports/)

Files are for the requested **CORE One+, stock 0.4 mm high-flow nozzle, PLA, smooth
PEI, no MMU**. All parts fit in two jobs. Print the steering/clamps/coupon job
first, check fit, then print the body only if starting a new boat. The owner
reports that the hull printed well. The revised steering job is software-checked,
not physically test-printed; leak and sailing tests remain outstanding. The clevis's fork gap
still needs a fit check. Use the current v2 CORE One+ files, not the superseded
MK4S files or the archived v1 jobs.
Both yard clamps together need eight M2 x 16 socket-cap bolts and eight standard
M2 hex nuts. The steering stands locate in their recessed keys and are glued
to the deck; there are no screw holes into the hull.

## Version history

| Version | Status | Record |
| --- | --- | --- |
| [v2](v2/README.md) | Hull printed; steering adhesion revision software-checked | Existing hull preserved; flat-backed solid vane, wider steering brim, slower first layer and two CORE One+ jobs |
| [v1](versions/v1/) | Archived; physically printed by the owner | Original assets preserved unchanged; [field observations](versions/v1/FIELD-NOTES.md) record leakage and fit problems |

The older pre-audit draft remains in git history at `4af5a90`; it was never a
separate printed version. See the [versioning rules](versions/README.md).
