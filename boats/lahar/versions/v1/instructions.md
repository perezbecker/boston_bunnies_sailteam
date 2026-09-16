# Printing Lahar on a Prusa CORE One+

## Read this first

These files were prepared for the setup you confirmed: **Prusa CORE One+,
stock 0.4 mm high-flow nozzle, ordinary 1.75 mm PLA, and a smooth PEI sheet**.
They are single-material jobs, without an MMU. Do not use them unchanged on a
different printer, nozzle, or material, including PETG, silk PLA, or foaming PLA.

**Status: generated and checked in software, not physically test-printed.**
PrusaSlicer reports **"Floating bridge anchors" for the body**. Its hollow
interior and beam/float transitions include unsupported bridges. The supplied
body job preserves the design's no-support, low-infill approach, but successful
bridging and watertightness are not established. Treat it as an experimental
first print. Check the body project in PrusaSlicer Preview before printing;
do not assume that a valid mesh or completed slicing guarantees success.
The steering job has automatic, removable supports and no slicing warnings.

The sail, mast, rods, bearings, and linkage are not part of these print jobs.
See the [assembly guide and bill of materials](docs/design-spec.md).

## Files to put on the thumb drive

Copy these **two G-code files** from [print/usb](print/usb/) onto the USB drive:

| File | What it prints | Estimated time | PLA consumed |
| --- | --- | --- | --- |
| [Lahar_Body_COREONEplus_PLA_04.gcode](print/usb/Lahar_Body_COREONEplus_PLA_04.gcode) | Main hull, two side floats, beams, and skeg as one piece | 4 h 27 min | 62.0 g |
| [Lahar_Steering_COREONEplus_PLA_04.gcode](print/usb/Lahar_Steering_COREONEplus_PLA_04.gcode) | Rudder blade, tiller, vane paddle, and vane arm | 1 h 20 min | 16.5 g |

Print each file **once**, clearing the sheet between jobs. Times are slicer
estimates in normal mode, not guarantees. Consumption includes brim/support
waste; it is not the assembled boat's weight. Have at least 100 g of usable
PLA available for the two jobs. The files occupy about 20 MB combined.

The CORE One+ reads these plain-text `.gcode` files directly. No computer,
Wi-Fi, Prusa Connect account, or additional slicing is needed at the printer
once they are on the drive. Binary `.bgcode` is also supported by current
firmware, but these files do not use it. **Do not rename an STL or 3MF to G-code.**
STLs describe shapes; 3MF projects are for the slicer, not the printer's Print menu.

## Prepare the USB drive

1. Use the USB drive supplied with the printer, or a reliable USB flash drive
   formatted as **FAT32 with an MBR partition scheme**. An 8-16 GB drive is ample.
   Avoid exFAT and NTFS.
2. Connect it to your computer. If it already works with the printer, do not
   reformat it. If formatting is necessary, back up its contents and double-check
   the selected drive: formatting erases it.
3. Copy the two linked G-code files to the drive's top-level folder. Keep their
   names unchanged. You may also keep this guide on the drive for reading on a
   computer; the printer will not display Markdown instructions.
4. Wait for copying to finish, then safely eject the drive from the computer.

## Prepare the printer

1. Place the printer on a stable surface in a ventilated space. Keep its vents
   clear and keep children, pets, and loose items away from moving and hot parts.
2. Switch on the printer. For a new or newly assembled machine, complete Prusa's
   setup/self-test and calibration wizard first. Print the supplied Prusa test
   keychain successfully before making Lahar your first long job.
3. Check that the configured nozzle is the **0.4 mm high-flow nozzle** and that
   the physical nozzle matches. These files retain Prusa's printer, nozzle,
   firmware-feature, and G-code compatibility checks. Do not bypass a mismatch
   warning. Check firmware under **Info > Version info**; use current stable
   CORE One+ firmware from Prusa if an update is needed.
4. With the bed cool, remove old prints, purge lines, and debris. Make sure the
   underside of the sheet and the heatbed are clean. Seat the smooth PEI sheet
   against the rear locating pins and lay it flat. Never print on the bare heatbed.
