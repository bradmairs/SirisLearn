"""General AI: how modern AI works, what it can and can't do, and how it's governed."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, path, svg, text, title

NESTED = svg(
    title("AI, machine learning, deep learning, generative AI"),
    '<ellipse cx="240" cy="165" rx="220" ry="118" fill="none" stroke="#7c93a6" stroke-width="2"/>',
    '<ellipse cx="265" cy="180" rx="165" ry="90" fill="none" stroke="#5fd3ff" stroke-width="2"/>',
    '<ellipse cx="290" cy="195" rx="110" ry="62" fill="none" stroke="#a78bfa" stroke-width="2"/>',
    '<ellipse cx="310" cy="208" rx="58" ry="32" fill="none" stroke="#8af5c8" stroke-width="2"/>',
    text(95, 110, "AI", 15, MUTED, weight="bold"), text(80, 128, "rules, search,", 11, MUTED), text(80, 143, "planning…", 11, MUTED),
    text(160, 165, "Machine learning", 13, BLUE), text(225, 182, "Deep learning", 13, PURPLE),
    text(310, 212, "GenAI", 13, GREEN, weight="bold"),
    text(240, 292, "each ring is a subset of the one around it", 11, MUTED),
)

LEARN = svg(
    title("Training: guess, measure the error, adjust"),
    box(20, 70, 100, 50, "Training data", BLUE, size=12, sub="inputs + labels"), arrow(120, 95, 160, 95, BLUE),
    box(160, 70, 100, 50, "Model", PURPLE, size=13, sub="weights"), arrow(260, 95, 300, 95, BLUE),
    box(300, 70, 80, 50, "Prediction", INK, size=12), arrow(380, 95, 410, 95, BLUE),
    box(410, 70, 60, 50, "Loss", RED, size=12),
    path("M440 120 L440 175 L210 175 L210 125", AMBER, 2.5), arrow(212, 150, 211, 126, AMBER),
    text(325, 195, "gradient descent nudges the weights", 12, AMBER),
    path("M60 280 Q150 210 240 255 Q320 290 420 225", GREEN, 2.5),
    circle(240, 255, 6, GREEN, "#0b1620"), text(240, 240, "X", 13, GREEN, weight="bold"),
    text(400, 270, "loss landscape", 11, MUTED),
)

OVERFIT = svg(
    title("Training error vs validation error"),
    line(60, 250, 450, 250, MUTED, 2), line(60, 250, 60, 50, MUTED, 2),
    text(255, 280, "Training time / model complexity", 12, MUTED), text(40, 150, "Error", 12, MUTED),
    path("M70 70 Q200 200 440 230", BLUE, 3), text(430, 222, "training", 12, BLUE, anchor="end"),
    path("M70 80 Q200 210 260 190 Q350 165 440 100", AMBER, 3), text(430, 95, "validation", 12, AMBER, anchor="end"),
    line(240, 60, 240, 250, GREEN, 2, "5 4"), text(240, 52, "stop here", 12, GREEN),
    text(140, 120, "A", 15, INK, weight="bold"), text(380, 160, "B", 15, RED, weight="bold"),
)

NETWORK = svg(
    title("A small neural network"),
    *[circle(80, 80 + 60 * i, 14, BLUE) for i in range(3)],
    *[circle(240, 60 + 50 * i, 14, PURPLE) for i in range(4)],
    *[circle(400, 110 + 60 * i, 14, GREEN) for i in range(2)],
    *[line(94, 80 + 60 * i, 226, 60 + 50 * j, MUTED, 1) for i in range(3) for j in range(4)],
    *[line(254, 60 + 50 * j, 386, 110 + 60 * k, MUTED, 1) for j in range(4) for k in range(2)],
    text(80, 270, "input layer", 12, BLUE), text(240, 270, "hidden layer", 12, PURPLE), text(400, 270, "output layer", 12, GREEN),
    text(160, 52, "w", 13, AMBER, weight="bold"), text(240, 38, "activation f(Σ w·x + b)", 11, AMBER),
)

TRANSFORMER = svg(
    title("A language model predicts the next token"),
    box(15, 60, 60, 36, "The", INK, size=12), box(80, 60, 70, 36, "pump", INK, size=12),
    box(155, 60, 60, 36, "was", INK, size=12), box(220, 60, 70, 36, "sized", INK, size=12),
    box(295, 60, 50, 36, "for", INK, size=12), box(355, 60, 110, 36, "?", AMBER, size=14),
    path("M115 96 Q200 140 255 96", PURPLE, 2), path("M50 96 Q170 160 255 96", PURPLE, 1.5, dash="4 3"),
    text(160, 155, "attention: which earlier tokens matter", 11, PURPLE),
    box(130, 175, 220, 40, "Transformer layers", BLUE, size=13),
    arrow(240, 215, 240, 235, BLUE),
    text(140, 255, "peak flow 62%", 12, GREEN, anchor="start"), text(140, 273, "duty 21%", 12, INK, anchor="start"),
    text(260, 255, "the 9%", 12, MUTED, anchor="start"), text(260, 273, "… probabilities", 11, MUTED, anchor="start"),
)

LIMITS = svg(
    title("Fluent is not the same as correct"),
    box(20, 60, 200, 90, "", GREEN), text(120, 85, "Strong", 14, GREEN, weight="bold"),
    text(120, 108, "drafting, summarising,", 11, INK), text(120, 124, "explaining, coding,", 11, INK), text(120, 140, "brainstorming", 11, INK),
    box(260, 60, 200, 90, "", RED), text(360, 85, "Watch out", 14, RED, weight="bold"),
    text(360, 108, "exact citations, niche facts,", 11, INK), text(360, 124, "recent events, arithmetic", 11, INK), text(360, 140, "without tools", 11, INK),
    line(40, 230, 440, 230, MUTED, 2), text(40, 250, "low confidence", 11, MUTED, anchor="start"), text(440, 250, "high confidence", 11, MUTED, anchor="end"),
    circle(380, 230, 9, AMBER, "#0b1620"), text(380, 210, "Q", 14, AMBER, weight="bold"),
    text(240, 280, "a wrong answer can sound just as sure as a right one", 11, MUTED),
)

AGENT = svg(
    title("Retrieval, tools and agents"),
    box(180, 50, 120, 50, "Model", PURPLE, size=14), arrow(240, 100, 240, 130, PURPLE),
    box(150, 130, 180, 44, "decide: answer or act?", INK, size=12),
    arrow(150, 152, 95, 152, BLUE), box(15, 128, 80, 48, "Search", BLUE, size=12, sub="RAG"),
    arrow(330, 152, 385, 152, BLUE), box(385, 128, 80, 48, "Tools", BLUE, size=12, sub="code, APIs"),
    path("M55 176 L55 230 L425 230 L425 176", GREEN, 2), arrow(240, 230, 240, 102, GREEN),
    text(240, 250, "results go back into the context", 12, GREEN),
    text(240, 275, "loop until done → an agent", 12, AMBER),
)

EVALS = svg(
    title("Precision and recall"),
    '<rect x="40" y="55" width="400" height="180" rx="12" fill="none" stroke="#7c93a6" stroke-width="2"/>',
    '<circle cx="190" cy="145" r="70" fill="#8af5c8" fill-opacity="0.18" stroke="#8af5c8" stroke-width="2"/>',
    '<circle cx="290" cy="145" r="70" fill="#5fd3ff" fill-opacity="0.18" stroke="#5fd3ff" stroke-width="2"/>',
    text(160, 145, "missed", 12, GREEN), text(240, 140, "found", 12, INK, weight="bold"), text(240, 156, "correctly", 12, INK),
    text(325, 145, "false", 12, BLUE), text(325, 160, "alarms", 12, BLUE),
    text(145, 75, "really defective", 11, GREEN), text(345, 75, "flagged by AI", 11, BLUE),
    text(240, 258, "precision = found ÷ flagged", 12, AMBER), text(240, 278, "recall = found ÷ really defective", 12, PURPLE),
)

RISK = svg(
    title("Managing AI risk across the lifecycle"),
    box(20, 60, 100, 50, "Govern", PURPLE, size=13, sub="policy, roles"), arrow(120, 85, 135, 85, MUTED),
    box(135, 60, 100, 50, "Map", BLUE, size=13, sub="use + context"), arrow(235, 85, 250, 85, MUTED),
    box(250, 60, 100, 50, "Measure", AMBER, size=13, sub="test, evaluate"), arrow(350, 85, 365, 85, MUTED),
    box(365, 60, 100, 50, "Manage", GREEN, size=13, sub="controls"),
    path("M415 110 L415 140 L70 140 L70 112", MUTED, 2, dash="4 3"), text(240, 156, "repeat as the system and its use change", 11, MUTED),
    text(240, 195, "Risks: bias · privacy · IP · security · errors · misuse", 12, RED),
    text(240, 225, "Frameworks: NIST AI RMF · ISO/IEC 42001 · EU AI Act", 12, INK),
    text(240, 250, "Australia: AI Ethics Principles · Guidance for AI Adoption", 12, INK),
)

L1 = {
    "title": "What AI is, and isn't",
    "minutes": 9,
    "photo_query": "artificial intelligence data centre servers",
    "body": """"AI" gets used for everything from a spreadsheet macro to a chatbot that writes reports. Being the person in the room who can explain it clearly starts with the vocabulary.

