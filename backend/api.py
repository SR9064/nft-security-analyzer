from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from nftscanner.main import run

import shutil
import os

# =====================================================
# FASTAPI INIT
# =====================================================
app = FastAPI()

# =====================================================
# REQUIRED DIRECTORIES
# =====================================================
os.makedirs("output", exist_ok=True)
os.makedirs("contracts", exist_ok=True)

# =====================================================
# STATIC FILES
# =====================================================
app.mount(
    "/output",
    StaticFiles(directory="output"),
    name="output"
)

# =====================================================
# CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# HEALTH CHECK
# =====================================================
@app.get("/")
def home():

    return {
        "message":
        "NFT Security Analyzer API Running"
    }

# =====================================================
# ANALYZE CONTRACT
# =====================================================
@app.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...)
):

    try:

        # -------------------------------------------------
        # SAVE CONTRACT
        # -------------------------------------------------
        temp_path = f"contracts/{file.filename}"

        print(
            f"[API] Saving contract → {temp_path}"
        )

        with open(temp_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -------------------------------------------------
        # RUN ANALYZER DIRECTLY
        # -------------------------------------------------
        print(
            "[API] Running analyzer..."
        )

        analysis_result = run(
            temp_path,
            verbose=True
        )

        print(
            "[API] Analyzer complete"
        )

        # =================================================
        # SAFE DEFAULTS
        # =================================================
        if not analysis_result:

            analysis_result = {}

        vulnerabilities = analysis_result.get(
            "issues",
            []
        )

        symbolic_vulns = analysis_result.get(
            "symbolic_vulns",
            []
        )

        risk = analysis_result.get(
            "risk",
            0
        )

        # =================================================
        # SYMBOLIC TRACE
        # =================================================
        symbolic_trace = []

        for vuln in symbolic_vulns:

            attack_flow = vuln.get(
                "attack_flow"
            )

            if attack_flow:

                symbolic_trace.append(
                    f"[TRACE] {attack_flow}"
                )

        # =================================================
        # ATTACK PATHS
        # =================================================
        attack_paths = [

            vuln.get("attack_flow")

            for vuln in symbolic_vulns

            if vuln.get("attack_flow")
        ]

        # =================================================
        # RISK COUNTS
        # =================================================
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

        for vuln in vulnerabilities:

            severity = vuln.get(
                "severity",
                ""
            ).upper()

            if severity == "CRITICAL":

                critical_count += 1

            elif severity == "HIGH":

                high_count += 1

            elif severity == "MEDIUM":

                medium_count += 1

            elif severity == "LOW":

                low_count += 1

        # =================================================
        # GRAPH URL
        # =================================================
        base_url = os.getenv(

            "RENDER_EXTERNAL_URL",

            "http://127.0.0.1:8000"
        )

        graph_url = (
            f"{base_url}/output/call_graph.png"
        )

        # =================================================
        # RESPONSE
        # =================================================
        return {

            "success": True,

            "vulnerabilities":
            vulnerabilities,

            "symbolic_trace":
            symbolic_trace,

            "attack_paths":
            attack_paths,

            "graph_url":
            graph_url,

            "risk_summary": {

                "score":
                risk,

                "critical":
                critical_count,

                "high":
                high_count,

                "medium":
                medium_count,

                "low":
                low_count
            }
        }

    # =====================================================
    # ERROR HANDLER
    # =====================================================
    except Exception as e:

        print(
            f"[API ERROR] {str(e)}"
        )

        return {

            "success": False,

            "error":
            str(e)
        }
