"""Civil and water engineering at expert level."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, path, svg, text, title

HAMMER = svg(
    title("Water hammer after a fast valve closure"),
    box(20, 60, 70, 60, "Tank", BLUE, size=12), line(90, 110, 380, 110, INK, 6),
    box(380, 96, 34, 28, "", RED), text(397, 145, "valve", 11, RED),
    line(90, 70, 380, 70, BLUE, 2, "6 4"), text(240, 62, "steady HGL", 11, BLUE),
    path("M260 70 L260 40 L380 40", AMBER, 3), arrow(250, 50, 150, 50, AMBER, "", 2.5),
    text(200, 36, "wave travels at a", 11, AMBER),
    text(320, 32, "ΔH", 14, AMBER, weight="bold"),
    text(240, 200, "ΔH = a × ΔV / g", 16, INK, weight="bold"),
    text(240, 228, "a ≈ 1000 m/s, ΔV = 1 m/s → ΔH ≈ 100 m", 12, GREEN),
    text(240, 256, "closing faster than 2L/a gives the full surge", 11, MUTED),
)

MODEL = svg(
    title("A calibrated network model"),
    box(20, 50, 80, 44, "Reservoir", BLUE, size=12), line(100, 72, 180, 72, BLUE, 4),
    path("M180 72 L340 72 L340 190 L180 190 Z", INK, 2), line(260, 72, 260, 190, INK, 2),
    circle(180, 72, 6, INK, "#0b1620"), circle(340, 72, 6, INK, "#0b1620"), circle(180, 190, 6, INK, "#0b1620"),
    circle(260, 190, 6, INK, "#0b1620"), circle(340, 190, 6, AMBER, "#0b1620"),
    text(350, 210, "logger", 11, AMBER, anchor="start"),
    path("M380 80 L400 70 L420 90 L440 60 L460 75", GREEN, 2), text(420, 110, "field", 11, GREEN),
    path("M380 150 L400 140 L420 158 L440 128 L460 145", PURPLE, 2, dash="4 3"), text(420, 175, "model", 11, PURPLE),
    text(240, 240, "nodes (demand), links (pipes, pumps, valves)", 12, MUTED),
    text(240, 265, "adjust roughness and demands until they match", 12, INK),
)

WETWELL = svg(
    title("Pump station wet well"),
    box(120, 50, 200, 210, "", INK), arrow(30, 90, 120, 90, AMBER, "inflow", 3),
    '<rect x="122" y="140" width="196" height="118" fill="#5fd3ff" opacity="0.3"/>',
    line(120, 140, 320, 140, GREEN, 2, "6 4"), text(330, 144, "duty start", 11, GREEN, anchor="start"),
    line(120, 200, 320, 200, AMBER, 2, "6 4"), text(330, 204, "stop", 11, AMBER, anchor="start"),
    line(120, 110, 320, 110, RED, 2, "6 4"), text(330, 114, "high level alarm", 11, RED, anchor="start"),
    box(150, 215, 50, 40, "P1", BLUE, size=12), box(240, 215, 50, 40, "P2", BLUE, size=12),
    arrow(225, 175, 225, 145, MUTED, "", 2), arrow(225, 145, 225, 175, MUTED, "", 2),
    text(232, 165, "Vs", 13, INK, anchor="start", weight="bold"),
    text(240, 285, "Vs ≥ T × Q / 4 (T = minimum cycle time)", 12, INK),
)

RISK = svg(
    title("Risk-based renewal"),
    line(80, 250, 440, 250, MUTED, 2), line(80, 250, 80, 50, MUTED, 2),
    text(260, 280, "Likelihood of failure", 12, MUTED), text(55, 150, "Consequence", 12, MUTED, anchor="middle"),
    '<rect x="80" y="50" width="180" height="100" fill="#ffb547" opacity="0.18"/>',
    '<rect x="260" y="50" width="180" height="100" fill="#ff6b6b" opacity="0.25"/>',
    '<rect x="80" y="150" width="180" height="100" fill="#8af5c8" opacity="0.15"/>',
    '<rect x="260" y="150" width="180" height="100" fill="#ffb547" opacity="0.18"/>',
    circle(380, 85, 9, RED, "#0b1620"), text(395, 80, "A", 14, RED, anchor="start", weight="bold"),
    circle(140, 215, 9, GREEN, "#0b1620"), text(155, 210, "B", 14, GREEN, anchor="start", weight="bold"),
    circle(340, 200, 9, AMBER, "#0b1620"), text(355, 195, "C", 14, AMBER, anchor="start", weight="bold"),
    circle(130, 90, 9, AMBER, "#0b1620"), text(145, 85, "D", 14, AMBER, anchor="start", weight="bold"),
)

STP = svg(
    title("Activated sludge plant"),
    box(10, 80, 70, 50, "Screens", MUTED, size=12, sub="+ grit"), arrow(80, 105, 95, 105, AMBER),
    box(95, 80, 70, 50, "Primary", AMBER, size=12, sub="settling"), arrow(165, 105, 180, 105, AMBER),
    box(180, 70, 110, 70, "Bioreactor", GREEN, size=12, sub="anoxic + aerobic"), arrow(290, 105, 305, 105, AMBER),
    box(305, 80, 75, 50, "Clarifier", BLUE, size=12), arrow(380, 105, 395, 105, BLUE),
    box(395, 80, 75, 50, "Tertiary", PURPLE, size=12, sub="filter + UV"),
    path("M342 130 L342 175 L235 175 L235 140", GREEN, 2), arrow(260, 175, 240, 175, GREEN, "RAS", 2, dy=16),
    arrow(342, 175, 342, 220, MUTED, "", 2), text(342, 238, "WAS → sludge", 11, MUTED),
    text(150, 225, "BOD, N and P removed by microbes", 12, INK),
    text(150, 248, "N: nitrify (aerobic) then denitrify (anoxic)", 11, MUTED),
)

IWM = svg(
    title("Design rainfall is changing"),
    line(60, 250, 450, 250, MUTED, 2), line(60, 250, 60, 50, MUTED, 2),
    text(255, 280, "Storm duration", 12, MUTED), text(40, 150, "Intensity", 12, MUTED, anchor="middle"),
    path("M70 80 Q140 180 440 230", BLUE, 3), text(440, 222, "historical IFD", 11, BLUE, anchor="end"),
    path("M70 60 Q140 160 440 218", RED, 3, dash="6 4"), text(140, 92, "future climate", 11, RED, anchor="start"),
    arrow(100, 115, 100, 92, RED, "", 2),
    text(290, 120, "short, intense bursts", 12, AMBER), text(290, 138, "may increase most", 12, AMBER),
)

L1 = {
    "title": "Water hammer and surge protection",
    "minutes": 12,
    "photo_query": "water hammer surge vessel pump station",
    "body": """Change the velocity of water in a pipe quickly and its momentum turns into a pressure wave. **Water hammer** (hydraulic transient) can burst pipes, collapse them under vacuum, blow joints and damage pumps. It's the most common cause of failure in rising mains and large trunk mains, and steady-state models don't show it.

