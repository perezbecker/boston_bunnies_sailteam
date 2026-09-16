# Printing Lahar v2 on the Prusa MK4S

These files are for the setup confirmed on 2026-09-15: **Original Prusa MK4S,
stock 0.4 mm high-flow nozzle, ordinary 1.75 mm PLA, smooth PEI, no MMU**.
Other nozzles, materials, printer models, or an MMU require re-slicing.

**Prototype status:** CAD, meshes, slicing, and project re-slicing have been
checked. The actual print, hardware fit, seal, and sailing behavior have not.
Start with the combined steering, clamps and coupon job. Do not interpret a successful slice as proof of
watertightness or steering performance.

**Use the one-piece revision below.** It replaces the earlier separate-hull/lid
v2 draft. There is now one body job, with the deck flat on the bed and rounded
bottoms upward. The amas, crossbeams and skeg are part of that same print.
The latest body has recessed steering-mount keys; its matching stands have feet.
All 16 parts now fit in **two jobs**. The steering job includes the solid vane,
both four-bolt yard-clamp sets and the fit coupon. Only placement and job grouping
changed; no part was resized or omitted. The standalone coupon job is no longer needed.
Do not mix the updated keyed stands with an earlier unkeyed v2 body.

## USB files

Print the steering job first, check the hardware fits, then print the body.
Print each job once, clearing the sheet between jobs:

| File | Contents | Normal-mode estimate | PLA including waste |
| --- | --- | --- | --- |
| [Lahar_v2_Steering_MK4S_PLA_04.gcode](print/usb/Lahar_v2_Steering_MK4S_PLA_04.gcode) | Fifteen parts: eight steering parts, six clamp pieces and the fit coupon | 6 h 4 min 48 s | 58.03 g |
| [Lahar_v2_Body_MK4S_PLA_04.gcode](print/usb/Lahar_v2_Body_MK4S_PLA_04.gcode) | Enclosed main hull, two amas, beams, skeg and steering-mount recesses, all deck-down | 26 h 3 min 12 s | 238.82 g |

Total: **32 h 8 min, 296.85 g**, including the coupon, supports and brims.
Have at least 350 g available to allow for loading and a repeat fit test.
These are ordinary text G-code files, not binary BGCODE. They have no thumbnail.

Use a working FAT32 USB drive. Copy the two linked G-code files to it, safely
eject, and insert it into the MK4S. Do not rename an STL or 3MF to G-code.
Do not reformat a working drive; formatting erases its contents.

## Fit check before the body

The coupon now shares the steering bed with all the other small parts. After
that job finishes, remove the parts, clear the sheet and use the coupon and
actual printed clamps to check fit before committing to the long body print.

Hold the coupon with the three projecting tongues pointing away from you.
From left to right, their thicknesses are **1.5, 1.8, 2.1 mm**; all have a
**2.3 mm pivot hole**. Behind those tongues, the bearing recess diameters are
**10.1, 10.2, 10.3 mm**, respectively. The larger hole between the first two
bearing recesses is the **6.4 mm mast gauge**; the smaller hole between the
second and third is the **3.2 mm stock-socket gauge**.

1. Remove the brim and small burrs without changing the test surfaces.
2. Try your clevis on the middle, 1.8 mm tongue. Its M2 pivot screw must pass
   freely, and the joint must rotate without squeezing the plastic between
   the cheeks. Check clearance after the screw is securely retained.
3. Try a 623ZZ bearing in the middle, 10.2 mm recess. It must seat without
   force that distorts the outer race. Try the neighboring diameters to learn
   which fit your printer produces. Never hammer a bearing into place.
4. Test the 6 mm mast and 3 mm carbon stock. Also slide the carbon stock through
   the real bearing before assembly; a printed gauge cannot certify that fit.
5. If the middle sizes do not work after removing burrs, stop before the body
   job. Change `TAB_THICKNESS`, `PIN_DIAMETER`, `BEARING_OD`, `MAST_DIAMETER`, or
   `STOCK_SOCKET` in the [macro](cad/lahar.FCMacro), then rebuild the affected files.
   Do not scale the entire boat to fix a hole.