## The nested terms

- **Artificial intelligence (AI)**: the broad field of making computers do things we'd call intelligent: perceiving, reasoning, planning, using language. It includes old-fashioned approaches such as hand-written **rules** ("expert systems"), search and optimisation.
- **Machine learning (ML)**: instead of writing the rules, you give the system **data** and it learns patterns. A model that predicts pipe failure from age, material and soil is ML.
- **Deep learning**: ML using **neural networks** with many layers. It powers image recognition, speech recognition and modern language models.
- **Generative AI (GenAI)**: deep learning models that **create** new content (text, images, code, audio, video) rather than just classifying or predicting a number. Large language models (**LLMs**) such as those behind ChatGPT, Claude, Gemini and Microsoft Copilot are the best-known examples.

Each term is a subset of the one before it. Plenty of valuable AI in engineering isn't generative: optimisation of pump schedules, defect detection in CCTV footage or demand forecasting.

## A very short history

- **1950s-80s**: symbolic AI and expert systems; impressive in narrow domains, brittle outside them.
- **1990s-2000s**: statistical ML (decision trees, support vector machines) on structured data.
- **2012 onwards**: deep learning takes off with big datasets, GPUs and better training methods (image recognition leaps ahead).
- **2017**: the **transformer** architecture is published; it scales extremely well.
- **2020s**: large language models trained on huge amounts of text become general-purpose assistants, then gain images, voice, tool use and longer "reasoning".

The pattern: progress came from **more data, more compute and better architectures**, not from programming in knowledge by hand.

## Narrow, general and the hype

- **Narrow AI** does specific tasks. Most deployed AI is narrow.
- Modern LLMs are unusually **general**: one model can draft, translate, summarise, code and answer questions across fields. But they still have real limits (later lessons).
- **AGI** (artificial general intelligence) usually means AI matching humans across most cognitive work. People disagree about the definition and the timeline; treat confident predictions either way with caution.

## Useful mental models

- An ML model is a **function learned from examples**: inputs in, outputs out, behaviour shaped by its training data.
- An LLM is, at its core, a **next-token predictor** trained on vast text and then tuned to be a helpful assistant. That simple objective, at scale, produces surprisingly capable behaviour, and also explains some failures (it produces plausible text, not guaranteed truth).
- AI is **software with statistical behaviour**: it can be right 95% of the time and confidently wrong the other 5%. Design how you use it around that.

## In practice

When someone at work says "we should use AI", ask: *which kind?* A rules engine, a predictive ML model and an LLM assistant need very different data, skills, testing and governance.""",
    "key_points": [
        "AI ⊃ machine learning ⊃ deep learning ⊃ generative AI; each is a subset of the last.",
        "ML learns patterns from data instead of hand-written rules; deep learning uses many-layered neural networks.",
        "Progress came from data, compute and architectures, especially the 2017 transformer.",
        "LLMs are general but statistical: plausible output isn't guaranteed to be true.",
    ],
    "figure_svg": NESTED,
    "figure_caption": "Generative AI sits inside deep learning, inside machine learning, inside the wider field of AI.",
    "questions": [
        mcq("Which statement best describes machine learning?", ["Computers following hand-written rules", "Systems that learn patterns from data rather than being explicitly programmed", "Any software that uses a database", "Robots"], 1,
            "ML learns from examples."),
        mcq("In the diagram, which ring is the smallest?", ["AI", "Machine learning", "Deep learning", "Generative AI"], 3,
            "GenAI is a subset of deep learning.",
            NESTED, "Four nested ellipses: AI outermost, then machine learning, deep learning and generative AI innermost."),
        mcq("A model that predicts which water mains will break next year from age, material and soil is…", ["Generative AI", "Machine learning (predictive)", "An expert system", "AGI"], 1,
            "It predicts a value or class from data; it doesn't generate content."),
        mcq("What architecture, published in 2017, underpins most modern language models?", ["Convolutional networks", "The transformer", "Decision trees", "Expert systems"], 1,
            "Transformers scale very well with data and compute."),
        mcq("What mainly drove the leap in AI capability since about 2012?", ["Hand-coding more knowledge", "More data, more compute and better architectures", "Faster internet", "Quantum computers"], 1,
            "Scale plus better methods."),
        mcq("In the diagram, where would an old rules-based expert system sit?", ["Inside GenAI", "Inside deep learning", "In AI but outside machine learning", "Outside AI"], 2,
            "Rules are written by people, not learned.",
            NESTED, "Nested ellipses with rules, search and planning noted in the outer AI ring only."),
        mcq("What is an LLM fundamentally trained to do first?", ["Look up facts in a database", "Predict the next token in text", "Run calculations", "Search the web"], 1,
            "Then it's tuned to behave as an assistant."),
        open_q("Explain the difference between AI, machine learning and generative AI to a colleague in two or three sentences.", "AI is the broad field of making computers do intelligent tasks, including rules and search. Machine learning is the part of AI where systems learn patterns from data instead of following hand-written rules. Generative AI is a type of deep learning that creates new content such as text, images or code.",
               ["AI is the broad field", "ML learns from data", "GenAI creates new content"], "Nested subsets."),
        open_q("Why does it matter which kind of AI someone means when they say 'let's use AI'?", "Because rules engines, predictive ML models and LLM assistants need different data, skills, costs, testing and governance; the right choice depends on the problem, and many valuable engineering uses aren't generative at all.",
               ["different data and skills", "different testing and governance", "match the tool to the problem"], "Ask which kind."),
        open_q("What does it mean to say AI is 'software with statistical behaviour'?", "Its outputs come from learned probabilities rather than fixed logic, so it can be right most of the time and confidently wrong some of the time; you have to design checks and use around that error rate.",
               ["learned probabilities, not fixed rules", "sometimes confidently wrong", "design checks around errors"], "Plan for the failure cases."),
    ],
}

L2 = {
    "title": "How machines learn",
    "minutes": 10,
    "photo_query": "",
    "body": """Every ML system, from a pipe failure predictor to a frontier language model, learns in roughly the same way: make a guess, measure how wrong it is, and adjust.