## Joukowsky's equation

For an instantaneous change in velocity ΔV, the pressure head change is:

**ΔH = a × ΔV / g**

where **a** is the pressure wave speed. a depends on the water's compressibility and the pipe's elasticity:

- Steel and ductile iron: roughly **1000-1300 m/s**.
- PVC: roughly **300-500 m/s**.
- PE: roughly **200-400 m/s**.

So stopping 1 m/s of flow in a ductile iron main produces about 1000 × 1 / 9.81 ≈ **100 m** of surge, on top of the operating pressure, which can easily exceed a PN16 pipe's rating. Flexible plastic pipes have lower surge for the same ΔV, but their pressure ratings, fatigue limits and **derating** (with temperature and repeated cycles, especially for PVC and PE) must also be checked.

## Fast versus slow changes

A wave travels from the disturbance to the far end and back in **2L/a** seconds (L is pipe length). If a valve closes in less than 2L/a, the full Joukowsky surge develops. Slower closures produce smaller surges because reflected waves arrive in time to cancel part of it. That's why large valves close slowly and in a controlled way, particularly over the last part of travel, where most of the flow change happens.

## The pump trip: the critical case

When power fails, pumps stop in a second or two. Flow decelerates, pressure **drops** first at the pump end, and a low-pressure wave travels down the rising main. At high points the pressure can fall to vapour pressure, causing **column separation**: the water column splits, a vapour cavity forms, then the columns rejoin violently, producing pressures far above simple Joukowsky estimates. Profiles with **knees** (a high point near the pump, or a long flat section after a climb) are the most at risk.

## Protection options

- **Surge vessels (air vessels)**: pressurised tanks near the pump that feed water into the main when pressure drops, keeping the column moving and smoothing both downsurge and upsurge. Common on rising mains.
- **Flywheels**: add inertia so pumps slow more gradually (limited, mostly small stations).
- **Air valves** (including anti-slam and vacuum-break types): let air in to stop vacuum and let it out slowly; must be selected carefully, since releasing air too fast can cause a slam.
- **Surge anticipation and pressure relief valves**: open to release the high-pressure wave.
- **One-way surge tanks or standpipes**: feed water at high points.
- **Controlled valve closure and VSD ramp-down** for normal operations.
- **Stronger pipe** or a better alignment.

## Analysis

Transient analysis uses the **method of characteristics** in software (for example, packages commonly used in industry such as Bentley HAMMER, Wanda or similar). Inputs include pump and motor inertia, valve characteristics, the pipe profile and wave speeds. Run scenarios: pump trip at maximum flow, start-up, valve closure, and failure of the protection itself (for example a surge vessel with low air volume).

> **Design principle:** check both maximum and minimum pressures along the whole profile. Many failures come from vacuum and column separation, not just high pressure.""",
    "key_points": [
        "Joukowsky: ΔH = aΔV/g; about 100 m per 1 m/s in stiff pipes with a ≈ 1000 m/s.",
        "Closures faster than 2L/a give the full surge; slow and staged closures reduce it.",
        "Pump trips cause downsurge, possible column separation at knees and high points, then violent rejoining.",
        "Protection includes surge vessels, air and relief valves, flywheels and controlled operation; analyse with the method of characteristics.",
    ],
    "figure_svg": HAMMER,
    "figure_caption": "Closing a valve quickly sends a pressure wave ΔH back up the pipe at wave speed a.",
    "questions": [
        mcq("Using Joukowsky, what surge results from stopping 1.5 m/s in a pipe with a = 1000 m/s?", ["About 15 m", "About 150 m", "About 1500 m", "About 1.5 m"], 1,
            "1000 × 1.5 / 9.81 ≈ 153 m."),
        mcq("Why do PE pipes usually see a lower surge than ductile iron for the same ΔV?", ["They're smoother", "Their wave speed is much lower", "They're bigger", "They have no joints"], 1,
            "Elastic walls lower the wave speed."),
        mcq("In the diagram, what controls whether the full Joukowsky surge occurs?", ["Valve colour", "Whether closure is faster than 2L/a", "Tank size only", "Pipe roughness"], 1,
            "The round-trip time of the wave sets what counts as fast.",
            HAMMER, "A tank feeding a pipe with a valve; a pressure wave ΔH travels back toward the tank at speed a; formula ΔH = aΔV/g."),
        mcq("After a pump trip, what happens first at the pump end of a rising main?", ["Pressure rises sharply", "Pressure drops (downsurge)", "Nothing", "Flow reverses instantly with no pressure change"], 1,
            "The column keeps moving away from the stopped pump."),
        mcq("What is column separation?", ["Pipes pulling apart at joints", "A vapour cavity forming when pressure falls to vapour pressure, then collapsing violently", "Air valve failure", "Sludge settling"], 1,
            "Rejoining can produce extreme pressures."),
        mcq("Which device feeds water into a main when pressure drops after a pump trip?", ["A PRV", "A surge vessel", "A scour valve", "A flow meter"], 1,
            "Stored pressurised water keeps the column moving."),
        mcq("In the diagram, for a ductile iron main with a ≈ 1000 m/s, roughly how much surge comes from stopping 1 m/s?", ["10 m", "About 100 m", "1000 m", "1 m"], 1,
            "1000 × 1 / 9.81 ≈ 102 m.", HAMMER, "Formula ΔH = a × ΔV / g with the example a ≈ 1000 m/s, ΔV = 1 m/s."),
        open_q("Why are profiles with a 'knee' near the pump especially vulnerable to transients?", "After a pump trip the downsurge travels up the main, and at a high point or knee close to the pump the pressure can drop to vapour pressure, causing column separation; when the columns rejoin they create very high pressure spikes.",
               ["downsurge after trip", "high point reaches vapour pressure", "column separation and violent rejoining"], "Check the minimum pressure envelope along the profile."),
        open_q("Why must large valves close slowly, especially near the end of their travel?", "Most of the change in flow happens in the last part of closure, so closing quickly there causes a large ΔV in less than 2L/a and a big surge; slow, staged closure lets reflected waves reduce the pressure rise.",
               ["most flow change near end of travel", "closing faster than 2L/a causes full surge", "slow closure reduces surge"], "Actuator timing is a design parameter."),
        open_q("What scenarios would you run in a transient analysis of a rising main?", "A power failure pump trip at maximum flow and minimum static head, normal start-up and shut-down, valve closures, and failure cases for the protection such as a surge vessel with low air volume or an air valve not working, checking maximum and minimum pressures along the profile.",
               ["pump trip", "start-up and valve closure", "failure of protection", "check max and min pressure envelopes"], "Worst cases aren't always obvious."),
    ],
}

L2 = {
    "title": "Network modelling and calibration",
    "minutes": 11,
    "photo_query": "water network pressure logger hydrant test",
    "body": """A hydraulic model of a water network answers questions that would be expensive or impossible to test in the field: can the network handle a new subdivision, which main to upsize, what happens when a reservoir is offline, and how long water sits in pipes.

