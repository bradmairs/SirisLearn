"""Civil and water engineering fundamentals: beginner."""

from app.coursepacks import calc, mcq, open_q, scenario
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, path, svg, text, title

CYCLE = svg(
    title("The urban water cycle"),
    box(15, 60, 85, 44, "Catchment", GREEN, size=12), arrow(100, 82, 120, 82, BLUE),
    box(120, 60, 85, 44, "Storage", BLUE, size=12), arrow(205, 82, 225, 82, BLUE),
    box(225, 60, 95, 44, "Treatment", BLUE, size=12, sub="WTP"), arrow(320, 82, 340, 82, BLUE),
    box(340, 60, 125, 44, "Distribution", BLUE, size=12),
    arrow(402, 104, 402, 140, BLUE), box(340, 142, 125, 44, "Customers", INK, size=12),
    arrow(340, 164, 300, 164, AMBER), box(195, 142, 105, 44, "Sewers", AMBER, size=12),
    arrow(195, 164, 160, 164, AMBER), box(15, 142, 145, 44, "Sewage treatment", AMBER, size=12, sub="WWTP"),
    arrow(87, 186, 87, 222, GREEN), box(15, 224, 145, 40, "River / recycled", GREEN, size=12),
    text(330, 245, "stormwater runs in a separate system", 12, PURPLE),
    text(270, 125, "P", 14, BLUE, weight="bold"), text(250, 205, "Q", 14, AMBER, weight="bold"),
)

HEAD = svg(
    title("Pressure head: 10 m of water ≈ 98 kPa"),
    box(40, 50, 120, 70, "Tank", BLUE), text(100, 100, "water level", 11, MUTED),
    line(160, 60, 450, 60, BLUE, dash="6 4"), text(450, 52, "HGL (no flow)", 12, BLUE, anchor="end"),
    path("M100 120 L100 240 L440 240", INK, 6),
    line(300, 240, 300, 60, AMBER, 2, "4 4"), text(310, 150, "h = 45 m", 13, AMBER, anchor="start"),
    circle(300, 240, 8, AMBER, "#0b1620"),
    text(300, 272, "Gauge at A", 12, AMBER), text(170, 225, "pipe", 12, MUTED),
    text(400, 150, "p = ρgh", 14, INK), text(400, 172, "≈ 441 kPa", 13, GREEN),
)

PIPES = svg(
    title("Common pipe materials"),
    box(20, 55, 140, 60, "PVC-U / PVC-O", BLUE, size=13, sub="water & sewer"),
    box(170, 55, 140, 60, "PE100", GREEN, size=13, sub="welded joints"),
    box(320, 55, 140, 60, "DICL", INK, size=13, sub="ductile iron"),
    box(20, 140, 140, 60, "MSCL steel", PURPLE, size=13, sub="large trunk mains"),
    box(170, 140, 140, 60, "Vitrified clay", AMBER, size=13, sub="older sewers"),
    box(320, 140, 140, 60, "Concrete (RCP)", MUTED, size=13, sub="stormwater"),
    text(240, 240, "DN = nominal size · PN = pressure class (PN16 ≈ 160 m)", 12, INK),
    text(240, 265, "SDR = diameter ÷ wall thickness (PE)", 12, MUTED),
)

NETWORK = svg(
    title("A water distribution network"),
    box(20, 50, 90, 50, "Reservoir", BLUE, size=12, sub="on high ground"),
    line(110, 75, 200, 75, BLUE, 5), text(155, 66, "trunk main", 11, MUTED),
    path("M200 75 L380 75 L380 200 L200 200 Z", INK, 3),
    line(290, 75, 290, 200, INK, 2),
    circle(200, 138, 7, AMBER, "#0b1620"), text(185, 142, "V", 12, AMBER, anchor="end"),
    circle(380, 138, 6, RED, "#0b1620"), text(395, 142, "H", 12, RED, anchor="start"),
    box(395, 180, 70, 40, "PRV", GREEN, size=12), line(380, 200, 395, 200, GREEN, 2),
    text(290, 230, "looped reticulation mains", 11, MUTED),
    text(240, 268, "V = isolation valve · H = hydrant · PRV = pressure reducing valve", 11, MUTED),
)

SEWER = svg(
    title("A gravity sewer and pump station"),
    path("M30 70 L210 150", AMBER, 5), circle(30, 70, 9, INK), circle(120, 110, 9, INK), circle(210, 150, 9, INK),
    text(30, 55, "MH", 11, MUTED), text(120, 95, "MH", 11, MUTED), text(120, 140, "falls at a grade", 11, AMBER),
    box(210, 150, 70, 90, "", BLUE), text(245, 175, "wet", 11, BLUE), text(245, 190, "well", 11, BLUE),
    '<rect x="212" y="205" width="66" height="33" fill="#5fd3ff" opacity="0.35"/>',
    path("M280 200 L330 200 L330 90 L450 90", PURPLE, 4), text(390, 80, "rising main", 12, PURPLE),
    box(395, 95, 70, 40, "", GREEN), text(430, 120, "higher", 11, GREEN),
    text(245, 262, "X", 15, BLUE, weight="bold"), text(345, 150, "Y", 15, PURPLE, weight="bold"),
)

STORM = svg(
    title("Minor and major drainage"),
    path("M20 120 L120 120 L160 150 L320 150 L360 120 L460 120", INK, 3),
    text(240, 140, "road", 11, MUTED),
    '<path d="M162 150 L318 150 L310 138 L170 138 Z" fill="#a78bfa" opacity="0.4"/>',
    text(240, 105, "major: 1% AEP flows along the road", 12, PURPLE),
    line(240, 150, 240, 205, MUTED, 2), box(200, 205, 80, 40, "pit", INK, size=12),
    line(40, 255, 440, 255, BLUE, 6), text(240, 280, "minor: pipes for frequent storms", 12, BLUE),
    line(240, 245, 240, 255, MUTED, 2),
)

