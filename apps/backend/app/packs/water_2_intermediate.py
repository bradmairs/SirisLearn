"""Civil and water engineering design: intermediate."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, path, svg, text, title

LOSSES = svg(
    title("Energy and hydraulic grade lines"),
    box(20, 50, 80, 60, "Tank A", BLUE, size=12), box(390, 140, 80, 60, "Tank B", BLUE, size=12),
    line(20, 60, 100, 60, BLUE, 2), line(390, 150, 470, 150, BLUE, 2),
    path("M100 100 L390 190", INK, 6), text(245, 170, "pipe, length L, diameter D", 11, MUTED),
    line(100, 60, 390, 150, GREEN, 2, "6 4"), text(250, 92, "HGL falls by hf", 12, GREEN),
    line(100, 50, 390, 140, PURPLE, 2, "2 4"), text(160, 45, "EGL", 12, PURPLE),
    arrow(430, 60, 430, 145, AMBER, "", 2), arrow(430, 145, 430, 60, AMBER, "", 2),
    text(440, 105, "H", 15, AMBER, anchor="start", weight="bold"),
    text(240, 250, "H = hf + minor losses (entry, bends, valves, exit)", 12, INK),
    text(240, 272, "the gap EGL−HGL is the velocity head V²/2g", 11, MUTED),
)

PUMP = svg(
    title("Pump curve meets system curve"),
    line(60, 250, 450, 250, MUTED, 2), line(60, 250, 60, 50, MUTED, 2),
    text(255, 280, "Flow Q (L/s)", 12, MUTED), text(40, 150, "Head", 12, MUTED, anchor="middle"),
    path("M60 75 Q250 85 430 230", BLUE, 3), text(420, 205, "pump", 12, BLUE, anchor="end"),
    path("M60 190 Q260 170 430 70", AMBER, 3), text(430, 62, "system", 12, AMBER, anchor="end"),
    line(60, 190, 450, 190, MUTED, 1, "4 4"), text(445, 184, "static lift", 11, MUTED, anchor="end"),
    circle(305, 140, 8, GREEN, "#0b1620"), text(318, 132, "D", 15, GREEN, anchor="start", weight="bold"),
    line(305, 148, 305, 250, GREEN, 1, "3 3"),
)

PARTIAL = svg(
    title("Partly full circular pipe"),
    circle(150, 150, 90, INK),
    '<path d="M70 192 A90 90 0 0 0 230 192 Z" fill="#5fd3ff" opacity="0.45"/>',
    line(70, 192, 230, 192, BLUE, 2), text(150, 185, "water surface", 11, BLUE),
    arrow(255, 240, 255, 192, AMBER, "", 2), arrow(255, 192, 255, 240, AMBER, "", 2), text(265, 220, "d", 14, AMBER, anchor="start"),
    arrow(290, 240, 290, 60, MUTED, "", 2), arrow(290, 60, 290, 240, MUTED, "", 2), text(300, 150, "D", 14, MUTED, anchor="start"),
    text(390, 90, "Manning:", 13, INK), text(390, 115, "V = (1/n) R^(2/3) S^(1/2)", 12, INK),
    text(390, 150, "R = A / P", 12, INK), text(390, 175, "(hydraulic radius)", 11, MUTED),
    text(390, 215, "d/D ≈ 0.94 → max Q", 12, GREEN), text(390, 238, "full pipe ≈ 93% of that", 11, MUTED),
)

MAIN = svg(
    title("Sizing a reticulation main"),
    box(20, 60, 100, 50, "Reservoir", BLUE, size=12, sub="TWL 180 m"),
    line(120, 85, 440, 85, BLUE, 5), text(280, 75, "DN? main", 12, BLUE),
    box(300, 120, 160, 70, "New estate", INK, size=13, sub="400 lots, RL 135 m"),
    line(380, 85, 380, 120, BLUE, 3),
    circle(440, 85, 7, RED, "#0b1620"), text(440, 70, "H", 12, RED),
    text(150, 160, "check 1: peak hour,", 12, AMBER, anchor="start"),
    text(150, 178, "pressure ≥ minimum", 12, AMBER, anchor="start"),
    text(150, 215, "check 2: fire flow +", 12, RED, anchor="start"),
    text(150, 233, "background demand", 12, RED, anchor="start"),
    text(240, 272, "and velocity / water age at low demand", 11, MUTED),
)

GRAVITY = svg(
    title("Gravity sewer long section"),
    path("M30 70 L240 70 L450 60", MUTED, 2), text(60, 62, "surface", 11, MUTED),
    path("M50 150 L250 180 L450 210", AMBER, 5),
    line(50, 70, 50, 150, INK, 3), line(250, 70, 250, 180, INK, 3), line(450, 60, 450, 210, INK, 3),
    text(50, 168, "MH1", 11, INK), text(250, 198, "MH2", 11, INK), text(440, 228, "MH3", 11, INK, anchor="end"),
    text(150, 150, "DN150 @ 1 in 150", 12, AMBER), text(350, 182, "DN225 @ 1 in 200", 12, AMBER),
    text(150, 240, "depth = cover + pipe", 11, MUTED),
    text(350, 255, "grade ≥ self-cleansing", 12, GREEN),
)

TREAT = svg(
    title("Conventional water treatment"),
    box(10, 70, 70, 50, "Raw", BLUE, size=12), arrow(80, 95, 95, 95, BLUE),
    box(95, 70, 85, 50, "Coag/floc", PURPLE, size=12), arrow(180, 95, 195, 95, BLUE),
    box(195, 70, 80, 50, "Clarify", PURPLE, size=12, sub="settle/DAF"), arrow(275, 95, 290, 95, BLUE),
    box(290, 70, 75, 50, "Filter", GREEN, size=12), arrow(365, 95, 380, 95, BLUE),
    box(380, 70, 90, 50, "Disinfect", AMBER, size=12, sub="Cl₂, UV"),
    arrow(425, 120, 425, 160, BLUE), box(370, 160, 100, 44, "Storage", BLUE, size=12),
    text(130, 165, "barrier for particles + pathogens", 12, MUTED),
    text(240, 230, "CT = residual (mg/L) × contact time (min)", 13, INK),
    text(240, 256, "turbidity after filtration is the key check", 11, GREEN),
)

L1 = {
    "title": "Friction and minor losses",
    "minutes": 10,
    "photo_query": "large water main pipeline construction",
    "body": """Water flowing through a pipe loses energy to friction against the wall and to turbulence at fittings. Predicting those **head losses** is the core calculation of pressure-pipe design: it decides pipe sizes, pump duties and whether customers at the end of the line get enough pressure.

