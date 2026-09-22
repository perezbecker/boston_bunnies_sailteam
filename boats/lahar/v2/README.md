# Lahar v2

Downwind trimaran prototype for the **Prusa CORE One+, stock 0.4 mm high-flow nozzle,
ordinary 1.75 mm PLA, smooth PEI, no MMU**. Design prepared 2026-09-15;
CORE One+ files prepared 2026-09-16; steering adhesion revision 2026-09-22.

**Already printed the hull? Reprint only the updated steering job.** The vane
now has a flat back so its blade contacts the bed directly, a 5 mm attached brim,
slower first-layer and motion settings, and a **solid counterweight arm with
no slot**. The hull and every other part's
geometry are unchanged. See the [retry instructions](instructions.md#steering-adhesion-revision)
and [vane bed-contact view](renders/vane-print-contact.png).

**One-piece revision:** the enclosed main hull, both amas, beams and skeg print
together, upside down, with a continuous rounded exterior. There are no separate
lids or ama joints. This replaces the earlier modular v2 draft.

**Rigging update:** the wind vane is now solid printed plastic, both yards have
four-bolt clamp sets, and both steering stands have matching recessed deck keys.
The updated steering parts fit the existing v2 body. The clamps need **eight M2 x 16
socket-cap bolts and eight standard M2 hex nuts** in total, supplied separately.

**Print experience:** the owner reports the hull printed well, but the previous
vane detached during printing. The revised steering job is software-checked,
not physically test-printed. Watertightness and steering authority still need
physical testing. For a new build, print the small-parts job first; an existing
hull can be reused. The clevis's internal fork gap is still unknown.

![Lahar v2 assembly](renders/hero.png)

## Start here

- [Printing instructions](instructions.md): two USB jobs, fit checks, and CORE One+ setup.
- [Design and assembly guide](docs/design-spec.md): sealing, linkage, weight budget, and test procedure.
- [Clamp and steering-mount details](renders/assembly-details.png): exploded assembly views.
- [Native FreeCAD assembly](cad/Lahar_v2.FCStd) and [STEP assembly](cad/Lahar_v2.step).
- [Parametric source macro](cad/lahar.FCMacro): edit parameters here to regenerate.
- [G-code](print/usb/), [self-contained 3MF projects](print/projects/), and [16 print-oriented STLs](print/stl/).

## What changed

The body restores v1's integrated, deck-down construction. Smooth half-ellipse
lofts form all three rounded hulls. The CAD has a measured **1.8 mm minimum
skin**, 0.9 mm ribs and 46 enclosed flotation cells. Hidden 45-degree roofs
close to a 0.6 mm gap, avoiding broad unsupported closures. Four perimeters
replace v1's two. The final body slice has no warnings or removable supports.
The rudder shaft stays outside the hull, eliminating that wet penetration.
Leak-testing is mandatory; a thin external seal coat may still be needed.

The quarter-chord rudder has **10.7 mm minimum clearance over its complete swept
envelope**. Both stocks use the existing 623ZZ bearings with short, loose lower
guides and inner-race spacers. The clevis tabs are **1.8 mm thick with 2.3 mm
holes**. A **64 x 96 mm solid vane with a 1.0 mm web** restores the printed blade,
with about 4.5 times v1's aerodynamic area-times-lever. Its extended counterweight
bar takes a lashed-on weight; no screw passes through it. The existing 45 mm rod and clevises
form a nominal 64 mm pin-to-pin linkage; actual insertion depth needs checking.
The flat-backed vane retains the shaft axis and nominal socket dimensions.
Filling the arm's slot adds about 0.60 g, making the complete vane about 11.18 g.
Rebalance sideways and fore-aft using the [counterweight instructions](docs/design-spec.md#counterweight-attachment).

Each yard has three printed clamp pieces and four bolts/nuts, holding the existing
6 mm mast and 4 mm yard without intersecting the rods. The steering stands fit
distinct asymmetric recesses with 1.8 mm of intact hull backing. Dry-fit them in
their keys, then bond the bases; the recesses are not snap fasteners or screw holes.

This is a conservative, heavier prototype: **220 x 199.4 x 65.2 mm body print,
about 319 g nominal all-up**, rather than v1's approximately 106 g target.
The forward hull sections have been filled out to carry the clamps and solid
vane. Minimum deck freeboard is calculated at 14.1 mm nominally and 13.0 mm at
a 340 g loading check. These are static estimates, not a certified payload or
wind rating. At 10 degrees of heel in the conservative-weight case, the low-side
deck is almost awash. Use sheltered water and verify the physical boat before sailing.

## Printer files

| Job | Time estimate | PLA including waste |
| --- | --- | --- |
| Revised steering, both clamp sets and fit coupon, 15 parts | 7 h 52 min | 53.45 g |
| One-piece body with locating recesses | 25 h 30 min | 238.81 g |

Full new-boat total: **33 h 22 min 29 s and 292.26 g**, including the coupon and
removable waste. All 16 parts are retained. The steering bed is rearranged for
its wider brim; the body files are unchanged. For this repair, only 53.45 g is
needed for the steering job, plus loading/retry allowance.
Colors in the renders distinguish materials; all G-code jobs are single-material.

**The slicing is not identical to v1.** Although both now target the CORE One+
and retain deck-down printing and 0.15 mm layers, v2 has different shell geometry,
perimeter counts, solid layers and supports. Use the current v2 files, not the
archived v1 jobs or superseded MK4S jobs. The current CORE One+ print volume is
**250 x 220 x 270 mm**; its official profile is named `Prusa CORE One HF0.4 nozzle`.

## More views and evidence

[One-piece body and print orientation](renders/one-piece-body.png) | [Hull section](renders/hull-section.png) |
[Steering](renders/steering-gear.png) | [Clamps and mount guides](renders/assembly-details.png) |
[Print layouts](renders/print-layouts.png) | [Flat vane bed contact](renders/vane-print-contact.png)

The [CAD checks](reports/cad-validation.json), [slicing checks](reports/print-validation.json),
[engineering estimates](reports/engineering.json), and [render checks](reports/render-validation.json)
record what was verified. No physical hardware fit, seal, bearing friction, or
on-water steering test has been performed.

The untouched predecessor is in [versions/v1](../versions/v1/).