5. Degrease the cool sheet with plain **90% or stronger isopropyl alcohol** and a
   clean paper towel. Let it evaporate before heating. Do not use hand sanitizer
   or touch the printing area afterward. PLA on clean smooth PEI normally needs
   no glue. Wash persistent grease off the removed sheet with dish soap and water,
   rinse, and dry completely before replacing it.
6. Close the door for printing. On the **CORE One+**, the printer automatically
   opens the top ventilation grille for PLA and manages the chamber fans. Keep
   that grille unobstructed; do not force it during movement. This differs from
   instructions for the original CORE One's manually operated vent.

Never put your hands inside while the printer is moving. The nozzle and bed
remain hot after a print or an abort; wait for them to cool before handling parts.

## Load PLA

1. If a different material is already loaded, select **Filament > Unload
   Filament** and follow the screen prompts. Do not pull cold filament out by force.
2. Put the PLA spool on the holder and check that it unwinds freely without a
   crossed strand. Cut the filament end to a point.
3. Feed it through the filament inlet/PTFE tube toward the Nextruder. With the
   filament sensor enabled, reaching the sensor starts loading automatically.
   Select **PLA** in the preheat prompt and wait for heating and feeding.
4. Check that filament actually emerges from the nozzle. Confirm **YES** when
   the color is correct, or **PURGE MORE** until it is. If nothing comes out,
   use **RETRY** and troubleshoot loading before printing. Remove purge waste
   only when the head is stationary, with a suitable tool; do not touch the nozzle.
5. Confirm that the screen shows PLA loaded. The supplied jobs use **230 C for
   the first layer, 225 C afterward, and a 60 C bed**, from Prusa's Generic PLA
   high-flow preset. The chamber setting is 20 C for ventilation control, not a
   request to preheat a hot enclosure. Check your spool's temperature guidance;
   if these temperatures are unsuitable, re-slice with its proper PLA profile.

## Start a print from the drive

1. Insert the USB drive into the printer's USB-A port. Leave it inserted for the
   entire job. No computer needs to remain connected.
2. Open **Print** on the LCD. Turn the knob to select the desired Lahar file and
   press it to confirm; the touchscreen can also be used where supported.
   The shorter steering job is a useful first check before committing to the body.
3. Check the filename, loaded material, and compatibility prompts. These files
   have no embedded thumbnail, so a missing picture is normal. Confirm **Print**
   to start. Menu wording can vary slightly with firmware.
4. Allow the automatic startup sequence to finish: preheating, homing, nozzle
   cleaning/probing, mesh bed leveling, final heating, and the purge line.
   The initial nozzle temperature around 170 C is intentional, not the final
   printing temperature. Do not move the sheet or touch the nozzle during probing.
5. Watch the entire first layer. The body prints **deck-down**, with all three
   hulls and connecting beams on the sheet. The steering job includes supports
   beneath the rudder and vane, plus the two flat arms. Lines should adhere
   continuously without peeling, dragging, or gathering around the nozzle.
6. If an object lifts, filament accumulates on the nozzle, or layers become loose
   strands, choose **Stop print** and confirm. Let everything cool, remove the
   failed print, clean the sheet, and correct the cause before restarting. Do not
   continue a detached print or reach in to push it back down.
7. Check progress periodically. If filament runs out, follow the printer's
   unloading/loading prompts with the same PLA type. Do not remove the USB drive
   or turn off power during normal printing. In an immediate hazard, stop the
   machine and disconnect power if safe to do so.

## Finish and assemble

1. Wait for the completion screen and for the bed and parts to cool.
2. Remove the steel sheet and gently flex it to release the print. Support the
   boat under the hulls; do not pull it free by its thin crossbeams or skeg.
3. Remove brim and steering supports carefully. The vane plate is only 1 mm
   thick. Trim and lightly deburr holes without enlarging them unnecessarily.
4. Clear every plastic fragment from the sheet and heatbed before the next job.
   Refit and clean the sheet, then repeat the Print steps for the other file.
5. Check the body for gaps or sagging near the hollow floats and beam transitions.
   Weigh it after removing waste. The design's approximately 75 g body and 106 g
   all-up targets are estimates, not the slicer's measured result or a guarantee.