The manufacturer's image gives the clevis's **8 mm outside width**, not its
inside gap. The middle tongue is a proposed fit, not a manufacturer-certified
dimension. The [design guide](docs/design-spec.md#clevis-and-pushrod) records
the verified and unknown dimensions.

The coupon checks the original rod sockets and clevis interface, not the new
clamp grooves, nut pockets or locating feet. Dry-fit the printed clamps with
your actual **eight M2 x 16 socket-cap bolts and eight standard M2 hex nuts**
before installing the sail. The clamp grooves are 6.2 and 4.2 mm, with split
gaps for tightening around nominal 6 and 4 mm dowels.

## Prepare and print

1. Complete the MK4S self-test and calibration, and confirm a normal Prusa test
   print works. Use current stable firmware from Prusa. Check that the physical
   nozzle is the stock 0.4 mm high-flow type.
2. With the machine cool, remove old prints and debris. Clean the smooth PEI
   sheet with plain 90%+ isopropyl alcohol and a clean paper towel; wash persistent
   grease off the removed sheet with dish soap and water, rinse, and dry.
3. Load ordinary PLA through the printer's filament-loading menu. These jobs use
   **230 C first layer, 225 C subsequent layers, and a 60 C bed**. Check the
   filament manufacturer's range; unsuitable PLA needs its own profile.
4. Select the appropriate file in **Print**. Keep all printer, nozzle and
   firmware compatibility checks enabled. Never dismiss a mismatch warning.
5. Let the printer finish its normal preheat, homing, nozzle cleaning, mesh
   probing and purge sequence. The temporary low nozzle temperature is intentional.
6. Watch the entire first layer. Stop if extrusion is intermittent, lines do
   not bond, a part lifts, or plastic accumulates on the nozzle. Wait for the
   machine to cool before reaching in or removing the sheet.
7. Check long jobs periodically. The body prints **deck-down, rounded bottoms
   upward**, like v1. Its 220 x 199.4 mm footprint, including the attached amas,
   fits the MK4S's 250 x 210 mm bed with the supplied brim. No removable support
   belongs inside the hulls; the modeled ribs and sloped roofs remain in the boat.
8. Let each completed job cool. Flex the sheet gently. Remove steering supports
   carefully, especially beneath the solid vane, mounting feet, clamp grooves,
   short stock guides, bearing shoulders and rudder socket. Do not lever against
   the 1 mm vane web or its counterweight arm. Clear supports from all four bolt
   passages and the captive nut pockets on each clamp set.
9. Support the cooled body under its hulls while releasing it; do not pull on
   an ama or the skeg. Check the outer walls, deck and rounded closures for
   voids, then weigh the cleaned parts and soak-test the body before adding the rig.

The [assembly-detail image](renders/assembly-details.png) and
[yard-clamp instructions](docs/design-spec.md#yard-clamps) identify the clamp
pieces. Print this job once: it already contains both complete sets. Metal
bolts and nuts are not printed. The [mount guide](docs/design-spec.md#steering-mount-guides)
shows where each stand belongs; dry-fit its feet in the shallow recesses and
then glue its base to the deck. Do not drill or deepen those recesses.

The MK4S is a bed-slinger, not a CORE One+ with chamber ventilation. Leave room
for bed motion. If it is inside a separate enclosure, follow Prusa's PLA
ventilation guidance; do not apply CORE One+ door/grille instructions to it.

## What is and is not the same as v1

| Setting | v1 | v2 |
| --- | --- | --- |
| Printer | CORE One / One+ HF0.4 | Original Prusa MK4S HF0.4 |
| Body construction / orientation | Integrated closed body, deck-down | Integrated closed body, deck-down |
| Layers / first layer | 0.15 / 0.20 mm | 0.15 / 0.20 mm |
| Perimeters | 2 | 4, 0.45 mm requested width |
| Top / bottom solid layers | 4 / 4 | Body 12 / 12; steering and coupon 8 / 12 |
| Hull cavities | Slicer infill: main 4%, amas 0% | 46 explicit enclosed CAD cells with 45-degree internal roofs |
| Infill in actual modeled plastic | Low-density body | 100% rectilinear; the hull cavities remain empty |
| Hull supports | Off, internal bridge warning | Off, no slicing warnings |
| Steering supports | Automatic snug | Automatic snug, build-plate only, 0.20 mm contact gap |
| Brim setting | 3 mm | 3 mm; actual brim extent depends on first-layer footprint |
| Perimeter / external speed | 60 / 40 mm/s | 40 / 25 mm/s |

The official presets are `0.15mm STRUCTURAL @MK4S 0.4`,
`Generic PLA @MK4S HF0.4`, and `Original Prusa MK4S HF0.4 nozzle`, from
PrusaSlicer 2.9.6. Startup and shutdown commands come from that printer preset,
not from the old CORE One+ files. Every project has a full resolved configuration.
The body uses the classic perimeter generator with thin-wall detection and
180-degree bridge direction. These settings were checked on the actual ribs
and final roof closures; changing them requires another preview and test.

## Inspect or re-slice

Open these **as projects**, not as imported geometry:

- [Steering, clamps and coupon project](print/projects/Lahar_v2_Steering_MK4S_PLA_04.3mf)
- [Body project](print/projects/Lahar_v2_Body_MK4S_PLA_04.3mf)

Use Preview to inspect the continuous first-layer deck and beams, rounded outer
walls, internal ribs and sloped closures, blind mast well and guide recesses,
solid vane web, thin tongues, clamp grooves and steering supports. The [STLs](print/stl/) are already
in millimetres and print-oriented. Do not flip them again.

The [assembly guide](docs/design-spec.md#rebuilding) includes rebuild commands.
Changing a 3MF or the macro does not update an existing G-code file.

## Checks performed

FreeCAD 1.1.3 and official PrusaSlicer 2.9.6 were used. All 16 meshes are closed
and manifold; printable CAD parts are valid single solids. The saved FreeCAD
document was reopened successfully. The body has one connected exterior and
46 closed internal cells. Both supplied slices completed without warnings;
the combined steering job has 14,716 actual support extrusion moves. Model extrusion paths fit
the MK4S's 250 x 210 x 220 mm volume. Each self-contained 3MF was re-sliced alone
and reproduced identical extrusion toolpaths and resolved settings.
All 16 parts appear exactly once across the two projects. The coupon remains
excluded from the assembled boat's weight even though it now shares a print job.
CAD checks also verify the solid vane web, nominal bolt/nut/dowel fit, all
eight clamp bolts, backed guide pockets, and rejection of reversed or swapped
steering stands. These remain nominal dimensions until checked on the real print.

None of those checks establishes real layer bonding, clevis fit, bearing
friction, watertightness or steering under water load. Those remain the
prototype's [acceptance tests](docs/design-spec.md#acceptance-tests).

## References

- [Official MK4S support, firmware, handbook and slicer](https://help.prusa3d.com/product/mk4s)
- [Prusa USB guidance](https://help.prusa3d.com/article/sd-cards-and-usb-drives_112291)
- [Prusa PLA guidance](https://help.prusa3d.com/article/pla_2062)
- [Prusa watertight-printing discussion](https://blog.prusa3d.com/watertight-3d-printing-part-2_53638/)