"""Using AI at work: practical, safe and leading AI use in an engineering consultancy."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, path, svg, text, title

PROMPT = svg(
    title("Anatomy of a good prompt"),
    box(20, 50, 440, 38, "Role + goal: what you want and who it's for", BLUE, size=12),
    box(20, 94, 440, 38, "Context: the project, the source documents, the audience", GREEN, size=12),
    box(20, 138, 440, 38, "Constraints: standards, length, tone, what not to do", AMBER, size=12),
    box(20, 182, 440, 38, "Examples: a sample of good output", PURPLE, size=12),
    box(20, 226, 440, 38, "Output format: table, headings, JSON, word count", INK, size=12),
    text(240, 286, "then iterate: review, correct, ask again", 12, MUTED),
)

VERIFY = svg(
    title("Verify before you rely"),
    box(20, 60, 120, 50, "AI draft", PURPLE, size=13), arrow(140, 85, 175, 85, MUTED),
    box(175, 50, 130, 70, "", AMBER), text(240, 75, "Check", 13, AMBER, weight="bold"),
    text(240, 93, "facts · numbers ·", 11, INK), text(240, 108, "references · logic", 11, INK),
    arrow(305, 85, 340, 85, MUTED), box(340, 60, 120, 50, "Engineer signs", GREEN, size=12),
    line(20, 160, 460, 160, MUTED, 1, "3 3"),
    text(240, 185, "Check effort scales with consequence", 13, INK, weight="bold"),
    box(30, 205, 120, 50, "Email tone", GREEN, size=12, sub="skim"),
    box(180, 205, 120, 50, "Report text", AMBER, size=12, sub="read fully"),
    box(330, 205, 120, 50, "Design calc", RED, size=12, sub="independent check"),
)

TASKS = svg(
    title("Where AI helps in a consultancy"),
    box(15, 55, 145, 60, "Bids & proposals", BLUE, size=12, sub="drafts, compliance matrix"),
    box(167, 55, 145, 60, "Reports", BLUE, size=12, sub="structure, summaries"),
    box(320, 55, 145, 60, "Specs & reviews", BLUE, size=12, sub="checklists, gaps"),
    box(15, 125, 145, 60, "Meetings", GREEN, size=12, sub="minutes, actions"),
    box(167, 125, 145, 60, "Scripts & data", GREEN, size=12, sub="Python, Excel, Dynamo"),
    box(320, 125, 145, 60, "Learning", GREEN, size=12, sub="explain, tutor"),
    box(15, 205, 450, 50, "Keep human: judgement, sign-off, client relationships, site safety calls", RED, size=12),
    text(240, 280, "AI drafts and accelerates; engineers decide", 12, MUTED),
)

DATA = svg(
    title("Classify before you paste"),
    box(20, 55, 140, 70, "Public", GREEN, size=13, sub="standards, papers"),
    box(170, 55, 140, 70, "Internal", AMBER, size=13, sub="firm templates"),
    box(320, 55, 140, 70, "Confidential", RED, size=13, sub="client data, PII"),
    text(90, 150, "any approved tool", 11, GREEN), text(240, 150, "enterprise tools", 11, AMBER), text(390, 150, "only if contract +", 11, RED),
    text(390, 165, "policy allow it", 11, RED),
    box(60, 190, 360, 50, "Enterprise tool: no training on your data, access controls, data location", BLUE, size=12),
    text(240, 270, "when unsure, ask or anonymise", 12, MUTED),
)

AUTOMATE = svg(
    title("Choosing the level of automation"),
    line(40, 230, 440, 230, MUTED, 2), arrow(40, 230, 440, 230, MUTED),
    text(240, 258, "more autonomy →", 12, MUTED),
    circle(80, 180, 26, GREEN, label="Chat", size=12), circle(190, 160, 26, BLUE, label="Flow", size=12),
    circle(300, 140, 26, PURPLE, label="Agent", size=12), circle(410, 115, 26, RED, label="Auto", size=12),
    text(80, 140, "you drive", 11, GREEN), text(190, 120, "fixed steps", 11, BLUE),
    text(300, 100, "plans + tools", 11, PURPLE), text(410, 75, "no human", 11, RED),
    text(240, 288, "add a human checkpoint before anything irreversible", 11, AMBER),
)

GOV = svg(
    title("A lightweight AI governance setup"),
    box(170, 45, 140, 44, "AI policy", PURPLE, size=13),
    arrow(200, 89, 100, 120, MUTED), arrow(240, 89, 240, 120, MUTED), arrow(280, 89, 380, 120, MUTED),
    box(20, 120, 150, 60, "Approved tools", BLUE, size=12, sub="+ data rules"),
    box(170, 120, 140, 60, "Use-case register", AMBER, size=12, sub="risk-rated"),
    box(320, 120, 145, 60, "Training", GREEN, size=12, sub="all staff"),
    box(20, 205, 210, 50, "Review & sign-off rules", INK, size=12),
    box(250, 205, 215, 50, "Incidents & lessons", RED, size=12),
    text(240, 282, "proportionate: more control for higher-risk uses", 11, MUTED),
)

PICK = svg(
    title("Picking AI use cases"),
    line(60, 250, 450, 250, MUTED, 2), line(60, 250, 60, 50, MUTED, 2),
    text(255, 280, "Feasibility (data, risk, effort)", 12, MUTED), text(40, 150, "Value", 12, MUTED),
    line(255, 50, 255, 250, MUTED, 1, "4 4"), line(60, 150, 450, 150, MUTED, 1, "4 4"),
    text(355, 70, "quick wins", 12, GREEN), text(150, 70, "big bets", 12, AMBER),
    text(355, 240, "nice to have", 11, MUTED), text(150, 240, "avoid", 11, RED),
    circle(380, 100, 9, GREEN, "#0b1620"), text(395, 95, "A", 14, GREEN, anchor="start", weight="bold"),
    circle(130, 110, 9, AMBER, "#0b1620"), text(145, 105, "B", 14, AMBER, anchor="start", weight="bold"),
    circle(120, 210, 9, RED, "#0b1620"), text(135, 205, "C", 14, RED, anchor="start", weight="bold"),
    circle(360, 200, 9, MUTED, "#0b1620"), text(375, 195, "D", 14, MUTED, anchor="start", weight="bold"),
)

LEAD = svg(
    title("Spreading AI capability"),
    circle(240, 160, 42, PURPLE, "#0b1620", "You", 14),
    circle(110, 90, 28, BLUE, label="Team", size=11), circle(370, 90, 28, BLUE, label="Leads", size=11),
    circle(100, 225, 28, GREEN, label="Grads", size=11), circle(380, 225, 28, GREEN, label="Clients", size=11),
    line(205, 140, 135, 103, MUTED, 2), line(275, 140, 345, 103, MUTED, 2),
    line(205, 180, 125, 215, MUTED, 2), line(275, 180, 355, 215, MUTED, 2),
    text(240, 40, "demos · prompt library · office hours", 12, AMBER),
    text(240, 285, "community of practice: share wins and failures", 12, INK),
)

L1 = {
    "title": "Prompting that works",
    "minutes": 9,
    "photo_query": "",
    "body": """The difference between "AI is useless" and "AI saved me two hours" is usually the prompt. Good prompting isn't magic phrasing; it's giving the model what a capable new colleague would need.

## The five ingredients

