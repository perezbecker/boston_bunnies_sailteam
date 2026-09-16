# Lahar

A small mechanical self-steering downwind trimaran. No electronics.

**Current design: [v2 one-piece prototype](v2/README.md), revised 2026-09-15.**
The enclosed main hull, amas, beams and skeg print together **deck-down**, with
continuous rounded bottoms and no glued lids or ama joints. The body is 220 mm
long, 199.4 mm wide, and the boat is approximately 318 g nominal all-up. A solid
printed vane, two four-bolt yard clamps and recessed steering-mount guides are
included. All assets are together in [v2](v2/).

![Lahar v2](v2/renders/hero.png)

## Build v2

- [MK4S printing instructions](v2/instructions.md)
- [Design, material reuse and assembly](v2/docs/design-spec.md)
- [Clamp and keyed-mount details](v2/renders/assembly-details.png)
- [FreeCAD assembly](v2/cad/Lahar_v2.FCStd) and [source macro](v2/cad/lahar.FCMacro)
- [USB G-code](v2/print/usb/) and [PrusaSlicer projects](v2/print/projects/)
- [Renders](v2/renders/) and [validation reports](v2/reports/)

Files are for the confirmed **MK4S, stock 0.4 mm high-flow nozzle, PLA, smooth
PEI, no MMU**. All parts fit in two jobs. Print the steering/clamps/coupon job
first, check fit, then print the body. Software checks passed; the prototype
has not been physically printed, seal-tested or sailed. The clevis's fork gap
still needs a fit check. Do not use v1's CORE One+ G-code on the MK4S.
Both yard clamps together need eight M2 x 16 socket-cap bolts and eight standard
M2 hex nuts. The steering stands locate in their recessed keys and are glued
to the deck; there are no screw holes into the hull.

## Version history

| Version | Status | Record |
| --- | --- | --- |
| [v2](v2/README.md) | Current one-piece prototype; software checked | Integrated rounded body, solid vane, two four-bolt clamps, recessed steering guides and two MK4S jobs |
| [v1](versions/v1/) | Archived; physically printed by the owner | Original assets preserved unchanged; [field observations](versions/v1/FIELD-NOTES.md) record leakage and fit problems |

The older pre-audit draft remains in git history at `4af5a90`; it was never a
separate printed version. See the [versioning rules](versions/README.md).