## Energy and grade lines

Bernoulli's equation, extended with losses, says that between points 1 and 2:

**z₁ + p₁/ρg + V₁²/2g = z₂ + p₂/ρg + V₂²/2g + h_L**

- The **hydraulic grade line (HGL)** joins z + p/ρg: it's the level water would rise to in a standpipe. Pressure head at a point is the HGL minus the pipe level.
- The **energy grade line (EGL)** sits above the HGL by the velocity head V²/2g (small: 1 m/s gives only about 0.05 m).
- Both lines fall in the direction of flow. If the HGL drops below the pipe, the pressure is negative there: avoid that.

## Friction: Darcy-Weisbach

**h_f = f × (L/D) × V²/2g**

The friction factor f depends on the **Reynolds number** (Re = VD/ν, where ν ≈ 1.0×10⁻⁶ m²/s for water at 20 °C) and the relative roughness k/D. Most water mains run turbulent (Re well above 4000), where the **Colebrook-White** equation (or the explicit **Swamee-Jain** approximation, or a Moody chart) gives f. Typical roughness values k range from around 0.003 to 0.015 mm for new plastic, larger for lined iron and much larger for old tuberculated cast iron. Australian practice often uses Colebrook-White with an **effective roughness** that also allows for joints, fittings and ageing.

**Key insight:** h_f rises roughly with V², and for the same flow V ∝ 1/D², so friction loss scales about with **1/D⁵**. Going up one pipe size can cut losses dramatically.

## Hazen-Williams

An older empirical formula, still common in network models:

**h_f = 10.67 × L × Q^1.852 / (C^1.852 × D^4.87)** (SI units, Q in m³/s, D in m)

C is a smoothness coefficient: around 140-150 for new plastic, lower for old pipes. It's handy but only valid for water at ordinary temperatures in turbulent flow; don't use it for other fluids or very small pipes.

## Minor losses

Bends, tees, valves, entries and exits add losses of the form **h_m = K × V²/2g**. Rough K values: a sharp entry about 0.5, an exit 1.0, a 90° bend 0.2-0.4, an open gate valve about 0.2, a partly closed valve much more. In long mains minor losses are small compared with friction; in pump stations and treatment plants, with short pipes and many fittings, they matter.

## Worked example

DN200 PVC (ID ≈ 0.2 m), L = 1000 m, Q = 30 L/s. A ≈ 0.0314 m², V ≈ 0.95 m/s, Re ≈ 190 000. With k ≈ 0.015 mm, f ≈ 0.016, so h_f ≈ 0.016 × 5000 × 0.046 ≈ **3.7 m** of head lost per kilometre.

> **Design velocities:** many designers aim for about 0.6-1.5 m/s in mains under normal peak demand, higher briefly for fire flow. Too slow and water ages; too fast and losses and surge risk rise. Check your water corporation's standards.""",
    "key_points": [
        "The HGL is z + p/ρg; the EGL sits V²/2g above it; both fall in the direction of flow.",
        "Darcy-Weisbach: h_f = f(L/D)V²/2g, with f from Colebrook-White using Re and roughness.",
        "Friction loss scales roughly with 1/D⁵ for a fixed flow, so small size increases help a lot.",
        "Minor losses are K × V²/2g; important in pump stations, small in long mains.",
    ],
    "figure_svg": LOSSES,
    "figure_caption": "Between two tanks the available head H is used up by friction and minor losses; the EGL sits a velocity head above the HGL.",
    "questions": [
        mcq("What does the hydraulic grade line (HGL) represent?", ["The pipe's invert level", "Elevation plus pressure head, the level water would rise to in a standpipe", "The energy including velocity head", "The ground surface"], 1,
            "The EGL adds velocity head on top of the HGL."),
        mcq("For a fixed flow, roughly how does friction loss change with diameter?", ["It scales with D", "It scales with about 1/D⁵", "It doesn't depend on D", "It scales with D²"], 1,
            "h_f ∝ V²/D and V ∝ 1/D², so h_f ∝ 1/D⁵."),
        mcq("In the diagram, what uses up the head H between tank A and tank B?", ["Only the velocity head", "Friction plus minor losses along the pipe", "The pipe's weight", "Air in the tanks"], 1,
            "At steady flow, all the available head goes into losses.",
            LOSSES, "Two tanks connected by a pipe, with a falling hydraulic grade line and energy line; the level difference H is marked."),
        mcq("What is the velocity head at 1 m/s?", ["About 0.05 m", "About 1 m", "About 9.8 m", "About 0.5 m"], 0,
            "V²/2g = 1/19.62 ≈ 0.051 m."),
        mcq("Which equation is commonly used to find the Darcy friction factor in turbulent flow?", ["Manning's", "Colebrook-White", "Joukowsky's", "The rational method"], 1,
            "Swamee-Jain is an explicit approximation of it."),
        mcq("When is Hazen-Williams NOT appropriate?", ["For water mains in normal conditions", "For fluids other than water or unusual temperatures", "In network models", "For PVC pipes"], 1,
            "It's empirical and calibrated for water."),
        mcq("In the diagram, what is the vertical gap between the EGL and the HGL?", ["Friction loss", "Velocity head V²/2g", "Static lift", "Pipe diameter"], 1,
            "EGL = HGL + V²/2g.", LOSSES, "Energy grade line drawn a small distance above the hydraulic grade line, both falling from tank A to tank B."),
        open_q("A pipe's HGL falls below the pipe itself at a high point. What does that mean and why does it matter?", "The pressure there is below atmospheric (negative), so air can come out of solution or be drawn in through joints and contaminated groundwater could enter; flow may become unstable. Redesign so the HGL stays above the pipe, for example with a larger pipe or a different alignment.",
               ["negative pressure", "air or contamination can enter", "keep HGL above the pipe"], "Air valves help with trapped air but don't fix sub-atmospheric pressure."),
        open_q("Why do minor losses matter more in a pump station than in a 5 km trunk main?", "In a pump station the pipes are short and full of bends, valves, tees and entries, so fitting losses are a large share of the total; over 5 km of straight main, friction dominates and fittings are a small fraction.",
               ["short pipes with many fittings", "friction dominates in long mains"], "K × V²/2g adds up quickly with high local velocities."),
        open_q("Estimate the velocity of 30 L/s in a 200 mm internal diameter pipe, showing your working.", "Area = π × 0.2² / 4 ≈ 0.0314 m²; V = Q / A = 0.030 / 0.0314 ≈ 0.95 m/s.",
               ["area about 0.0314 m²", "V = Q/A", "about 0.95 m/s"], "Convert L/s to m³/s first."),
    ],
}