L1 = {
    "title": "The urban water cycle and who runs it",
    "minutes": 8,
    "time_sensitive": True,
    "photo_query": "water treatment plant clarifier",
    "body": """Turning on a tap and flushing a toilet rely on one of the largest pieces of infrastructure most people never see. Civil and water engineers plan, design, build, operate and renew it.

## Water supply

1. **Catchments**: rain falls on land that drains to rivers and **reservoirs**, or soaks into **groundwater** aquifers. Protecting catchments (keeping stock, septic tanks and contaminants away) is the first barrier for safe water.
2. **Storage**: dams and weirs hold water through dry periods.
3. **Treatment**: a **water treatment plant (WTP)** removes particles and pathogens and disinfects the water, typically by coagulation, filtration and chlorination.
4. **Distribution**: pipes, pumps, valves and **service reservoirs** (tanks) carry water to every property at a useful pressure.

## Sewerage

5. **Sewers**: pipes from each property carry wastewater, mostly by **gravity**, with **pump stations** lifting it where the ground doesn't fall the right way.
6. **Sewage treatment**: a **wastewater treatment plant (WWTP)** removes solids, organic matter and nutrients. Regional Victorian towns often use **lagoon** systems.
7. **Return or reuse**: treated effluent is released to waterways or land under an environmental licence, or treated further as **recycled water** for irrigation, industry and toilets.

## Stormwater: a separate system

In Australia, rainwater from roofs and roads runs in a **separate stormwater system** of pits, pipes, channels and waterways, untreated or lightly treated before reaching rivers and bays. That's why nothing but rain should go down a street drain. Stormwater is usually managed by local councils (and in Melbourne, Melbourne Water's larger drains).

## Who's responsible in Victoria

- **Water corporations** (such as Goulburn Valley Water, Yarra Valley Water and the other regional and metropolitan corporations) supply water and sewerage services.
- The **Department of Health** regulates drinking water quality under the *Safe Drinking Water Act 2003*.
- **EPA Victoria** regulates discharges to the environment, including treated effluent and recycled water.
- The **Essential Services Commission** regulates prices and service standards.
- Nationally, the **Australian Drinking Water Guidelines (ADWG)** set out how to manage drinking water safety, and the **WSAA codes** (from the Water Services Association of Australia) set common design standards for water supply, sewerage and pumping stations.

> **The multiple-barrier idea:** no single step guarantees safe water. Catchment protection, treatment, disinfection, a sealed distribution system and monitoring each reduce risk, so one failure doesn't make people sick.

## In practice

Find your local water corporation's latest annual drinking water quality report (they publish them). Note where your town's water comes from, how it's treated, and which barriers protect it.""",
    "key_points": [
        "Supply runs catchment → storage → treatment (WTP) → distribution; sewerage runs sewers → treatment (WWTP) → return or reuse.",
        "Australian stormwater is a separate system from sewerage, mostly managed by councils.",
        "In Victoria: water corporations deliver services; Department of Health regulates drinking water; EPA regulates discharges; ESC regulates prices.",
        "Safe water relies on multiple barriers, guided nationally by the ADWG; WSAA codes standardise design.",
    ],
    "figure_svg": CYCLE,
    "figure_caption": "Water flows from catchment to customers (P), then as sewage to treatment and back to the environment or reuse (Q); stormwater is separate.",
    "questions": [
        mcq("What is the first barrier in providing safe drinking water?", ["Chlorination", "Protecting the catchment", "The customer's tap", "The sewer"], 1,
            "Keeping contamination out of source water reduces what treatment has to remove."),
        mcq("In the diagram, which path does the label Q mark?", ["Drinking water supply", "Wastewater from customers to treatment", "Stormwater", "Recycled water to customers"], 1,
            "Q is the sewerage path: customers to sewers to the WWTP.",
            CYCLE, "Boxes from catchment to storage, treatment, distribution and customers (path P), then sewers to sewage treatment and to a river or recycled use (path Q); stormwater noted as separate."),
        mcq("In Australia, where does rain from a street drain usually go?", ["To the sewage treatment plant", "Through the separate stormwater system to waterways", "Into the drinking water reservoir", "Into customers' homes"], 1,
            "Stormwater and sewerage are separate systems."),
        mcq("Which body regulates drinking water quality in Victoria?", ["EPA Victoria", "The Department of Health", "The Essential Services Commission", "Local councils"], 1,
            "Under the Safe Drinking Water Act 2003."),
        mcq("What do the WSAA codes provide?", ["Water prices", "Common design standards for water, sewerage and pumping infrastructure", "Drinking water health limits", "Rainfall data"], 1,
            "For example WSA 03 (water supply), WSA 02 (gravity sewerage), WSA 04 (pumping stations)."),
        mcq("Which treatment type is common for sewage in small regional Victorian towns?", ["Reverse osmosis", "Lagoon systems", "Desalination", "Ozone towers"], 1,
            "Lagoons are simple, robust and suit available land."),
        mcq("In the diagram, which path (P) carries treated drinking water?", ["From treatment through distribution to customers", "From sewers to the WWTP", "From roads to rivers", "From the WWTP to the river"], 0,
            "P runs from the WTP through distribution to customers.", CYCLE, "Urban water cycle with supply path P and sewerage path Q."),
        open_q("Explain the 'multiple barrier' approach to safe drinking water.", "Several independent controls each reduce the risk: protecting the catchment, treatment such as coagulation and filtration, disinfection, keeping the distribution system sealed, and monitoring; if one barrier fails the others still protect people.",
               ["several independent barriers", "catchment, treatment, disinfection, distribution", "one failure isn't enough to cause harm"], "It's the core idea of the ADWG."),
        open_q("Why should only rain go down a street drain?", "Because the stormwater system usually flows to creeks, rivers and bays with little or no treatment, so paint, oil, detergent or rubbish poured into it ends up polluting waterways.",
               ["stormwater goes to waterways", "little or no treatment"], "It's not connected to the sewage plant."),
        open_q("Name the roles of a water corporation, EPA Victoria and the Essential Services Commission.", "The water corporation supplies drinking water and sewerage services; EPA Victoria regulates discharges to the environment such as treated effluent; the Essential Services Commission regulates prices and service standards.",
               ["water corporation delivers services", "EPA regulates discharges", "ESC regulates prices and service standards"], "The Department of Health covers drinking water quality."),
    ],
}