## Three kinds of learning

- **Supervised learning**: examples come with the right answer (**labels**). "Here are 10 000 CCTV images, each labelled with its defect code." The model learns to map inputs to labels. Two flavours: **classification** (pick a category) and **regression** (predict a number such as demand).
- **Unsupervised learning**: no labels; the model finds structure, for example **clustering** customers by usage pattern or spotting **anomalies** in SCADA data.
- **Reinforcement learning (RL)**: an agent takes actions and gets **rewards**, learning a strategy by trial and error (game playing, control systems, and part of how chat models are tuned).

Many modern systems mix these. LLMs are first trained with **self-supervised** learning, where the "label" is just the next word in real text, so no human labelling is needed for that stage.

## The training loop

1. A model has **parameters** (also called **weights**): numbers that determine its behaviour. At the start they're random.
2. Feed in a training example and get a **prediction**.
3. A **loss function** measures how wrong it was (for example the squared error for a number, or cross-entropy for categories).
4. **Gradient descent** works out which direction to nudge each weight to reduce the loss, and takes a small step (the **learning rate** sets the step size).
5. Repeat over millions or billions of examples, usually in **batches**; one pass over the data is an **epoch**.

Think of standing on a foggy hillside (the **loss landscape**) and always stepping downhill. You may not find the very lowest valley, but you get somewhere useful.

## Generalisation: the whole point

A model that memorises its training data is useless on new data. So data is split:

- **Training set**: used to fit the weights.
- **Validation set**: used to tune settings and decide when to stop.
- **Test set**: held back until the end for an honest estimate of real performance.

**Overfitting** is when training error keeps falling but validation error rises: the model is learning noise. **Underfitting** is when it hasn't captured the pattern at all. Fixes for overfitting include more data, simpler models, **regularisation** and early stopping.

## Data is the product

- **Garbage in, garbage out**: biased, mislabelled or unrepresentative data produces a biased, unreliable model.
- **Data leakage**: information from the answer sneaking into the inputs (for example a "replaced" flag when predicting failure) makes test results look brilliant and real results poor.
- **Distribution shift**: a model trained on one network, era or climate may degrade when conditions change. Monitor it after deployment.

## Features versus learned representations

Classic ML relies on people designing **features** (pipe age, material, number of previous breaks). Deep learning learns its own internal features from raw data such as pixels or text, which is why it needs much more data and compute but works on messy inputs.

> **Engineering parallel:** training is calibration. Like calibrating a hydraulic model, you fit parameters to observed data, then validate on data you didn't use for fitting. The same discipline applies.""",
    "key_points": [
        "Supervised (labelled), unsupervised (find structure) and reinforcement (rewards) learning; LLMs pre-train self-supervised.",
        "Training loop: predict, compute loss, gradient descent adjusts weights, repeat.",
        "Split data into training, validation and test sets; overfitting means memorising noise.",
        "Data quality, leakage and distribution shift decide real-world performance.",
    ],
    "figure_svg": LEARN,
    "figure_caption": "The model predicts, the loss measures the error, and gradient descent adjusts the weights; X marks a low point in the loss landscape.",
    "questions": [
        mcq("Labelled CCTV images used to train a defect classifier are an example of…", ["Unsupervised learning", "Supervised learning", "Reinforcement learning", "Rules"], 1,
            "Each example comes with the right answer."),
        mcq("Grouping customers by usage pattern without any labels is…", ["Supervised classification", "Unsupervised clustering", "Regression", "Reinforcement learning"], 1,
            "No labels, find structure."),
        mcq("In the diagram, what does the loss measure?", ["The size of the model", "How wrong the prediction was", "How fast training runs", "The amount of data"], 1,
            "Lower loss means better predictions on that data.",
            LEARN, "Training data feeds a model, which makes a prediction compared with the label to give a loss; an arrow loops back to adjust the weights."),
        mcq("What does gradient descent do?", ["Deletes bad data", "Nudges weights in the direction that reduces the loss", "Adds layers", "Labels data"], 1,
            "Step downhill on the loss landscape."),
        mcq("Why keep a test set aside until the end?", ["To save storage", "To get an honest estimate of performance on unseen data", "To train faster", "Regulators require it"], 1,
            "If you tune on it, it's no longer independent."),
        mcq("A pipe failure model includes a 'pipe replaced' flag that's only set after failures. What's the problem?", ["Underfitting", "Data leakage", "Too little compute", "Reinforcement"], 1,
            "The answer leaks into the inputs."),
        mcq("In the diagram, what loops back from the loss to the model?", ["New data", "Weight updates from gradient descent", "The test set", "Labels"], 1,
            "The feedback path adjusts weights.", LEARN, "Arrow from loss back to the model labelled gradient descent nudges the weights."),
        open_q("Explain overfitting and how you'd detect it.", "Overfitting is when a model learns the noise and quirks of its training data, so it does well on training data but poorly on new data; you detect it when training error keeps falling while validation error starts rising.",
               ["learns noise in training data", "poor on new data", "validation error rises while training error falls"], "Early stopping is one fix."),
        open_q("Why might a model trained on one water network perform poorly on another?", "Distribution shift: the new network has different materials, ages, soils, pressures and data practices, so the patterns the model learned don't hold; you need to validate on the new network and possibly retrain.",
               ["distribution shift", "different conditions and data", "validate or retrain"], "Monitor models after deployment."),
        open_q("How is training an ML model like calibrating a hydraulic model?", "Both fit parameters to observed data (weights versus roughness and demands) and must be validated on data not used for fitting, so you know they generalise rather than just match the calibration data.",
               ["fit parameters to data", "validate on independent data"], "Same discipline, different parameters."),
    ],
}