1. **Role and goal**: what you want and who it's for. "Draft the executive summary of a sewer condition assessment report for a council's asset manager who isn't an engineer."
2. **Context**: paste or attach the source material (the findings, the data, the scope). Without it the model fills gaps with generic or invented content.
3. **Constraints**: length, tone, standards to follow, what to avoid ("Australian English, no marketing language, don't recommend specific products, stay under 300 words").
4. **Examples**: show a sample of the style or structure you want. One good example is often worth a paragraph of instructions.
5. **Output format**: headings, a table with named columns, dot points, a compliance matrix, JSON for a script.

## Techniques that help

- **Be specific about the task**, not just the topic. "Review this specification for missing items compared with WSA 03 headings, and list each gap with the clause you'd expect" beats "check this spec".
- **Ask for reasoning or assumptions** on analytical tasks: "List the assumptions you've made." It exposes misunderstandings early.
- **Break big jobs into steps**: outline first, agree it, then draft each section. You stay in control and catch errors sooner.
- **Ask it to ask you**: "Before you start, ask me up to five questions about anything unclear."
- **Ground it**: "Answer only from the attached report. Quote the section for each point. If the report doesn't say, write 'not stated'."
- **Iterate**: treat the first answer as a draft. Say what's wrong ("too long, section 3 misses the cost implications") rather than starting over.
- **Ask for critique**: "Act as a sceptical client reviewer. What are the five weakest points in this proposal?"

## Reusable prompts

Good prompts are assets. Save the ones that work in a **prompt library** for your team: proposal methodology drafts, meeting minutes, RFI responses, report review checklists. Many tools support saved instructions, custom assistants or "projects" that keep context and files for a whole job.

## Long documents

- Tell the model what to focus on ("sections 4 to 6, the hydraulic modelling").
- Ask for page or section references so you can check.
- For huge sets of documents, a retrieval-based tool (covered later) is better than pasting everything.

## Common mistakes

- **Vague asks** ("make this better") give vague results.
- **No context**, then blaming the model for generic output.
- **Leading questions** that invite it to agree with you.
- **One giant prompt** for a complex deliverable instead of stages.
- **Trusting the first answer** without review.

## A worked example

> *You are helping a senior civil engineer at a consultancy. Using the attached site notes and survey summary, draft the "Existing conditions" section of a design report for a DN300 sewer upgrade for the water corporation. Audience: the corporation's project manager. Australian English, formal but plain, 400-500 words, headings for Site, Existing assets, Constraints, Gaps in information. Only use facts in the attachments; mark anything uncertain with [CHECK]. Then list three questions I should resolve before finalising.*

That prompt has role, goal, context, constraints, format, grounding and a built-in review step.""",
    "key_points": [
        "Five ingredients: role and goal, context, constraints, examples and output format.",
        "Be specific, ground it in sources, ask for assumptions and references, and work in steps.",
        "Iterate on drafts and ask for critique rather than accepting the first answer.",
        "Save prompts that work in a team prompt library or reusable assistant.",
    ],
    "figure_svg": PROMPT,
    "figure_caption": "A good prompt stacks role and goal, context, constraints, examples and output format, then you iterate.",
    "questions": [
        mcq("Why does adding context (the actual source documents) improve AI output so much?", ["It makes the prompt longer", "Without it the model fills gaps with generic or invented content", "It changes the model's training", "It's required by law"], 1,
            "Grounding beats guessing."),
        mcq("In the diagram, which layer covers 'Australian English, under 300 words, no product recommendations'?", ["Role + goal", "Context", "Constraints", "Examples"], 2,
            "Constraints set limits on tone, length and content.",
            PROMPT, "Five stacked boxes: role and goal, context, constraints, examples, output format; then iterate."),
        mcq("Which prompt is best for reviewing a specification?", ["Check this spec", "Make the spec better", "List gaps in this spec compared with WSA 03 headings, with the clause you'd expect for each", "Is this spec OK?"], 2,
            "Specific task, reference and output."),
        mcq("What's the main benefit of asking the model to list its assumptions?", ["It's polite", "It exposes misunderstandings early", "It makes output shorter", "It stops hallucination completely"], 1,
            "You can correct wrong assumptions before they spread."),
        mcq("For a complex 40-page report, what approach works best?", ["One giant prompt for the whole report", "Stages: agree an outline, then draft and review each section", "Ask for it in one line", "Avoid AI entirely"], 1,
            "Stages keep you in control."),
        mcq("What's a prompt library?", ["A list of AI vendors", "A shared collection of prompts that work well for common tasks", "A book about AI", "A database of model weights"], 1,
            "Good prompts are team assets."),
        mcq("In the diagram, what happens after the first output?", ["Send it to the client", "Iterate: review, correct and ask again", "Delete the prompt", "Change models"], 1,
            "First answers are drafts.", PROMPT, "The note 'then iterate: review, correct, ask again' under the five prompt layers."),
        open_q("Rewrite 'write a proposal for this job' into a strong prompt (outline the parts).", "State the role and goal, such as drafting the methodology section of a proposal for a named client and scope; attach the RFT and relevant past proposals as context; set constraints like length, tone, compliance with the RFT criteria and no unverified claims; give an example of a strong past methodology; specify the output format such as headings matching the evaluation criteria; and ask it to flag gaps or questions.",
               ["role and goal", "attach RFT and context", "constraints and format", "ask it to flag gaps"], "Map output to the evaluation criteria."),
        open_q("How would you prompt an AI so its answer about a report can be checked?", "Tell it to answer only from the attached report, quote or cite the section or page for each point, and say 'not stated' where the report doesn't cover something, so you can verify each claim against the source.",
               ["answer only from the source", "cite section or page", "say when not stated"], "Grounding plus citations."),
        open_q("Why ask an AI to critique your own draft as a sceptical reviewer?", "It surfaces weak arguments, gaps, unclear wording and risks you might not see yourself, giving you a quick second perspective before a real client or reviewer finds them.",
               ["finds weaknesses and gaps", "second perspective", "before the client does"], "Use it to strengthen, then decide yourself."),
    ],
}

L2 = {
    "title": "Checking AI output",
    "minutes": 10,
    "photo_query": "",
    "body": """The fastest way to lose credibility with AI is to pass on something it got wrong. The fastest way to gain it is to be the person who uses AI heavily **and** never gets caught out. That comes from systematic checking.

## What goes wrong most often

- **Invented references**: papers, standards clauses, case studies and URLs that don't exist or don't say what's claimed. Australian Standards and WSA codes are often paywalled, so models have seen less of their exact text.
- **Plausible numbers**: design values, coefficients, peak factors or costs that look right but aren't from a real source or don't suit the context.
- **Unit and arithmetic slips**: kPa vs m head, L/s vs m³/s, misplaced decimals.
- **Outdated information**: superseded standard editions, old regulations, retired products.
- **Misread inputs**: wrong values pulled from a scanned table or drawing.
- **Generic content**: text that sounds right but isn't specific to the site, client or brief.
- **Overstated certainty** and missing caveats.

## A checking routine