L2 = {
    "title": "Pumps and system curves",
    "minutes": 10,
    "photo_query": "centrifugal pump station water",
    "body": """When gravity can't deliver, pumps add energy. Choosing a pump means matching what the pump can do to what the system needs, and checking it works across every condition, not just one.

## The system curve

The **system curve** is the head the pipework needs at each flow:

**H_sys = H_static + k × Q²**

- **Static head**: the level difference the pump must lift through (discharge water level minus suction water level). It changes as wells and tanks fill and empty.
- **Dynamic losses**: friction plus minor losses, rising roughly with Q² (Hazen-Williams gives Q^1.85).

## The pump curve and the duty point

A centrifugal pump's **head-flow curve** falls as flow increases. Where it crosses the system curve is the **duty point**: the flow and head the pump will actually run at. Manufacturers also give **efficiency**, **power** and **NPSH required** curves against flow.

Choose a pump whose duty point sits near its **best efficiency point (BEP)**, typically within about 70-120% of the BEP flow. Running far left (low flow) causes recirculation, heat and vibration; running far right risks cavitation and motor overload.

**Hydraulic power** = ρgQH. Divide by pump efficiency (and motor efficiency) for the input power. Example: 50 L/s at 40 m with 75% pump efficiency needs about 1000 × 9.81 × 0.05 × 40 / 0.75 ≈ **26 kW** shaft power.

## Pumps in parallel and series

- **Parallel** (common in water and sewer stations): add flows at the same head. Because the system curve rises with Q², two pumps give **less than double** the flow of one.
- **Series**: add heads at the same flow; used for high lifts or boosters.
- Stations usually have **duty and standby** pumps (for example duty/standby or duty/assist/standby) so one can fail or be serviced.

## Variable speed drives and the affinity laws

A **variable speed drive (VSD)** changes pump speed N. For the same pump:

- Q ∝ N
- H ∝ N²
- P ∝ N³

So running at 80% speed needs only about half (0.8³ ≈ 0.51) the power, though with high static head the savings are less because the pump must still overcome the lift.

## Cavitation and NPSH

If pressure at the pump inlet falls below the water's vapour pressure, vapour bubbles form and collapse violently: **cavitation**, which pits impellers and makes a gravel-like noise. To avoid it, the **NPSH available** (from the suction conditions: atmospheric pressure, submergence, suction losses and vapour pressure) must exceed the **NPSH required** by the pump with a margin. Flooded suctions, short straight suction pipes and adequate submergence help; suction lifts make it worse.

## Check every scenario

Plot curves for minimum and maximum static head, new and aged pipes, one pump and all duty pumps. The pump must stay in its acceptable range and meet the required flow in every case.

> **Rule of thumb:** a pump selected only for the design point often runs badly most of the time. Look at where it actually operates day to day.""",
    "key_points": [
        "System head = static head + losses that rise with about Q²; the duty point is where pump and system curves cross.",
        "Select pumps near their best efficiency point; check all static levels and pipe conditions.",
        "Parallel pumps add flow at the same head but give less than double the flow; series pumps add head.",
        "Affinity laws: Q ∝ N, H ∝ N², P ∝ N³. Avoid cavitation by keeping NPSH available above NPSH required.",
    ],
    "figure_svg": PUMP,
    "figure_caption": "The pump's falling head curve meets the rising system curve at the duty point D; the system curve starts at the static lift.",
    "questions": [
        mcq("In the diagram, what is point D?", ["The pump's shut-off head", "The duty point where pump and system curves cross", "The static lift", "The cavitation limit"], 1,
            "The pump settles where the head it makes equals the head the system needs.",
            PUMP, "A falling pump curve and a rising system curve that starts at the static lift; they cross at point D."),
        mcq("Why does the system curve not start at zero head?", ["Because of pump efficiency", "Because static head must be overcome even at tiny flows", "Because of velocity head", "Because of air"], 1,
            "At zero flow there are no losses, but the lift remains."),
        mcq("Two identical pumps run in parallel on a system with significant friction. What flow results?", ["Exactly double one pump's flow", "Less than double", "The same as one pump", "More than double"], 1,
            "Higher flow raises system head, moving each pump back up its curve."),
        mcq("By the affinity laws, roughly what power does a pump need at 80% speed?", ["80%", "64%", "About 51%", "20%"], 2,
            "P ∝ N³; 0.8³ ≈ 0.51."),
        mcq("What causes cavitation?", ["Too much discharge pressure", "Inlet pressure falling below vapour pressure", "Pumps running in series", "A VSD"], 1,
            "Vapour bubbles form and collapse, damaging the impeller."),
        mcq("Which condition makes NPSH available worse?", ["A flooded suction", "A long suction lift with many fittings", "More submergence", "Colder water"], 1,
            "Lift and suction losses reduce the absolute pressure at the inlet."),
        mcq("In the diagram, if the static lift increased (the wet well drops), where would D move?", ["To higher flow", "To lower flow and higher head", "It wouldn't move", "Off the chart to zero"], 1,
            "The system curve shifts up, crossing the pump curve further left.",
            PUMP, "Pump curve and system curve with the static lift marked as a dashed line."),
        open_q("Calculate the shaft power for 50 L/s at 40 m head with 75% pump efficiency.", "Hydraulic power = ρgQH = 1000 × 9.81 × 0.05 × 40 ≈ 19.6 kW; dividing by 0.75 gives about 26 kW.",
               ["ρgQH ≈ 19.6 kW", "divide by efficiency", "about 26 kW"], "Remember to convert L/s to m³/s."),
        open_q("Why should a pump's duty point be near its best efficiency point?", "Near the BEP the pump uses least energy and runs smoothly; far to the left it recirculates, heats and vibrates, and far to the right it risks cavitation and overloading the motor, which shortens its life.",
               ["least energy", "low flow causes recirculation and vibration", "high flow risks cavitation and overload"], "Typically within about 70-120% of BEP flow."),
        open_q("Why does a VSD save less energy on a system dominated by static head?", "Because the pump must still produce at least the static lift at any speed; with high static head the speed can't drop much before flow stops, so you can't take advantage of the cubic power saving.",
               ["must still overcome static lift", "speed can't fall far", "cubic saving mostly applies to friction-dominated systems"], "Affinity laws hold for the pump, not the system."),
    ],
}