L2 = {
    "title": "Pressure, head and flow",
    "minutes": 9,
    "photo_query": "",
    "body": """Water engineering is mostly about getting the right amount of water to the right place at the right pressure. Three ideas do most of the work: **pressure head**, **flow** and **energy**.

## Pressure and head

Pressure in still water depends only on depth: **p = ρgh**, where ρ is density (about 1000 kg/m³), g is 9.81 m/s² and h is depth in metres. So every **metre of water** adds about **9.81 kPa**.

Engineers often talk in **metres of head** instead of kPa, because it relates directly to height:

- 10 m head ≈ 98 kPa ≈ 1 bar.
- 1 m head ≈ 9.81 kPa; 100 kPa ≈ 10.2 m.

A tank whose water level is 45 m above a point gives about 45 m of static head there, roughly 441 kPa, regardless of the pipe route in between. That's why service reservoirs sit on hills or towers: height becomes pressure.

## Flow, velocity and continuity

**Flow rate (Q)** is volume per time: m³/s or, more usually, litres per second (L/s). It's linked to the average velocity (V) and pipe area (A):

**Q = V × A**, with A = πD²/4.

Example: a DN150 main (internal diameter about 0.15 m) has A ≈ 0.0177 m². At 20 L/s (0.020 m³/s), V = 0.020 / 0.0177 ≈ **1.13 m/s**.

**Continuity**: water is (practically) incompressible, so in a pipe without branches the same Q passes every point. Where the pipe narrows, velocity rises.

## Energy: Bernoulli

At any point, flowing water's **total head** is the sum of:

- **elevation head** z (height above a datum),
- **pressure head** p/ρg,
- **velocity head** V²/2g (small in pipes: 1.13 m/s gives only 0.065 m).

In a perfect pipe, total head stays constant (**Bernoulli's equation**). In real pipes, friction and fittings use up energy, so total head **falls along the flow**. That loss is **head loss**, covered in the intermediate course.

## The hydraulic grade line

Plot elevation plus pressure head along a pipe and you get the **hydraulic grade line (HGL)**. With no flow it's flat at the tank's water level. With flow, it slopes down as friction uses energy. The vertical gap between the HGL and the pipe is the pressure head at that point. If the HGL drops below the pipe, the pressure goes negative, which risks drawing contamination in, so designers keep the HGL well above the pipe everywhere.

> **Common misconception:** a bigger pipe "gives more pressure". Static pressure comes from height. A bigger pipe reduces velocity and friction losses, so it keeps more of that pressure when water is flowing.

## In practice

Find the top water level of the reservoir supplying a street and the street's ground level (from a map with contours or your water corporation's GIS). The difference is the static head, about 9.81 kPa per metre. Compare it with a pressure gauge reading from a hose tap.""",
    "key_points": [
        "Pressure in still water is p = ρgh: about 9.81 kPa per metre of head; 10 m ≈ 98 kPa.",
        "Flow Q = V × A; continuity means the same Q passes each point of an unbranched pipe.",
        "Total head = elevation + pressure head + velocity head; friction makes it fall along the flow.",
        "The HGL shows pressure along a pipe; keep it well above the pipe to avoid negative pressure.",
    ],
    "figure_svg": HEAD,
    "figure_caption": "With no flow, the gauge at A sits 45 m below the tank's water level, so it reads about 441 kPa.",
    "questions": [
        mcq("Roughly how much pressure does 10 m of water head produce?", ["10 kPa", "98 kPa", "1000 kPa", "1 kPa"], 1, "ρgh = 1000 × 9.81 × 10 ≈ 98 kPa."),
        mcq("In the diagram, about what pressure does the gauge at A read with no flow?", ["45 kPa", "about 441 kPa", "4.5 kPa", "981 kPa"], 1,
            "45 m × 9.81 kPa/m ≈ 441 kPa.",
            HEAD, "A tank with its water level 45 m above a gauge at point A on a pipe below; the static HGL is a flat line at the tank level."),
        mcq("A DN150 pipe carries 20 L/s. Roughly what is the velocity?", ["0.11 m/s", "1.1 m/s", "11 m/s", "0.01 m/s"], 1, "V = Q/A = 0.020 / 0.0177 ≈ 1.13 m/s."),
        mcq("What happens to velocity where a pipe narrows (same flow)?", ["It falls", "It rises", "It stays the same", "Flow stops"], 1, "Continuity: Q = V × A, so smaller A means higher V."),
        mcq("Why are service reservoirs built on high ground?", ["To keep water cool", "Height provides pressure in the network", "To make them easier to clean", "To reduce evaporation"], 1,
            "Every metre of height is about 9.81 kPa."),
        mcq("What does it mean if the hydraulic grade line falls below a pipe?", ["Pressure there is negative", "Flow has stopped", "The pipe is too big", "Velocity is zero"], 0,
            "Negative pressure can draw contaminants in through leaks."),
        mcq("In the diagram, what would happen to the gauge reading if water started flowing through the pipe?", ["It would rise", "It would fall, because friction lowers the HGL", "It would stay at 441 kPa", "It would become negative straight away"], 1,
            "Flow causes head loss, so the HGL slopes down and pressure at A drops.", HEAD, "Static head diagram with a 45 m column above gauge A."),
        open_q("Explain why a bigger pipe doesn't create more static pressure, but can still improve pressure at the tap.", "Static pressure depends only on the height of the water surface above the point. A bigger pipe has lower velocity for the same flow, so it loses less head to friction, keeping more of that pressure available when water is flowing.",
               ["static pressure comes from height", "bigger pipe means less friction loss when flowing"], "Size controls losses, not static head."),
        open_q("Convert 350 kPa into metres of head and explain your working.", "Divide by about 9.81 kPa per metre: 350 / 9.81 ≈ 35.7 m of head.",
               ["divide by 9.81", "about 36 m"], "Or roughly 350 / 10 = 35 m as a quick check."),
        open_q("Name the three parts of total head in Bernoulli's equation.", "Elevation head (height z above a datum), pressure head (p/ρg) and velocity head (V²/2g).",
               ["elevation head", "pressure head", "velocity head"], "Velocity head is usually small in water mains."),
        calc("A town's service reservoir has its water level 52 m above a house's tap. Ignoring flow, what is the static pressure at the tap, in kPa?", 510, "kPa",
             "1. Every metre of water adds ρg ≈ 9.81 kPa.\n2. p = 52 m × 9.81 kPa/m = 510.1 kPa.", "Static head converts to pressure at about 9.81 kPa per metre.", tolerance=2),
        calc("Water flows at 1.2 m/s in a pipe with an internal diameter of 100 mm. What is the flow rate, in L/s?", 9.42, "L/s",
             "1. A = π × 0.1² / 4 = 0.007854 m².\n2. Q = V × A = 1.2 × 0.007854 = 0.009425 m³/s.\n3. × 1000 = 9.42 L/s.", "Q = V × A, then convert m³/s to L/s.", tolerance=2),
    ],
}