L3 = {
    "title": "Neural networks and deep learning",
    "minutes": 10,
    "photo_query": "",
    "body": """Neural networks are the engine of modern AI. You don't need the maths to lead on AI, but a clear picture of what's inside helps you judge what's plausible.

## Neurons and layers

An artificial **neuron** takes several inputs, multiplies each by a **weight**, adds them up with a **bias**, then passes the result through an **activation function** (such as ReLU, which outputs zero for negatives and the value itself for positives). The activation is what lets networks model curved, non-linear relationships.

Neurons are arranged in **layers**:

- An **input layer** receives the data (pixel values, sensor readings, word embeddings).
- One or more **hidden layers** transform it.
- An **output layer** produces the answer (a probability for each class, or a number).

"Deep" just means many hidden layers. Modern models have billions or even trillions of weights.

## How they learn: backpropagation

**Backpropagation** is the algorithm that works out, for every weight in the network, how much it contributed to the error. Gradient descent then adjusts them all a little. GPUs (and specialised chips) make this practical because the work is huge numbers of matrix multiplications done in parallel.

## Learned representations

Each layer learns to represent the data more usefully. In an image network, early layers detect edges, middle layers shapes and textures, later layers whole objects such as "crack" or "root intrusion". Nobody programs these features; they emerge from training.

**Embeddings** are a key idea: representing things (words, documents, images) as lists of numbers (vectors) where **similar meanings sit close together**. "Pump" and "impeller" end up near each other. Embeddings power semantic search and retrieval over company documents.

## Common architectures

- **Convolutional neural networks (CNNs)**: built for images and grids; scan small filters across the input. Used for defect detection, aerial imagery and satellite analysis.
- **Recurrent networks (RNNs, LSTMs)**: older approach for sequences such as time series and text, largely overtaken by transformers.
- **Transformers**: use **attention** to relate every part of the input to every other part; now dominant for language, and widely used for images, audio and time series too.
- **Diffusion models**: generate images (and video) by learning to remove noise step by step.

## Why "black box"?

A network's knowledge is spread across millions of weights, so it's hard to explain *why* it made a specific prediction. The field of **interpretability** works on this, and tools such as feature attribution help, but for high-stakes engineering decisions you should still rely on validation, testing and human review rather than explanations alone.

## Scale and cost

Bigger models trained on more data with more compute have reliably got better (**scaling laws**), which is why frontier models cost huge sums to train. **Inference** (running a trained model) is much cheaper per use but adds up across millions of users. Smaller models, often **distilled** from larger ones, can run on a laptop or phone and are good enough for many tasks.

> **Practical takeaway:** a neural network is a very flexible curve-fitter. Give it lots of representative data and it can find patterns humans can't; give it biased or narrow data and it will faithfully learn those flaws.""",
    "key_points": [
        "A neuron weights its inputs, adds a bias and applies an activation; layers of neurons form a network.",
        "Backpropagation assigns error to every weight so gradient descent can train deep networks on GPUs.",
        "Layers learn representations; embeddings place similar meanings close together as vectors.",
        "CNNs for images, transformers for language and more, diffusion for image generation; networks are hard to interpret.",
    ],
    "figure_svg": NETWORK,
    "figure_caption": "Inputs pass through weighted connections (w) into a hidden layer with activations, then to the outputs.",
    "questions": [
        mcq("What does an activation function add to a neural network?", ["More data", "The ability to model non-linear relationships", "Labels", "Storage"], 1,
            "Without it, layers collapse into one linear function."),
        mcq("In the diagram, what do the lines between circles represent?", ["Data files", "Weighted connections between neurons", "Electricity", "Layers"], 1,
            "Each connection has a weight that training adjusts.",
            NETWORK, "Three input neurons, four hidden neurons and two output neurons, fully connected; a weight w labelled on one connection."),
        mcq("What does backpropagation compute?", ["The final answer", "How much each weight contributed to the error", "The training data", "The activation function"], 1,
            "Then gradient descent adjusts the weights."),
        mcq("What is an embedding?", ["A compressed file", "A vector of numbers representing meaning, with similar things close together", "A type of chip", "A database table"], 1,
            "Embeddings power semantic search."),
        mcq("Which architecture is classically used for image tasks like defect detection?", ["Recurrent networks", "Convolutional neural networks", "Decision trees", "Diffusion only"], 1,
            "CNNs scan filters across images; transformers are also used now."),
        mcq("Why are GPUs important for deep learning?", ["They store more data", "They do huge numbers of matrix multiplications in parallel", "They're cheaper than CPUs", "They label data"], 1,
            "Training is mostly parallel arithmetic."),
        mcq("In the diagram, what does 'deep' in deep learning refer to?", ["A big input layer", "Many hidden layers", "A large output layer", "Long training"], 1,
            "This small example has one hidden layer; deep networks have many.",
            NETWORK, "Network with input, one hidden and output layers labelled."),
        open_q("Why are neural networks often called 'black boxes', and what should an engineer do about it?", "Their knowledge is spread across millions of weights, so it's hard to explain why they made a particular prediction; for high-stakes decisions, rely on independent validation, testing on representative data and human review rather than trusting explanations alone.",
               ["knowledge spread across weights", "hard to explain individual predictions", "validate, test and review"], "Interpretability tools help but don't replace testing."),
        open_q("How do embeddings make searching company documents better than keyword search?", "Embeddings represent the meaning of text as vectors, so a search finds documents with similar meaning even if they use different words, such as finding 'impeller wear' when you search 'pump damage'.",
               ["represent meaning as vectors", "finds similar meaning", "different words still match"], "This is the basis of retrieval for LLMs."),
        open_q("Explain the trade-off between large frontier models and small distilled models.", "Large models are generally more capable and handle harder, broader tasks, but cost more per use and usually run in the cloud; small models are cheaper and faster and can run locally, which helps privacy, but are less capable on complex tasks.",
               ["large: more capable, costlier", "small: cheaper, faster, local", "privacy benefit of local"], "Pick the smallest model that does the job well."),
    ],
}

L4 = {
    "title": "Transformers and large language models",
    "minutes": 11,
    "photo_query": "",
    "body": """Large language models (LLMs) are the AI most people now use daily. Understanding how they're built explains both their power and their quirks.

## Tokens

Text is split into **tokens**, chunks that are often whole short words or pieces of longer ones (roughly 3-4 characters of English each on average). "Hydrostatic" might be two or three tokens. Models read and write tokens, prices are per token, and limits are in tokens.

## The transformer and attention

A transformer turns each token into an embedding and passes them through many layers. The key mechanism is **self-attention**: for every token, the model weighs how relevant every other token in the context is. In "the pump was sized for peak flow", attention links "sized" to "pump" and "flow". Attention is computed in parallel, which is why transformers train efficiently on GPUs, and stacking dozens of layers builds rich understanding.

The model's final output is a **probability distribution over the next token**. It picks one (more or less randomly, controlled by **temperature**), adds it to the text and repeats. That's all generation is: next-token prediction, one token at a time.

## How an assistant is made

1. **Pre-training**: predict the next token across a vast corpus (web pages, books, code, papers). The model absorbs grammar, facts, reasoning patterns and styles. This is by far the most expensive stage.
2. **Fine-tuning** (instruction tuning): train on examples of good instructions and responses so it behaves as a helpful assistant.
3. **Preference training**: methods such as **RLHF** (reinforcement learning from human feedback) and related techniques use human or AI judgements of which answer is better to shape helpfulness, honesty and safety.
4. **Reasoning training**: many recent models are also trained with reinforcement learning on problems with checkable answers (maths, code), learning to "think" step by step before answering.

## Key concepts you'll hear

- **Parameters**: the model's weights; more usually means more capable, but training data and methods matter as much.
- **Context window**: how many tokens the model can consider at once (your prompt, documents, the conversation and its reply). Modern windows hold hundreds of pages; but quality can still drop on details buried deep in very long contexts.
- **Knowledge cutoff**: the model only "knows" what was in its training data up to a date. Anything newer needs to be provided (search, documents).
- **System prompt**: hidden instructions from the app developer that set behaviour.
- **Temperature**: higher gives more varied output, lower more consistent; even at low settings outputs can vary.
- **Open-weight vs closed models**: some models' weights are published to run yourself; others are only available through a provider's service.

## What's really going on?

Predicting the next token well across all of human text requires building internal representations of concepts, relationships and procedures, which is why LLMs can explain hydraulics or draft a specification. But the objective rewards **plausible** continuations, not verified truth. When the model lacks knowledge, the most plausible continuation may be a confident fabrication: a **hallucination**.

> **Leader's summary:** an LLM is a next-token predictor, pre-trained on vast text, then tuned to be an assistant. It works on tokens in a limited context window, knows nothing after its cutoff unless told, and produces plausible rather than guaranteed-correct text.""",
    "key_points": [
        "Text is processed as tokens; pricing and limits are in tokens.",
        "Transformers use self-attention to relate every token to every other; output is a probability over the next token.",
        "Assistants are built by pre-training, instruction fine-tuning, preference training (e.g. RLHF) and often reasoning training.",
        "Context window, knowledge cutoff, temperature and system prompts shape behaviour; plausibility isn't truth.",
    ],
    "figure_svg": TRANSFORMER,
    "figure_caption": "Attention links the relevant earlier tokens, and the transformer outputs probabilities for the next token.",
    "questions": [
        mcq("What is a token?", ["A password", "A chunk of text such as a word or part of a word", "A sentence", "A training example"], 1,
            "Models read, write and charge by tokens."),
        mcq("In the diagram, what does attention do?", ["Deletes words", "Weighs which earlier tokens are relevant to each token", "Counts words", "Translates"], 1,
            "It links 'sized' to 'pump', for example.",
            TRANSFORMER, "The tokens 'The pump was sized for ?' with curved attention links from 'sized' back to 'pump' and 'The', feeding transformer layers that output next-token probabilities."),
        mcq("What is the most expensive stage of building an LLM?", ["Writing the system prompt", "Pre-training on a vast corpus", "Choosing a temperature", "Tokenising"], 1,
            "It uses enormous compute."),
        mcq("What does RLHF do?", ["Adds facts", "Uses human feedback on preferred answers to shape behaviour", "Speeds up inference", "Increases the context window"], 1,
            "Reinforcement learning from human feedback."),
        mcq("A model released mid-year is asked about something from last month. Why might it fail?", ["Low temperature", "Its knowledge cutoff predates the event", "Too many parameters", "Attention"], 1,
            "Provide recent information via search or documents."),
        mcq("What does raising the temperature do?", ["Makes output more varied", "Makes output faster", "Makes it more accurate", "Increases the context window"], 0,
            "Lower temperature gives more consistent output."),
        mcq("In the diagram, what does the model output at each step?", ["A full paragraph", "Probabilities for the next token", "A database query", "An image"], 1,
            "It picks one token, appends it and repeats.",
            TRANSFORMER, "Transformer layers producing a list of candidate next tokens with percentages."),
        open_q("Explain in plain words why LLMs hallucinate.", "They're trained to produce the most plausible continuation of text, not to check facts; when they don't actually know something, a fluent, confident but made-up answer can still be the most plausible-sounding continuation.",
               ["trained for plausible text", "not checking facts", "confident fabrication when knowledge is missing"], "That's why grounding and checking matter."),
        open_q("Describe the stages that turn a pre-trained model into a helpful assistant.", "After pre-training on vast text, the model is fine-tuned on examples of instructions and good responses, then trained with preference methods such as RLHF so it gives helpful, honest and safe answers; many models are also trained with reinforcement learning on checkable problems to reason step by step.",
               ["instruction fine-tuning", "preference training such as RLHF", "reasoning training"], "Each stage shapes behaviour."),
        open_q("What is a context window and why does it matter when you give a model a long report?", "It's the maximum number of tokens the model can consider at once, covering the prompt, documents, conversation and reply; a report must fit, and even when it does, details deep in very long inputs can be missed, so point the model to the relevant sections and check.",
               ["max tokens considered at once", "includes documents and reply", "details in long inputs can be missed"], "Bigger windows help, but aren't perfect."),
    ],
}

