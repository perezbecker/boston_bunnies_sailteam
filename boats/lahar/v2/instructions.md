# Printing Lahar v2 on the Prusa CORE One+

These files are for the setup confirmed on 2026-09-16: **Prusa CORE One+,
stock 0.4 mm high-flow nozzle, ordinary 1.75 mm PLA, smooth PEI, no MMU**.
The steering job was revised on **2026-09-22** after the owner reported vane
detachment. The body STL, project and G-code are unchanged.
Other nozzles, materials, printer models, or an MMU require re-slicing.
These replace the previous v2 MK4S printer files. Do not run those old files on
the CORE One+, and do not bypass a printer or nozzle compatibility warning.

**Your existing hull does not need reprinting.** The owner reports that it
printed well. Print only the updated steering job to retry the failed parts.
Its geometry, first-layer paths and project re-slicing have been checked, but
the revised vane has not yet been physically printed. Hardware fit, watertightness
and sailing performance still require physical checks.

## Steering adhesion revision

- The solid vane has a common flat back across its blade, spine and counterweight
   rail. The broad 64 x 96 mm blade now prints directly on PEI, not on supports.
- The long counterweight-arm slot is now completely filled. The arm is one
   continuous solid bar, not two thin rails. Attach the balance weight around
   the bar with thread, rather than through a slot; see the
   [counterweight instructions](docs/design-spec.md#counterweight-attachment).
- A **5 mm attached brim** replaces the 3 mm steering brim. The body keeps its
   original 3 mm brim and original settings.
- Steering first-layer perimeter **and infill** speeds are **15 mm/s**. Actual
   first-layer G-code speeds are checked, not just the preset value. The earlier
   preset's separate 100 mm/s first-layer infill setting is explicitly overridden.
- First-layer acceleration is **300 mm/s2**; subsequent perimeter/external
   perimeter speeds are 30/20 mm/s, with lower acceleration and travel speed.
- The vane still uses the same 3 mm stock and nominal 3.2 mm x 32 mm blind socket.
   The socket is now cut after its braces are joined so a brace cannot block it.
   Both steering stands, keyed feet, bearings, arms, gain holes and stock axes
   are unchanged and fit the existing v2 hull.

See the [vane contact view](renders/vane-print-contact.png). Filling the slot
adds about 0.60 g to the flat-backed vane, bringing it to approximately 11.18 g.
The blade retains its 2.4 mm sideways offset and flat printing face. Rebalance
the assembled vane fore-aft and sideways before sailing. Do not glue the vane's
broad face to the boat; that face is only its printing surface. The slot was a
suspected contributor, not a confirmed cause of the earlier print failure.

Before retrying, wash the removed cool smooth PEI sheet with plain dish soap
and warm water, rinse thoroughly, dry, and handle only its edges. Clean the
nozzle tip before the loadcell probing sequence. Keep the standard PLA chamber
ventilation unobstructed. Watch the full first layer, especially the vane panel
and long counterweight rail; stop if either starts lifting. No geometry or
slicing change can guarantee adhesion on a contaminated or poorly calibrated bed.

**Use the one-piece revision below.** It replaces the earlier separate-hull/lid
v2 draft. There is now one body job, with the deck flat on the bed and rounded
bottoms upward. The amas, crossbeams and skeg are part of that same print.
The latest body has recessed steering-mount keys; its matching stands have feet.
All 16 parts still fit in **two jobs**. The revised steering layout includes
the flat-backed solid vane, both four-bolt yard-clamp sets and the fit coupon,
with room for the wider brim. The standalone coupon job is not needed.
Do not mix the updated keyed stands with an earlier unkeyed v2 body.

## USB files

For the reported failure, **reprint only the steering job**. Replace any earlier
USB copy with the current file of the same name; its new estimate is about
7 h 52 min. For a new boat, print each job once, with steering first, checking
hardware fits and clearing the sheet between jobs:

| File | Contents | Normal-mode estimate | PLA including waste |
| --- | --- | --- | --- |
| [Lahar_v2_Steering_COREONEplus_PLA_04.gcode](print/usb/Lahar_v2_Steering_COREONEplus_PLA_04.gcode) | Fifteen parts, including the flat-backed vane with solid counterweight arm, six clamp pieces and fit coupon | 7 h 52 min 7 s | 53.45 g |
| [Lahar_v2_Body_COREONEplus_PLA_04.gcode](print/usb/Lahar_v2_Body_COREONEplus_PLA_04.gcode) | Enclosed main hull, two amas, beams, skeg and steering-mount recesses, all deck-down | 25 h 30 min 22 s | 238.81 g |

Full new-boat total: **33 h 22 min 29 s, 292.26 g**, including the coupon,
supports and brims. The slower steering job uses less support material.
Have at least 350 g available to allow for loading and a repeat fit test.
These are ordinary text G-code files, not binary BGCODE. They have no thumbnail.

Use a working FAT32 USB drive. Copy the two linked G-code files to it, safely
eject, and insert it into the CORE One+. Do not rename an STL or 3MF to G-code.
Do not reformat a working drive; formatting erases its contents.

## Fit check before the body

The coupon now shares the steering bed with all the other small parts. After
that job finishes, remove the parts, clear the sheet and use the coupon and
actual printed clamps to check fit before committing to the long body print.
If the hull is already printed, use these checks before assembling the steering
onto it; there is no reason to print the body again.

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

1. Complete the CORE One+ self-test and calibration, and confirm a normal Prusa test
   print works. Use current stable firmware from Prusa. Check that the physical
   nozzle is the stock 0.4 mm high-flow type.
2. With the machine cool, remove old prints and debris. Clean the smooth PEI
   sheet with plain 90%+ isopropyl alcohol and a clean paper towel; wash persistent
   grease off the removed sheet with dish soap and water, rinse, and dry.
3. Load ordinary PLA through the printer's filament-loading menu. These jobs use
   **230 C first layer, 225 C subsequent layers, and a 60 C bed**. Check the
   filament manufacturer's range; unsuitable PLA needs its own profile.
   The 20 C chamber setting controls ventilation, not a hot-chamber preheat;
   the minimum chamber temperature is 0 C. Close the door before printing and
   leave the CORE One+'s automatic top ventilation grille unobstructed.
4. Select the appropriate file in **Print**. Keep all printer, nozzle and
   firmware compatibility checks enabled. Never dismiss a mismatch warning.
5. Let the printer finish its normal preheat, homing, nozzle cleaning, mesh
   probing and purge sequence. The temporary low nozzle temperature is intentional.
6. Watch the entire first layer. Stop if extrusion is intermittent, lines do
   not bond, a part lifts, or plastic accumulates on the nozzle. Wait for the
   machine to cool before reaching in or removing the sheet.
7. Check long jobs periodically. The body prints **deck-down, rounded bottoms
   upward**, like v1. Its 220 x 199.4 mm footprint, including the attached amas,
   fits the CORE One+'s 250 x 220 mm bed with the supplied brim. No removable support
   belongs inside the hulls; the modeled ribs and sloped roofs remain in the boat.
8. Let each completed job cool. Flex the sheet gently. Remove steering supports
   carefully around the mounting feet, clamp grooves,
   short stock guides, bearing shoulders and rudder socket. Do not lever against
   the 1 mm vane web or its counterweight arm. The vane's broad face should
   release directly from the sheet, with no support interface to peel from it.
   Trim the attached brim carefully without thinning the blade or the guide feet.
   Clear supports from all four bolt
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

The CORE One+ manages the PLA chamber fans and opens its top ventilation grille
automatically. Do not obstruct or force the grille during movement. This differs
from the original CORE One's manual vent. Keep the door closed during printing
and wait for the printer to stop and cool before reaching inside.

## What is and is not the same as v1

| Setting | v1 | v2 |
| --- | --- | --- |
| Printer | CORE One / One+ HF0.4 | CORE One / One+ HF0.4 |
| Body construction / orientation | Integrated closed body, deck-down | Integrated closed body, deck-down |
| Layers / first layer | 0.15 / 0.20 mm | 0.15 / 0.20 mm |
| Perimeters | 2 | 4, 0.45 mm requested width |
| Top / bottom solid layers | 4 / 4 | Body 12 / 12; steering and coupon 8 / 12 |
| Hull cavities | Slicer infill: main 4%, amas 0% | 46 explicit enclosed CAD cells with 45-degree internal roofs |
| Infill in actual modeled plastic | Low-density body | 100% rectilinear; the hull cavities remain empty |
| Hull supports | Off, internal bridge warning | Off, no slicing warnings |
| Steering supports | Automatic snug | Automatic snug, build-plate only, 0.20 mm contact gap |
| Brim setting | 3 mm | Body 3 mm; steering 5 mm with zero separation |
| Perimeter / external speed | 60 / 40 mm/s | Body 40 / 25 mm/s; steering 30 / 20 mm/s |

The official presets are `0.15mm STRUCTURAL @COREONE 0.4`,
`Generic PLA @COREONE HF0.4`, and `Prusa CORE One HF0.4 nozzle`, from
PrusaSlicer 2.9.6. Startup and shutdown commands come from that printer preset,
including chamber controls and compatibility checks; the old MK4S G-code was
not renamed or hand-edited. The bundled `COREONE` model explicitly covers
**CORE One and CORE One+**, so that model name in G-code is expected. Do not
select CORE One L. Every project has a full resolved configuration.
The body uses the classic perimeter generator with thin-wall detection and
180-degree bridge direction. These settings were checked on the actual ribs
and final roof closures; changing them requires another preview and test.

## Inspect or re-slice

Open these **as projects**, not as imported geometry:

- [Steering, clamps and coupon project](print/projects/Lahar_v2_Steering_COREONEplus_PLA_04.3mf)
- [Body project](print/projects/Lahar_v2_Body_COREONEplus_PLA_04.3mf)

Use Preview to inspect the continuous first-layer deck and beams, rounded outer
walls, internal ribs and sloped closures, blind mast well and guide recesses,
flat vane web touching the first layer, thin tongues, clamp grooves and steering
supports. The [STLs](print/stl/) are already
in millimetres and print-oriented. Do not flip them again.

The [assembly guide](docs/design-spec.md#rebuilding) includes rebuild commands.
Changing a 3MF or the macro does not update an existing G-code file.

## Checks performed

FreeCAD 1.1.3 and official PrusaSlicer 2.9.6 were used. All 16 meshes are closed
and manifold; printable CAD parts are valid single solids. The saved FreeCAD
document was reopened successfully. The body has one connected exterior and
46 closed internal cells. Both supplied slices completed without warnings;
the revised steering job has 11,071 actual support extrusion moves. Model extrusion paths fit
the CORE One+'s 250 x 220 x 270 mm volume. Each self-contained 3MF was re-sliced alone
and reproduced identical extrusion toolpaths and resolved settings.
All 16 parts appear exactly once across the two projects. The coupon remains
excluded from the assembled boat's weight even though it now shares a print job.
CAD checks also verify the solid vane web, nominal bolt/nut/dowel fit, all
eight clamp bolts, backed guide pockets, and rejection of reversed or swapped
steering stands. These remain nominal dimensions until checked on the real print.
The vane has about 6,863 mm2 of direct CAD contact at its printing face. The
actual G-code covers more than 99% of the sampled blade interior at nominal
extrusion width with first-layer model plastic, zero support paths underneath,
and no first-layer extrusion above 15 mm/s. This is a toolpath check, not a
physical adhesion guarantee. Existing body outputs were preserved byte-for-byte.

None of those checks establishes real layer bonding, clevis fit, bearing
friction, watertightness or steering under water load. Those remain the
prototype's [acceptance tests](docs/design-spec.md#acceptance-tests).

## References

- [Official CORE One+ support, firmware, handbook and slicer](https://help.prusa3d.com/product/core-one-plus)
- [Prusa USB guidance](https://help.prusa3d.com/article/sd-cards-and-usb-drives_112291)
- [Prusa PLA guidance](https://help.prusa3d.com/article/pla_2062)
- [Prusa watertight-printing discussion](https://blog.prusa3d.com/watertight-3d-printing-part-2_53638/)