L3 = {
    "title": "Open channels and partly full pipes",
    "minutes": 9,
    "photo_query": "concrete stormwater channel",
    "body": """Sewers, stormwater drains and channels usually flow with a free surface open to the air. The driving force is the slope of the pipe or channel, not pressure, and **Manning's equation** is the everyday design tool.

## Manning's equation

**V = (1/n) × R^(2/3) × S^(1/2)** and **Q = V × A**

- **n**: Manning's roughness, around 0.009-0.011 for PVC, about 0.011-0.013 for concrete pipe, 0.013-0.015 for finished concrete channels, and much higher (0.03+) for grassed or natural channels.
- **R**: hydraulic radius = flow area A ÷ wetted perimeter P. For a full circular pipe R = D/4.
- **S**: slope of the energy line, which for uniform flow equals the pipe grade (e.g. 1 in 200 = 0.005).

Example: DN300 concrete pipe flowing full, n = 0.013, S = 0.005. A ≈ 0.0707 m², R = 0.075 m, R^(2/3) ≈ 0.178, S^(1/2) ≈ 0.0707. V ≈ (1/0.013) × 0.178 × 0.0707 ≈ **0.97 m/s**, Q ≈ **69 L/s**.

Colebrook-White can also be used for gravity pipes (WSA 02 allows it), but Manning is standard for drainage.

## Partly full circular pipes

A pipe rarely flows exactly full. Hydraulic elements charts give V and Q relative to the full-pipe values for any depth ratio d/D:

- At **half depth**, velocity equals the full-bore velocity and flow is half the full flow.
- Peak **velocity** occurs at about d/D ≈ 0.81 and peak **flow** at about d/D ≈ 0.94, slightly more than full-pipe flow, because the last bit of depth adds lots of wetted perimeter (friction) for little area.
- At low depths velocity drops fast, which is why sewers at low flow can deposit solids.

## Critical flow and the Froude number

The **Froude number** Fr = V / √(g·D_h) (D_h is hydraulic depth, A ÷ top width) compares flow speed with the speed of a surface wave.

- **Fr < 1: subcritical** (deep and slow, tranquil); disturbances travel upstream.
- **Fr > 1: supercritical** (shallow and fast, rapid), common on steep grades.
- **Fr ≈ 1: critical**, unstable and wavy; avoid designing near it.

When supercritical flow meets a slower downstream condition it jumps abruptly to subcritical in a **hydraulic jump**, dissipating lots of energy. Engineers use this deliberately in energy dissipators downstream of spillways and steep chutes, and avoid it in pipes where it can surcharge manholes.

## Practical checks

- **Self-cleansing:** gravity sewers need enough velocity (or boundary shear) at regular flows to carry solids. Older rules aimed for about 0.6-0.75 m/s; WSA 02 uses minimum grades based on shear stress.
- **Maximum velocity:** very high velocities (often above about 3 m/s in sewers) cause scour and turbulence that releases odour and hydrogen sulfide; steep drops need special manholes.
- **Freeboard:** open channels need spare height above the design water level.
- **Tailwater:** a stormwater outlet into a river that's in flood may run surcharged; check the downstream water level, not just the pipe.""",
    "key_points": [
        "Manning: V = (1/n) R^(2/3) S^(1/2); R = A/P, and R = D/4 for a full circular pipe.",
        "Half-full pipes carry half the full flow at the same velocity; peak flow is at about 94% depth.",
        "Froude number below 1 is subcritical, above 1 supercritical; a hydraulic jump dissipates energy where they meet.",
        "Check self-cleansing at low flow, scour at high velocity, freeboard and downstream tailwater.",
    ],
    "figure_svg": PARTIAL,
    "figure_caption": "A circular pipe flowing at depth d: Manning's equation uses the hydraulic radius of the wet part.",
    "questions": [
        mcq("What is the hydraulic radius of a circular pipe flowing full?", ["D/2", "D/4", "D", "πD"], 1,
            "A/P = (πD²/4) / (πD) = D/4."),
        mcq("A pipe flows half full. Compared with flowing full, its velocity is…", ["Half", "The same", "Double", "A quarter"], 1,
            "Both A and P halve, so R is unchanged; flow halves."),
        mcq("In the diagram, at roughly what depth ratio d/D does a circular pipe carry its maximum flow?", ["0.5", "0.81", "About 0.94", "1.0"], 2,
            "The last few percent of depth adds lots of friction perimeter for little area.",
            PARTIAL, "A circular pipe partly full to depth d, with Manning's equation and the note that maximum flow occurs near 94% depth."),
        mcq("Which Manning's n would suit a grassed floodway?", ["0.010", "0.013", "Around 0.03 or more", "0.001"], 2,
            "Vegetation is much rougher than concrete or plastic."),
        mcq("What does a Froude number of 2 mean?", ["Subcritical, tranquil flow", "Supercritical, rapid flow", "Critical flow", "Pressurised flow"], 1,
            "Fr > 1 is supercritical."),
        mcq("What's a hydraulic jump?", ["A pump surge", "An abrupt change from supercritical to subcritical flow that dissipates energy", "Water hammer", "A siphon"], 1,
            "Used deliberately in stilling basins."),
        mcq("In the diagram, what does R = A/P use?", ["The whole pipe's area and perimeter", "The flow area and wetted perimeter of the water", "The pipe's wall thickness", "The water surface width only"], 1,
            "Only the wet part counts.", PARTIAL, "Partly full pipe with the formula R = A / P beside it."),
        open_q("Calculate the full-pipe velocity and flow for a DN300 concrete pipe (n = 0.013) at a grade of 1 in 200.", "A ≈ 0.0707 m²; R = D/4 = 0.075 m, so R^(2/3) ≈ 0.178; S^(1/2) = √0.005 ≈ 0.0707; V ≈ 0.178 × 0.0707 / 0.013 ≈ 0.97 m/s; Q ≈ 0.97 × 0.0707 ≈ 0.069 m³/s, about 69 L/s.",
               ["R = 0.075 m", "V about 0.97 m/s", "Q about 69 L/s"], "Use S = 0.005."),
        open_q("Why can a sewer that's large enough for peak flow still have problems at night?", "At low night-time flows the depth and velocity are small, so the flow may not be self-cleansing; solids settle, causing blockages, odour and hydrogen sulfide. Oversized or flat sewers make this worse.",
               ["low flow, low velocity", "solids settle", "oversizing or flat grades make it worse"], "That's why minimum grades exist."),
        open_q("Why should you check tailwater at a stormwater outlet?", "If the receiving river or channel is high during the same storm, the outlet can be drowned and the pipe will run surcharged, raising water levels upstream and possibly flooding pits; designing only on the pipe's own capacity would overestimate performance.",
               ["receiving water may be high", "pipe surcharges", "upstream flooding"], "Use a hydraulic grade line analysis from the outlet up."),
    ],
}