L5 = {
    "title": "What AI is good and bad at",
    "minutes": 10,
    "photo_query": "",
    "body": """Leaders in AI aren't the people who are most excited about it; they're the people who know **where it's reliable and where it isn't**, and can use it accordingly.

## Where LLMs are strong

- **Language work**: drafting, rewriting for audience and tone, summarising, translating, extracting structured information from messy text.
- **Explaining**: walking through a concept at the level you need, generating analogies and worked examples.
- **Coding**: writing scripts, formulas, macros and queries; explaining and debugging code. Often a big productivity gain for engineers who code occasionally.
- **Brainstorming and critique**: options, risks, counter-arguments, checklists, "what have I missed?".
- **Transforming formats**: notes to a report, a table to prose, a spec to a checklist.

## Where they're weak or risky

- **Hallucination**: invented facts, numbers, references, clauses of standards, case law or URLs, delivered fluently. Risk is highest for niche, specific or recent facts, exactly the things engineering depends on.
- **Exact calculation**: models can slip on arithmetic and units when "doing maths in their head". With a code tool or calculator they're much more reliable; without one, check every number.
- **Recency**: anything after the knowledge cutoff is unknown unless provided.
- **Long-context recall**: may miss or blur details in very long documents.
- **Consistency**: the same question can get different answers. Important for repeatable processes.
- **Overconfidence and sycophancy**: models may agree with a wrong premise in your question or sound equally sure whether right or wrong. Ask neutrally.
- **Local knowledge**: your organisation's standards, clients' preferences and site conditions aren't in the model unless you provide them.

## Reasoning models

Many current models can spend extra computation "thinking" (an internal chain of reasoning) before answering. This markedly improves multi-step maths, coding, planning and analysis, at the cost of time and tokens. It reduces, but doesn't eliminate, errors: a long chain of reasoning can still rest on a wrong assumption.

## Jagged capability

AI capability is **jagged**: a model may solve a hard hydraulics derivation and then miscount items in a list. Don't extrapolate from impressive examples, and don't dismiss it because of a silly failure. Test it on **your** tasks.

## Calibrate your trust

Ask three questions for any use:

1. **How would I know if it's wrong?** If you can easily verify (code that runs, a draft you'll review), AI is low risk. If errors are hard to spot (a plausible but wrong clause), be careful.
2. **What does an error cost?** A clumsy email sentence is trivial; a wrong pipe class in a design is not.
3. **Can I ground it?** Giving the model the actual standard, report or data, and asking it to quote its sources, cuts hallucination sharply.

## Getting more reliable results

- Provide sources and ask it to answer **only** from them, citing sections.
- Let it use **tools** (code execution, search) for calculations and current facts.
- Ask it to state assumptions and uncertainty.
- Break big tasks into steps you can check.
- Have a person with domain knowledge review anything that matters.

> **Rule for engineers:** AI can draft the calculation, but an engineer owns the answer. Treat AI output like a graduate's first draft: often useful, sometimes brilliant, never signed off unchecked.""",
    "key_points": [
        "Strong at drafting, summarising, explaining, coding, brainstorming and reformatting.",
        "Weak at niche/recent facts, exact citations and unaided arithmetic; can be inconsistent and overconfident.",
        "Reasoning models help with multi-step problems but don't eliminate errors; capability is jagged.",
        "Calibrate trust by verifiability and cost of error; ground the model in sources and use tools.",
    ],
    "figure_svg": LIMITS,
    "figure_caption": "Strengths and weak spots; an answer at Q can sound highly confident whether or not it's correct.",
    "questions": [
        mcq("Which task is an LLM generally most reliable at?", ["Quoting the exact clause number of a niche standard from memory", "Rewriting a technical paragraph for a non-technical client", "Reporting yesterday's news without search", "Long arithmetic without tools"], 1,
            "Language transformation is a core strength."),
        mcq("Why are hallucinations especially risky in engineering?", ["Engineers don't use AI", "Engineering relies on specific, niche facts and numbers where fabrication is most likely and hard to spot", "Hallucinations only affect images", "They're illegal"], 1,
            "Plausible but wrong specifics are dangerous."),
        mcq("In the diagram, what does point Q illustrate?", ["The model is always right when confident", "A confident-sounding answer that may or may not be correct", "Low confidence", "A tool call"], 1,
            "Confidence in tone isn't evidence of correctness.",
            LIMITS, "A strengths box and a watch-out box above a confidence scale, with Q marked near high confidence and a note that wrong answers can sound just as sure."),
        mcq("What most reduces hallucination when asking about a standard?", ["Asking more politely", "Providing the actual document and asking it to answer only from it with citations", "Raising temperature", "Using capital letters"], 1,
            "Grounding in sources."),
        mcq("What does 'jagged capability' mean?", ["AI is equally good at everything", "AI may excel at hard tasks yet fail at some easy ones", "AI only works in bursts", "AI improves every day"], 1,
            "Test on your own tasks."),
        mcq("A model gives different answers to the same question on two runs. This is…", ["A bug that never happens", "Normal; outputs are sampled and can vary", "Proof it's hacked", "Caused by the knowledge cutoff"], 1,
            "Plan for variability in repeatable processes."),
        mcq("In the diagram, which item is in the 'watch out' list?", ["Drafting", "Brainstorming", "Exact citations and niche facts", "Explaining"], 2,
            "Specific facts are where hallucination bites.",
            LIMITS, "Watch out box listing exact citations, niche facts, recent events and arithmetic without tools."),
        open_q("What three questions help you decide how much to trust AI for a task?", "How would I know if it's wrong (can I easily verify)? What does an error cost? Can I ground it in real sources or tools?",
               ["can I verify it", "cost of an error", "can I ground it in sources"], "High cost plus hard to verify means caution."),
        open_q("Why can a leading question like 'Isn't PN12 fine for this main?' give you a worse answer?", "Models tend to be sycophantic and agree with the premise in a question, so asking leadingly can produce confirmation rather than an independent check; ask neutrally, such as 'what pressure class does this main need and why?'.",
               ["models tend to agree with the premise", "ask neutrally"], "Sycophancy is a known failure mode."),
        open_q("Explain the 'graduate's first draft' rule for engineers using AI.", "Treat AI output like a graduate's draft: often useful and sometimes excellent, but it must be reviewed and checked by a competent engineer who owns the result before it's relied on or signed off.",
               ["useful but not final", "competent review", "engineer owns the answer"], "Professional responsibility doesn't move to the tool."),
    ],
}