## How models work

Software such as **EPANET** (free, from the US EPA) and commercial tools built on similar solvers represent the network as:

- **Nodes (junctions)** with elevation and demand, plus **reservoirs** (fixed head) and **tanks** (levels that change).
- **Links**: pipes (length, diameter, roughness), **pumps** (curves), and **valves** (PRVs, flow controls, check valves).

The solver uses the **gradient method** (Todini-Pilati) to find heads and flows that satisfy continuity at every node and energy loss in every link.

## Steady state versus extended period

- **Steady state**: one snapshot, for example peak hour or fire flow.
- **Extended period simulation (EPS)**: runs over 24 hours or more with **diurnal demand patterns**, pump controls and tank levels. Needed for storage sizing, pump scheduling, energy and **water quality** (water age, chlorine decay) analysis.

## Building the model

- Pipes from GIS, with diameters, materials and ages.
- Elevations from survey or a good digital elevation model.
- Demands: allocate **billed consumption** to nodes (by meter location), add **non-revenue water** (losses), and apply patterns from SCADA flows. Big users get their own patterns.
- **Skeletonisation**: simplify small pipes for strategic models; keep all mains for fire flow and water quality work.
- Controls: reservoir inlet valves, pump start/stop levels and PRV settings, from operations staff, not just drawings.

## Calibration

A model isn't trustworthy until it matches the real network:

1. Collect field data: **pressure loggers** at spread-out hydrants, flows and tank levels from SCADA, pump status, plus **hydrant flow tests** (open a hydrant, measure flow and the pressure drop nearby) to stress the network.
2. Compare model and field pressures and flows across the day.
3. Adjust **roughness**, demands and, more importantly, find **errors**: closed valves that are shown open, wrong diameters, missing connections. Large mismatches usually mean a data error, not roughness.
4. Check against criteria. Commonly used guidance targets model pressures within about 1-2 m of field values for most points at a given time, and flows within a few percent on main transfer lines. Agree criteria up front for the model's purpose.

## Using the model

- **Growth scenarios**: add future demands and test pressure, fire flow and storage.
- **Criticality**: close each main in turn and see who loses supply or pressure.
- **Fire flow analysis** at every hydrant node, with background demand.
- **Water age and chlorine decay** to find dead ends and oversized mains.
- **Energy optimisation** of pump schedules against off-peak tariffs.
- **Pressure management**: test PRV zones that cut leakage and burst rates, since leakage rises with pressure (roughly with pressure to a power between 0.5 and 1.5 depending on the pipe materials and leak types).

## Limits

A model is only as good as its data. Document assumptions, version the model, and record what it's calibrated for. A strategic model skeletonised for planning shouldn't be used for detailed fire flow checks in a single street.