L4 = {
    "title": "Designing a water main",
    "minutes": 11,
    "photo_query": "water main installation trench",
    "body": """Designing a reticulation main for a new estate brings together demand, hydraulics and standards. In Australia the starting point is the **Water Supply Code of Australia (WSA 03)** plus your water corporation's own supplement, which overrides it where they differ.

## Step 1: demand

Water corporations specify design demands, often expressed per lot or as **equivalent tenements (ET)**. Typical structure (check the local numbers, they vary widely with climate):

- **Average day demand** per ET (a figure in the hundreds of litres per day for a typical household, more in hot inland towns with garden watering).
- **Peak day** = average day × a peak day factor (often around 1.5 to 2.5 for urban areas, higher in regional and hot areas).
- **Peak hour** = peak day rate × a peak hour factor (often around 2 or more), applied as an instantaneous flow in L/s.

Smaller groups of lots have higher relative peaks, which is why codes give peak factors that fall as the number of lots rises.

## Step 2: pressure criteria

Mains must deliver:

- A **minimum service pressure** at the property boundary during peak hour (WSA 03 commonly uses around 20 m; many corporations specify their own, sometimes higher).
- A **maximum static pressure**, often around 80-90 m, above which PRVs are needed to protect fittings and limit leakage.
- **Fire flow**: enough flow at hydrants for firefighting, at a minimum residual pressure, usually checked with a background demand (a fraction of peak) at the same time. Residential fire flow commonly sits around 10 L/s or more at a residual pressure in the order of 10-20 m; industrial and commercial areas need more. Use the corporation's and fire authority's values.

Fire flow often governs main sizing in residential areas, not everyday demand.

## Step 3: hydraulic check

Model the main from a known boundary condition (a reservoir level or a pressure provided by the water corporation at the connection) using Darcy-Weisbach or Hazen-Williams. Check:

- Pressures at the critical points: high ground and the far end.
- Velocities: typically below about 1.5-2 m/s at peak, and not so low that water ages badly in dead ends.
- **Looping**: connect to existing mains at two points where possible for security and better pressure.

## Step 4: layout and details

- Locate mains in the standard **road reserve allocation** (a set offset from the property boundary), with minimum cover (often around 600-750 mm, more under roads).
- **Valves** to isolate sections so a break affects only a small number of properties; **hydrants** at regular spacing (often around 60-100 m in residential streets) and at dead ends for flushing.
- **Scour valves** at low points and **air valves** at high points on larger mains.
- **Thrust blocks** or restrained joints at bends, tees and ends.
- **Clearances** from sewers, gas, power and trees.

## Step 5: water quality

Bigger isn't always better. An oversized main has low velocity, long **water age** and lost chlorine residual. Avoid dead ends; design for flushing.

> **Worked thinking:** 400 lots, connection pressure from a reservoir with top water level 180 m, estate ground 135 m. Static head ≈ 45 m: fine. Peak hour flow may be in the order of 20-30 L/s; fire flow plus background might demand a similar flow but at a lower residual pressure. Size the main for whichever case is worse, often a DN150-DN200 spine with DN100 reticulation, then confirm in a model.""",
    "key_points": [
        "WSA 03 plus the water corporation's supplement sets design rules; local values override national ones.",
        "Design demand uses average day per ET with peak day and peak hour factors that fall as lot numbers rise.",
        "Check minimum pressure at peak hour, maximum static pressure, and fire flow with background demand, which often governs.",
        "Lay out valves, hydrants, scours, air valves and thrust restraint; avoid oversizing and dead ends for water quality.",
    ],
    "figure_svg": MAIN,
    "figure_caption": "Sizing a main for a new estate: check peak hour pressure, then fire flow with background demand, then water age.",
    "questions": [
        mcq("Which document is the national starting point for water supply design in Australia?", ["WSA 02", "WSA 03", "ARR", "AS 3500 only"], 1,
            "WSA 02 is gravity sewerage."),
        mcq("Where a water corporation's supplement differs from WSA 03, which applies?", ["WSA 03", "The corporation's supplement", "Whichever is cheaper", "The designer chooses"], 1,
            "Supplements tailor the national code to local conditions."),
        mcq("Why do smaller groups of lots get higher peak factors?", ["They use more water per day", "Their demands are less likely to average out, so instantaneous peaks are relatively higher", "Pipes are rougher", "Codes are inconsistent"], 1,
            "Diversity smooths peaks in large populations."),
        mcq("In the diagram, which check often governs main sizing in residential areas?", ["Average day demand", "Fire flow with background demand", "Water temperature", "Pipe colour"], 1,
            "Fire flow usually needs a bigger main than everyday peaks.",
            MAIN, "A reservoir feeding a main to a new estate, with check 1 peak hour pressure and check 2 fire flow plus background demand."),
        mcq("What's the main water quality risk of an oversized main?", ["Too much pressure", "Low velocity and long water age, losing chlorine residual", "Cavitation", "Corrosion of the road"], 1,
            "Water sits too long."),
        mcq("Why are valves placed throughout a reticulation network?", ["To raise pressure", "So breaks and works affect only small sections", "To measure flow", "To add chlorine"], 1,
            "Isolation limits disruption."),
        mcq("In the diagram, with a reservoir at 180 m and the estate at 135 m, what's the approximate static head?", ["45 m", "180 m", "135 m", "315 m"], 0,
            "180 − 135 = 45 m, about 440 kPa.", MAIN, "Reservoir with top water level 180 m and estate at reduced level 135 m."),
        open_q("Why is fire flow checked together with a background demand?", "A fire can happen while customers are also using water, so the network must supply the fire flow at a minimum residual pressure while also meeting a share of normal demand; checking fire flow alone would overstate the available pressure.",
               ["fire happens during normal use", "residual pressure must be maintained", "alone would overestimate capacity"], "Values come from the water corporation and fire authority."),
        open_q("Why connect a new estate's main to the network at two points where possible?", "Looping gives a second supply path, so a break or shutdown doesn't cut off supply; it also lowers velocities and head losses, improves pressure and fire flow, and reduces dead ends that cause water age problems.",
               ["security of supply", "better pressure and fire flow", "fewer dead ends"], "Looped networks are standard practice."),
        open_q("List the fittings you'd expect along a large main and what each is for.", "Isolation valves to shut off sections; hydrants for firefighting and flushing; scour valves at low points to drain and flush; air valves at high points to release or admit air; and thrust blocks or restrained joints at bends, tees and ends to resist hydraulic thrust.",
               ["valves isolate", "hydrants for fire and flushing", "scours at low points, air valves at high points", "thrust restraint"], "WSA 03 has standard drawings for these."),
    ],
}