L3 = {
    "title": "Pipes and pipe materials",
    "minutes": 8,
    "photo_query": "polyethylene pipe butt fusion welding",
    "body": """Pipes are most of the value of a water or sewer network. Choosing the right material, size and class, and laying it properly, decides how long it lasts.

## Sizes and classes

- **DN** (nominal diameter) is a size label, roughly the bore in millimetres: DN100, DN150, DN300. The actual internal diameter differs by material and class, so hydraulic calculations use the real ID.
- **PN** (pressure nominal) is the rated working pressure in bar: **PN16** is 16 bar ≈ 1.6 MPa ≈ 160 m head. Choose a class that covers the maximum operating pressure **plus** surges.
- **SDR** (standard dimension ratio) for PE pipe is outside diameter ÷ wall thickness. Lower SDR means a thicker wall and higher pressure rating (SDR11 PE100 is PN16).

## Common materials

- **PVC-U, PVC-M and PVC-O**: light, smooth, corrosion-free; the workhorse for reticulation water mains and sewers. PVC-O (oriented) is stronger for its weight.
- **Polyethylene (PE100)**: flexible, joints are **butt-fusion** or **electrofusion** welded into one continuous pipe, so it suits directional drilling and difficult ground. Watch for lower wave speed (helpful for surges) and creep under load.
- **Ductile iron, cement lined (DICL)**: strong and tough, used for larger mains, high pressures and where damage is likely.
- **Mild steel, cement lined (MSCL)**: large trunk mains and pumping mains, welded joints; needs corrosion protection (coatings, cathodic protection).
- **GRP** (glass-reinforced plastic): large diameters, light, corrosion resistant.
- **Vitrified clay (VC)**: long-lasting older sewers, brittle; still used in some places.
- **Reinforced concrete (RCP)**: stormwater and large gravity sewers (sewer concrete needs protection from hydrogen sulphide corrosion).
- **Asbestos cement (AC)** and **cast iron (CICL)** are legacy materials still in the ground in many towns, and a big part of renewal programs.

## Laying pipes

A pipe's strength depends on how it's installed:

- **Bedding and embedment**: selected material (often sand or crushed rock) under and around the pipe, compacted, supports it. Flexible pipes (PVC, PE) rely on side support to stop excessive **deflection**.
- **Cover**: enough depth to protect the pipe from traffic loads and damage, as set by the relevant standard and the water corporation.
- **Thrust blocks** or restrained joints stop unrestrained joints pulling apart at bends, tees and dead ends, where water pressure pushes the pipe.
- **Testing**: new mains are pressure tested and (for water) disinfected and sampled before connection.

> **Tip:** the cheapest pipe isn't always the cheapest choice. Consider ground conditions, corrosion, installation method, the skills and spares of the maintenance crews, and whole-of-life cost.

## In practice

Look at your water corporation's standard drawings or approved products list (most adopt the WSAA codes with local supplements). Note which materials are accepted for water reticulation, sewers and property connections, and why.""",
    "key_points": [
        "DN is a nominal size; PN is pressure class in bar (PN16 ≈ 160 m head); SDR is OD ÷ wall thickness for PE.",
        "PVC and PE dominate reticulation; DICL, MSCL and GRP suit larger or tougher duties; VC, RCP and legacy AC/CI also exist.",
        "Bedding, embedment, cover and thrust restraint matter as much as the pipe itself.",
        "Choose on whole-of-life cost, ground, corrosion and maintenance, not just purchase price.",
    ],
    "figure_svg": PIPES,
    "figure_caption": "Common pipe materials, with what DN, PN and SDR mean.",
    "questions": [
        mcq("What does PN16 mean for a pipe?", ["16 mm wall", "Rated to about 16 bar working pressure (≈160 m head)", "16 m long", "16 years' life"], 1, "PN is the pressure class in bar."),
        mcq("How are PE pipes usually joined?", ["Rubber ring sockets only", "Butt-fusion or electrofusion welding", "Glue", "Flanges only"], 1, "Welded joints make a continuous pipe."),
        mcq("In the diagram, which material is typical for large trunk mains with welded joints?", ["PVC-U", "MSCL steel", "Vitrified clay", "RCP"], 1,
            "Mild steel cement-lined pipe suits large, high-pressure mains.",
            PIPES, "Six materials: PVC-U/PVC-O for water and sewer, PE100 with welded joints, DICL ductile iron, MSCL steel for large trunk mains, vitrified clay for older sewers, and concrete RCP for stormwater."),
        mcq("Why do flexible pipes like PVC and PE need good side support in the trench?", ["To stop them floating", "To limit deflection under soil and traffic loads", "To reduce friction", "For corrosion protection"], 1,
            "Embedment carries much of the load for flexible pipes."),
        mcq("What is a thrust block for?", ["Supporting the pipe's weight", "Resisting the force of water pressure at bends, tees and dead ends", "Stopping tree roots", "Measuring flow"], 1,
            "Unrestrained joints can pull apart without it."),
        mcq("For PE pipe, what does a lower SDR mean?", ["Thinner wall, lower pressure rating", "Thicker wall, higher pressure rating", "Larger diameter", "Different plastic"], 1, "SDR = OD ÷ wall thickness."),
        mcq("In the diagram, which material is mostly used for stormwater?", ["PE100", "Concrete (RCP)", "DICL", "PVC-O"], 1,
            "Reinforced concrete pipe is the stormwater standard.", PIPES, "Pipe materials chart including concrete (RCP) for stormwater."),
        open_q("Why might an engineer choose PE pipe for a main crossing under a river by directional drilling?", "Because PE is flexible and its welded joints make one continuous, fully restrained string that can be pulled through the drilled bore without joints separating.",
               ["flexible", "welded joints make it continuous and restrained", "suits being pulled through a bore"], "Welded PE is the standard for HDD."),
        open_q("Why is DN alone not enough for a hydraulic calculation?", "DN is only a nominal size; the actual internal diameter depends on the material and pressure class, and hydraulics needs the real internal diameter for area and velocity.",
               ["DN is nominal", "internal diameter varies by material and class"], "Use the manufacturer's ID."),
        open_q("Give two reasons the cheapest pipe to buy might not be the best choice.", "It might not suit the ground (corrosive soils, rock, poor support), might cost more to install, could have a shorter life or higher failure rate, or might need spares and skills the maintenance crews don't have; whole-of-life cost matters.",
               ["ground or corrosion suitability", "installation or maintenance costs", "life and whole-of-life cost"], "Think 80 to 100 years."),
    ],
}