> **Field reality check:** if the model says pressure is fine but customers complain, believe the customers and look for a closed valve.""",
    "key_points": [
        "Models are nodes (elevation, demand) and links (pipes, pumps, valves) solved by the gradient method, as in EPANET.",
        "Extended period simulation with diurnal patterns is needed for storage, pumps, energy and water quality.",
        "Calibrate with pressure loggers, SCADA and hydrant flow tests; big mismatches usually mean data errors like closed valves.",
        "Use models for growth, criticality, fire flow, water age and pressure management, within what they're calibrated for.",
    ],
    "figure_svg": MODEL,
    "figure_caption": "A model of looped mains and a reservoir, calibrated by comparing logger data with model results.",
    "questions": [
        mcq("What does a junction node in EPANET carry?", ["Pipe roughness", "Elevation and demand", "A pump curve", "Valve settings"], 1,
            "Links carry roughness, pumps and valves."),
        mcq("Which analysis is needed to study water age?", ["Steady state at peak hour", "Extended period simulation", "A fire flow snapshot", "A pipe stress analysis"], 1,
            "Water quality depends on time and changing flows."),
        mcq("In the diagram, what is calibration doing?", ["Drawing the pipes", "Adjusting the model until it matches field measurements", "Choosing pipe colours", "Installing loggers only"], 1,
            "Match model and field data.",
            MODEL, "A looped network with a reservoir and a pressure logger; field and model traces compared."),
        mcq("A model's pressures are 15 m too high in one zone. What's the most likely cause?", ["Roughness slightly wrong", "A data error such as a closed valve or wrong pipe", "Weather", "The solver"], 1,
            "Big mismatches are rarely fixed by tweaking roughness."),
        mcq("What does a hydrant flow test give you?", ["Water age", "Flow and pressure drop data that stress the network for calibration", "Chlorine residual", "Pipe material"], 1,
            "It exercises friction losses that are small at normal flows."),
        mcq("Why does pressure management reduce leakage?", ["Leaks are fixed by pressure", "Leakage rises with pressure, so lower pressure means less loss and fewer bursts", "It increases flow", "It improves taste"], 1,
            "Leakage scales with pressure to a power."),
        mcq("In the diagram, what do the links between nodes represent?", ["Customers", "Pipes, pumps and valves", "Pressure loggers", "Demand patterns"], 1,
            "Nodes carry demand and elevation.", MODEL, "Network of nodes joined by links, with a note that links are pipes, pumps and valves."),
        open_q("What is skeletonisation and when shouldn't you use a skeletonised model?", "It simplifies the model by removing or merging small pipes to speed up strategic analysis; it shouldn't be used for detailed checks like fire flow in a particular street or water age in small mains, because those depend on the pipes that were removed.",
               ["simplify by removing small pipes", "fine for strategic planning", "not for detailed fire flow or water quality"], "Match model detail to purpose."),
        open_q("Describe how you'd allocate demands in a new model.", "Take billed consumption from customer meters and allocate it to the nearest nodes by location, add non-revenue water as losses spread across the network, give large users their own demand and patterns, and apply diurnal patterns from SCADA flow data for each zone.",
               ["billed consumption to nodes", "add non-revenue water", "patterns from SCADA", "large users separately"], "Balance against zone inflow."),
        open_q("How would you use a model to find critical mains?", "Close each main (or each valve-bounded section) in turn in the model and check which customers lose supply or fall below minimum pressure; mains whose failure affects many customers or key sites such as hospitals are critical and get priority for renewal, monitoring or duplication.",
               ["close each main in turn", "see who loses supply or pressure", "prioritise critical mains"], "Combine with likelihood for a risk score."),
    ],
}

L3 = {
    "title": "Sewage pump station design",
    "minutes": 11,
    "photo_query": "sewage pump station",
    "body": """Where gravity sewers get too deep, sewage is collected in a **wet well** and pumped up a **rising main** to a higher gravity sewer or treatment plant. In Australia the **Sewage Pumping Station Code (WSA 04)** and the water corporation's supplement set the requirements.

## Design flows and pumps

- Design for **PWWF** with the duty pumps running; at least one **standby** pump of equal capacity, so the station meets the design flow with the largest pump out of service.
- Submersible pumps with non-clog or vortex impellers suit most stations; larger stations may use dry-well pumps.
- **Rising main velocity**: high enough to keep solids moving and scour settled material (commonly a minimum around 0.75-1 m/s), but not so high that friction and surge become excessive (often below about 2.5-3 m/s).
- Check the pump against the full range of static heads and new versus aged pipe conditions.

## Wet well sizing

Pumps must not start too often or motors overheat. For a single fixed-speed pump, the shortest cycle (fill plus empty) happens when inflow equals half the pump rate, giving:

**Vs = T × Q / 4**

where Vs is the **active storage** between start and stop levels, T is the minimum cycle time (the inverse of the allowed starts per hour) and Q is the pump rate. Example: a 30 L/s pump allowed 10 starts per hour (T = 360 s) needs Vs ≥ 360 × 0.030 / 4 ≈ **2.7 m³**. Alternating duty pumps and VSDs relax this. Manufacturer limits on starts per hour decide T.

