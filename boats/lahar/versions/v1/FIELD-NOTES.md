# Lahar v1 field observations

Recorded 2026-09-15, when v2 was requested. Original files in this directory
are preserved unchanged; this note updates their historical status.

## What was built

The 200 mm downwind trimaran, approximately 196-197 mm beam, with a nominal
106 g design target, 190 x 170 mm square sail, two 623ZZ bearings and an M2
clevis/pushrod linkage. The owner has physically printed v1. Its original
CORE One+ slicer jobs and all design assets are retained here.

## Owner observations

- The boat takes in water while floating. The specific entry path and leak
  rate were not measured or isolated.
- There is insufficient clearance behind the skeg for the rotating rudder,
  especially the cylindrical boss.
- The printed arms are too thick for the MECCANIXITY metal clevises, and the
  pivot holes are too small for their screws.
- The owner reports substantial apparent friction and doubts downwind steering
  authority. No measured breakaway torque or loaded steering response was supplied.
- Existing materials include the two bearings, 6 mm hardwood dowel, 3 mm carbon
  rod, 4 mm dowel, MECCANIXITY M2 45 mm rod and metal clevises.

## Why v2 changes these parts

v1's macro requests 4 mm arm thickness and 1.6 mm holes. Its rudder axis and
skeg trailing edge are both at X=172, putting the 8 mm boss in the skeg region.
Its print notes already warn about unvalidated watertightness and floating
bridge anchors. The shaft passage through the hull is another potential water
path, not a proven explanation of the owner's particular leak.

v2 uses inspectable thicker open shells with bonded lids, removes the wet shaft
penetration, checks full rudder sweep clearance, adapts the tabs and screw holes,
and uses a larger light-film vane with a less oblique linkage and better bearing
clearances. It also increases displacement and recomputes trim for the extra
weight. Its files are for the owner's confirmed MK4S, not the CORE One+.

The [v2 design guide](../../v2/docs/design-spec.md) records the remaining physical
tests. v1's asserted light-wind authority and capsize numbers are not physical
measurements and must not be carried forward as established performance.