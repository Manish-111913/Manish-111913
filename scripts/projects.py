"""The nine project cards. Every node, number and claim here was checked against the project's code
or documents; anything that could not be checked is drawn as "planned" or "not verified".

Diagram coordinates are inside the 843-px-wide diagram box. Node kinds:
    io (input/output), proc (step), hot (core step), store (data), ext (external service),
    decision, planned (dashed), unverified (dotted).
Edges run from node a to node b; sa/sb pick the side (l r t b), mx/my move the bend,
ay/by attach at a given height, via gives explicit bend points, dashed marks a not-built link.
build_svgs.py refuses to build a card whose text does not fit its boxes.
"""


def N(id, x, y, w, h, t, s=None, kind="proc", icon=None):
    return {"id": id, "x": x, "y": y, "w": w, "h": h, "t": t, "s": s, "kind": kind, "icon": icon}


def E(a, b, sa="r", sb="l", **kw):
    return dict(a=a, b=b, sa=sa, sb=sb, **kw)


def S(t, m, kind="proc"):
    """One numbered step: title and a one-line explanation (used on mobile and in the README)."""
    return {"t": t, "m": m, "kind": kind}


PROJECTS = [
    # ---------------------------------------------------------------------------- 01
    {
        "key": "medivorax",
        "name": "MEDIVORAX",
        "subtitle": "Hospital pharmacy operations platform · Next.js · NestJS · PostgreSQL · OCR",
        "badge": ("IN PROGRESS", "warn"),
        "icons": ["nextjs", "nestjs", "postgresql", "python"],
        "summary": "A multi-hospital pharmacy platform where supplier bills are read by OCR, stock is tracked in an "
                   "append-only ledger, and a 252,678-medicine catalogue powers search and substitutes.",
        "problem": "Hospital pharmacies juggle supplier bills, stock, billing and a huge medicine catalogue in separate "
                   "places. MEDIVORAX brings them onto one platform, with each hospital's data kept in its own database schema.",
        "diagram": {
            "h": 264,
            "labels": [(18, 16, "SCAN A SUPPLIER BILL"), (18, 112, "FIND A MEDICINE")],
            "nodes": [
                N("bill", 18, 26, 124, 50, "Upload bill", "Next.js app", "io"),
                N("api", 160, 26, 124, 146, "NestJS API", "JWT · tenant", "hot"),
                N("ocr", 302, 26, 124, 50, "OCR service", "PaddleOCR"),
                N("match", 444, 26, 128, 50, "Extract + match", "pg_trgm ≥ 0.5"),
                N("ok", 590, 18, 92, 66, "Staff\nconfirms?", kind="decision"),
                N("ledger", 712, 26, 113, 50, "Stock ledger", "append-only", "store"),
                N("q", 18, 122, 124, 50, "Search", "name · salt", "io"),
                N("rank", 302, 122, 124, 50, "Rank matches", "exact→trgm"),
                N("cat", 444, 122, 146, 50, "Medicine catalog", "252,678 records", "store"),
                N("res", 608, 122, 217, 50, "Results + substitutes", "same salt, in stock", "io"),
            ],
            "edges": [
                E("bill", "api", by=51), E("api", "ocr", ay=51), E("ocr", "match"), E("match", "ok"),
                E("ok", "ledger", label="yes"),
                E("q", "api", by=147), E("api", "rank", ay=147), E("rank", "cat"), E("cat", "res"),
            ],
            "notes": [(594, 98, "no → nothing is saved")],
            "chips": [(192, "BUILT", ["Inventory + FEFO", "POS billing", "Returns", "Purchase orders", "Wastage", "Reports"], "built"),
                      (220, "PLANNED", ["AI copilot", "Diagnostics", "QR prescriptions", "Demand prediction"], "planned")],
        },
        "stack": [("Frontend", "Next.js 16 · React 19 · TypeScript · Tailwind 4"),
                  ("Backend", "NestJS 11 · SQL via pg · JWT · argon2"),
                  ("Data", "PostgreSQL · pg_trgm · one schema per hospital"),
                  ("OCR", "Python · FastAPI · PaddleOCR")],
        "stack_note": "No LLM, embeddings or semantic search in the code yet: medicine search is lexical + trigram.",
        "decision": ("FROM THE CODE",
                     "Each hospital gets its own database schema, cloned from a template, while the 252,678-medicine "
                     "catalogue lives once in a shared read-only schema. Hospitals stay isolated without copying the catalogue for each one."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "One platform for many workflows gives staff one place to look, but every new module has to respect "
                     "tenant boundaries and the ledger's rules, and schema-per-tenant means each migration runs once per hospital."),
        "steps": [
            S("Staff uploads a supplier bill", "A photo, PDF or spreadsheet, sent from the Next.js app.", "io"),
            S("NestJS API checks the request", "Verifies the JWT and membership, then selects that hospital's schema.", "hot"),
            S("OCR service reads the bill", "FastAPI + PaddleOCR; PDFs that already contain text skip OCR."),
            S("Lines are extracted and matched", "Invoice number, GSTIN and items; each item matched to the catalogue by brand and trigram similarity."),
            S("Staff confirms the suggestions", "Nothing changes stock until a person approves; a wrong match is worse than a blank.", "decision"),
            S("Stock ledger is updated", "Purchase invoice, batches and an append-only stock movement are written.", "store"),
            S("Staff searches for a medicine", "By name, code or composition; ranked exact → prefix → trigram over 252,678 records.", "io"),
            S("Results and substitutes appear", "Substitutes are in-stock medicines with exactly the same composition.", "io"),
        ],
        "links": [],
    },
    # ---------------------------------------------------------------------------- 02
    {
        "key": "sentilex",
        "name": "SENTILEX",
        "subtitle": "Explainable network intrusion detection · XGBoost · SHAP · FastAPI · React",
        "badge": ("RESEARCH PROTOTYPE", "blue"),
        "icons": ["python", "fastapi", "react", "ollama"],
        "summary": "An intrusion-detection prototype that classifies network flows, explains each alert with SHAP and an "
                   "LLM narrative it fact-checks, and only then proposes a simulated response.",
        "problem": "Intrusion detectors usually say \"attack\" without saying why. SENTILEX classifies network flows, shows "
                   "which traffic features drove each alert, writes a plain-English explanation and checks it before proposing a simulated response.",
        "diagram": {
            "h": 314,
            "groups": [(8, 8, 827, 76, "TRAINING · OFFLINE"), (8, 94, 827, 198, "DETECTION · EVERY FLOW")],
            "nodes": [
                N("ds", 18, 30, 140, 44, "CICIDS2017", "7 classes", "store"),
                N("prep", 176, 30, 150, 44, "Clean + split", "60/20/20 · scaler"),
                N("train", 344, 30, 166, 44, "Train two models", "XGBoost · Keras MLP"),
                N("art", 528, 30, 160, 44, "Model artifacts", "+ SHAP explainer", "store"),
                N("flow", 18, 118, 118, 50, "Flow replay", "CSV / parquet", "io"),
                N("det", 154, 118, 124, 50, "Classify", "XGBoost or MLP", "hot"),
                N("atk", 296, 108, 92, 70, "Attack?", kind="decision"),
                N("alert", 414, 118, 118, 50, "Alert + SHAP", "top features"),
                N("llm", 548, 118, 124, 50, "LLM narrative", "Ollama llama3.1", "ext"),
                N("efm", 690, 118, 135, 50, "Check claims", "EFM faithfulness"),
                N("stored", 282, 208, 120, 50, "Stored flow", "no alert"),
                N("view", 414, 208, 118, 50, "Analyst view", "React · LIME"),
                N("kb", 548, 208, 124, 50, "ATT&CK index", "ChromaDB", "store"),
                N("act", 690, 208, 135, 50, "Response", "SIMULATED ONLY"),
            ],
            "edges": [
                E("ds", "prep"), E("prep", "train"), E("train", "art"),
                E("art", "det", sa="b", sb="t", my=89, label="load"),
                E("flow", "det"), E("det", "atk"), E("atk", "alert", label="yes"),
                E("atk", "stored", sa="b", sb="t", label="no"),
                E("alert", "llm"), E("kb", "llm", sa="t", sb="b"), E("llm", "efm"),
                E("alert", "view", sa="b", sb="t"),
                E("efm", "act", sa="b", sb="t"),
                E("act", "view", sa="b", sb="b", my=276, label="approve"),
            ],
            "notes": [(706, 48, "other datasets never"), (706, 61, "replace the live model")],
        },
        "stack": [("Frontend", "React 19 · TypeScript · Vite"),
                  ("Backend", "FastAPI · SQLAlchemy · WebSocket"),
                  ("ML", "XGBoost · Keras MLP · SHAP · LIME"),
                  ("AI", "ChromaDB · Ollama llama3.1:8b"),
                  ("Data", "SQLite"), ("Infra", "Docker Compose")],
        "stack_note": "Named SentinelX in the code. Traffic is replayed from dataset files; prevention only writes rows to a rules table.",
        "decision": ("FROM THE CODE",
                     "No response happens on a model's word alone. Every proposed action needs a justification: SHAP evidence, "
                     "a narrative and a faithfulness score. A low score sends it back to a person, even under an automatic policy."),
        "tradeoff": ("DATASET RESULT, NOT LIVE",
                     "XGBoost reached 0.996 macro-F1 on held-out CICIDS2017 flows; that is a dataset result, not proof on a live "
                     "network. Explanations cost time too: the narrative and its check take about 50 s on a CPU, so they run after the alert."),
        "steps": [
            S("Train offline", "Clean CICIDS2017, split 60/20/20, train XGBoost and a Keras MLP, save the SHAP explainer."),
            S("Replay network flows", "Rows from a CICIDS-format file stand in for live traffic.", "io"),
            S("Classify each flow", "XGBoost by default; the MLP is a selectable baseline.", "hot"),
            S("Attack or benign?", "Benign or below its class threshold: stored as a flow, no alert.", "decision"),
            S("Create the alert with SHAP", "The features that pushed the prediction are saved with it; LIME is available on request."),
            S("Find matching ATT&CK techniques", "ChromaDB looks up related MITRE ATT&CK techniques and mitigations.", "store"),
            S("Write the explanation", "Ollama (llama3.1:8b) explains the alert using only the evidence it is given.", "ext"),
            S("Check the explanation", "EFM scores whether its claims match the evidence; low scores need a human."),
            S("Simulated prevention", "A rule row is added or suggested in the database; no real firewall is touched."),
            S("Analyst reviews and approves", "React dashboard with alerts, explanations and pending actions.", "io"),
        ],
        "links": [],
    },
    # ---------------------------------------------------------------------------- 03
    {
        "key": "indusmind",
        "name": "IndusMind",
        "subtitle": "Industrial knowledge intelligence · FastAPI · pgvector · Neo4j · React",
        "badge": ("IN PROGRESS", "warn"),
        "icons": ["python", "fastapi", "postgresql", "neo4j", "react"],
        "summary": "A plant-knowledge platform that ingests manuals, drawings and logs, then answers engineers' questions "
                   "with hybrid retrieval and citations it verifies.",
        "problem": "Plant knowledge is buried in manuals, drawings, shift logs and regulations. IndusMind ingests those documents "
                   "and lets engineers ask questions in plain language, with answers that cite the exact source passages.",
        "diagram": {
            "h": 302,
            "groups": [(8, 8, 827, 140, "INGEST · CELERY WORKER"), (8, 158, 827, 124, "ASK · COPILOT")],
            "nodes": [
                N("docs", 18, 30, 128, 48, "Plant docs", "PDF·docx·xlsx", "io"),
                N("s3", 164, 30, 112, 48, "MinIO / S3", "originals", "store"),
                N("read", 294, 30, 124, 48, "Read text", "PyMuPDF · OCR"),
                N("chunk", 436, 30, 112, 48, "Chunk", "400–600 tokens"),
                N("emb", 566, 30, 112, 48, "Embed", "bge-large"),
                N("pg", 696, 30, 129, 48, "pgvector", "Postgres · HNSW", "store"),
                N("ent", 436, 92, 112, 44, "Entities", "rules + LLM"),
                N("neo", 566, 92, 128, 44, "Neo4j graph", "equipment·docs", "store"),
                N("q", 18, 184, 118, 50, "Question", "React app", "io"),
                N("cache", 154, 176, 92, 66, "Cached\nanswer?", kind="decision"),
                N("ret", 264, 184, 156, 50, "Hybrid retrieval", "vector + full-text", "hot"),
                N("llm", 438, 184, 128, 50, "LLM answer", "Claude (default)", "ext"),
                N("cite", 584, 184, 118, 50, "Verify cites", "drop bad [n]"),
                N("ans", 720, 184, 105, 50, "Answer", "with sources", "io"),
            ],
            "edges": [
                E("docs", "s3"), E("s3", "read"), E("read", "chunk"), E("chunk", "emb"), E("emb", "pg"),
                E("chunk", "ent", sa="b", sb="t"), E("ent", "neo"),
                E("pg", "ret", sa="b", sb="t", my=153, label="top-40 each · RRF"),
                E("q", "cache"), E("cache", "ret", label="no"), E("ret", "llm"), E("llm", "cite"), E("cite", "ans"),
                E("cache", "ans", sa="b", sb="b", my=266, label="yes"),
            ],
        },
        "stack": [("Frontend", "React 19 · Vite · Tailwind 4"),
                  ("Backend", "FastAPI · Celery · Redis"),
                  ("Data", "PostgreSQL + pgvector · Neo4j · MinIO / S3"),
                  ("AI", "bge-large embeddings · Claude by default (OpenAI, Gemini, Ollama optional)"),
                  ("OCR", "PyMuPDF · PaddleOCR · Tesseract")],
        "stack_note": "Not in the code: Elasticsearch, Pinecone, LangChain, Next.js, or a reranker.",
        "decision": ("FROM THE CODE",
                     "Retrieval is hybrid: pgvector similarity and Postgres full-text search, merged with Reciprocal Rank Fusion. "
                     "Keywords catch exact equipment tags, vectors catch paraphrases, and every citation is checked against what was retrieved."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "Each extra store improves one kind of lookup but adds indexing work and another copy to keep fresh. Neo4j is "
                     "rebuilt from Postgres so a graph failure never blocks ingestion, at the cost of the graph possibly lagging behind."),
        "steps": [
            S("Upload plant documents", "Manuals, P&IDs, shift logs, regulations; originals stored in MinIO / S3.", "io"),
            S("Read the text", "PyMuPDF text layer; scanned pages through PaddleOCR, Tesseract as fallback."),
            S("Split into chunks", "400–600 tokens with 15% overlap; tables stay whole."),
            S("Embed and index", "bge-large vectors in pgvector (HNSW) plus a Postgres full-text index.", "store"),
            S("Extract entities into a graph", "Rules plus an optional LLM pass, projected into Neo4j for the graph explorer.", "store"),
            S("An engineer asks a question", "In plain language, from the React app.", "io"),
            S("Already answered?", "Near-identical questions (cosine ≥ 0.97) reuse a cached answer for 24 hours.", "decision"),
            S("Hybrid retrieval", "Vector top-40 + full-text top-40, fused with RRF; equipment tags boost their documents.", "hot"),
            S("Generate the answer", "An LLM (Claude by default) answers from numbered context blocks.", "ext"),
            S("Verify the citations", "Any [n] that doesn't point to a retrieved chunk is removed.", "io"),
        ],
        "links": [("Source code", "https://github.com/Manish-111913/INDUS_MIND")],
    },
    # ---------------------------------------------------------------------------- 04
    {
        "key": "campus",
        "name": "3D Campus Tour",
        "subtitle": "Browser 3D campus explorer · Three.js · Express · MongoDB",
        "icons": ["threedotjs", "javascript", "nodejs", "mongodb"],
        "summary": "A browser tour where visitors walk through 3D models of campus locations and open hotspots that "
                   "explain each spot; admins place and edit the hotspots.",
        "problem": "Not everyone can visit a campus in person. This tour lets visitors walk through 3D models of campus "
                   "locations in the browser and open hotspots that explain what they are looking at, with nothing to install.",
        "diagram": {
            "h": 262,
            "labels": [(18, 16, "IN THE BROWSER"), (296, 140, "SERVER + FILES")],
            "nodes": [
                N("in", 18, 26, 118, 50, "Sign in", "JWT session", "io"),
                N("pick", 154, 26, 124, 50, "Pick a place", "5 locations"),
                N("load", 296, 26, 136, 50, "Load 3D model", "GLTFLoader·.glb", "hot"),
                N("hs", 450, 26, 124, 50, "Get hotspots", "per model"),
                N("walk", 592, 26, 112, 50, "Walk around", "WASD · mouse"),
                N("click", 722, 18, 103, 66, "Hotspot\nclicked?", kind="decision"),
                N("admin", 18, 150, 118, 50, "Admin edits", "place hotspots", "io"),
                N("glb", 296, 150, 136, 50, ".glb models", "static files", "store"),
                N("api", 450, 150, 124, 50, "Express API", "JWT · roles"),
                N("db", 592, 150, 112, 50, "MongoDB", "hotspots·users", "store"),
                N("info", 722, 150, 103, 50, "Info card", "tooltip", "io"),
            ],
            "edges": [
                E("in", "pick"), E("pick", "load"), E("load", "hs"), E("hs", "walk"), E("walk", "click"),
                E("click", "info", sa="b", sb="t", label="yes"),
                E("glb", "load", sa="t", sb="b", label="download"),
                E("hs", "api", sa="b", sb="t", label="GET"), E("api", "db"),
                E("admin", "api", sa="b", sb="b", my=222, label="save · admin only"),
            ],
        },
        "stack": [("Frontend", "HTML · CSS · JavaScript · Three.js r128 (WebGL)"),
                  ("3D", "GLTFLoader · pointer-lock controls · raycasting"),
                  ("Backend", "Node.js · Express · JWT · bcrypt"),
                  ("Data", "MongoDB Atlas (Mongoose)"),
                  ("Hosting", "Netlify (site) · Render (API)")],
        "stack_note": "The public repos show 5 locations as 3D models; no panoramas or React Three Fiber.",
        "decision": ("FROM THE CODE",
                     "Hotspots are stored as 3D coordinates in MongoDB rather than baked into the models, so an admin can place, "
                     "drag and edit them in the browser without re-exporting a single model file."),
        "tradeoff": ("SEEN IN THE CODE",
                     "Full 3D models feel more real than flat photos, but each .glb must download before its scene appears and "
                     "uses GPU memory. The app frees the previous model on every switch: memory stays flat, but going back means reloading it."),
        "steps": [
            S("Sign in", "Email and password; the Express API returns a JWT.", "io"),
            S("Pick a place", "The location list comes from the API: 5 places in the current build."),
            S("Load the 3D model", "Three.js GLTFLoader fetches the .glb; the previous model is disposed first.", "hot"),
            S("Fetch the hotspots", "Hotspots for this model come from MongoDB through the API."),
            S("Walk around", "First-person controls with WASD and the mouse."),
            S("Hotspot clicked?", "Raycasting finds the hotspot under the cursor.", "decision"),
            S("Show the info card", "A tooltip explains that spot.", "io"),
            S("Admins edit hotspots", "Add, drag and edit; changes are saved through the API (admin role only)."),
        ],
        "links": [("Frontend", "https://github.com/Manish-111913/3D-CAMPUS-TOUR-FRONTEND"),
                  ("Backend", "https://github.com/Manish-111913/3D-CAMPUS-TOUR-BACKEND")],
    },
    # ---------------------------------------------------------------------------- 05
    {
        "key": "jewellery",
        "name": "AI Jewellery Design",
        "subtitle": "Sketch-to-design generation with a Pix2Pix GAN · Python · TensorFlow · OpenCV",
        "icons": ["python", "tensorflow", "opencv"],
        "summary": "A Pix2Pix conditional GAN, trained on paired sketches and images, that turns a new jewellery sketch "
                   "into a realistic design concept.",
        "problem": "Turning a jewellery sketch into a realistic concept can take a CAD artist hours. This project trains a "
                   "Pix2Pix conditional GAN on paired sketches and images, so a new sketch becomes a design concept in a single pass.",
        "diagram": {
            "h": 272,
            "groups": [(8, 8, 827, 130, "TRAINING · ONCE"), (8, 148, 827, 98, "GENERATING · EVERY SKETCH")],
            "nodes": [
                N("pairs", 18, 32, 128, 48, "Paired images", "sketch ↔ image", "store"),
                N("pre", 164, 32, 116, 48, "Preprocess", "OpenCV"),
                N("gen", 298, 32, 128, 48, "Generator", "U-Net", "hot"),
                N("disc", 444, 32, 134, 48, "Discriminator", "PatchGAN: real?"),
                N("upd", 596, 32, 106, 48, "Update", "GAN + L1"),
                N("w", 720, 32, 105, 48, "Saved model", "generator", "store"),
                N("sk", 18, 174, 128, 48, "New sketch", "line drawing", "io"),
                N("pre2", 164, 174, 116, 48, "Preprocess", "to [-1, 1]"),
                N("gen2", 298, 174, 128, 48, "Generator", "one pass", "hot"),
                N("out", 444, 174, 134, 48, "Design concept", "generated image"),
                N("rev", 596, 174, 229, 48, "Designer reviews", "a concept, not a CAD model", "io"),
            ],
            "edges": [
                E("pairs", "pre"), E("pre", "gen"), E("gen", "disc"), E("disc", "upd"), E("upd", "w"),
                E("upd", "gen", sa="b", sb="b", my=108, label="repeat"),
                E("w", "gen2", sa="b", sb="t", my=143, label="load weights"),
                E("sk", "pre2"), E("pre2", "gen2"), E("gen2", "out"), E("out", "rev"),
            ],
            "notes": [(18, 238, "the discriminator is only used during training")],
        },
        "stack": [("ML", "Python · TensorFlow · Pix2Pix conditional GAN"), ("Images", "OpenCV")],
        "stack_note": "From project documentation; the source code was not available to review, and no accuracy figure is claimed.",
        "decision": ("ARCHITECTURAL CONSIDERATION",
                     "Pix2Pix is conditional: it learns to map this sketch to this image from paired examples, so the result "
                     "follows the sketch's outlines instead of inventing a new piece. Its L1 loss keeps shapes close to the target."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "Paired data is costly to collect, and a GAN trained on a narrow set of styles can produce blurry or odd "
                     "results for sketches unlike anything it saw. Training is the slow part; generating a design is one fast pass."),
        "steps": [
            S("Collect paired images", "Each sketch has a matching target image.", "store"),
            S("Preprocess", "OpenCV resizes and cleans every image the same way."),
            S("Generator draws", "A U-Net generator turns a sketch into an image.", "hot"),
            S("Discriminator judges", "A PatchGAN checks image patches for realism (training only)."),
            S("Update both networks", "Adversarial loss + L1 loss; repeat across the dataset."),
            S("Save the generator", "Only the generator is needed after training.", "store"),
            S("A new sketch comes in", "Normalised exactly like the training data.", "io"),
            S("Generate a concept", "One forward pass through the trained generator.", "hot"),
            S("Designer reviews it", "A visual concept, not a manufacturable CAD model.", "io"),
        ],
        "links": [],
    },
    # ---------------------------------------------------------------------------- 06
    {
        "key": "ranking",
        "name": "Candidate Ranking",
        "subtitle": "Semantic matching + cross-encoder reranking · FastAPI · Next.js",
        "badge": ("REDROB DATA & AI CHALLENGE", "blue"),
        "icons": ["python", "fastapi", "huggingface", "nextjs"],
        "summary": "Ranks 100,000 candidate profiles against a job description: a fast combined score for everyone, "
                   "then a cross-encoder rerank of the shortlist, returning a top 100 with score breakdowns.",
        "problem": "No one can read 100,000 profiles for one job. This system scores every candidate against a job description, "
                   "sends only a shortlist through a slower, more precise model, and returns a top 100 with the reasons behind each score.",
        "diagram": {
            "h": 302,
            "groups": [(8, 8, 827, 104, "PREPARE ONCE · OFFLINE"), (8, 122, 827, 162, "RANK FOR ONE JOB")],
            "nodes": [
                N("prof", 18, 32, 140, 48, "100,000 profiles", "candidates.jsonl", "store"),
                N("val", 176, 32, 122, 48, "Validate", "normalise fields"),
                N("txt", 316, 32, 136, 48, "Profile text", "role·skills·summary"),
                N("emb", 470, 32, 150, 48, "Embed", "MiniLM-L6 · 384-d"),
                N("mat", 638, 32, 187, 48, "Embedding matrix", "NumPy .npy · no vector DB", "store"),
                N("jd", 18, 150, 140, 50, "Job post", "JD + overrides", "io"),
                N("score", 176, 150, 170, 50, "Score everyone", "semantic + rule signals", "hot"),
                N("short", 364, 150, 106, 50, "Shortlist", "top ≤ 300"),
                N("ce", 488, 150, 150, 50, "Cross-encoder", "MS MARCO MiniLM"),
                N("blend", 656, 150, 169, 50, "Blend + top 100", "0.4 rule · 0.6 CE"),
                N("llm", 364, 224, 210, 46, "LLM (optional mode)", "Gemini / OpenAI · JD, chat", "ext"),
                N("ui", 656, 224, 169, 46, "Recruiter reviews", "Next.js dashboard", "io"),
            ],
            "edges": [
                E("prof", "val"), E("val", "txt"), E("txt", "emb"), E("emb", "mat"),
                E("mat", "score", sa="b", sb="t", my=117, label="load"),
                E("jd", "score"), E("score", "short"), E("short", "ce"), E("ce", "blend"),
                E("blend", "ui", sa="b", sb="t"), E("llm", "ui"),
            ],
        },
        "stack": [("Frontend", "Next.js 15 · React 19 · TypeScript · Tailwind 4"),
                  ("Backend", "FastAPI · live progress over SSE"),
                  ("Models", "all-MiniLM-L6-v2 bi-encoder · ms-marco-MiniLM-L-6-v2 cross-encoder"),
                  ("Search", "NumPy dot product, no vector DB"), ("Infra", "Docker · Hugging Face Spaces")],
        "decision": ("FROM THE CODE",
                     "Embeddings for all 100,000 profiles are computed once, offline. At query time a cheap combined score ranks "
                     "everyone, and the expensive cross-encoder reads only a shortlist of at most 300 job-candidate pairs, never the full pool."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "A wider shortlist improves recall but slows the cross-encoder. Scores also weigh location and education tier, "
                     "and the code has no bias audit, so the ranking supports a recruiter's review rather than replacing it."),
        "steps": [
            S("Load 100,000 profiles", "Validated and normalised from the challenge dataset.", "store"),
            S("Build one text per profile", "Title, headline, summary, last 3 roles and top 8 skills."),
            S("Embed once, offline", "all-MiniLM-L6-v2 gives a 100,000 × 384 NumPy matrix saved to disk.", "store"),
            S("A job description comes in", "Requirements, plus overrides from the UI.", "io"),
            S("Score every candidate", "Cosine similarity combined with skills, career, experience, location and education signals.", "hot"),
            S("Keep a shortlist", "Top 300, or 30% of a smaller pool."),
            S("Rerank with a cross-encoder", "Reads each job-candidate pair together for a sharper relevance score."),
            S("Blend and cut to 100", "0.4 × rule score + 0.6 × cross-encoder score."),
            S("Recruiter reviews", "Score breakdowns, reasoning and CSV export in the dashboard.", "io"),
        ],
        "links": [("Source code", "https://github.com/Manish-111913/AI-JD")],
    },
    # ---------------------------------------------------------------------------- 07
    {
        "key": "ecosphere",
        "name": "EcoSphere",
        "subtitle": "Enterprise ESG management platform · NestJS · Prisma · PostgreSQL · React",
        "badge": ("ODOO HACKATHON FINALIST", "gold"),
        "icons": ["nestjs", "prisma", "postgresql", "react"],
        "summary": "An ESG platform that collects environmental, social and governance records, scores departments and the "
                   "organisation, and runs reports and approvals by role.",
        "problem": "Sustainability data usually lives in scattered spreadsheets. EcoSphere collects environmental, social and "
                   "governance records in one system, turns them into department and company ESG scores, and produces reports people review.",
        "diagram": {
            "h": 274,
            "nodes": [
                N("in", 18, 26, 128, 50, "ESG data in", "forms · import", "io"),
                N("guard", 164, 26, 140, 50, "Guard + validate", "JWT · permission"),
                N("db", 322, 26, 130, 50, "PostgreSQL", "Prisma models", "store"),
                N("co2", 470, 26, 140, 50, "CO2e calculation", "qty × factor"),
                N("score", 628, 26, 197, 50, "ESG scoring", "E/S/G weights · daily", "hot"),
                N("appr", 164, 136, 140, 50, "Approval queue", "CSR·policy·audit"),
                N("rev", 322, 136, 130, 50, "Human review", "compliance team", "io"),
                N("rep", 470, 136, 140, 50, "Reports", "CSV · XLSX"),
                N("dash", 628, 136, 197, 50, "Role dashboards", "React · Recharts"),
            ],
            "edges": [
                E("in", "guard"), E("guard", "db"), E("db", "co2"), E("co2", "score"),
                E("score", "dash", sa="b", sb="t"), E("dash", "rep", sa="l", sb="r"), E("rep", "rev", sa="l", sb="r"),
                E("guard", "appr", sa="b", sb="t", label="needs sign-off"), E("appr", "rev"),
            ],
            "chips": [(204, "ACCESS", ["7 roles", "permission per action", "data scope: own · dept · all", "audit log"], "built"),
                      (232, "NOT YET", ["PDF export", "email delivery"], "planned")],
        },
        "stack": [("Frontend", "React 19 · Vite · TypeScript · Tailwind 4 · Recharts"),
                  ("Backend", "NestJS 10 · class-validator · scheduled jobs"),
                  ("Data", "PostgreSQL 16 · Prisma 5"),
                  ("Auth", "JWT + rotating refresh tokens · argon2")],
        "stack_note": "Built for the Odoo Hackathon brief but implemented on NestJS + React; there are no Odoo modules in the code.",
        "decision": ("FROM THE CODE",
                     "Behaviour lives in database configuration rather than code: permissions, ESG weights, approval rules and state "
                     "transitions. Each calculation also stores the factor or weights it used, so past results don't shift when settings change."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "Configurable workflows let each organisation adapt the platform without code changes, but every rule becomes "
                     "data that must be kept accurate: a wrong weight or factor quietly skews scores until someone reviews it."),
        "steps": [
            S("Enter ESG data", "Operational records, CSR activities, training, diversity and policies, by form or file import.", "io"),
            S("Guard and validate", "JWT, a permission check per action and input validation; every write is audit-logged."),
            S("Store the records", "PostgreSQL via Prisma, with separate environmental, social and governance models.", "store"),
            S("Calculate CO2e", "Quantity × the active emission factor, with the factor saved alongside the result."),
            S("Score departments and the company", "Metrics normalised and weighted into E, S and G scores, recomputed daily.", "hot"),
            S("Role dashboards", "Each role sees its own view, built with React and Recharts."),
            S("Reports", "Environmental, social, governance and summary reports; CSV and XLSX export."),
            S("Human review", "Approvals for CSR participation, policies, audits and compliance issues.", "io"),
        ],
        "links": [("Source code", "https://github.com/Manish-111913/EcoSphere_Enterprise-ESG-Management-Platform")],
    },
    # ---------------------------------------------------------------------------- 08
    {
        "key": "dealflow",
        "name": "DealFlow360",
        "subtitle": "B2B sales operations · Next.js · Prisma · PostgreSQL · Gemini",
        "badge": ("ODOO HACKATHON · 24H", "blue"),
        "icons": ["nextjs", "typescript", "prisma", "postgresql", "googlegemini"],
        "summary": "Carries a B2B quotation from draft through risk-based approval, customer negotiation, multi-warehouse "
                   "fulfilment and billing, with deal-health tracking.",
        "problem": "Discount approvals, customer negotiation, fulfilment and billing often run in separate tools. DealFlow360 "
                   "carries one quotation from first draft through approval, negotiation, warehouse fulfilment and billing in a single system.",
        "diagram": {
            "h": 302,
            "labels": [(18, 140, "AFTER THE CUSTOMER CONFIRMS")],
            "nodes": [
                N("draft", 18, 30, 128, 50, "Draft quote", "lines + discount", "io"),
                N("risk", 164, 30, 124, 50, "Risk score", "0–100"),
                N("need", 306, 22, 96, 66, "Needs\napproval?", kind="decision"),
                N("chain", 432, 30, 138, 50, "Approval chain", "Manager → Finance"),
                N("portal", 588, 30, 120, 50, "Portal quote", "magic link"),
                N("cc", 726, 22, 99, 66, "Counter or\nconfirm?", kind="decision"),
                N("conf", 690, 150, 135, 50, "Confirmed", "version check"),
                N("ful", 520, 150, 152, 50, "Fulfilment plan", "fewest shipments"),
                N("bill", 350, 150, 152, 50, "Billing", "one-time · recurring"),
                N("health", 164, 150, 168, 50, "Deal health", "100 − penalties", "hot"),
                N("dash", 18, 150, 128, 50, "Dashboard", "live · WebSocket", "io"),
                N("ai", 588, 226, 237, 46, "Gemini", "explain · draft · summarise", "ext"),
            ],
            "edges": [
                E("draft", "risk"), E("risk", "need"), E("need", "chain", label="yes"), E("chain", "portal"),
                E("need", "portal", sa="b", sb="b", my=106, label="no"),
                E("portal", "cc"),
                E("cc", "risk", sa="t", sb="t", my=9, label="counter-offer → re-score"),
                E("cc", "conf", sa="b", sb="t", label="confirm"),
                E("conf", "ful", sa="l", sb="r"), E("ful", "bill", sa="l", sb="r"),
                E("bill", "health", sa="l", sb="r"), E("health", "dash", sa="l", sb="r"),
            ],
            "notes": [(18, 244, "Gemini explains quotes and drafts messages;"), (18, 258, "prices, rules and risk are computed by code")],
        },
        "stack": [("Frontend", "Next.js 16 · React 19 · TypeScript · Tailwind"),
                  ("Backend", "Next.js API routes → framework-free TypeScript domain · Zod"),
                  ("Data", "PostgreSQL 17 · Prisma 7"),
                  ("Auth", "Auth.js: credentials, Google, portal magic link"),
                  ("AI", "Google Gemini"), ("Realtime", "WebSocket hub fed by Postgres NOTIFY")],
        "stack_note": "Uses an Odoo Hackathon brief as requirements but is not built on Odoo. No lead stage, email, CRM or payment gateway.",
        "decision": ("FROM THE CODE",
                     "Approval routing comes from a 0–100 risk score built from discount-ceiling breaches, margin shortfall, "
                     "negotiation rounds and delivery risk. Score bands stored in the database decide who signs: a Manager from 30, Finance from 60."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "One connected flow lets a counter-offer be re-scored instantly and a confirmation start fulfilment on its own, "
                     "but every stage now depends on shared rules and versions, so one change (a ceiling, a price) ripples through the rest."),
        "steps": [
            S("Draft a quotation", "Lines, quantities and discounts for a customer.", "io"),
            S("Score the risk", "Ceiling breaches, margin shortfall, negotiation rounds and delivery risk give a score from 0 to 100."),
            S("Approval needed?", "Yes if any line breaks its discount ceiling or the score falls in an approval band.", "decision"),
            S("Approval chain", "Manager from 30, Finance from 60; each approver is checked by role."),
            S("Customer portal", "The customer opens the quote through a magic link; internal fields are stripped."),
            S("Counter or confirm?", "A counter-offer is re-scored at once and may need re-approval.", "decision"),
            S("Confirm the order", "A version check rejects the confirmation if the terms changed meanwhile."),
            S("Plan fulfilment", "Split across warehouses: fewest shipments first, then cost."),
            S("Bill it", "One-time and recurring invoices, issued by staff."),
            S("Track deal health", "100 minus penalties, pushed live to the dashboard over WebSocket.", "hot"),
            S("Gemini assists", "Explains quotes, drafts messages and suggests next actions; code computes the numbers.", "ext"),
        ],
        "links": [("Source code", "https://github.com/Manish-111913/DEALFLOW360")],
    },
    # ---------------------------------------------------------------------------- 09
    {
        "key": "pharmacy",
        "name": "Pharmacy App Prototype",
        "subtitle": "Inspired by Apollo Pharmacy · built in 135 minutes at CoinQuest",
        "badge": ("1ST PRIZE · COINQUEST", "gold"),
        "icons": ["html", "javascript", "bootstrap", "django"],
        "summary": "A hackathon prototype of a pharmacy app focused on finding a medicine and its details quickly; "
                   "it won first prize at CoinQuest.",
        "problem": "Built in 135 minutes for the CoinQuest Hackathon, where it won first prize, this prototype explores how a "
                   "pharmacy app can make finding a medicine and its details quick. Its source wasn't available, so the flow is conceptual.",
        "diagram": {
            "h": 204,
            "labels": [(18, 16, "WHAT A VISITOR DOES"), (18, 118, "BEHIND THE SEARCH")],
            "nodes": [
                N("open", 18, 26, 140, 48, "Opens the app", "web prototype", "io"),
                N("find", 176, 26, 140, 48, "Browse or search", "medicines"),
                N("list", 334, 26, 140, 48, "Matching results", "medicine list"),
                N("det", 492, 26, 140, 48, "Medicine details", "detail page"),
                N("next", 650, 26, 175, 48, "Next step", "cart / order?", "unverified"),
                N("srch", 176, 128, 140, 48, "Catalog search", "Django view?", "unverified"),
                N("data", 334, 128, 140, 48, "Medicine data", "storage unknown", "unverified"),
            ],
            "edges": [
                E("open", "find"), E("find", "list"), E("list", "det"), E("det", "next", dashed=True),
                E("find", "srch", sa="b", sb="t"), E("srch", "data"), E("data", "list", sa="t", sb="b"),
            ],
        },
        "stack": [("Frontend", "HTML · CSS · JavaScript · Bootstrap"), ("Backend", "Python · Django")],
        "stack_note": "From portfolio records; the source was not available to review. Not affiliated with Apollo Pharmacy.",
        "decision": ("ARCHITECTURAL CONSIDERATION",
                     "A pharmacy-first interface puts search and medicine details up front, so the most common task, finding a "
                     "medicine and checking it, takes the fewest steps. That focus is what fits a working demo into a 135-minute build."),
        "tradeoff": ("GENERAL TRADE-OFF",
                     "A prototype can skip what a real pharmacy app cannot: verified medicine data, live inventory, prescription "
                     "checks and secure payments. Each adds significant backend work and compliance requirements."),
        "steps": [
            S("Open the app", "A web prototype built in 135 minutes.", "io"),
            S("Browse or search", "Look for a medicine by name or browse the list."),
            S("Catalog search", "A Django backend is recorded; the exact search logic was not verified.", "unverified"),
            S("Matching results", "Medicines that match the query."),
            S("Medicine details", "The detail view for one medicine."),
            S("Next step", "Cart or ordering features could not be verified.", "unverified"),
        ],
        "links": [],
    },
]