Other levels: the **stop level** keeps the pump submerged enough to avoid vortices and cavitation (follow the pump maker's submergence), the **high level alarm** warns of failure, and the **overflow level** is set so any overflow goes to a designated, licensed point rather than into homes.

## Emergency storage

When power or pumps fail, sewage keeps arriving. Stations provide **emergency storage** (in the wet well, an extra tank, or upstream sewers) for a period at ADWF, commonly a few hours, set by the corporation based on response time and consequences. Many stations also have a connection for a **mobile generator**, or a fixed one for critical sites.

## Septicity and odour

Long rising mains at low flows hold sewage for hours. It goes **septic**, generating **H₂S** that corrodes concrete and steel and causes odour complaints at the discharge manhole. Controls include:

- Limiting detention time (size the main sensibly, avoid oversizing for distant future flows).
- Chemical dosing (magnesium hydroxide, iron salts, nitrate or oxygen).
- Corrosion-resistant materials and lined receiving manholes.
- Ventilation and odour control units with activated carbon or biofilters.

## Safety and operability

- **Confined space**: design so routine work happens from the surface; pumps lift out on **guide rails**.
- Valves in a separate, dry **valve chamber**.
- **Flow meter**, level sensors (often both a continuous sensor and backup float switches), and **SCADA** telemetry for alarms.
- Hard-standing, vehicle access for a crane truck, wash-down water, security fencing.
- **Surge analysis** of the rising main, since pump trips are routine events here.

## Whole-of-life thinking

A station is an operating cost for 50+ years: energy, maintenance, odour control and renewals. Sometimes a deeper gravity sewer or a different catchment boundary is cheaper over its life than another pump station.

> **Typical failure:** a station sized for full development runs at a tiny fraction of its capacity for 15 years. The rising main goes septic, the pumps cycle badly and odour complaints follow. Staged designs avoid this.""",
    "key_points": [
        "WSA 04 plus the corporation supplement: design for PWWF with duty pumps and a standby pump.",
        "Wet well active storage Vs ≥ T × Q / 4 for a single fixed-speed pump, with T from allowed starts per hour.",
        "Provide emergency storage, generator connection, alarms and SCADA; set overflow to a licensed point.",
        "Control septicity and H₂S in rising mains; design for safe access, surge and whole-of-life cost.",
    ],
    "figure_svg": WETWELL,
    "figure_caption": "Wet well with start, stop and alarm levels; the active storage Vs between start and stop limits pump starts.",
    "questions": [
        mcq("Why is the minimum cycle time worst when inflow equals half the pump rate?", ["The pump is fastest then", "Fill and empty times sum to a minimum at that inflow", "Pumps can't run below half flow", "It's a rule of thumb with no basis"], 1,
            "Calculus on fill time + empty time gives the minimum at Qin = Q/2."),
        mcq("A 30 L/s pump is allowed 10 starts per hour. What's the minimum active storage?", ["About 0.3 m³", "About 2.7 m³", "About 27 m³", "About 10.8 m³"], 1,
            "T = 360 s; 360 × 0.030 / 4 = 2.7 m³."),
        mcq("In the diagram, what volume is Vs?", ["The whole well", "The active storage between duty start and stop levels", "The emergency storage", "The pump volume"], 1,
            "Vs controls cycling.",
            WETWELL, "Wet well with high level alarm, duty start and stop levels and two pumps; Vs marked between start and stop."),
        mcq("Why is the stop level set above a minimum?", ["To save space", "To keep pumps submerged enough to avoid vortices and cavitation", "To store more sewage", "For odour"], 1,
            "Follow the pump maker's submergence."),
        mcq("What's emergency storage for?", ["Extra pump capacity", "Holding inflow while power or pumps are restored", "Septic treatment", "Groundwater"], 1,
            "Sized from response time and consequence."),
        mcq("What causes odour and corrosion at the end of a long rising main at low flows?", ["High velocity", "Septic sewage producing hydrogen sulfide", "Too much oxygen", "Chlorine"], 1,
            "Long detention in a full pipe goes anaerobic."),
        mcq("In the diagram, what should happen if the level reaches the high level alarm?", ["Nothing", "Telemetry alerts operators so they respond before an overflow", "The station shuts down", "The pumps slow down"], 1,
            "Alarms go via SCADA.", WETWELL, "Wet well with a high level alarm line above the duty start level."),
        open_q("Why must a sewage pump station have a standby pump of equal capacity?", "So the station can still pump the design peak flow when the largest pump fails or is out for maintenance, avoiding overflows; pumps are mechanical and do fail.",
               ["meet design flow with largest pump out", "avoid overflows", "maintenance and failure"], "Usually duty/standby alternate to share wear."),
        open_q("Explain why staging a pump station for growth can be better than building it for full development.", "A station sized for the future runs at low flows for years, so the rising main has long detention and goes septic, pumps cycle poorly and operate far from best efficiency; staging pumps, impellers or even mains matches capacity to actual flows and spreads cost.",
               ["low flows for years", "septicity and poor pump operation", "match capacity to actual flow"], "Civil works may be built once, with mechanical items staged."),
        open_q("What design features make a pump station safe to operate?", "Pumps on guide rails that lift out from the surface, valves in a separate dry chamber, avoiding routine confined-space entry, good vehicle and crane access, level sensors with backup floats, telemetry alarms, ventilation and odour control, and security fencing.",
               ["avoid confined space entry", "pumps lift out on rails", "valve chamber", "alarms and access"], "WSA 04 covers these."),
    ],
}

L4 = {
    "title": "Asset management and renewal planning",
    "minutes": 10,
    "photo_query": "old cast iron water pipe",
    "body": """Most water infrastructure already exists. Much of it was built in the post-war decades and is now ageing, so the expert job is often deciding **what to renew, when, and how** with limited money. That's asset management.

## The framework

**ISO 55000** (asset management) describes coordinated activity to realise value from assets, balancing **cost, risk and performance** over the whole life. Key elements:

- An **asset management policy and strategy** linked to the organisation's objectives and customer service levels.
- An **asset register**: what you own, where, size, material, age, condition and criticality. Data quality is often the weakest link.
- **Levels of service**: what customers and regulators expect (interruptions, pressure, spills, odour, water quality), and what they're willing to pay.
- **Lifecycle plans** for each asset class: create, operate, maintain, renew, dispose.

In Victoria, water corporations report performance to the Essential Services Commission, and their price submissions must justify renewal programs, so this is real money.

## Risk = likelihood × consequence

For each asset, estimate:

- **Likelihood of failure (LoF)**: from age, material, failure history, soil, pressure, condition data. For water mains, a cluster of breaks is the strongest predictor of more breaks.
- **Consequence of failure (CoF)**: customers affected, critical customers (hospitals, dialysis patients), traffic, flooding or environmental damage, repair difficulty and cost.

Plot them on a **risk matrix**. High-consequence, high-likelihood assets get renewed first; high-consequence, low-likelihood assets get monitored or given redundancy; low-consequence assets may simply be **run to failure** and repaired.

## Condition assessment

- **Sewers**: **CCTV** inspection coded to a standard (in Australia, the WSA's Conduit Inspection Reporting Code) giving structural and service grades.
- **Water mains**: break history, pipe samples taken during repairs, and for critical large mains, specialised tools (acoustic, electromagnetic and in-pipe inspection).
- **Pump stations and plants**: inspections, vibration and thermal monitoring, run hours.
- **Remaining useful life** combines condition, deterioration rate and the asset's expected life.

## Renewal options

- **Replace** by open trench.
- **Trenchless**: pipe bursting, horizontal directional drilling, and for sewers **relining** (cured-in-place pipe, CIPP), often cheaper and much less disruptive in established streets.
- **Rehabilitate**: lining manholes, cathodic protection for steel.
- **Defer** with monitoring when risk is acceptable.

## Making the case

A renewal program should show:

- How risk and service levels change with different investment levels (scenarios).
- **Whole-of-life cost**: capital plus operating plus failure costs, discounted (net present value).
- Benefits beyond the asset: fewer interruptions, lower leakage, fewer spills, reduced emergency work.

## Common traps

- Renewing by age alone: many old pipes are fine, and some young ones are failing.
- Ignoring data quality: wrong materials or diameters in GIS skew everything.
- Replacing like with like without asking if the asset is still needed or should be resized for growth or decline.

> **Good practice:** close the loop. Record every failure, its cause and the pipe details, and feed it back into the likelihood model.""",
    "key_points": [
        "ISO 55000 asset management balances cost, risk and performance over the whole life, linked to levels of service.",
        "Risk = likelihood × consequence; renew high-high first, add redundancy to high-consequence assets, run low-consequence assets to failure.",
        "Condition: CCTV for sewers, break history and samples for mains, monitoring for plant.",
        "Renewal options include trench, trenchless and relining; justify programs with risk scenarios and whole-of-life cost.",
    ],
    "figure_svg": RISK,
    "figure_caption": "A risk matrix: asset A (high likelihood, high consequence) is the top priority, B the lowest.",
    "questions": [
        mcq("What does ISO 55000 cover?", ["Pipe sizes", "Asset management", "Drinking water quality", "Pump curves"], 1,
            "It's the asset management standard series."),
        mcq("Which is often the strongest predictor of future water main breaks?", ["Pipe colour", "A history of recent breaks on that main", "Water temperature only", "The street name"], 1,
            "Breaks cluster."),
        mcq("In the diagram, which asset should be renewed first?", ["A", "B", "C", "D"], 0,
            "High likelihood and high consequence.",
            RISK, "Risk matrix with likelihood on the horizontal axis and consequence vertical; A in high/high, B low/low, C high likelihood low consequence, D low likelihood high consequence."),
        mcq("In the diagram, what's a sensible approach for asset D (low likelihood, high consequence)?", ["Run it to failure", "Monitor it and consider redundancy", "Ignore it", "Demolish it"], 1,
            "Failure would be serious even if unlikely.",
            RISK, "Risk matrix with D in the low likelihood, high consequence quadrant."),
        mcq("How are sewers usually inspected for condition?", ["Pressure logging", "CCTV coded to a standard", "Water sampling", "Hydrant tests"], 1,
            "CCTV gives structural and service grades."),
        mcq("What is CIPP?", ["A pump type", "Cured-in-place pipe, a trenchless sewer relining method", "A water quality test", "A valve"], 1,
            "It lines the existing pipe from inside."),
        mcq("Why is renewing pipes by age alone a trap?", ["Old pipes always fail", "Age is a weak predictor; condition and consequence matter more", "It's too cheap", "Regulators forbid it"], 1,
            "Some old pipes are fine, some young ones fail."),
        open_q("Explain why some assets can be deliberately run to failure.", "If failure has low consequences and repair is cheap and quick, it costs less overall to repair when it fails than to renew early; money is better spent on high-risk assets.",
               ["low consequence", "repair cheaper than early renewal", "spend on high-risk assets"], "It's a conscious, documented choice."),
        open_q("What would you include in a business case for a water main renewal program?", "Investment scenarios showing the resulting risk and service levels, whole-of-life cost with net present value including failure costs, benefits such as fewer interruptions, lower leakage and less emergency work, the data and models used, and links to customer and regulatory expectations.",
               ["scenarios of risk and service", "whole-of-life cost and NPV", "benefits beyond the asset"], "In Victoria, price submissions to the ESC rely on this."),
        open_q("Why does asset data quality matter so much?", "Risk models rely on the register; wrong materials, sizes, ages or locations give wrong likelihood and consequence scores, sending money to the wrong assets and missing real risks; recording failures accurately also improves future predictions.",
               ["models rely on the register", "wrong data misdirects spending", "record failures to improve"], "Close the data loop."),
    ],
}

L5 = {
    "title": "Wastewater treatment and recycled water",
    "minutes": 12,
    "photo_query": "activated sludge aeration tank",
    "body": """Wastewater treatment protects public health and the waterways that receive the effluent. Modern plants remove organic matter, solids, **nutrients** (nitrogen and phosphorus) and pathogens, and increasingly produce **recycled water** and recover energy.

## What's in sewage

Key measures are **BOD** (biochemical oxygen demand, the oxygen microbes need to break down organic matter), **suspended solids (SS)**, **total nitrogen (TN)** and **total phosphorus (TP)**, plus pathogens such as *E. coli* as an indicator. Raw domestic sewage typically has BOD and SS in the low hundreds of mg/L.

## Treatment stages

1. **Preliminary**: screens remove rags and plastics; grit chambers remove sand.
2. **Primary**: settling tanks remove a good share of SS and some BOD as primary sludge (some plants skip this).
3. **Secondary (biological)**: microbes eat dissolved and fine organic matter. A well-run secondary plant commonly achieves effluent BOD around 20 mg/L and SS around 30 mg/L or better; nutrient removal plants go much lower.
4. **Tertiary**: filtration, disinfection (UV, chlorine) and sometimes membranes, to meet discharge or reuse standards.
5. **Sludge (biosolids)**: thickened, often digested anaerobically (making biogas for energy), dewatered and reused on land where suitable.

## Activated sludge

The workhorse of larger plants. Wastewater is mixed with a suspension of microbes (**mixed liquor**) in an aerated **bioreactor**, then settled in a **clarifier**. Most settled sludge returns (**RAS**, return activated sludge) to keep the microbe population high; the excess is wasted (**WAS**). The **sludge age** (solids retention time) controls which organisms grow.

**Nitrogen removal** takes two steps:

- **Nitrification**: in aerobic zones, slow-growing bacteria convert ammonia to nitrate. They need enough sludge age, oxygen and warmth.
- **Denitrification**: in **anoxic** zones (no dissolved oxygen, but nitrate present), other bacteria use nitrate as their oxygen source and release nitrogen gas, using the sewage's carbon.

**Phosphorus** is removed biologically (with an anaerobic zone that encourages phosphorus-accumulating organisms) or chemically by dosing iron or aluminium salts. Variants include sequencing batch reactors (SBRs), oxidation ditches and membrane bioreactors (MBRs).

## Lagoons

Many regional Victorian towns use **lagoon** systems: large, shallow ponds where natural processes (bacteria, algae, sunlight) treat sewage over weeks. They're cheap to run and robust, but need lots of land, struggle to meet tight nutrient limits, can produce algae in effluent and have variable performance in winter. Effluent often goes to winter storage and irrigation rather than to rivers.

## Recycled water in Victoria

EPA Victoria's guidance on water recycling uses **classes** from **A** (highest quality, suitable for uses with high human contact such as dual-pipe residential supply for toilets and gardens, and unrestricted irrigation) through **B** and **C** to **D** (lowest, restricted uses such as some non-food crops and woodlots). Higher classes need more treatment barriers, log-reduction validation and monitoring. Schemes also need management plans covering health and environmental risks, such as nutrient and salt loads on irrigated land.

## Licensing and the environment

Discharges are licensed by **EPA Victoria**, with limits set to protect the receiving environment. Inland rivers often have stringent nutrient limits because of algal bloom risk. Overflows from sewers and plants in wet weather are a major regulatory and community focus.

> **Trend:** plants are becoming **resource recovery facilities**, producing biogas, biosolids and recycled water, and aiming to reduce energy use and greenhouse emissions (including nitrous oxide from nitrogen removal).""",
    "key_points": [
        "Measure sewage by BOD, SS, TN, TP and pathogens; treatment runs preliminary, primary, secondary, tertiary and sludge handling.",
        "Activated sludge uses mixed liquor, clarifiers and RAS/WAS; sludge age controls the microbes.",
        "Nitrogen removal: nitrification in aerobic zones then denitrification in anoxic zones; phosphorus by biological or chemical removal.",
        "Victorian recycled water classes run A (highest) to D (lowest); discharges are licensed by EPA Victoria.",
    ],
    "figure_svg": STP,
    "figure_caption": "Activated sludge: screens, primary settling, a bioreactor with anoxic and aerobic zones, clarifier with return sludge, then tertiary treatment.",
    "questions": [
        mcq("What does BOD measure?", ["Water hardness", "Oxygen needed by microbes to break down organic matter", "Nitrogen content", "Turbidity"], 1,
            "Biochemical oxygen demand."),
        mcq("In the diagram, what is RAS?", ["Raw sewage", "Return activated sludge from the clarifier to the bioreactor", "A screen", "Recycled water"], 1,
            "It keeps the microbe population high.",
            STP, "Activated sludge flow: screens, primary, bioreactor, clarifier, tertiary; a return line labelled RAS from the clarifier to the bioreactor, and WAS to sludge."),
        mcq("Where does nitrification happen?", ["In anoxic zones", "In aerobic zones", "In the screens", "In the digester"], 1,
            "Nitrifiers need oxygen."),
        mcq("What do denitrifying bacteria use instead of dissolved oxygen?", ["Chlorine", "Nitrate", "Phosphate", "Methane"], 1,
            "They release nitrogen gas."),
        mcq("Which Victorian recycled water class is the highest quality?", ["Class D", "Class C", "Class B", "Class A"], 3,
            "Class A suits the highest-contact uses."),
        mcq("What's a common limitation of lagoon systems?", ["High energy use", "Difficulty meeting tight nutrient limits and needing lots of land", "Too much biogas", "They need skilled operators 24/7"], 1,
            "They're robust but land-hungry and variable."),
        mcq("In the diagram, what is WAS used for?", ["Returning to the bioreactor", "Removing excess sludge to control sludge age", "Disinfection", "Odour control"], 1,
            "Wasting sets the solids retention time.", STP, "Activated sludge plant with WAS leaving the clarifier toward sludge treatment."),
        open_q("Explain why nitrogen removal needs both aerobic and anoxic zones.", "Ammonia is first converted to nitrate by nitrifying bacteria, which need oxygen (aerobic zone); then denitrifying bacteria, in an anoxic zone without dissolved oxygen, use the nitrate as their oxygen source and release nitrogen gas to the air, using carbon from the sewage.",
               ["nitrification needs oxygen", "denitrification in anoxic zone", "nitrate to nitrogen gas"], "Recycle mixed liquor from aerobic to anoxic zones."),
        open_q("Why do inland Victorian rivers often have strict nutrient limits for treated effluent?", "Nitrogen and phosphorus feed algae, and slow-flowing warm inland rivers are prone to algal blooms, including toxic blue-green algae, that harm ecosystems and water supplies; so EPA licences restrict nutrient loads.",
               ["nutrients feed algae", "blue-green algal blooms", "EPA licence limits"], "That's why many plants irrigate or store instead of discharging."),
        open_q("What makes a modern treatment plant a 'resource recovery facility'?", "Instead of only disposing of waste, it recovers resources: biogas from anaerobic digestion for energy, biosolids for land application, recycled water for irrigation, industry or homes, and sometimes nutrients, while reducing energy use and emissions.",
               ["biogas energy", "biosolids reuse", "recycled water"], "Nitrous oxide emissions are a growing focus."),
    ],
}

L6 = {
    "title": "Integrated water management and a changing climate",
    "minutes": 10,
    "photo_query": "constructed wetland stormwater",
    "body": """Expert water engineering increasingly means designing **systems**, not just pipes: linking water supply, sewerage, stormwater and waterways, and planning for a hotter, more variable climate.

## Integrated water management (IWM)

IWM treats all water in a place, drinking water, wastewater, stormwater, groundwater and waterways, as one resource. In Victoria, IWM forums bring together water corporations, councils, catchment management authorities and Traditional Owners to plan projects with shared benefits. Typical outcomes:

- **Fit-for-purpose water**: recycled water and harvested stormwater for parks, sports fields, industry and toilets, saving drinking water.
- **Water sensitive urban design (WSUD)**: wetlands, raingardens and swales that treat stormwater and cool cities.
- **Green, cool urban landscapes**: irrigated trees and open space reduce heat island effects.
- **Healthy waterways**: lower stormwater flows and pollutant loads.

IWM projects are judged on many values (liveability, environment, culture, cost), not just lowest capital cost.

## Rainfall and floods: ARR

**Australian Rainfall and Runoff (ARR)**, from Engineers Australia, is the national guide for flood estimation. It provides:

- **IFD** (intensity-frequency-duration) design rainfall from the Bureau of Meteorology for any location.
- **Temporal patterns** (how rain is distributed within a storm), **areal reduction factors** for large catchments, and **losses**.
- Methods from simple (rational method for small catchments) to **ensemble or Monte Carlo** approaches with hydrologic and hydraulic models (for example RORB, WBNM, or rainfall on grid 2D models).
- Terminology based on **AEP** (annual exceedance probability), such as the 1% AEP event, replacing older "1 in 100 year" language that people misread.

## Climate change

Climate projections for Victoria point to warmer conditions, generally less cool-season rainfall in the south, longer droughts, and more intense short-duration rainfall extremes. ARR's climate change guidance (updated in recent years) increases design rainfall depending on the warming scenario and planning horizon, with larger increases for short, intense bursts. Practical implications:

- **Drainage**: pipes and overland flow paths sized today may be undersized for 2070; design overland paths and floor levels with margin and consider adaptive designs.
- **Supply security**: inflows to storages can fall more than rainfall does, because drier catchments absorb more. Water corporations plan with scenarios, including climate-independent sources (desalination, recycled water) and the Victorian water grid.
- **Assets**: higher temperatures speed septicity and odour in sewers and algal blooms in storages; bushfires can damage catchments and water quality for years.
- **Sea level rise**: coastal outfalls, pump stations and low-lying drainage face higher tailwater.

## Planning under uncertainty

Experts don't pick one future. They use:

- **Scenario planning**: test plans against several climate and growth futures.
- **Adaptive pathways**: decide what to do now, and define triggers (a demand level, a storage level) for the next action.
- **No-regret measures**: leakage reduction, efficiency and WSUD pay off in all futures.
- **Real options**: build in the ability to expand later, such as larger easements or a pump station designed for extra pumps.

## Working with Traditional Owners

Victorian water planning increasingly recognises Aboriginal water values and rights, for example through the Victorian Government's *Water is Life* roadmap. Engaging early, and genuinely, with Traditional Owner corporations is part of good practice.

> **The expert mindset:** your assets will outlive today's assumptions. Design for flexibility, document your assumptions, and plan how to adapt.""",
    "key_points": [
        "IWM manages supply, wastewater, stormwater, groundwater and waterways together for multiple values.",
        "ARR is the national flood estimation guide: IFDs, temporal patterns, losses, and AEP terminology.",
        "Climate change raises short-duration rainfall intensity and lowers inflows; ARR guidance increases design rainfall.",
        "Plan with scenarios, adaptive pathways, no-regret measures and real options; engage Traditional Owners early.",
    ],
    "figure_svg": IWM,
    "figure_caption": "Future-climate design rainfall sits above the historical IFD curve, with the biggest increases expected for short, intense bursts.",
    "questions": [
        mcq("What does integrated water management treat as one resource?", ["Only drinking water", "All water in a place: supply, wastewater, stormwater, groundwater and waterways", "Only stormwater", "Only rivers"], 1,
            "Fit-for-purpose use of every source."),
        mcq("What does ARR provide?", ["Pipe prices", "National guidance on flood estimation and design rainfall", "Drinking water limits", "Pump curves"], 1,
            "Australian Rainfall and Runoff."),
        mcq("Why does ARR prefer '1% AEP' to '1 in 100 year'?", ["It's shorter", "People misread '1 in 100' as meaning it happens only once a century", "It's a different event", "Regulators forbid numbers"], 1,
            "A 1% AEP flood can happen in consecutive years."),
        mcq("In the diagram, where does future-climate design rainfall sit?", ["Below historical", "Above historical, especially for short durations", "Equal to historical", "Only at long durations"], 1,
            "Short intense bursts may increase most.",
            IWM, "Intensity-duration curves: a dashed future climate curve above the historical IFD curve, with an arrow at short durations."),
        mcq("Why can storage inflows fall more than rainfall does?", ["Evaporation from pipes", "Drier catchments soak up more rain before runoff", "Climate change stops rivers", "Water corporations divert it"], 1,
            "Runoff is a non-linear response to rainfall."),
        mcq("What's an adaptive pathway?", ["A cycle path", "A plan with triggers that set when the next action is taken", "A pipe route", "A fixed 50-year plan"], 1,
            "Act now, monitor, and respond to triggers."),
        mcq("In the diagram, which storm durations are expected to see the biggest increases?", ["Long, multi-day storms", "Short, intense bursts", "None", "Only snow events"], 1,
            "Warmer air holds more moisture, intensifying short bursts.", IWM, "Two IFD curves with the note that short, intense bursts may increase most."),
        open_q("Give two examples of 'no-regret' measures for a water corporation facing climate change.", "Reducing leakage and improving water efficiency save water and money under any future; water sensitive urban design and stormwater harvesting also add value whether the climate gets drier or wetter.",
               ["leakage reduction", "water efficiency", "WSUD or stormwater harvesting", "pay off in any future"], "They're good investments however the future unfolds."),
        open_q("How would you make a new stormwater design more resilient to climate change?", "Use ARR climate guidance to increase design rainfall for the asset's life, provide generous overland flow paths and freeboard to floor levels, consider adaptive designs such as space for future pipes or detention, and test sensitivity to higher rainfall.",
               ["apply ARR climate uplift", "overland flow paths and freeboard", "adaptive design", "sensitivity testing"], "Major system capacity is cheaper to provide early."),
        open_q("Why are climate-independent sources important for supply security in Victoria?", "Rainfall-dependent storages can fall sharply in long droughts as inflows drop, so sources such as desalination and recycled water, connected via the water grid, keep supply secure whatever the rainfall.",
               ["storages depend on inflows", "droughts reduce inflows", "desalination and recycled water", "water grid"], "The Millennium Drought drove these investments."),
    ],
}

PACK = {
    "id": "water-advanced",
    "version": 1,
    "topic": "Civil and water engineering",
    "title": "Water engineering at expert level",
    "summary": "Hydraulic transients and surge protection, network modelling and calibration, sewage pump station design, asset management, wastewater treatment and recycled water, and integrated water management in a changing climate. For practising engineers.",
    "icon": "waves",
    "level": "advanced",
    "length": "short",
    "area": "engineering",
    "tags": ["water", "civil-engineering", "hydraulics", "asset-management", "wastewater", "climate"],
    "sections": [
        {"title": "Advanced hydraulics", "summary": "Transients, models and pump stations.", "lessons": [
            {"title": L1["title"], "summary": "Estimate surge and choose protection for mains.", "lesson": L1},
            {"title": L2["title"], "summary": "Build, calibrate and use network models.", "lesson": L2},
            {"title": L3["title"], "summary": "Design sewage pump stations to WSA 04.", "lesson": L3},
        ]},
        {"title": "Systems and strategy", "summary": "Managing assets, treatment and the future.", "lessons": [
            {"title": L4["title"], "summary": "Prioritise renewals using risk and condition.", "lesson": L4},
            {"title": L5["title"], "summary": "Explain biological treatment, nutrient removal and recycled water classes.", "lesson": L5},
            {"title": L6["title"], "summary": "Plan water systems with IWM, ARR and climate uncertainty.", "lesson": L6},
        ]},
    ],
}
