# Lahar v1 — Downwind Trimaran

Boston Bunnies Sail Team. Design specification and build guide. Companion file:
[`cad/lahar.FCMacro`](../cad/lahar.FCMacro) (run inside FreeCAD via Macro → Macros…
→ Execute; edit the PARAMETERS block and re-run to regenerate any part).

## Principal dimensions

| Item | Value |
|---|---|
| Length overall (main hull) | 200 mm |
| Beam overall | 196 mm |
| Main hull max beam × depth | 69 × 40 mm (fullest section aft of midships) |
| Ama length × beam × depth | 165 × 31 × 14.5 mm |
| Design waterline | ~16 mm below deck at 106 g |
| Design displacement (all-up weight) | ~106 g |
| Ama clearance above waterline | +1.4 mm at 106 g (+0.4 mm even at 114 g) |
| Print footprint (one-piece body) | 200 × 196 mm, 46 mm tall — fits a 220 × 220 bed |

Sized by a full end-to-end audit (mass build-up -> equilibrium waterline ->
trim -> stability -> balance). The fullest hull section sits aft of midships so
the centre of buoyancy (x=106) lands under the centre of gravity (x=111): the
boat floats with a mild +2.3 deg stern-down trim, which lightens the bow and
helps downwind tracking. If your build comes out heavier than the table below,
the amas immerse early and drag; re-run the macro with fatter `MAIN_B` values.

## Weight budget

| Component | Estimate | Print settings that matter |
|---|---|---|
| Main hull (in body) | ~42 g | 2 perimeters (0.8 mm), **4 % infill**, 4 top layers |
| Both amas (in body) | ~17 g | **0 % infill** — they are floats |
| Beams, gussets, skeg, pads (in body) | ~16 g | print as sliced |
| Mast + yards + cloth | ~10.5 g | 6 mm + 4 mm dowels, light cloth |
| Printed steering parts + stocks | ~9 g | rudder/vane/arms, 3 mm rods |
| Bearings, pushrod, screw, glue | ~11 g | 623ZZ x2, M2 rod, M3 screw |
| **All-up** | **~106 g** | |

Weigh the printed body: target ~75 g. Every extra 8 g costs ~1 mm of ama
clearance; the design still floats the amas clear at 114 g all-up.

## Sail (you build this part)

* **Rig:** square sail on a mast with two transverse yards, exactly as you planned.
* **Sail: 190 mm wide × 170 mm tall**, flat cloth (light ripstop, a plastic bag,
  or Tyvek). Lash head and foot to the yards, mast between them.
  Same area as a 160 x 200 sail but 65 mm lower in the air — see stability below.
* **Mast:** 6 mm hardwood dowel, ~250 mm long. 24 mm sits in the printed socket;
  foot yard at 40 mm above deck, head yard at 210 mm.
* **Yards:** 4 mm dowel or bamboo, ~210 mm each.
* **Mast position:** the socket is at 40 % LOA from the bow — sail effort forward,
  skeg aft, per the arrow rule.
### Stability (why the rig is short and wide)

Sail centre of effort is **125 mm above deck**; heeling lever to the centre of
lateral resistance is 135 mm. One fully buried ama gives **30 mN·m** of
righting moment (37 cm³ of buoyancy at an 82.5 mm arm).

| Apparent wind, 30° off axis | Heeling moment |
|---|---|
| 2.0 m/s | 6.4 mN·m |
| 3.0 m/s | 14.4 mN·m |
| 3.5 m/s | 19.6 mN·m |
| 4.3 m/s | **30 mN·m — capsize** |

* **Wind limit:** comfortable to ~3.3 m/s apparent; capsize at ~4.3 m/s in a
  30° gust. Note apparent wind downwind is true wind *minus* boat speed, so the
  boat is most vulnerable at the moment you let it go, before it accelerates.
* A 200 mm tall sail on a 330 mm mast (the first version of this design) put the
  CE at 190 mm and dropped the capsize threshold to ~3.5 m/s. Trading height for
  width at constant area bought 21 % more wind for free.
* **The main hull alone has negative GM** (about −9 mm): it is too slender to
  stand up by itself and will loll a degree or two until one ama takes up. That
  is normal trimaran behaviour, not a fault — the amas *are* the stability.
* **Lengthening the main hull does nothing for this.** BM_T = I_T/V, and both
  scale with length, so stretching 200 → 280 mm leaves BM_T at 10.2 mm exactly
  while adding 40 % wetted area. Heel resistance is a beam property. The amas
  were lengthened to 165 mm and their sections grown 12 % instead — 37 cm³ each,
  +58 % righting moment over the original amas, inside the same footprint.
* Widening the ama spacing would also help, but 82.5 mm already puts overall
  beam at 196 mm, near the limit of a 220 mm print bed.

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
  leaving ~33 g.mm. An **M3 x 16 screw + nut (~1.2 g) at ~28 mm** along the slot
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
  close like a dome). 2 perimeters; **4 % infill in the main hull, 0 % in the amas** — the weight
  budget and ama clearance depend on these — 4 top layers for water-tightness.
* **Rudder blade & vane paddle:** print lying flat on their sides.
* **Arms:** print flat as oriented.
* PLA is fine for pond duty; seal the hull with a light acrylic spray if it seeps.

## Bill of materials

| Qty | Item |
|---|---|
| 2 | 623ZZ bearing, 3 × 10 × 4 mm |
| 1 | 6 mm hardwood dowel, ≥ 260 mm (mast, cut to 250) |
| 2 | 4 mm dowel/bamboo, 210 mm (yards) |
| 1 | 3 mm carbon rod or skewers, ≥ 150 mm total (stocks) |
| 1 | M2 RC pushrod + 2 clevises (adjustable link) |
| 1 | M3 × 16 screw + 2–4 nuts (vane counterweight) |
| — | Light sail cloth ~210 × 190 mm (finished sail 190 × 170), thread, CA glue |

## First-sail checklist

1. Float the bare body: waterline ~16 mm below deck, amas just clear, and a
   *slight stern-down attitude is correct* — the design puts LCG a few mm aft
   of LCB on purpose. Trim with coins only if the bow digs or the stern is awash.
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

## End-to-end audit summary (25 Aug 2026)

Computed, not assumed: all-up 106 g floats at 15.9 mm freeboard with +1.4 mm ama
clearance (robust −8/+8 g). Trim +2.3 deg stern-down (LCB 106 / LCG 111). Sail
CE at x=80 vs CLR at x=122: 21 % LOA separation — arrow-rule stable. Capsize at
4.3 m/s apparent (30 deg gust), comfortable to ~3.3 m/s. Expected boat speed
0.5–0.7 m/s (Fr ≈ 0.45–0.5, wave-drag limited), so apparent wind ≈ true − 0.6.
Vane torque at 1 m/s apparent and 10 deg error is ~0.037 N·mm vs ~0.003 N·mm of
friction + residual-imbalance losses: authority margin >10x once the boat has
any breeze; below ~0.7 m/s apparent the vane will wander — that is physics, not
a defect. Geometry cleared: socket floors ≥ 14 mm, bearing pads ≥ 31 mm wide,
skeg embeds 25 mm into the hull, body 200 × 196 × 46 mm on a 220 × 220 bed.
Corrections made during audit: weight budget raised 95 → 106 g (original was
optimistic), main hull widened and its volume shifted aft to cure a 5.7 deg
stern squat, amas re-proportioned wider/shallower, skeg and rudder deepened to
keep grip under the deeper hull.