6. Test flotation and leakage in a shallow container before adding the rig or
   sailing. A closed CAD mesh is not proof of a watertight FDM print. If it seeps,
   follow the sealing advice in the [design specification](docs/design-spec.md).
   Recheck total weight and balance after assembly.

## Change settings or regenerate

Open the relevant project **as a project**, not just imported geometry, in
PrusaSlicer 2.9.6 or newer:

- [Body project](print/projects/Lahar_Body_COREONEplus_PLA_04.3mf)
- [Steering project](print/projects/Lahar_Steering_COREONEplus_PLA_04.3mf)

The projects include the objects, layout, modifiers, and full resolved settings.
Prusa calls the printer preset **Prusa CORE One HF0.4 nozzle**; its bundled model
definition explicitly covers **CORE One and CORE One+**. Do not select CORE One L.

Both jobs use 0.15 mm layers throughout, a 0.20 mm first layer, two perimeters,
four top and bottom layers, and a 3 mm outer brim. The body has 4% gyroid infill
with two exact side-float modifiers at 0%; supports are off. Steering has 15%
infill and automatic snug supports from the build plate, with a 0.20 mm contact
gap. Bridge speed is 20 mm/s. Do not replace all infill with a uniform value or
scale the parts: flotation and hardware fits depend on these choices.

Review the first layer, supports, hollow closures, and bridge regions in Preview.
The body warning must be judged with a test print; simply enabling supports can
leave inaccessible support inside its hollow regions. If bridges fail, stop and
revise the local slicing or design before trying again. Export new G-code after
any change; changing a 3MF does not update the existing USB files.

The [five STLs](print/stl/) are already in millimetres and print-oriented. Do not
flip the exported body a second time. They do not carry the infill modifiers or
printer settings. The [source macro](cad/lahar.FCMacro) remains in sailing
orientation; its ellipse-axis construction was corrected to make this export work.
The measured body mesh is 200 x 197.29 x 45.63 mm; interpolated curves differ
slightly from the nominal dimensions in the original design notes.

For a reproducible rebuild from the repository root, use
[export_print.py](cad/export_print.py) with FreeCAD's Python environment and then
[slice_print.py](cad/slice_print.py) with ordinary Python 3.10+:

```sh
"$FREECAD_PYTHON" boats/lahar/cad/export_print.py --amf-dir "$WORK"
python3 boats/lahar/cad/slice_print.py \
  --slicer "$PRUSA_SLICER" --profiles "$PRUSA_PROFILES" --amf-dir "$WORK"
```

Set these variables to your FreeCAD Python executable, a temporary working
directory, the PrusaSlicer command-line executable, and its bundled PrusaResearch
profile INI. The FreeCAD environment must be able to import FreeCAD, Part, and
MeshPart; a stock Python installation cannot. With a Windows slicer launched
from WSL, put the working directory on a Windows-mounted drive. Rebuilding
overwrites the generated STLs, projects, and G-code in this boat's print folder.

Prepared using **FreeCAD 1.1.3 and official PrusaSlicer 2.9.6** on 2026-09-11.
Checks included valid single CAD solids, closed/manifold meshes, project
round-tripping, preserved zero-infill modifiers, actual steering support paths,
and extrusion bounds inside the 250 x 220 x 270 mm build volume. No physical
printer, thumb drive, hardware fit, or flotation test was performed.

## Official references

- [CORE One+ support and current downloads](https://help.prusa3d.com/product/core-one-plus)
- [CORE One+ handbook 1.02](https://www.prusa3d.com/downloads/manual/prusa3d_manual_core_one_plus_1_02_en.pdf), sections 5.5-5.8 and 6.1
- [Prusa USB drive formatting](https://help.prusa3d.com/article/sd-cards-and-usb-drives_112291)
- [Prusa PLA material guidance](https://help.prusa3d.com/article/pla_2062)
- [Official PrusaSlicer 2.9.6 release](https://github.com/prusa3d/PrusaSlicer/releases/tag/version_2.9.6)