1. **Trace every fact to a source.** If you can't find the source, treat it as unverified. Ask the model where each claim came from, and then check that source yourself.
2. **Re-do or independently check calculations**, preferably with your normal tools (spreadsheet, design software) or by having the AI write code you can inspect and run.
3. **Sense-check magnitudes**: does a 26 kW pump for 50 L/s at 40 m make sense? Engineering judgement is the best hallucination detector.
4. **Check against the brief**: does it answer the actual question, for this client, site and scope?
5. **Look for what's missing**: risks, exclusions, assumptions, constraints.
6. **Read it as the recipient**: would the client or reviewer trust it?

## Scale effort to consequence

- **Low**: internal email, brainstorm, first outline. Skim and fix.
- **Medium**: report text, proposal content, client correspondence. Read fully, verify facts, own every sentence.
- **High**: design calculations, compliance statements, safety advice, anything relied on for decisions. Independent check by a competent engineer, documented like any other verification.

## Professional responsibility

Engineering codes of ethics (such as Engineers Australia's) require you to practise competently and honestly. Signing work means you've satisfied yourself it's correct, regardless of the tools used. Courts and tribunals in several countries have already sanctioned professionals for submitting AI-fabricated references. Keep simple records for important work: what AI was used for and how outputs were checked.

## Make checking easier

- Ask for **citations and quotes** from provided documents.
- Ask the model to **mark uncertainty** ([CHECK] tags).
- Use tools that **show sources** side by side.
- Get the AI to **check itself in a fresh conversation**: "Here's a draft and the source; list any statement not supported by the source." Useful, but not a substitute for your review.
- Prefer AI writing **code or formulas** you can inspect over AI doing calculations invisibly.

## Teach the habit

When reviewing juniors' work, ask how AI was used and how they checked it. Make "where did this come from?" a normal question. That's how a firm builds safe AI use rather than hidden AI use.

> **Rule of thumb:** if you couldn't defend a sentence in a review meeting without saying "the AI said so", it isn't ready.""",
    "key_points": [
        "Common failures: invented references, plausible but wrong numbers, unit slips, outdated info, misread inputs, generic content.",
        "Routine: trace facts to sources, independently check calcs, sense-check magnitudes, check against the brief, look for gaps.",
        "Scale checking effort to the consequence; design calcs need an independent check.",
        "You remain professionally responsible; keep records and make checking a team habit.",
    ],
    "figure_svg": VERIFY,
    "figure_caption": "AI drafts, a person checks facts, numbers, references and logic, and an engineer signs; checking effort rises with consequence.",
    "questions": [
        mcq("Why are AI-quoted clauses from Australian Standards especially risky?", ["Standards are free online", "Their exact text is often paywalled, so models have seen less of it and may fabricate", "Models can't read numbers", "Standards never change"], 1,
            "Check against the actual standard."),
        mcq("What's the best first step when AI gives you a design value?", ["Use it", "Trace it to a real source and check it suits the context", "Ask a different AI", "Round it"], 1,
            "Unverified values aren't design inputs."),
        mcq("In the diagram, which item needs an independent check?", ["Email tone", "Report text", "Design calc", "All need none"], 2,
            "High consequence needs independent verification.",
            VERIFY, "AI draft to check (facts, numbers, references, logic) to engineer signs; below, email tone skim, report text read fully, design calc independent check."),
        mcq("What's a good way to make AI calculations checkable?", ["Ask it to do maths in its head", "Have it write code or spreadsheet formulas you can inspect and run", "Ask it to be careful", "Use higher temperature"], 1,
            "Visible working beats invisible arithmetic."),
        mcq("Who is responsible for an AI-assisted report you sign?", ["The AI provider", "You", "The client", "Your manager only"], 1,
            "Signing means you've satisfied yourself it's correct."),
        mcq("An AI says a 50 L/s pump at 40 m needs 260 kW. What catches this fastest?", ["Asking the AI again", "Engineering judgement on magnitude (about 26 kW is expected)", "Changing the font", "Nothing"], 1,
            "Sense-check magnitudes."),
        mcq("In the diagram, how should you treat AI-drafted report text?", ["Skim it", "Read it fully and verify the facts", "Send it unchanged", "Ignore it"], 1,
            "Medium consequence: own every sentence.", VERIFY, "Report text box labelled read fully."),
        open_q("Describe a checking routine for an AI-drafted section of a design report.", "Trace each fact and value to a real source, independently check any calculations with normal tools, sense-check magnitudes with engineering judgement, confirm it answers the brief for this site and client, look for missing risks or assumptions, and read it as the recipient would.",
               ["trace facts to sources", "check calculations independently", "sense-check magnitudes", "check against the brief and look for gaps"], "Then you can sign it."),
        open_q("Why keep records of how AI was used on important work?", "So you can show how outputs were produced and verified if questioned by a reviewer, client, insurer or in a dispute, demonstrating competent practice; it also helps the firm learn what works and where errors occur.",
               ["show how work was produced and checked", "defensible if questioned", "learn and improve"], "Simple notes are enough."),
        open_q("How can a senior engineer encourage safe rather than hidden AI use in their team?", "Make it normal to say AI was used and to ask how outputs were checked, set clear expectations for verification, share examples of AI errors caught, and review the checking as well as the result, so people don't hide AI use or skip checks.",
               ["normalise disclosure", "ask how it was checked", "share errors caught"], "Culture matters as much as policy."),
    ],
}

L3 = {
    "title": "AI across consulting work",
    "minutes": 10,
    "photo_query": "engineers meeting office laptop",
    "body": """Knowing *where* AI adds value in a consultancy, and where it doesn't, is the most useful practical knowledge you can share with colleagues.

## Bids and proposals

- Summarise a long RFT and extract the **evaluation criteria**, mandatory requirements and dates into a table.
- Build a **compliance matrix** against the requirements.
- Draft methodology and approach sections from your notes and past winning bids.
- Tailor CVs and project experience to the criteria.
- Critique a draft as an evaluator would.

*Watch:* confidentiality of the client's RFT, and making sure claims about experience are true.

## Reports and documents

- Turn notes, site observations and data into structured drafts.
- Write executive summaries for non-technical audiences.
- Check consistency (terminology, numbering, units) across a long document.
- Convert between formats: findings to a table, a table to prose.

## Specifications and design reviews

- Compare a specification against a checklist or standard headings to find gaps.
- Generate review checklists for a discipline (sewer design, pump stations, drainage).
- Summarise RFIs and design changes, and draft responses for engineer review.

*Watch:* the model's knowledge of current standards may be incomplete; give it the documents.

## Meetings and communication

- Transcribe and produce minutes and action lists (with participants' agreement).
- Draft client emails, especially difficult ones, in a calm, clear tone.
- Prepare briefing notes before a meeting from the project file.

## Scripts, data and automation

Often the biggest time saver for engineers:

- **Python** for data cleaning, plots, batch processing of model results, or reading SCADA exports.
- **Excel** formulas, Power Query and VBA.
- Scripting for design software: **Civil 3D** (.NET, Dynamo), QGIS (PyQGIS), and similar.
- Quantity take-offs and checks from exported data.

You don't need to be a programmer, but you do need to test what it writes on known cases.

## Learning and problem solving

- Explain an unfamiliar concept, standard approach or software feature at your level.
- Generate practice problems or a study plan (as this app does).
- Rubber-duck a design problem: talk through options and trade-offs.

## Where AI shouldn't lead

- **Engineering judgement** on design decisions, risk acceptance and safety.
- **Sign-off** of anything relied on.
- **Client relationships**: trust is personal.
- **Site safety calls** and anything needing physical inspection.
- **Commercial and legal advice** without proper review.

## Getting value, not just novelty

Start with tasks that are **frequent**, **text-heavy** and **easy to check**: minutes, first drafts, summaries, scripts. Measure the time saved. Expand to higher-value work once your team has habits for prompting and checking.

> **Mindset:** AI drafts and accelerates; engineers decide and stand behind the work.""",
    "key_points": [
        "Bids: extract criteria, compliance matrices, tailored drafts and evaluator-style critique.",
        "Reports, specs and reviews: structured drafts, summaries, gap checks and checklists, grounded in real documents.",
        "Scripts and data (Python, Excel, Civil 3D/Dynamo) are often the biggest time saver; test on known cases.",
        "Keep judgement, sign-off, relationships and safety calls human; start with frequent, text-heavy, easy-to-check tasks.",
    ],
    "figure_svg": TASKS,
    "figure_caption": "AI helps across bids, reports, reviews, meetings, scripts and learning; judgement and sign-off stay human.",
    "questions": [
        mcq("Which proposal task is a strong fit for AI?", ["Deciding the bid price", "Extracting evaluation criteria and mandatory requirements from a long RFT into a table", "Signing the tender", "Inventing project experience"], 1,
            "Extraction and structuring are strengths."),
        mcq("In the diagram, which item stays human?", ["Meeting minutes", "Scripts and data", "Sign-off and site safety calls", "Report summaries"], 2,
            "Judgement and accountability stay with people.",
            TASKS, "Six boxes of AI-assisted work (bids, reports, specs, meetings, scripts, learning) above a red box: keep human judgement, sign-off, client relationships and site safety calls."),
        mcq("Why is scripting often the biggest time saver for engineers?", ["Engineers love code", "AI can write Python, Excel and design-software scripts that automate repetitive work, even for occasional coders", "Scripts never need testing", "It replaces design software"], 1,
            "Test on known cases."),
        mcq("Before using AI to minute a client meeting, what should you do?", ["Nothing", "Get participants' agreement to recording and transcription", "Hide the recorder", "Ask the AI for permission"], 1,
            "Consent and confidentiality matter."),
        mcq("What's the best way to have AI check a specification against a standard?", ["Rely on the model's memory of the standard", "Provide the relevant standard or checklist and ask for gaps with references", "Ask if it's OK", "Skip it"], 1,
            "Ground it in the actual document."),
        mcq("Which tasks are best to start with when introducing AI to a team?", ["Rare, high-risk design decisions", "Frequent, text-heavy, easy-to-check tasks", "Legal advice", "Client negotiations"], 1,
            "Build habits on low-risk, high-frequency work."),
        mcq("In the diagram, which category includes Dynamo and Python?", ["Bids", "Meetings", "Scripts & data", "Learning"], 2,
            "Automation of design and data tasks.", TASKS, "Scripts and data box listing Python, Excel and Dynamo."),
        open_q("Give three examples of how AI could speed up writing a design report, and the check you'd apply to each.", "Turning site notes into a structured existing-conditions draft, checked against the notes and survey; writing an executive summary for a non-technical client, checked for accuracy and tone; and checking terminology, units and numbering consistency across the report, with flagged items confirmed manually.",
               ["structured drafts from notes", "executive summary", "consistency checks", "a check for each"], "Grounded drafts plus review."),
        open_q("Why must claims in an AI-drafted proposal be checked carefully?", "The model may invent or exaggerate experience, capabilities or project details to sound persuasive; false claims in a tender can mislead the client, breach procurement rules and damage the firm's reputation.",
               ["may invent or exaggerate", "misleading the client", "reputation and procurement risk"], "Every claim must be true and supportable."),
        open_q("How would you safely use AI to write a Python script that processes hydraulic model results?", "Describe the data format and the goal clearly, have the AI write the script and explain it, run it first on a small dataset where you know the correct answers, check outputs and edge cases, and keep the script under version control for reuse.",
               ["clear description of data and goal", "test on known cases", "check outputs and edge cases"], "Trust tested code, not untested code."),
    ],
}

L4 = {
    "title": "Working with company and client information",
    "minutes": 10,
    "photo_query": "",
    "body": """The most common AI mistake in professional firms isn't a bad answer; it's putting information into the wrong tool. Knowing the data rules is essential to leading safely.

## Know your tools

- **Consumer tools** (free or personal accounts): terms may allow the provider to retain conversations and use them to improve models, and your firm has no admin control.
- **Enterprise tools** (for example Microsoft 365 Copilot, ChatGPT Enterprise/Team, Claude for Work, Gemini for Workspace, under the firm's agreement): usually **no training on your data**, admin controls, retention settings, security certifications and stated data location. Check your firm's agreements; terms differ between products and change over time.
- **Embedded AI** in software you already use (document management, design tools, PDF editors): check what's sent where.

## Classify before you paste

A simple scheme:

- **Public**: published standards summaries, papers, your public website. Any approved tool.
- **Internal**: firm templates, processes, non-sensitive project information. Enterprise tools only.
- **Confidential**: client data, commercially sensitive information, personal information, security-sensitive infrastructure details (for example critical asset locations or vulnerabilities). Only where the **contract and firm policy allow**, in approved tools, and often anonymised.

Water, energy and transport clients may treat infrastructure details as security-sensitive; government clients often have specific AI and data rules. Read the contract.

## Personal information

Under the *Privacy Act 1988*, personal information (names, contact details, health information, customer records) must be handled consistent with why it was collected and kept secure. Before using it with AI: do you need it at all? Can you remove or anonymise it? Is the tool approved for personal information?

## Retrieval over your own documents

Enterprise assistants and RAG tools let you ask questions across project files, past reports, standards libraries and lessons learned. To make them useful:

- **Fix permissions first**: assistants show users whatever they already have access to. Overshared folders become visible with a simple question.
- **Curate sources**: current, approved documents give better answers than a pile of drafts and superseded versions.
- **Prefer tools that cite** the document and page so people can check.
- **Mind the boundary between clients**: don't let information from one client's project leak into another's deliverable.

## Copyright and IP

- Standards documents are licensed; check your licence before uploading them into AI tools or shared indexes.
- AI-generated content's IP position is unsettled; contracts may assign ownership of deliverables to clients, and some clients require disclosure of AI use.
- Don't paste third-party copyrighted material wholesale into public tools.

## Practical rules for everyone

1. Use only **approved tools** for work.
2. **Classify** information before entering it.
3. **Anonymise** where you can (Client A, Site 1).
4. Don't enter **passwords, keys or security details**, ever.
5. Check **contract conditions** for AI and data clauses.
6. When unsure, **ask** (your AI lead, IT or legal).

> **Leadership tip:** make the safe path the easy path. If the approved enterprise tool is good and easy to access, people stop using personal accounts.""",
    "key_points": [
        "Consumer tools may retain and train on data; enterprise tools usually don't and add admin, security and location controls.",
        "Classify information as public, internal or confidential before entering it; read client contracts.",
        "Handle personal information under the Privacy Act; anonymise where possible.",
        "Enterprise assistants expose whatever users can access: fix permissions, curate sources and keep client boundaries.",
    ],
    "figure_svg": DATA,
    "figure_caption": "Classify information before entering it: public anywhere approved, internal in enterprise tools, confidential only where contract and policy allow.",
    "questions": [
        mcq("What's the main data risk of using a personal free AI account for client work?", ["It's slower", "Terms may allow retention and training on your data, with no firm control", "It can't read PDFs", "None"], 1,
            "Use the firm's approved enterprise tools."),
        mcq("In the diagram, where can confidential client data go?", ["Any tool", "Only where contract and policy allow, in approved tools", "Public chatbots", "Nowhere ever"], 1,
            "Check both the contract and the firm's policy.",
            DATA, "Three boxes: public (any approved tool), internal (enterprise tools), confidential (only if contract and policy allow); enterprise tool features below."),
        mcq("Before rolling out an enterprise assistant across SharePoint, what should be fixed first?", ["Font sizes", "File and folder permissions", "Email signatures", "Desktop backgrounds"], 1,
            "The assistant surfaces whatever users can access."),
        mcq("Which is the safest way to get AI help on a sensitive client issue?", ["Paste everything into any tool", "Use an approved tool and anonymise details where possible", "Use a personal account at home", "Post it on a forum"], 1,
            "Minimise and anonymise."),
        mcq("Why might a water utility treat some asset information as sensitive?", ["It's boring", "Details of critical infrastructure and vulnerabilities can be security-sensitive", "It's copyrighted", "It's too large"], 1,
            "Critical infrastructure has security obligations."),
        mcq("What should you never enter into an AI tool?", ["Public standards summaries", "Passwords, keys or security credentials", "Your own draft text", "Generic questions"], 1,
            "Never share secrets."),
        mcq("In the diagram, what typically makes enterprise tools safer?", ["Bigger models", "No training on your data, access controls and data location", "Lower price", "Faster responses"], 1,
            "Contract and admin controls matter.", DATA, "Box describing enterprise tool features: no training on your data, access controls, data location."),
        open_q("List practical data rules every staff member should follow when using AI.", "Use only approved tools; classify information before entering it; anonymise where possible; never enter passwords, keys or security details; check contract conditions for AI and data clauses; and ask the AI lead, IT or legal when unsure.",
               ["approved tools only", "classify and anonymise", "no secrets", "check contracts and ask when unsure"], "Short, memorable rules work best."),
        open_q("Why does 'make the safe path the easy path' matter for AI governance?", "If the approved tool is hard to access or poor, people quietly use personal accounts, creating hidden data risk; making the approved option good and convenient reduces shadow AI more effectively than prohibitions.",
               ["poor approved tools drive shadow use", "convenient safe option", "better than bans"], "Shadow AI is a real risk."),
        open_q("How could client information leak between projects with a company-wide AI knowledge tool, and how would you prevent it?", "If the tool indexes all projects and users can access them, answers or drafts for one client could include another client's confidential details; prevent it with project-level permissions, separate indexes or workspaces per client, citing sources, and reviewing outputs before they go out.",
               ["shared index mixes client data", "project-level permissions or separate workspaces", "review outputs"], "Keep client boundaries."),
    ],
}

L5 = {
    "title": "Automation and agents in practice",
    "minutes": 10,
    "photo_query": "",
    "body": """Once people are comfortable with chat, the next step is automation: AI doing multi-step work with less hand-holding. Knowing when to automate, and how much autonomy to give, is a key leadership skill.

## Levels of automation

1. **Chat assistance**: a person drives every step; AI helps. Lowest risk.
2. **Workflows**: fixed steps with AI inside some of them, for example "for each incoming invoice: extract fields → validate against the PO → file it → flag exceptions". Predictable and testable. Built with tools such as Power Automate, Zapier, scripts or the AI features of your document system.
3. **Agents**: the AI plans its own steps and uses tools (search, files, code, email) to reach a goal, for example "research recent pump station odour complaints in this region and summarise the causes". Flexible but less predictable.
4. **Full autonomy**: no human in the loop. Rarely appropriate for professional work with real consequences.

Choose the **lowest level that does the job**. Most business value today comes from levels 1 and 2.

## Good candidates for automation

- High volume, repetitive and rule-like: document classification, data extraction from forms, timesheet or invoice processing, RFI logging.
- Clear inputs and outputs.
- Errors are easy to detect or cheap to fix.
- Someone can review exceptions.

Poor candidates: rare, judgement-heavy tasks; anything where a mistake is costly and hard to spot.

## Agents for engineers

- **Coding agents** (for example Claude Code, GitHub Copilot agent modes, Cursor) can build and modify scripts and small tools, run them and fix errors, within a project folder. Great for automating design calculations, data processing and reports, under review.
- **Research agents** gather and summarise sources; check the citations.
- **Office agents** act across email, calendars and documents; give the least access needed.

## Controls

- **Human-in-the-loop** at checkpoints, and always before **irreversible or external actions**: sending to clients, deleting, paying, publishing, changing design files of record.
- **Least privilege**: only the folders, mailboxes and systems needed.
- **Logs** of what the automation did.
- **Testing** on representative cases before going live; re-test after changes.
- **Prompt injection awareness**: any document, email or web page the agent reads can contain hostile instructions. Don't let agents that read untrusted content also take high-impact actions without approval.
- **Ownership**: a named person is accountable for each automation.
- **Fallback**: what happens when it fails? There must be a manual path.

## Build versus buy

Many capabilities now come built into tools you already licence (document management, CRM, design software, Microsoft 365). Before building, check what's available. Build when the workflow is specific to your firm and valuable enough to maintain.

## Costs

AI usage is often priced per **token** or per user. Agents use many more tokens than chat because they loop. Track costs during pilots so business cases are realistic.

> **Rule:** automate the boring, keep humans on the consequential, and put a checkpoint before anything you can't undo.""",
    "key_points": [
        "Levels: chat, fixed workflows, agents and full autonomy; choose the lowest level that works.",
        "Automate high-volume, rule-like tasks with clear inputs and easy-to-detect errors.",
        "Control with checkpoints before irreversible actions, least privilege, logs, testing, injection awareness and named owners.",
        "Check built-in features before building; agents use more tokens, so track costs.",
    ],
    "figure_svg": AUTOMATE,
    "figure_caption": "From chat to workflows, agents and full autonomy; add a human checkpoint before anything irreversible.",
    "questions": [
        mcq("What's the difference between a workflow and an agent?", ["No difference", "A workflow follows fixed steps; an agent plans its own steps and tool use", "Agents are always cheaper", "Workflows can't use AI"], 1,
            "Workflows are more predictable."),
        mcq("In the diagram, which level has the most risk for professional work?", ["Chat", "Flow", "Agent", "Auto (no human)"], 3,
            "No human in the loop.",
            AUTOMATE, "Four circles along an autonomy axis: chat (you drive), flow (fixed steps), agent (plans and tools), auto (no human); note to add a human checkpoint before anything irreversible."),
        mcq("Which task is the best candidate for automation?", ["Deciding whether to accept a design risk", "Extracting fields from hundreds of standard forms with exceptions reviewed", "Negotiating a variation", "Signing off a report"], 1,
            "High volume, rule-like, reviewable."),
        mcq("Where must a human checkpoint go?", ["After every token", "Before irreversible or external actions such as sending to clients", "Nowhere", "Only at the start"], 1,
            "Check before you can't undo."),
        mcq("Why should an agent that reads incoming emails not send payments without approval?", ["Emails are boring", "Emails can contain prompt injection that hijacks the agent", "Agents can't do maths", "It's slower"], 1,
            "Untrusted input plus high-impact action is dangerous."),
        mcq("Why do agents often cost more to run than chat?", ["They use bigger screens", "They loop through many steps, using many more tokens", "They need licences per step", "They don't"], 1,
            "Track token use in pilots."),
        mcq("In the diagram, where would 'extract invoice data, validate, file, flag exceptions' sit?", ["Chat", "Flow (fixed steps)", "Agent", "Auto"], 1,
            "Fixed, known steps.", AUTOMATE, "Flow circle labelled fixed steps."),
        open_q("What controls would you require before letting a coding agent automate a design calculation workflow?", "Limit it to a project folder, keep code under version control, review and test the code on known cases, log runs, require an engineer to check outputs before use, name an owner, and keep a manual fallback.",
               ["restricted access", "test on known cases", "engineer checks outputs", "owner and fallback"], "Treat it like any calculation tool."),
        open_q("Why choose the lowest level of automation that does the job?", "Lower levels are more predictable, easier to test and govern, and keep people in control, with less risk of compounding errors; more autonomy adds flexibility but also risk and cost that should be justified by the task.",
               ["more predictable and testable", "less risk", "autonomy must be justified"], "Most value is in chat and workflows today."),
        open_q("How would you decide whether to build an AI automation or use a built-in feature?", "First check whether tools you already licence offer the capability; build only when the workflow is specific to the firm, valuable enough, and someone can maintain and own it, considering cost, security and support.",
               ["check existing tools first", "build when specific and valuable", "maintenance and ownership"], "Buy before build, usually."),
    ],
}

L6 = {
    "title": "AI governance in a consultancy",
    "minutes": 10,
    "photo_query": "",
    "body": """Governance sounds bureaucratic, but done well it's what lets a firm use AI confidently. As an AI leader you may help shape it, and you should certainly be able to explain it.

## Why it matters for consultancies

- **Professional liability**: advice and designs are relied on. Errors from unchecked AI use are still the firm's errors; professional indemnity insurers are asking about AI practices.
- **Client trust and contracts**: clients, especially government and utilities, increasingly set AI conditions in contracts and tenders and ask about your AI policy.
- **Confidentiality and privacy**: the information you hold belongs to clients and individuals.
- **Competitive edge**: firms that use AI well, and can show they do it responsibly, win work.

## Core elements (keep them proportionate)

1. **AI policy**: short and practical. Approved tools, data rules, review and sign-off requirements, disclosure, prohibited uses, who to ask.
2. **Approved tools list** with what each may be used for and what data may go in.
3. **Use-case register**: significant AI uses (especially automations and client-facing ones), with an owner, a risk rating, controls and evaluation results.
4. **Risk-based review**: low-risk uses (drafting internal emails) need nothing extra; higher-risk uses (AI in design checks, client-facing tools, processing personal information) need assessment, testing and approval.
5. **Training** for all staff, with more depth for heavy users and reviewers.
6. **Review and sign-off rules** for AI-assisted deliverables, folded into the existing quality management system rather than a separate process.
7. **Incident and lessons reporting**: errors and near misses caught, shared without blame.
8. **Vendor due diligence**: data use, security, location, retention, certifications.

## Frameworks to borrow from

- Australia's **AI Ethics Principles** and the government's **guidance on AI adoption** (essential practices such as clear accountability, understanding impacts, risk management, testing and monitoring, transparency and human control).
- **ISO/IEC 42001** for an AI management system; integrates with ISO 9001 (quality) and ISO 27001 (information security) that many consultancies already hold.
- The **NIST AI RMF** functions: Govern, Map, Measure, Manage.

## Disclosure to clients

There's no single rule yet. Good practice: follow contract requirements; be open where AI materially contributed to deliverables or where clients ask; never misrepresent AI output as something it isn't (such as a site inspection). Many firms add a short statement on AI use to proposals and their quality documentation.

## Common governance mistakes

- **Banning AI**: drives use underground into personal accounts.
- **A 30-page policy nobody reads**.
- **No owner**: nobody keeps the tool list or register up to date.
- **Treating all uses the same**: heavy process for trivial uses, too little for risky ones.
- **Set and forget**: tools, terms and laws change every few months.

## The AI lead's role

You don't need to own governance to help it: be the person who knows the policy, explains it simply, flags new risks and opportunities, brings real use cases to the people who approve them, and shares lessons learned.

> **Principle:** governance should make good AI use easy and risky AI use visible.""",
    "key_points": [
        "Consultancies face liability, contract, confidentiality and competitive pressures on AI use.",
        "Core elements: short policy, approved tools, use-case register, risk-based review, training, sign-off in the QMS, incidents and vendor checks.",
        "Borrow from Australia's AI principles and adoption guidance, ISO/IEC 42001 and the NIST AI RMF.",
        "Avoid bans, unread policies, ownerless registers, one-size-fits-all rules and set-and-forget.",
    ],
    "figure_svg": GOV,
    "figure_caption": "A short policy drives approved tools, a risk-rated use-case register and training, with sign-off rules and incident learning.",
    "questions": [
        mcq("Why is banning AI usually a poor governance choice?", ["It's illegal", "It drives use into personal accounts where the firm has no control", "AI can't be banned technically", "It's expensive"], 1,
            "Shadow AI is riskier than managed AI."),
        mcq("In the diagram, what does the use-case register record?", ["Staff birthdays", "Significant AI uses with owners, risk ratings and controls", "Tool prices", "Model weights"], 1,
            "It makes risky use visible.",
            GOV, "AI policy at the top leading to approved tools with data rules, a risk-rated use-case register and training; below, review and sign-off rules and incidents and lessons."),
        mcq("Which standard provides a certifiable AI management system?", ["ISO 9001", "ISO/IEC 42001", "AS 2200", "ISO 14001"], 1,
            "It integrates with quality and security systems."),
        mcq("How should review of AI-assisted deliverables be handled?", ["A separate new process for every document", "Folded into the existing quality management system", "Not needed", "Only by IT"], 1,
            "Use the QMS you already have."),
        mcq("What does risk-based review mean?", ["Every AI use needs board approval", "Controls scale with the risk of the use", "Only high-risk uses are allowed", "No review"], 1,
            "Proportionate governance."),
        mcq("Why do PI insurers care about AI practices?", ["They sell AI", "Unchecked AI errors in relied-on advice create liability claims", "They don't", "For marketing"], 1,
            "Professional liability still applies."),
        mcq("In the diagram, what's the purpose of 'incidents & lessons'?", ["Punish staff", "Capture and share AI errors and near misses so the firm learns", "Track tool costs", "Record client complaints only"], 1,
            "Blame-free learning.", GOV, "Box labelled incidents and lessons."),
        open_q("Outline a proportionate AI governance setup for a mid-sized engineering consultancy.", "A short AI policy; an approved tools list with data rules; a register of significant use cases with owners and risk ratings; risk-based review so higher-risk uses get testing and approval; training for all staff; AI review and sign-off folded into the QMS; blame-free incident reporting; and vendor due diligence, reviewed regularly.",
               ["short policy and approved tools", "use-case register with risk rating", "training", "QMS sign-off and incident reporting"], "Proportionate and kept current."),
        open_q("What's good practice on disclosing AI use to clients?", "Follow contract requirements; be open where AI materially contributed to deliverables or when clients ask; never misrepresent AI output, for example as human inspection or analysis; and consider a short AI use statement in proposals and quality documents.",
               ["follow the contract", "be open when material or asked", "never misrepresent"], "Honesty builds trust."),
        open_q("How can you act as an AI leader without owning the firm's governance?", "Know the policy and explain it simply, help colleagues use approved tools well, bring real use cases forward for approval, flag new risks and opportunities, and share lessons learned and good examples.",
               ["explain the policy", "support colleagues", "bring use cases forward", "share lessons"], "Influence beats authority."),
    ],
}

L7 = {
    "title": "Choosing use cases and proving value",
    "minutes": 10,
    "photo_query": "",
    "body": """Enthusiasm gets AI started; evidence keeps it going. Leaders pick the right problems and show measurable results.

## Find the opportunities

Ask people where time goes. Good sources:

- Tasks people dread or repeat weekly (minutes, reporting, data cleaning, document formatting).
- Bottlenecks (proposal deadlines, review queues, RFI turnaround).
- Knowledge problems ("we've done this before but nobody can find it").
- Quality issues (inconsistent reports, missed requirements).

## Prioritise: value × feasibility

Score each idea:

- **Value**: hours saved × frequency × people, quality improvement, risk reduction, revenue (winning bids).
- **Feasibility**: data available and allowed, tool exists, error risk manageable, effort to implement, change needed.

Plot them. **Quick wins** (high value, high feasibility) go first: they build momentum and credibility. **Big bets** (high value, harder) need a business case and a pilot. Low value, low feasibility ideas are dropped, however exciting.

## Run a pilot properly

1. **Define the problem and success measures** up front: "cut time to produce draft minutes from 60 to 15 minutes with no loss of accuracy."
2. **Measure the baseline**: how long and how good is the current process?
3. **Small group, real work, fixed period** (for example 6 weeks, 5-10 people).
4. **Measure**: time, quality (error rates, reviewer ratings), adoption, user feedback, cost (licences, tokens, set-up time).
5. **Decide**: scale, adjust or stop. Stopping a pilot that didn't work is a success of the process.

## Measure honestly

- Count **review and correction time**, not just generation time. A draft in 30 seconds that needs 40 minutes of fixing may not beat writing it yourself.
- Look at **quality**, not just speed: fewer missed requirements, more consistent reports.
- Watch for **uneven benefits**: AI often helps less experienced staff most on some tasks and experts most on others.
- Note **risks reduced or added**.

## Build the business case

- Annualised hours saved × charge-out or cost rate, minus licence, usage and support costs.
- Non-financial benefits: speed to client, bid win rate, staff satisfaction, capability.
- Risks and controls.
- Example: 40 engineers each saving 2 hours a week on drafting and minutes at an internal cost of $120 per hour is roughly 40 × 2 × 46 weeks × $120 ≈ **$440 000 a year**, before costs. Real savings are often lower than surveys suggest, so use measured pilot data.

## Scale thoughtfully

- Package what works: prompts, templates, guides, short training.
- Name **champions** in each team.
- Keep measuring after rollout.
- Revisit as tools improve: something infeasible six months ago may now be easy.

## Beware

- **Pilot purgatory**: endless pilots, nothing scaled. Set decision dates.
- **Solution looking for a problem**: start from pain points, not features.
- **Vanity metrics**: logins and prompt counts aren't value.

> **Leader's habit:** every AI initiative gets a baseline, a measure and a decision date.""",
    "key_points": [
        "Find opportunities in repetitive tasks, bottlenecks, knowledge gaps and quality issues.",
        "Prioritise by value × feasibility; start with quick wins, pilot big bets.",
        "Pilot with a baseline, success measures, real work and a decision date; count review time.",
        "Business cases use measured savings minus costs, plus quality and risk; avoid pilot purgatory and vanity metrics.",
    ],
    "figure_svg": PICK,
    "figure_caption": "Plot ideas by value and feasibility: A is a quick win, B a big bet, C to avoid, D nice to have.",
    "questions": [
        mcq("In the diagram, which idea should you start with?", ["A", "B", "C", "D"], 0,
            "High value, high feasibility: a quick win.",
            PICK, "Value versus feasibility matrix with quadrants big bets, quick wins, avoid, nice to have; A in quick wins, B in big bets, C in avoid, D in nice to have."),
        mcq("In the diagram, what does idea B need before proceeding?", ["Nothing", "A business case and a pilot", "Immediate full rollout", "To be dropped"], 1,
            "High value but harder to deliver.",
            PICK, "Idea B in the high value, low feasibility quadrant labelled big bets."),
        mcq("Why measure a baseline before a pilot?", ["For fun", "So you can show the real improvement against the current process", "It's required by AI vendors", "To slow things down"], 1,
            "No baseline, no evidence."),
        mcq("A tool produces drafts in 30 seconds but each needs 40 minutes of correction. What's missing from the analysis?", ["Nothing", "Review and correction time", "Token cost only", "User logins"], 1,
            "Count the whole process."),
        mcq("Which is a vanity metric?", ["Hours saved per report", "Number of logins", "Error rate", "Bid win rate"], 1,
            "Usage isn't value."),
        mcq("What is 'pilot purgatory'?", ["A failed AI model", "Endless pilots that never get scaled or stopped", "A training method", "A licence type"], 1,
            "Set decision dates."),
        mcq("40 engineers each save 2 hours a week for 46 weeks at $120/hour. Roughly what's the annual value before costs?", ["$44 000", "About $440 000", "$4.4 million", "$9 600"], 1,
            "40 × 2 × 46 × 120 ≈ $441 600."),
        open_q("Design a pilot for AI-generated meeting minutes in your team.", "Define success such as reducing minute preparation from about an hour to 15 minutes with equal accuracy; measure current time and quality; run it for a fixed period with a small group on real meetings with consent; track time including review, accuracy, adoption, feedback and cost; then decide to scale, adjust or stop.",
               ["success measure and baseline", "small group, real work, fixed period", "measure time including review and quality", "decision at the end"], "Every pilot gets a decision date."),
        open_q("Why can stopping a pilot be a success?", "It means the firm tested an idea with evidence and avoided spending more on something that doesn't deliver, freeing resources for better uses; good process, not every idea, is the goal.",
               ["evidence-based decision", "avoids wasted spending", "frees resources"], "Learning counts."),
        open_q("What would you include in a business case for rolling out an AI drafting tool across the firm?", "Measured time savings from the pilot annualised across users and valued at cost rates, minus licence, usage, training and support costs; quality and speed benefits; staff and client benefits; risks and controls; and a plan for rollout and ongoing measurement.",
               ["measured savings minus costs", "quality and other benefits", "risks and controls", "rollout and measurement plan"], "Use pilot data, not survey guesses."),
    ],
}

L8 = {
    "title": "Being the AI leader in your firm",
    "minutes": 10,
    "photo_query": "presentation workshop engineers",
    "body": """Being "one of the AI people" in a consultancy is less about knowing the latest model and more about **judgement, generosity and staying current**. This lesson pulls the course together into habits.

## What credible AI leaders do

- **Use it daily** on real work, so your advice comes from experience, not headlines.
- **Know the limits** and say so. Credibility comes from being the person who catches the AI's mistakes, not the one who oversells it.
- **Translate**: explain AI in plain language to directors, engineers and clients, linked to their problems.
- **Share**: prompts, workflows, wins and failures.
- **Connect** AI use to the firm's strategy: winning work, delivering better, developing people, managing risk.
- **Stay ethical**: protect clients' information, be honest about AI use, keep engineering judgement central.

## Spreading capability

- **Demos beat decks**: a 10-minute live demo on a real (anonymised) task persuades more than slides.
- **Lunch-and-learns and office hours**: low pressure, practical.
- **A prompt and workflow library** for common consulting tasks.
- **Champions** in each team or office, and a **community of practice** channel to swap tips and lessons.
- **Pair with sceptics**: they find the real failure modes, and when they're won over others follow.
- **Teach checking**, not just prompting.
- **Support graduates**: AI can accelerate their learning, but they must still build fundamentals. Encourage them to use AI to explain and quiz, not just to produce.

## Working with leadership

- Bring **evidence** (pilot results), not hype.
- Frame AI in **business terms**: margin, utilisation, bid success, risk, staff retention.
- Help leadership understand **risks and governance** without fear.
- Propose **small, concrete next steps** with owners and dates.

## Talking to clients

Clients increasingly want to know how you use AI and how you could help them use it. Be ready to explain:

- How AI makes your delivery faster or better.
- How you protect their information.
- How engineers remain accountable.
- Opportunities for them: asset data analysis, document search, reporting automation, customer communications. This is a growing advisory opportunity for engineering consultancies.

## Staying current without drowning

AI changes monthly. Build a light routine:

- Follow a few **reliable sources**: the official blogs and release notes of the main AI providers, reputable newsletters, and national bodies (such as Australia's National AI Centre and CSIRO's Data61).
- **Try new features** on a standard set of your own test tasks, so you can judge real improvements.
- Keep a **personal log** of what works (this app can turn new topics into courses).
- Join professional discussions (Engineers Australia technical societies, industry associations such as the water sector's).
- Revisit your assumptions every few months: things that didn't work may now work.

## A 90-day plan

- **Weeks 1-4**: use AI daily on your own work; build your prompt library; note time saved.
- **Weeks 5-8**: run a lunch-and-learn; start a community channel; pick one quick-win use case with your team and measure it.
- **Weeks 9-12**: present results and a next-steps proposal to leadership; help update the policy or guidance; plan the next pilot.

> **The long game:** tools will change; the leaders will be the people who combine engineering judgement, AI fluency and the ability to bring others with them.""",
    "key_points": [
        "Credible AI leaders use AI daily, know and state its limits, translate, share and stay ethical.",
        "Spread capability with demos, libraries, champions, communities of practice, sceptics and teaching checking.",
        "Bring evidence and business framing to leadership; be ready to explain AI use and opportunities to clients.",
        "Stay current with reliable sources, your own test tasks and a regular review; follow a 90-day plan.",
    ],
    "figure_svg": LEAD,
    "figure_caption": "You at the centre, spreading capability to your team, leaders, graduates and clients through demos, a prompt library and office hours.",
    "questions": [
        mcq("What most builds credibility as an AI leader?", ["Overselling AI", "Using it daily and knowing and stating its limits", "Knowing every model name", "Avoiding sceptics"], 1,
            "Experience plus honesty."),
        mcq("In the diagram, what keeps the community going?", ["A long policy", "Sharing wins and failures in a community of practice", "Banning tools", "Annual reports"], 1,
            "Shared learning spreads capability.",
            LEAD, "You in the centre connected to team, leads, graduates and clients; demos, prompt library and office hours above; community of practice below."),
        mcq("Why pair with sceptics?", ["To argue", "They find real failure modes, and their support persuades others", "To slow adoption", "They're always wrong"], 1,
            "Sceptics improve and validate your approach."),
        mcq("What's the best way to persuade a team to try AI?", ["A 40-slide deck", "A short live demo on a real, anonymised task", "An email", "A policy"], 1,
            "Demos beat decks."),
        mcq("How should graduates use AI?", ["To avoid learning fundamentals", "To accelerate learning, such as explanations and quizzes, while still building fundamentals", "Not at all", "Only for emails"], 1,
            "Learning tool, not a crutch."),
        mcq("Which is a good way to judge whether a new model is better?", ["Read the launch post", "Run it on your own standard set of test tasks", "Trust social media", "Check its parameter count"], 1,
            "Your tasks, your evidence."),
        mcq("In the diagram, which group might become an advisory opportunity?", ["Clients", "Your desk", "The printer", "None"], 0,
            "Helping clients use AI is a growing service.", LEAD, "Clients node connected to you in the capability diagram."),
        open_q("Outline a 90-day plan to establish yourself as an AI leader in your firm.", "First month: use AI daily on your own work, build a prompt library and track time saved. Second month: run a lunch-and-learn, start a community channel and run one measured quick-win use case with your team. Third month: present results and next steps to leadership, help improve the policy or guidance and plan the next pilot.",
               ["use it daily and build a library", "share through sessions and a community", "measured quick win", "present evidence to leadership"], "Evidence, then influence."),
        open_q("How would you explain your firm's AI use to a cautious water utility client?", "Explain that AI helps us draft, summarise and analyse faster, that client information only goes into approved enterprise tools under our policy and their contract terms, that engineers check and remain accountable for all deliverables, and offer to discuss how AI could help them with things like asset data or document search.",
               ["benefits to delivery", "information protection", "engineers accountable", "opportunities for them"], "Lead with trust."),
        open_q("Describe a light routine for staying current with AI.", "Follow a few reliable sources such as provider release notes, a good newsletter and national bodies; test new features on a standard set of your own tasks; keep a log of what works; join professional discussions; and revisit assumptions every few months.",
               ["few reliable sources", "test on your own tasks", "keep a log", "revisit regularly"], "Depth beats volume."),
    ],
}

PACK = {
    "id": "ai-use",
    "version": 1,
    "topic": "Using AI at work",
    "title": "Leading with AI in engineering consulting",
    "summary": "Practical, safe and credible AI use for engineering consultants: prompting, checking output, where AI helps across bids, reports, reviews and scripts, handling client data, automation and agents, governance, proving value, and leading AI adoption in your firm.",
    "icon": "rocket",
    "level": "advanced",
    "length": "standard",
    "area": "technology",
    "tags": ["ai", "ai-at-work", "consulting", "ai-governance", "productivity", "leadership"],
    "sections": [
        {"title": "Using AI well", "summary": "Skills for everyday work.", "lessons": [
            {"title": L1["title"], "summary": "Write prompts that get useful, checkable results.", "lesson": L1},
            {"title": L2["title"], "summary": "Verify AI output and stay professionally responsible.", "lesson": L2},
            {"title": L3["title"], "summary": "Know where AI helps across consulting work.", "lesson": L3},
            {"title": L4["title"], "summary": "Handle company, client and personal information safely.", "lesson": L4},
        ]},
        {"title": "Leading AI adoption", "summary": "Taking your firm with you.", "lessons": [
            {"title": L5["title"], "summary": "Choose the right level of automation and control it.", "lesson": L5},
            {"title": L6["title"], "summary": "Set up proportionate AI governance.", "lesson": L6},
            {"title": L7["title"], "summary": "Pick use cases and prove value with pilots.", "lesson": L7},
            {"title": L8["title"], "summary": "Build capability and influence as the firm's AI leader.", "lesson": L8},
        ]},
    ],
}