L5 = {
    "title": "Designing a gravity sewer",
    "minutes": 11,
    "photo_query": "sewer manhole construction",
    "body": """Gravity sewers are designed to carry wastewater for 50-100 years with no pumping, few blockages and minimal odour. In Australia the starting point is the **Gravity Sewerage Code of Australia (WSA 02)** and the water corporation's supplement.

## Step 1: design flows

Sewage flow comes from households and businesses plus water that shouldn't be there:

- **ADWF (average dry weather flow)**: the daily average sewage flow, often expressed per ET (commonly in the order of 150-200 L/person/day, check locally).
- **PDWF (peak dry weather flow)**: ADWF × a peaking factor that falls as the catchment grows.
- **PWWF (peak wet weather flow)**: PDWF plus **inflow and infiltration (I/I)**, stormwater and groundwater entering through cracked pipes, illegal stormwater connections and low gully traps. In many systems wet weather flows are several times dry weather flows, and they drive overflows.

WSA 02 provides a method based on ETs, catchment area and allowances for groundwater infiltration and rainfall-dependent inflow.

## Step 2: pipe size and grade

- **Minimum size**: DN150 for reticulation sewers (DN100 for property connections) in most codes.
- **Capacity**: the pipe should carry PWWF, usually flowing no more than a set proportion of full (designers commonly leave some headroom for ventilation and future growth).
- **Self-cleansing**: WSA 02 sets **minimum grades** so that boundary **shear stress** at regular daily flows is enough to move solids, around 1.5 Pa in common guidance, rather than relying on a single velocity rule. For DN150 that typically means grades not much flatter than about 1 in 150 to 1 in 180 at the head of a line where flows are tiny.
- **Maximum velocity/steep grades** need care to avoid scour, turbulence and gas release.

## Step 3: depth, alignment and manholes

- Sewers are deep enough to serve the lowest part of each lot (the **property connection point**) with a grade on the house drain, and to give **cover** against loads (more under roads).
- Lines are straight between **maintenance holes (MH)** in older practice; modern codes allow curved lines and **maintenance shafts** in some cases.
- MH spacing is limited so cleaning equipment can reach (often around 100-150 m).
- At changes in size, keep the **obvert** (top of pipe) continuous or drop the downstream pipe, so the upstream pipe doesn't surcharge.
- **Drops** in level at a manhole beyond a certain height need special drop structures.

## Step 4: long sections

A **long section** shows ground level, pipe invert, grade, size, material, MH depths and cover along each line. It's the main drawing for checking a design and building it. The designer checks that each lot can connect, minimum cover is met, grades are achievable and depths aren't needlessly deep (deep sewers are expensive and risky to build).

## Step 5: avoiding septicity and odour

Long rising mains, flat grades and warm sewage lead to anaerobic conditions and **hydrogen sulfide (H₂S)**. H₂S smells, is toxic and turns into sulfuric acid on concrete crown surfaces, eating away pipes and manholes. Designs minimise detention times and turbulence at discharge points, use corrosion-resistant materials (PVC, PE, lined concrete) and provide ventilation.

## Construction realities

Trench safety, groundwater, rock, existing services and reinstatement drive cost. A design that shaves half a metre off depth across a whole estate can save a lot of money and risk.""",
    "key_points": [
        "WSA 02 plus the corporation supplement governs; design flows build from ADWF to PDWF to PWWF including inflow and infiltration.",
        "Minimum DN150 reticulation; minimum grades from a shear stress criterion (about 1.5 Pa) for self-cleansing.",
        "Depth serves each lot's connection point with cover; MHs at changes and limited spacing; keep obverts aligned.",
        "Long sections are the key design drawing; avoid septicity and H₂S by limiting detention and using resistant materials.",
    ],
    "figure_svg": GRAVITY,
    "figure_caption": "A long section: the sewer falls between manholes at grades steep enough to self-cleanse, and grows in size downstream.",
    "questions": [
        mcq("What does PWWF include that PDWF doesn't?", ["Industrial flows", "Inflow and infiltration from rain and groundwater", "Night flows", "Pump flows"], 1,
            "Wet weather adds I/I."),
        mcq("What's the usual minimum size for a reticulation gravity sewer?", ["DN100", "DN150", "DN300", "DN50"], 1,
            "DN100 is for property connections."),
        mcq("What criterion does WSA 02 use to set minimum grades?", ["Pipe colour", "Boundary shear stress for self-cleansing", "Maximum depth", "Odour"], 1,
            "Around 1.5 Pa in common guidance."),
        mcq("In the diagram, why is the downstream pipe larger?", ["For looks", "More catchment and flow join downstream", "To slow the flow", "Because it's deeper"], 1,
            "Flows accumulate down the line.",
            GRAVITY, "A long section with three manholes; DN150 at 1 in 150 upstream and DN225 at 1 in 200 downstream."),
        mcq("At a change from DN150 to DN225, what's usually kept continuous?", ["The invert", "The obvert (top of pipe)", "The manhole lid", "The cover"], 1,
            "Matching obverts prevents the smaller pipe backing up."),
        mcq("What damages concrete sewers in septic conditions?", ["Chlorine", "Hydrogen sulfide turning into sulfuric acid on the crown", "UV light", "Frost"], 1,
            "H₂S is oxidised to acid by bacteria above the waterline."),
        mcq("In the diagram, what drawing is this?", ["A cross-section", "A long section showing grades, sizes and manhole depths", "A site plan", "A pump curve"], 1,
            "Long sections are the core sewer design drawing.",
            GRAVITY, "Surface line, a falling sewer line and three manholes with sizes and grades labelled."),
        open_q("Explain the difference between ADWF, PDWF and PWWF.", "ADWF is the average daily sewage flow in dry weather; PDWF is the peak flow in dry weather, ADWF times a peaking factor; PWWF adds inflow and infiltration from rain and groundwater to give the peak flow in wet weather, which usually governs pipe capacity and overflows.",
               ["ADWF average dry weather", "PDWF peak dry weather with peaking factor", "PWWF adds inflow and infiltration"], "I/I can multiply flows several times."),
        open_q("Why is a sewer at the head of a line hard to design?", "Flows there are tiny, so it's hard to achieve self-cleansing shear or velocity; the code requires a minimum grade for DN150 that may make the sewer deeper downstream, so there's a trade-off between grade and depth.",
               ["tiny flows", "needs minimum grade", "grade versus depth trade-off"], "That's why head-of-line grades are steeper."),
        open_q("Why does sewer depth matter so much for cost and safety?", "Deeper sewers need bigger, shored trenches, more excavation, dewatering and reinstatement, and expose workers to collapse and confined-space hazards, so unnecessary depth increases cost and risk; depth is set by serving lots and achieving grades.",
               ["more excavation and shoring", "trench collapse and safety risk", "depth driven by lot service and grade"], "Shallow but compliant is the goal."),
    ],
}