L6 = {
    "title": "Multimodal models, tools and agents",
    "minutes": 10,
    "photo_query": "",
    "body": """Modern AI isn't just a chat box. Models can see, hear, search, run code and take actions. These capabilities are where much of the practical value, and much of the new risk, now sits.

## Multimodal

Many models accept **images** (photos, scanned drawings, charts, screenshots), and some handle **audio** and **video**. You can photograph a site defect and ask for a description, paste a chart and ask what it shows, or have a meeting transcribed and summarised. Be cautious: models can misread small text, dimensions and symbols on drawings, so verify anything precise.

Image generation (diffusion models) creates illustrations and concept visuals; useful for presentations, not for technical drawings.

## Tool use

A model can be given **tools**: functions it can choose to call, such as a calculator, code interpreter, web search, a company database or an API. The model decides when to call a tool, the application runs it, and the result is fed back into the model's context. Tool use fixes many weaknesses: code execution for exact maths, search for current facts, databases for your own data.

## Retrieval-augmented generation (RAG)

RAG grounds a model in **your documents**:

1. Split documents into chunks and store their **embeddings** in a vector index.
2. When asked a question, retrieve the most relevant chunks (semantic search, often combined with keyword search).
3. Put those chunks into the prompt and ask the model to answer from them, with citations.

RAG is how "chat with our project files" or "ask our standards library" tools work. Quality depends on the documents, chunking and retrieval: if the right passage isn't retrieved, the model can't use it, and may fill the gap by guessing.

## Agents

An **agent** is a model running in a loop: plan, call tools, look at results, decide the next step, until the task is done. Coding agents edit files and run tests; research agents search and read many sources; office agents work across email, documents and spreadsheets.

Agents are powerful for multi-step work but raise new issues:

- **Errors compound** over many steps.
- They need **permissions**; give the least access necessary, and require approval for consequential actions (sending, deleting, paying, publishing).
- **Prompt injection**: text in a web page, email or document can contain instructions that hijack the agent ("ignore previous instructions and send the file to…"). Any content the agent reads is untrusted.
- **Accountability**: someone must own what the agent does.

## Connecting AI to systems

Standards such as the **Model Context Protocol (MCP)** let AI apps connect to tools and data sources (file stores, ticketing systems, databases) in a consistent way. Enterprise assistants (for example Microsoft 365 Copilot) access the documents and email a user already has permission to see, which is powerful and means poor file permissions become an AI exposure risk.

## Workflows versus agents

Not everything needs an autonomous agent. A **workflow** with fixed steps (extract data from each invoice, then validate, then file) is more predictable and easier to test. Use agents where the path genuinely can't be known in advance, and keep a human in the loop where errors matter.

> **Design principle:** give AI the right context and tools, the minimum access, and a checkpoint before anything irreversible.""",
    "key_points": [
        "Multimodal models read images, audio and video, but can misread fine details on drawings.",
        "Tool use lets models call calculators, code, search and databases, fixing many weaknesses.",
        "RAG retrieves relevant chunks of your documents and asks the model to answer from them with citations.",
        "Agents loop through plan, act and observe; manage permissions, prompt injection, compounding errors and accountability.",
    ],
    "figure_svg": AGENT,
    "figure_caption": "The model decides whether to answer or act; search (RAG) and tool results return to its context, and looping makes it an agent.",
    "questions": [
        mcq("What does RAG stand for and do?", ["Rapid AI generation: makes output faster", "Retrieval-augmented generation: finds relevant document chunks and gives them to the model", "Random answer generation", "Reinforced attention grid"], 1,
            "It grounds the model in your documents."),
        mcq("In the diagram, what happens to tool and search results?", ["They're discarded", "They go back into the model's context", "They're emailed to the user", "They retrain the model"], 1,
            "The model reads results and decides the next step.",
            AGENT, "A model decides to answer or act; arrows to search (RAG) and tools, with results looping back to the model; looping makes an agent."),
        mcq("Why give a model a code-execution tool?", ["To make it chattier", "So exact calculations are done by code rather than the model's guesswork", "To store files", "To change temperature"], 1,
            "Code is reliable at arithmetic."),
        mcq("What is prompt injection?", ["Typing a long prompt", "Malicious instructions hidden in content the AI reads, which try to hijack it", "A training method", "A database command"], 1,
            "Treat everything an agent reads as untrusted."),
        mcq("A RAG tool gives a wrong answer even though the right document is in the library. A likely cause is…", ["The model is too big", "The right passage wasn't retrieved", "Temperature is zero", "The document is too short"], 1,
            "Retrieval quality limits answer quality."),
        mcq("Which is the best reason to choose a fixed workflow over an agent?", ["Agents are illegal", "The steps are known, so a workflow is more predictable and testable", "Workflows can't use AI", "Agents are always cheaper"], 1,
            "Use agents when the path can't be planned."),
        mcq("In the diagram, what turns this into an agent?", ["The search box", "Looping until the task is done", "The model's size", "Citations"], 1,
            "Plan, act, observe, repeat.", AGENT, "Diagram with a loop arrow and the note 'loop until done → an agent'."),
        open_q("Why do poor SharePoint or file permissions become a bigger risk with enterprise AI assistants?", "Assistants can search everything a user has access to, so documents that were overshared but hard to find become easy to surface through a simple question, exposing confidential or personal information.",
               ["assistant sees what the user can access", "overshared files become easy to find", "confidential exposure"], "Fix permissions before rolling out."),
        open_q("What controls would you put on an agent that can send emails on your behalf?", "Least privilege access, a human approval step before sending, logging of its actions, treating all incoming content as untrusted to resist prompt injection, limits on recipients or volume, and clear ownership of what it does.",
               ["least privilege", "human approval before sending", "logging", "resist prompt injection"], "Checkpoint before anything irreversible."),
        open_q("Why should you verify dimensions an AI reads from a scanned drawing?", "Multimodal models can misread small text, symbols and numbers in images, especially on low-quality scans, and may state them confidently; a wrong dimension could propagate into design or quantities.",
               ["can misread small text and symbols", "confident errors", "errors propagate"], "Check against the source."),
    ],
}