L4 = {
    "title": "Water distribution networks",
    "minutes": 9,
    "photo_query": "fire hydrant water main",
    "body": """A distribution network has to deliver enough water, at acceptable pressure, at all times, including the hottest summer afternoon and a fire, while keeping water fresh and safe.

## The parts

- **Service reservoirs** (tanks): store treated water, usually on high ground. They balance the difference between steady supply from the WTP and the daily swings in demand, hold a **fire reserve** and **emergency storage**, and set the pressure in their zone.
- **Trunk mains**: large pipes moving water between treatment, reservoirs and zones.
- **Reticulation mains**: the smaller mains in streets (often DN100–DN200).
- **Property services**: the small pipe from the main to each meter.
- **Pump stations** lift water to reservoirs or boost pressure in high areas.

## Valves and fittings

- **Isolation valves** let crews shut off a section for repairs without cutting supply to everyone.
- **Hydrants** provide water for firefighting and for flushing mains.
- **Scour valves** drain mains at low points; **air valves** release trapped air at high points (air reduces capacity and can cause surges).
- **Pressure reducing valves (PRVs)** lower pressure into a downhill zone.

## Pressure zones

Pressure must be high enough to serve every property and firefighting, but not so high that it bursts pipes and fittings and increases leakage. Typical design targets are around **20 m minimum** and around **80–90 m maximum** under normal conditions, but the actual criteria come from **WSA 03** and your water corporation's supplement. Hilly towns are split into **pressure zones**, each fed from its own reservoir height or a PRV.

## Demand varies

Use follows a **diurnal pattern**: low overnight, peaks in the morning and evening, and much higher on hot days (garden watering). Designers check the network at **peak hour** of the **peak day**, and separately for **fire flow** on top of a base demand.

## Looping and water quality

- **Looped** mains (connected at both ends) keep supply going during a break and share flow, so pressures are more even.
- **Dead ends** let water sit, losing **chlorine residual** and growing in **water age**, which can cause taste, discolouration and microbial risk. Routine flushing helps.
- Oversized mains also slow water down and age it, so bigger isn't always better.

> **Common misconception:** "the reservoir pumps water to houses." In a gravity zone, the reservoir's height does the work: water flows downhill through the mains, and pumps only refill the reservoir.

## In practice

Walk your street and spot the hydrant markers (blue reflective road markers and posts) and valve covers. On your water corporation's maps or GIS, trace your house back through the reticulation main and trunk main to its service reservoir and note the reservoir's top water level.""",
    "key_points": [
        "Service reservoirs balance supply and demand, hold fire and emergency reserves, and set zone pressure.",
        "Trunk mains move bulk water; reticulation mains serve streets; isolation, scour and air valves, hydrants and PRVs control the network.",
        "Design for peak hour of the peak day and for fire flow, within pressure limits from WSA 03 and local standards.",
        "Looped mains improve reliability; dead ends and oversized mains age water and lose chlorine.",
    ],
    "figure_svg": NETWORK,
    "figure_caption": "A reservoir feeds a trunk main into looped reticulation, with isolation valves (V), hydrants (H) and a PRV into a lower zone.",
    "questions": [
        mcq("What is one job of a service reservoir?", ["Treating water", "Balancing steady supply against varying demand", "Removing nutrients", "Measuring rainfall"], 1,
            "It also holds fire and emergency storage and sets pressure."),
        mcq("In the diagram, what does the valve marked V let crews do?", ["Fight fires", "Isolate a section of main for repairs", "Release air", "Reduce pressure"], 1,
            "V is an isolation valve.", NETWORK, "Reservoir feeding a trunk main into a looped network with an isolation valve V, a hydrant H and a PRV into a lower area."),
        mcq("Why are hilly towns divided into pressure zones?", ["To save pipe", "To keep pressure between minimum and maximum limits everywhere", "To separate sewer and water", "For billing"], 1,
            "Each zone gets an appropriate supply level or PRV."),
        mcq("What does an air valve do?", ["Adds oxygen to water", "Releases trapped air at high points", "Drains the main", "Measures pressure"], 1, "Trapped air cuts capacity and can cause surges."),
        mcq("Why can dead-end mains cause water quality problems?", ["They're too small", "Water sits longer, loses chlorine residual and ages", "They leak more", "They get too much pressure"], 1,
            "Flushing and looping help."),
        mcq("When is a network usually checked for its toughest demand conditions?", ["Midnight in winter", "Peak hour on the peak day, and fire flow", "Christmas Day only", "During maintenance"], 1,
            "Plus fire flow on top of a base demand."),
        mcq("In the diagram, what is the PRV for?", ["Isolating the loop", "Reducing pressure into a lower zone", "Firefighting", "Draining the main"], 1,
            "Pressure reducing valves protect lower areas from excess pressure.", NETWORK, "Network diagram with a PRV feeding a lower zone."),
        open_q("Explain why looped mains are preferred to long dead ends.", "Looped mains can be fed from both directions, so a break can be isolated while most customers stay supplied, pressures are more even and water keeps moving, which keeps it fresher with a better chlorine residual.",
               ["supply from two directions", "more reliable during breaks", "better water quality"], "Dead ends need regular flushing."),
        open_q("Why is very high pressure a problem in a water network?", "It increases leakage and the risk of main breaks and damage to customer plumbing and fittings, and wastes energy, so networks limit maximum pressure with zones and PRVs.",
               ["more leakage and bursts", "damages fittings or plumbing"], "Pressure management is a key leakage tool."),
        open_q("In a gravity-fed zone, what actually pushes water to people's houses?", "The height of the water in the service reservoir above the houses; gravity provides the pressure, and pumps only refill the reservoir.",
               ["reservoir height provides pressure", "pumps only refill the reservoir"], "Elevation is stored energy."),
    ],
}