L6 = {
    "title": "Water treatment processes",
    "minutes": 10,
    "photo_query": "water treatment plant filters",
    "body": """A water treatment plant turns raw water from a river, reservoir or bore into water that's safe and pleasant to drink. Each step is a **barrier** with a target, set within the risk-based framework of the **Australian Drinking Water Guidelines (ADWG)**.

## The conventional train

1. **Screening and intake**: remove debris and fish; choose the best water level to draw from.
2. **Coagulation**: add a coagulant (commonly aluminium sulfate, ferric chloride or polyaluminium chloride) with rapid mixing. It neutralises the negative charges on tiny particles and organic matter so they can stick together. pH control matters; **jar tests** find the best dose.
3. **Flocculation**: gentle mixing for some minutes grows particles into larger **floc**.
4. **Clarification**: remove floc by **sedimentation** in settling tanks, or by **dissolved air flotation (DAF)**, which floats light floc (good for algae and coloured water).
5. **Filtration**: rapid **sand or dual-media filters** remove remaining particles, including many pathogens attached to them. Filters are backwashed when headloss or turbidity rises. **Membrane** filtration (micro/ultra-filtration) is a physical barrier alternative.
6. **Disinfection**: **chlorine** (or chloramine for long systems) kills bacteria and viruses and leaves a **residual** to protect the network. **UV** is very effective against protozoa like *Cryptosporidium* and *Giardia*, which are resistant to chlorine, but leaves no residual.
7. **pH correction and fluoridation**: lime or soda ash adjust pH to reduce corrosion; fluoride is added where directed (in Victoria, under the *Health (Fluoridation) Act 1973*).
8. **Clear water storage**: provides contact time for disinfection and buffers demand.

## Why turbidity matters

**Turbidity** (cloudiness, measured in NTU) is the quick indicator that filtration is working. Particles shield pathogens from disinfectants, so low filtered turbidity (individual filter targets are commonly well below 0.5 NTU, often around 0.1-0.2 NTU) is critical, and filters are monitored continuously.

## CT: disinfection dose

Disinfection effectiveness depends on concentration and time: **CT = C (mg/L) × T (minutes)**, using the residual at the outlet and the effective contact time (adjusted for short-circuiting with a baffling factor). Required CT values depend on the target pathogen, temperature and pH: colder water and higher pH need more CT for chlorine.

## Risk-based management

The ADWG framework asks water suppliers to understand their catchment hazards and set **health-based targets**, often expressed as **log reductions** (a 4-log reduction removes 99.99%). Each barrier earns log credits, for example a well-run conventional filtration plant might be credited for some protozoan removal, UV for more. **Critical control points** have limits and alarms, and operators respond to excursions. In Victoria, the Department of Health oversees this under the Safe Drinking Water Act, including risk management plans and audits.

## Other processes

- **Activated carbon** (powdered or granular) for taste, odour and algal toxins.
- **Ozone** for oxidation and taste/odour, often followed by biological activated carbon.
- **Reverse osmosis** for desalination or salty groundwater.
- **Iron and manganese removal** by oxidation and filtration for many bore supplies.

> **Big picture:** treatment is designed around the worst plausible raw water, not the average day. Storms, algal blooms and bushfire ash can change raw water quality in hours.""",
    "key_points": [
        "Conventional train: coagulation, flocculation, clarification, filtration, disinfection, pH correction, storage.",
        "Filtered turbidity is the key indicator; particles shield pathogens.",
        "CT = residual concentration × contact time; requirements rise in cold water and at high pH for chlorine.",
        "ADWG is risk-based: health-based targets, log reduction credits and critical control points.",
    ],
    "figure_svg": TREAT,
    "figure_caption": "Raw water passes through coagulation, clarification, filtration and disinfection before storage.",
    "questions": [
        mcq("What does a coagulant do?", ["Kills bacteria", "Neutralises particle charges so they can clump together", "Adds fluoride", "Raises pressure"], 1,
            "Charge neutralisation lets particles stick."),
        mcq("Which pathogen is resistant to chlorine but well controlled by UV?", ["E. coli", "Cryptosporidium", "Most viruses", "Legionella"], 1,
            "Protozoa such as Crypto and Giardia resist chlorine."),
        mcq("In the diagram, what step comes straight after clarification?", ["Disinfection", "Filtration", "Coagulation", "Storage"], 1,
            "Filters polish the clarified water.",
            TREAT, "Treatment train: raw water, coagulation and flocculation, clarification, filtration, disinfection, then storage."),
        mcq("Why is low filtered turbidity so important?", ["It improves taste only", "Particles can shield pathogens from disinfectant", "It reduces pressure", "It lowers pH"], 1,
            "Clear water lets disinfection work."),
        mcq("A 4-log reduction removes what fraction of organisms?", ["90%", "99%", "99.99%", "99.9999%"], 2,
            "Each log is a factor of 10."),
        mcq("Why might DAF be chosen over sedimentation?", ["It's slower", "It handles light floc such as algae and colour well", "It uses no chemicals", "It disinfects"], 1,
            "Light particles float more easily than they settle."),
        mcq("In the diagram, what does CT stand for?", ["Chlorine type", "Concentration × contact time", "Clear tank", "Coagulant total"], 1,
            "CT measures disinfection dose.", TREAT, "Treatment train with the note CT = residual (mg/L) × contact time (min)."),
        open_q("Why is chlorine used even when a plant also has UV?", "UV is very effective against protozoa but leaves no residual, so chlorine or chloramine is added to keep a residual disinfectant through the distribution network, protecting against contamination after treatment.",
               ["UV leaves no residual", "chlorine keeps a residual in the network", "protects after treatment"], "Barriers complement each other."),
        open_q("Explain why colder water needs more CT for chlorine disinfection.", "Disinfection reactions are slower at low temperature, so the same kill needs either a higher concentration or a longer contact time; CT tables give higher requirements for cold water.",
               ["slower reactions in cold water", "need higher C or longer T"], "pH also affects chlorine strongly."),
        open_q("What does the ADWG mean by a risk-based approach?", "Rather than relying only on testing the final water, the supplier identifies hazards from catchment to tap, sets health-based targets, uses multiple barriers with log reduction credits, sets critical limits at control points and responds quickly to problems, with regular review and audit.",
               ["identify hazards catchment to tap", "health-based targets and barriers", "critical control points with limits"], "Testing alone finds problems too late."),
    ],
}