L7 = {
    "title": "Evaluating AI systems",
    "minutes": 10,
    "photo_query": "",
    "body": """"Does it work?" is the most important question about any AI system, and "it looked good in the demo" isn't an answer. Evaluation is where engineering discipline adds the most value.

## Benchmarks: useful, limited

Model makers publish scores on public **benchmarks** (exam-style knowledge tests, maths, coding, reasoning). They're helpful for comparing models broadly, but:

- They may not reflect **your** tasks.
- **Contamination**: test questions can leak into training data, inflating scores.
- Benchmarks **saturate**: once models score near 100%, they stop discriminating.
- Small score differences rarely matter in practice.

## Build your own evaluation

For any serious use, create a **test set from your real work**:

1. Collect representative examples (say 30-100) including hard and edge cases: messy scans, unusual clauses, ambiguous requests.
2. Define what "good" looks like for each: a correct answer, required points, or a rubric.
3. Run the AI system on all of them and score the results.
4. Re-run whenever you change the model, prompt or retrieval setup, to catch **regressions**.

Scoring can be **exact** (does the extracted pipe diameter match?), **rubric-based** by a person, or done by another model acting as a **judge** (fast and scalable, but check it agrees with human judgement on a sample).

## Metrics that matter

For classification tasks (for example flagging defects or non-compliant clauses):

- **Precision**: of the items the AI flagged, how many were truly issues? Low precision means many false alarms, which wastes time and erodes trust.
- **Recall**: of the real issues, how many did the AI find? Low recall means misses, which is dangerous in safety-critical reviews.
- There's usually a **trade-off**. For a compliance pre-check, high recall with human review of flags is often right; for automatic actions, high precision matters more.

Also measure **time saved**, **cost per task**, **consistency** across runs and **user satisfaction**.

## Human factors

- **Automation bias**: people over-trust automated outputs, especially when tired or busy. Review steps need to be designed so people actually check, for example by showing sources side by side.
- **Deskilling**: if juniors never do the task themselves, they may not learn to spot errors. Plan for capability building.
- **Accountability**: decide who signs off and what they must check.

## Pilot properly

- Compare against a **baseline** (how long and how accurate is the current process?).
- Run a **pilot** with real users and real work, measure outcomes, gather feedback.
- Watch for failure patterns, not just averages: a tool that's 95% accurate but fails on all asbestos pipe records may be unacceptable.

## Monitor after launch

Models are updated by providers, documents change and usage drifts. Keep sampling outputs, track complaints and errors, and re-run your evaluation set periodically.

> **Engineering parallel:** treat an AI tool like any instrument: calibrate it against known values, understand its error characteristics, and re-check it periodically.""",
    "key_points": [
        "Public benchmarks are a rough guide; contamination and saturation limit them.",
        "Build a test set from your own work with clear criteria, and re-run it after every change.",
        "Precision counts false alarms, recall counts misses; choose based on the cost of each.",
        "Design for automation bias, deskilling and accountability; pilot against a baseline and keep monitoring.",
    ],
    "figure_svg": EVALS,
    "figure_caption": "Precision is the share of flagged items that are real issues; recall is the share of real issues that got flagged.",
    "questions": [
        mcq("Why aren't public benchmark scores enough to choose a tool for your firm?", ["They're always fake", "They may not reflect your tasks and can be inflated by contamination", "They're too expensive", "They only test images"], 1,
            "Test on your own work."),
        mcq("An AI flags 50 clauses as non-compliant; 40 truly are. What's its precision?", ["40%", "80%", "50%", "Can't tell"], 1,
            "40 ÷ 50 = 80%."),
        mcq("In the diagram, what does recall measure?", ["How many flagged items were real", "How many real issues were found", "Speed", "Cost"], 1,
            "Found ÷ really defective.",
            EVALS, "Two overlapping circles: really defective and flagged by AI; overlap is found correctly; precision = found ÷ flagged, recall = found ÷ really defective."),
        mcq("For a safety-critical pre-check where a person reviews every flag, which metric usually matters most?", ["Precision", "Recall", "Speed", "Token count"], 1,
            "Misses are dangerous; false alarms just cost review time."),
        mcq("What is automation bias?", ["AI being biased against automation", "People over-trusting automated outputs", "A training error", "A benchmark"], 1,
            "Design reviews so people really check."),
        mcq("Why re-run your evaluation set when the provider updates the model?", ["It's free", "To catch regressions in performance on your tasks", "To retrain it", "Regulators require it hourly"], 1,
            "Updates can change behaviour."),
        mcq("In the diagram, what are the items in the blue-only part of the flagged circle?", ["Missed issues", "False alarms", "Correct finds", "Unflagged good items"], 1,
            "Flagged but not really defective.", EVALS, "Overlapping circles with the flagged-only region labelled false alarms."),
        open_q("Describe how you'd build an evaluation for an AI tool that extracts data from geotechnical reports.", "Collect a representative set of real reports including difficult ones, record the correct values for each field, run the tool on all of them, score accuracy per field and look for failure patterns, then re-run the set after any change to the model, prompts or setup.",
               ["representative real examples including hard cases", "known correct answers", "score and look for patterns", "re-run after changes"], "Exact-match scoring suits extraction."),
        open_q("Why can an AI with 95% average accuracy still be unacceptable?", "Because errors may cluster in important cases, such as one material type or safety-critical items, and the consequences of those specific errors may be severe; you need to look at failure patterns and the cost of errors, not just the average.",
               ["errors may cluster", "severe consequences in specific cases", "look at failure patterns"], "Averages hide tails."),
        open_q("What is the risk of deskilling and how might a firm manage it?", "If juniors rely on AI and never do tasks themselves, they may not develop the judgement to spot errors, weakening review; manage it with training that includes doing work manually, explaining AI outputs, mentoring and reviews that test understanding.",
               ["juniors may not build judgement", "weaker review", "training and mentoring"], "Capability building is part of adoption."),
    ],
}