L5 = {
    "title": "Sewerage systems",
    "minutes": 9,
    "photo_query": "sewage pumping station",
    "body": """Sewers carry wastewater from every toilet, shower and factory to treatment, reliably and without overflows, odours or blockages. Most of the work is done by gravity.

## Gravity sewers

Sewage flows downhill in partly full pipes laid at a **grade** (slope). Designers balance:

- a grade steep enough to keep velocities up, so solids keep moving and don't settle (**self-cleansing**), and
- keeping the sewer as shallow as possible, because depth costs money and eventually forces a pump station.

The **WSA 02 Gravity Sewerage Code** (with each water corporation's supplement) sets minimum sizes, minimum grades for each pipe size and other rules. Reticulation sewers are commonly **DN150** or larger, with property connections often DN100.

## Maintenance holes

**Maintenance holes** (manholes, MHs) are placed at changes of direction, grade, size and at junctions, and at intervals along straight runs, so crews and CCTV cameras can get in to inspect and clear the line. Pipes between MHs are laid straight.

## Flows

Sewage flow follows water use, so it varies through the day. Designers estimate:

- **ADWF**: average dry weather flow, from the population served (equivalent population, EP) or land use;
- **PDWF**: peak dry weather flow, applying a peaking factor;
- **PWWF**: peak wet weather flow, adding **inflow and infiltration (I/I)**: rainwater and groundwater getting in through illegal stormwater connections, cracked pipes, leaky joints and maintenance hole lids.

Excessive I/I in wet weather overwhelms sewers and pump stations and causes overflows.

## Pump stations and rising mains

Where gravity can't reach the treatment plant, a **sewage pump station** collects flow in a **wet well** and pumps it through a **rising main** (pressure main) to a higher point, from where gravity takes over again. The **WSA 04 Sewage Pumping Station Code** covers their design: duty and standby pumps, emergency storage, alarms and access.

Long rising mains can hold sewage for hours. Without oxygen it turns **septic**, producing **hydrogen sulphide (H₂S)**: the rotten-egg smell, toxic to workers, and it forms sulphuric acid that corrodes concrete and metal.

## Overflows

When flow exceeds capacity (heavy rain, blockages, pump failure), sewage can spill. Systems include **emergency relief structures** so any spill happens at a controlled, less harmful point rather than inside homes. Spills are reported to EPA Victoria.

> **Common misconception:** "a bigger sewer is always safer." In dry weather, an oversized sewer runs very shallow and slow, so solids settle. Sizing balances peak capacity with self-cleansing at everyday flows.

## In practice

Find your street's sewer on the water corporation's map: note the pipe size, the maintenance holes (round lids, often in the road or nature strip) and which way it falls. Where does it reach the nearest pump station?""",
    "key_points": [
        "Gravity sewers run partly full at a grade that keeps solids moving, set by WSA 02 and local supplements.",
        "Maintenance holes sit at changes of direction, grade, size and junctions, with straight pipe between.",
        "Design flows build from ADWF to PDWF to PWWF, which includes inflow and infiltration.",
        "Pump stations lift sewage through rising mains (WSA 04); long rising mains go septic and produce H₂S.",
    ],
    "figure_svg": SEWER,
    "figure_caption": "A gravity sewer falls between maintenance holes into a pump station wet well (X), which pumps up a rising main (Y).",
    "questions": [
        mcq("How does most sewage get to the treatment plant?", ["Pumped the whole way", "By gravity, with pump stations where needed", "By truck", "Through stormwater drains"], 1, "Gravity first; pumps lift it where the ground doesn't fall."),
        mcq("In the diagram, what is X?", ["A maintenance hole", "The pump station's wet well", "The rising main", "The treatment plant"], 1,
            "Flow collects in the wet well before being pumped.",
            SEWER, "A gravity sewer falling between maintenance holes into a wet well X, which pumps up a rising main Y to a higher point."),
        mcq("What is the main purpose of a minimum sewer grade?", ["To reduce cost", "To keep velocities high enough for self-cleansing", "To increase pressure", "To reduce odour"], 1, "Solids must keep moving."),
        mcq("What is inflow and infiltration?", ["Sewage leaking out", "Rain and groundwater entering the sewer", "Pump station power", "Treated effluent"], 1,
            "It swells wet weather flows."),
        mcq("Why does sewage in a long rising main cause odour and corrosion?", ["It cools down", "Without oxygen it turns septic and produces hydrogen sulphide", "It speeds up", "It gets chlorinated"], 1,
            "H₂S smells, is toxic and forms acid."),
        mcq("Where are maintenance holes placed?", ["Only at the treatment plant", "At changes of direction, grade, size, junctions and along straight runs", "Every 5 m", "Only at pump stations"], 1, "Pipes are straight between them."),
        mcq("In the diagram, what is Y?", ["A gravity sewer", "The rising main (pressure main)", "A maintenance hole", "Stormwater"], 1,
            "Y carries pumped sewage uphill.", SEWER, "Sewer diagram with wet well X and rising main Y."),
        open_q("Explain the difference between PDWF and PWWF.", "PDWF is the peak flow in dry weather, from normal water use with a peaking factor; PWWF adds inflow and infiltration from rain and groundwater, so it's the larger flow sewers must carry in storms.",
               ["PDWF is dry weather peak", "PWWF adds rain and groundwater inflow and infiltration"], "I/I can multiply flows in storms."),
        open_q("Why is an oversized gravity sewer not always better?", "At everyday dry weather flows it runs shallow and slow, so solids settle and cause blockages and odour; sizing balances peak capacity with self-cleansing velocity at normal flows.",
               ["shallow, slow flow at normal times", "solids settle"], "Grade and size work together."),
        open_q("What is an emergency relief structure in a sewer system for?", "It provides a controlled place for sewage to overflow when flows exceed capacity, so any spill happens at a less harmful, managed location rather than inside homes or at random points.",
               ["controlled overflow point", "avoids spills into homes"], "Spills are reported to EPA Victoria."),
    ],
}

