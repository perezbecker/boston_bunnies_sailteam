# Boston Bunnies Sail Team — Downwind Trimaran

Design specification and build guide. Companion file: [`cad/BostonBunnies_Trimaran.FCMacro`](../cad/BostonBunnies_Trimaran.FCMacro)
(run inside FreeCAD via Macro → Macros… → Execute; edit the PARAMETERS block and
re-run to regenerate any part).

## Principal dimensions

| Item | Value |
|---|---|
| Length overall (main hull) | 200 mm |
| Beam overall | 191 mm |
| Main hull max beam × depth | 60 × 40 mm |
| Ama length × beam × depth | 130 × 26 × 14 mm |
| Design waterline | 16 mm below deck |
| Design displacement (all-up weight) | ~95 g |
| Ama clearance above waterline | ~2 mm ("just kissing") |
| Print footprint (one-piece body) | 200 × 191 mm, 42 mm tall — fits a 220 × 220 bed |

The hull volume was sized numerically against the weight budget below: at 95 g
all-up the boat floats with 16 mm freeboard and the amas skimming the surface.
If your build comes out heavier, the amas immerse early and drag; keep to the
budget or fatten the `MAIN_B`/`MAIN_D` station values and re-run the macro.

## Weight budget

| Component | Target |
|---|---|
| Printed tri-hull body (2 walls, 5–8 % infill) | ≤ 60 g |
| Mast + two yards + sail cloth | ≤ 12 g |
| Rudder, vane, arms (printed) + stocks | ≤ 8 g |
| Bearings, pushrod, counterweight, glue | ≤ 12 g |
| Margin | ~5 g |
| **Total** | **~95 g** |

Weigh the body after printing. If it exceeds 60 g, drop infill before touching
the design.

## Sail (you build this part)

* **Rig:** square sail on a mast with two transverse yards, exactly as you planned.
* **Sail: 160 mm wide × 200 mm tall**, flat cloth (light ripstop, a plastic bag,
  or Tyvek). Lash head and foot to the yards, mast between them.
* **Mast:** 6 mm hardwood dowel, ~330 mm long. 24 mm sits in the printed socket,
  leaving ~90 mm of clear post under the sail's foot yard.
* **Yards:** 4 mm dowel or bamboo, ~180 mm each.
* **Mast position:** the socket is at 40 % LOA from the bow — sail effort forward,
  skeg aft, per the arrow rule.
* **Wind limit:** comfortable up to ~2.5 m/s steady; a 3.5 m/s gust 30° off-axis
  will bury an ama and round the boat up. That is the design working as a fuse.
  For breezier days, lash the sail lower or roll one turn onto the top yard.

## Steering gear

Layout matches the diagram from our conversation: vane pivot at x = 140 mm,
rudder stock at x = 172 mm, skeg immediately ahead of the rudder, all on centerline.

* **Bearings:** two **623ZZ (3 × 10 × 4 mm)** pressed into the deck counterbores.
  Vane spins in one; rudder stock runs through the other plus a plain hole where
  it exits the hull bottom.
* **Stocks:** 3 mm carbon rod (best, waterproof) or bamboo skewer, ~70 mm for the
  rudder, ~60 mm for the vane. Push-fit into the printed sockets; a drop of CA if loose.
* **Vane paddle:** blade faces **forward** (downwind of the axis when running).
  Blade is 36 x 72 x 1.0 mm — deliberately thin, because blade mass is the whole
  balance problem. A 50 mm counterweight arm sits aft at the blade's vertical
  centroid (z = 62), so it trims both the yaw moment and the tipping couple on
  the bearing.
* **Balancing (do not skip):** blade moment is ~67 g.mm, arm gives back ~35 g.mm,
  leaving ~33 g.mm. An **M3 x 10 screw + nut (~0.85 g) at ~39 mm** along the slot
  cancels it. Slide the screw until the paddle sits indifferent at every angle
  with the boat tipped 10-15 deg, then lock the nut.
  Why it matters: the axis is vertical, so gravity makes no yaw torque when level
  — but at 5 deg of heel a 96 g.mm imbalance produces 0.085 N.mm, against only
  0.037 N.mm of aerodynamic torque at 1 m/s apparent wind and 10 deg of error.
  An unbalanced vane steers to the low side, not to the wind.
* **Linkage:** M2 RC threaded pushrod with a clevis at each end — your variable-
  length calibration rod. **Vane arm points to PORT, tiller arm to STARBOARD.**
  Opposite sides is mandatory: it reverses the sense so the rudder pushes the bow
  back. Same side and the boat spirals; if that happens, flip one arm.
* **Gain** = vane-hole radius ÷ tiller-hole radius. Holes at 6/10/14/18 mm (vane)
  and 12/18/24/30 mm (tiller). **Start at 6/18 ≈ 0.33.** Fishtailing → smaller
  ratio; lazy wandering → larger.

## Printing

* **Body:** flip 180° about X in the slicer so the deck is on the bed. Beams then
  lie flat on the bed, all sockets print as simple recesses, no supports. Use
  0.12–0.16 mm layers for the last 5 mm of the hull crowns (the rounded bottoms
  close like a dome). 2 perimeters, 5–8 % infill, 4 top layers for water-tightness.
* **Rudder blade & vane paddle:** print lying flat on their sides.
* **Arms:** print flat as oriented.
* PLA is fine for pond duty; seal the hull with a light acrylic spray if it seeps.

## Bill of materials

| Qty | Item |
|---|---|
| 2 | 623ZZ bearing, 3 × 10 × 4 mm |
| 1 | 6 mm hardwood dowel, ≥ 330 mm (mast) |
| 2 | 4 mm dowel/bamboo, 180 mm (yards) |
| 1 | 3 mm carbon rod or skewers, ≥ 150 mm total (stocks) |
| 1 | M2 RC pushrod + 2 clevises (adjustable link) |
| 1 | M3 × 16 screw + 2–4 nuts (vane counterweight) |
| — | Light sail cloth ~180 × 220 mm, thread, CA glue |

## First-sail checklist

1. Float the bare body: waterline should sit ~16 mm below deck, amas just clear.
   Trim with coins taped on deck if it floats bow- or stern-heavy.
2. Fit rudder only, lock it centered, sail without the vane: the skeg should give
   one gentle swing back after a nudge. Two or more overshoots → sand the skeg smaller.
3. Add the vane at gain 0.33, dead-downwind setting (arm neutral when the paddle
   points at the bow). Nudge the bow off course by hand: rudder must deflect to
   bring it back. Wrong way → swap an arm to the other side.
4. Lengthen/shorten the pushrod so the rudder is exactly centered when the vane
   is aligned — that screw adjustment is your trim tab.

## Design history (from the conversation, 25 Aug 2026)

Sideways drift traced to coincident centers of effort and lateral resistance →
fixed with the arrow rule (effort forward, resistance aft). Skeg sized against
overshoot/fishtailing. Cross-sail rejected (destabilizing vane, cos-flat gains);
keel rejected downwind (ballast useful, lateral area harmful). Trimaran chosen
over mono/cat/proa: amas need no precision because they carry no load. Amas
double-ended — transoms only pay above Froude ≈ 0.5, far beyond this scale — and
finless: all lateral resistance lives in one centerline skeg. Vane gear per
classic model-yacht practice: needle-supported vane upwind of the sail, short
vane arm / long tiller arm (gain = Lv/Lt — corrected from an earlier statement),
arms on opposite sides. Upwind conversion deferred; would need cambered sail,
daggerboard forward, and reversed CE/CLR order.