PACK = {
    "id": "water-intermediate",
    "version": 1,
    "topic": "Civil and water engineering",
    "title": "Water engineering design",
    "summary": "Hands-on hydraulic design: friction losses, pumps and system curves, open channel flow, designing water mains and gravity sewers to WSA codes, and how water treatment plants work. For people who know the basics.",
    "icon": "waves",
    "level": "intermediate",
    "length": "short",
    "area": "engineering",
    "tags": ["water", "civil-engineering", "hydraulics", "pumps", "sewerage", "water-treatment"],
    "sections": [
        {"title": "Hydraulics", "summary": "The calculations behind pipes, pumps and channels.", "lessons": [
            {"title": L1["title"], "summary": "Calculate friction and minor losses and read grade lines.", "lesson": L1},
            {"title": L2["title"], "summary": "Select pumps against system curves and avoid cavitation.", "lesson": L2},
            {"title": L3["title"], "summary": "Apply Manning's equation to channels and partly full pipes.", "lesson": L3},
        ]},
        {"title": "Design practice", "summary": "Designing real water and sewer assets.", "lessons": [
            {"title": L4["title"], "summary": "Size and lay out a reticulation main to WSA 03.", "lesson": L4},
            {"title": L5["title"], "summary": "Design a gravity sewer to WSA 02.", "lesson": L5},
            {"title": L6["title"], "summary": "Explain the treatment train and the ADWG risk approach.", "lesson": L6},
        ]},
    ],
}