L6 = {
    "title": "Stormwater and drainage",
    "minutes": 9,
    "photo_query": "stormwater wetland Australia",
    "body": """When it rains, water has to go somewhere. Stormwater design protects people and property from flooding while protecting waterways from pollution and erosion.

## Catchments and runoff

A **catchment** is the area that drains to a point. When rain falls, some soaks in and some runs off. **Impervious** surfaces (roofs, roads, car parks) shed almost all of it, quickly, so urban development turns gentle rainfall into fast, large flows.

## How big a storm?

Storms are described by their probability: a **1% AEP** (annual exceedance probability) event has a 1 in 100 chance of being equalled or exceeded in any year. (Older documents call it a "100-year ARI", which wrongly suggests it happens only once a century.) Australian design rainfall and methods come from **Australian Rainfall and Runoff (ARR)** and the Bureau of Meteorology's design rainfall data.

## The rational method

For small urban catchments, peak flow is often estimated with the **rational method**:

**Q = C × I × A / 360**

- Q is peak flow in m³/s,
- C is the runoff coefficient (near 0.9 for roofs and roads, much lower for grass),
- I is rainfall intensity in mm/h for a storm lasting the catchment's **time of concentration** (the time for water to travel from its furthest point),
- A is the area in hectares.

Example: a 2 ha car park (C = 0.9) with I = 90 mm/h gives Q = 0.9 × 90 × 2 / 360 = **0.45 m³/s** (450 L/s). Larger or complex catchments use runoff-routing models.

## Minor and major systems

Urban drainage works as two systems together:

- The **minor system**: pits and pipes sized for frequent storms (often around 20% to 5% AEP, set by the council), keeping roads and properties clear in ordinary rain.
- The **major system**: overland flow paths, mostly roads and reserves, that safely carry rarer storms up to the **1% AEP**, with limits on depth and velocity so people and cars aren't swept away.

Floor levels are set above the 1% AEP flood level with **freeboard** (a safety margin).

## Water sensitive urban design

Fast, polluted runoff erodes creeks and carries litter, sediment, nutrients and oils. **WSUD** treats and slows stormwater close to where it falls:

- **raingardens** and **bioretention** basins that filter water through soil and plants,
- **constructed wetlands**, **swales** and **sediment basins**,
- **rainwater tanks** and stormwater harvesting for reuse.

Victorian planning includes stormwater quality targets for new development; councils and Melbourne Water publish guidance.

## Climate change

Design rainfall intensities are expected to increase as the climate warms, so ARR's climate change guidance increases rainfall for future conditions. Long-lived drainage assets should consider it.

> **Remember:** "never drive through floodwater". Just 15 cm of fast-moving water can float a small car, which is why major flow paths have depth-velocity limits.

## In practice

Estimate the runoff from your own roof with the rational method (C about 0.9, area in hectares, a short-duration intensity from the BoM design rainfall website for your town), then see if your downpipes and stormwater connection could carry it.""",
    "key_points": [
        "Impervious urban surfaces turn rainfall into fast, large runoff; catchments drain to a point.",
        "Storm size is expressed as AEP (1% AEP = 1 in 100 chance per year); ARR sets Australian methods.",
        "Rational method: Q = CIA/360 (m³/s, mm/h, ha) for small catchments.",
        "Minor pipes handle frequent storms; major overland paths carry up to 1% AEP; WSUD treats and slows runoff.",
    ],
    "figure_svg": STORM,
    "figure_caption": "Pits and pipes (minor system) carry frequent storms; the road and reserves (major system) safely carry rarer floods.",
    "questions": [
        mcq("What does '1% AEP' mean?", ["It happens once every 100 years exactly", "A 1 in 100 chance of being equalled or exceeded in any year", "1% of rain runs off", "1 mm per hour"], 1,
            "It can happen in consecutive years."),
        mcq("Using Q = CIA/360, what is Q for C = 0.9, I = 90 mm/h, A = 2 ha?", ["0.045 m³/s", "0.45 m³/s", "4.5 m³/s", "45 m³/s"], 1, "0.9 × 90 × 2 / 360 = 0.45 m³/s."),
        mcq("In the diagram, what carries a 1% AEP flood?", ["Only the pipe", "The road and overland flow paths (major system)", "The sewer", "The pit only"], 1,
            "Rare floods exceed pipe capacity, so roads and reserves carry them safely.",
            STORM, "A road cross-section with floodwater along it labelled major: 1% AEP flows along the road, and a pit connected to a pipe labelled minor: pipes for frequent storms."),
        mcq("Which surface has the highest runoff coefficient?", ["Parkland", "A roof", "A forest", "A sports oval"], 1, "Impervious surfaces shed almost all rain."),
        mcq("What is the time of concentration?", ["The rain duration", "The time for water to travel from the furthest point of the catchment to the outlet", "Pipe life", "Pump run time"], 1,
            "The rational method uses rainfall intensity for that duration."),
        mcq("Which is a WSUD measure?", ["A bigger concrete drain", "A raingarden (bioretention)", "A sewer pump station", "A water main"], 1, "Raingardens filter and slow runoff."),
        mcq("In the diagram, what does the pit connect to?", ["The sewer", "The minor system pipe", "The water main", "A reservoir"], 1,
            "Pits collect road runoff into the minor pipe system.", STORM, "Stormwater cross-section with a pit feeding a pipe below the road."),
        open_q("Explain why urban development increases flooding downstream.", "Roofs, roads and paving are impervious, so much more rain runs off instead of soaking in, and it reaches drains faster through pipes and kerbs, giving larger, sharper peak flows downstream.",
               ["more runoff from impervious surfaces", "water arrives faster", "higher peak flows"], "WSUD and retention aim to reduce this."),
        open_q("Why do drainage designs include both a minor and a major system?", "Pipes big enough for the rarest floods would be hugely expensive, so pipes handle frequent storms and roads and reserves are designed as safe overland paths for rare events up to the 1% AEP, with depth and velocity limits.",
               ["pipes for frequent storms", "overland paths for rare floods", "cost and safety balance"], "Floor levels sit above the 1% AEP flood with freeboard."),
        open_q("Why does climate change matter for designing a stormwater pipe today?", "Drainage assets last many decades, and rainfall intensities are expected to increase with warming, so designs based only on past rainfall may be undersized; ARR guidance adjusts design rainfall for future climate.",
               ["long asset life", "rainfall intensity expected to rise", "ARR climate guidance"], "Check the current ARR guidance."),
    ],
}