L8 = {
    "title": "Risks, ethics and regulation",
    "minutes": 11,
    "photo_query": "",
    "body": """Knowing the risks and the rules is what separates a credible AI leader from an enthusiast. The rules are changing quickly, so learn the principles and check the current position before relying on details.

## The main risk areas

- **Accuracy and reliability**: hallucinations, errors in calculations, misread drawings, over-reliance.
- **Privacy**: personal information in prompts, uploads or training data. Under Australia's *Privacy Act 1988* and the Australian Privacy Principles, using personal information in AI tools must fit the purpose it was collected for, be secured, and be disclosed appropriately. Reforms passed in 2024 add transparency obligations about substantially automated decisions, commencing in late 2026; check the current requirements.
- **Confidentiality**: client and commercial information entered into tools whose terms allow retention or training. Use enterprise agreements that exclude training on your data, and check where data is stored.
- **Intellectual property**: unclear ownership of AI-generated content, and risk of reproducing copyrighted material. Contracts with clients may also restrict AI use.
- **Bias and fairness**: models learn biases in their data; matters most in decisions about people (hiring, performance) and communities (service prioritisation).
- **Security**: prompt injection, data leakage through agents, malicious use (better phishing), and insecure AI-written code.
- **Transparency**: people affected by AI-assisted decisions and clients receiving AI-assisted work may expect to be told.
- **Environmental and social**: energy and water use of data centres, effects on jobs and skills.

## Frameworks to know

- **Australia's AI Ethics Principles** (2019): eight voluntary principles including human, societal and environmental wellbeing, fairness, privacy and security, reliability and safety, transparency, contestability and accountability.
- **Australian Government guidance**: the National AI Centre's *Voluntary AI Safety Standard* (2024) was followed by *Guidance for AI Adoption* (2025), setting out essential practices such as deciding who is accountable, understanding impacts, measuring and managing risk, sharing essential information, testing and monitoring, and maintaining human control. Government signalled in late 2025 that it would rely mainly on existing laws (privacy, consumer, anti-discrimination, safety) plus guidance rather than a standalone AI Act. Check for updates.
- **ISO/IEC 42001** (2023): a certifiable **AI management system** standard, like ISO 9001 for quality, increasingly asked about in tenders.
- **NIST AI Risk Management Framework** (US): Govern, Map, Measure, Manage; widely used as a practical structure.
- **EU AI Act**: risk-based law (prohibited, high-risk, limited-risk transparency, minimal) with obligations phasing in from 2025 onwards; relevant if you work with EU clients or products. Timelines have been subject to change.

## Professional responsibility

For engineers, AI changes the tools, not the duty. Engineers Australia's Code of Ethics requires competence, honesty and acting in the public interest. You remain responsible for work you sign, so you need to understand AI-assisted outputs well enough to stand behind them, keep records of how important work was produced, and be honest with clients about AI use where it matters. Professional indemnity insurers and clients are increasingly asking about AI practices.

## Practical controls for a firm

- An **AI use policy**: approved tools, data rules (what can and can't be entered), review requirements, disclosure.
- A register of **AI use cases** with risk ratings.
- **Training** for staff on safe and effective use.
- Clear **accountability** for each AI system and for outputs.
- **Vendor due diligence**: data handling, security, location, training use.
- **Incident reporting** for AI errors and near misses.

## Safety and alignment

Beyond today's practical risks, AI developers and governments are working on longer-term safety: making sure more capable systems reliably do what people intend (**alignment**), can't be easily misused, and are tested for dangerous capabilities before release. Several countries, including Australia, have set up AI safety bodies. You don't need to be an expert, but understanding the debate helps you speak credibly.

> **The leadership stance:** neither hype nor fear. Enable people to use AI productively, with clear guardrails that protect clients, the public and the firm.""",
    "key_points": [
        "Key risks: accuracy, privacy, confidentiality, IP, bias, security, transparency and wider impacts.",
        "Australia relies on its AI Ethics Principles, government guidance on AI adoption and existing laws such as the Privacy Act.",
        "ISO/IEC 42001, the NIST AI RMF and the EU AI Act give structure; check current timelines.",
        "Engineers stay professionally responsible; firms need policy, training, accountability, vendor checks and incident reporting.",
    ],
    "figure_svg": RISK,
    "figure_caption": "Govern, map, measure, manage: a repeating cycle for managing AI risk, supported by recognised frameworks.",
    "questions": [
        mcq("Which Australian law most directly governs personal information entered into AI tools?", ["The Water Act", "The Privacy Act 1988 and Australian Privacy Principles", "The Corporations Act only", "None"], 1,
            "APPs apply to AI use of personal information."),
        mcq("What is ISO/IEC 42001?", ["A cybersecurity patch", "A certifiable AI management system standard", "A pipe standard", "An AI model"], 1,
            "Like ISO 9001, but for managing AI."),
        mcq("In the diagram, what are the four functions of the NIST AI RMF?", ["Plan, Do, Check, Act", "Govern, Map, Measure, Manage", "Design, Build, Test, Deploy", "Collect, Train, Evaluate, Release"], 1,
            "A practical structure for AI risk.",
            RISK, "Four boxes in a cycle: Govern (policy, roles), Map (use and context), Measure (test, evaluate), Manage (controls); risks and frameworks listed below."),
        mcq("An engineer signs a report partly drafted by AI. Who is responsible for its accuracy?", ["The AI vendor", "The engineer", "Nobody", "The client"], 1,
            "AI changes the tools, not the duty."),
        mcq("Why prefer an enterprise AI agreement over a free consumer tool for client work?", ["It's more fun", "Enterprise terms typically exclude training on your data and offer security and data location controls", "Consumer tools are illegal", "Enterprise tools never hallucinate"], 1,
            "Confidentiality is the main reason."),
        mcq("How does the EU AI Act classify AI systems?", ["By model size only", "By risk level: prohibited, high-risk, limited-risk transparency and minimal", "By country of origin", "It doesn't"], 1,
            "Obligations depend on the risk level."),
        mcq("In the diagram, why does the cycle repeat?", ["To use more paper", "Because systems, their uses and risks change over time", "Regulators require monthly audits", "It doesn't"], 1,
            "Risk management is ongoing.", RISK, "The four functions connected by a return arrow labelled repeat as the system and its use change."),
        open_q("List the key elements of an AI use policy for an engineering consultancy.", "Approved tools; data rules saying what can and can't be entered, especially client confidential and personal information; review and sign-off requirements for AI-assisted work; disclosure to clients where appropriate; training; accountability; and how to report AI errors or incidents.",
               ["approved tools", "data rules for confidential and personal information", "review and sign-off", "disclosure and incident reporting"], "Keep it short enough that people read it."),
        open_q("Why might a client contract affect whether you can use AI on a project?", "Contracts can include confidentiality, data handling, data location, IP ownership or explicit AI clauses that restrict entering client information into tools or require disclosure or approval, so check before using AI on their information.",
               ["confidentiality and data clauses", "IP ownership", "may need disclosure or approval"], "Government and utility clients often have specific rules."),
        open_q("Explain the 'neither hype nor fear' leadership stance on AI.", "A good AI leader neither oversells AI nor blocks it: they help people use it productively where it adds value, while putting clear, proportionate guardrails in place for accuracy, privacy, confidentiality and accountability to protect clients, the public and the firm.",
               ["enable productive use", "proportionate guardrails", "protect clients, public and firm"], "Credibility comes from balance."),
    ],
}

PACK = {
    "id": "ai-general",
    "version": 1,
    "topic": "Artificial intelligence",
    "title": "How AI works",
    "summary": "A clear, accurate grounding in modern AI: machine learning, neural networks, transformers and LLMs, what models are good and bad at, tools, RAG and agents, evaluating AI properly, and the risks, ethics and rules (with an Australian focus). For professionals who want to be the go-to person on AI.",
    "icon": "brain",
    "level": "intermediate",
    "length": "standard",
    "area": "technology",
    "tags": ["ai", "machine-learning", "llms", "ai-governance", "ai-literacy"],
    "sections": [
        {"title": "Foundations", "summary": "What AI is and how it learns.", "lessons": [
            {"title": L1["title"], "summary": "Explain AI, ML, deep learning and generative AI clearly.", "lesson": L1},
            {"title": L2["title"], "summary": "Describe how models learn from data and why they fail.", "lesson": L2},
            {"title": L3["title"], "summary": "Understand neural networks, embeddings and architectures.", "lesson": L3},
            {"title": L4["title"], "summary": "Explain tokens, attention and how LLM assistants are built.", "lesson": L4},
        ]},
        {"title": "Capabilities, limits and governance", "summary": "Using AI with judgement.", "lessons": [
            {"title": L5["title"], "summary": "Know where AI is reliable and how to calibrate trust.", "lesson": L5},
            {"title": L6["title"], "summary": "Understand multimodal AI, tools, RAG and agents.", "lesson": L6},
            {"title": L7["title"], "summary": "Evaluate AI systems with real tests and metrics.", "lesson": L7},
            {"title": L8["title"], "summary": "Manage AI risks and know the main frameworks and rules.", "lesson": L8},
        ]},
    ],
}