PACK = {
    "id": "water-beginner",
    "version": 2,
    "topic": "Civil and water engineering",
    "title": "Water and civil engineering fundamentals",
    "summary": "How towns get safe water and get rid of wastewater and stormwater: the urban water cycle, pressure and flow, pipes, distribution networks, sewers and drainage, in a Victorian and Australian context. For beginners.",
    "icon": "waves",
    "level": "beginner",
    "length": "short",
    "area": "engineering",
    "tags": ["water", "civil-engineering", "hydraulics", "sewerage", "stormwater"],
    "sections": [
        {"title": "Water basics", "summary": "The water cycle, hydraulics and pipes.", "lessons": [
            {"title": L1["title"], "summary": "Describe the urban water cycle and who regulates it in Victoria.", "lesson": L1},
            {"title": L2["title"], "summary": "Use head, pressure, flow and continuity in simple calculations.", "lesson": L2},
            {"title": L3["title"], "summary": "Choose and specify pipe materials, sizes and classes.", "lesson": L3},
        ]},
        {"title": "Infrastructure", "summary": "Water networks, sewers and drainage.", "lessons": [
            {"title": L4["title"], "summary": "Explain how distribution networks deliver water at the right pressure.", "lesson": L4},
            {"title": L5["title"], "summary": "Explain how gravity sewers and pump stations move sewage.", "lesson": L5},
            {"title": L6["title"], "summary": "Estimate runoff and explain minor, major and WSUD drainage.", "lesson": L6},
        ]},
    ],
}
