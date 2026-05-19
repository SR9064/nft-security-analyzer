from fastapi.staticfiles import StaticFiles
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import subprocess
import os

app = FastAPI()

# =====================================================
# STATIC FILES
# =====================================================
os.makedirs("output", exist_ok=True)

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
        "message": "NFT Security Analyzer API Running"
    }


# =====================================================
# ANALYZE CONTRACT
# =====================================================
@app.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...)
):

    # -------------------------------------------------
    # SAVE FILE
    # -------------------------------------------------
    temp_path = f"contracts/{file.filename}"

    with open(temp_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -------------------------------------------------
    # RUN ANALYZER
    # -------------------------------------------------
    try:

        print("[API] Starting analyzer...")

        result = subprocess.run(
            [
                "python3",
                "-m",
                "nftscanner.main",
                temp_path
            ],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=None
        )

        print("[API] Analyzer finished")

        output = (
            result.stdout
            + "\n"
            + result.stderr
        )

        # -------------------------------------------------
        # SPLIT SYMBOLIC TRACE
        # -------------------------------------------------
        symbolic_trace = []

        for line in output.split("\n"):

            if (
                "[TRACE]" in line
                or "[CALL]" in line
                or "[REENTRY]" in line
                or "[OWNER CHANGE]" in line
                or "[BALANCE CHANGE]" in line
                or "[PATH BLOCKED]" in line
            ):

                symbolic_trace.append(line)

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    # =====================================================
    # PARSE VULNERABILITIES
    # =====================================================
    vulnerabilities = []

    detector_map = [

        (
            "Missing Ownership Access Control",
            "Missing Ownership Access Control",
            "HIGH"
        ),

        (
            "Unsafe tx.origin Authentication",
            "Unsafe tx.origin Authentication",
            "HIGH"
        ),

        (
            "Dangerous Selfdestruct Usage",
            "Dangerous Selfdestruct Usage",
            "CRITICAL"
        ),

        (
            "Dangerous Delegatecall Usage",
            "Dangerous Delegatecall Usage",
            "HIGH"
        ),

        (
            "Unchecked External Call",
            "Unchecked External Call",
            "HIGH"
        ),

        (
            "Unlimited NFT Minting Risk",
            "Unlimited NFT Minting Risk",
            "HIGH"
        ),

        (
            "Mutable NFT Metadata Risk",
            "Mutable NFT Metadata Risk",
            "MEDIUM"
        ),

        (
            "Royalty Manipulation Risk",
            "Royalty Manipulation Risk",
            "MEDIUM"
        ),

        (
            "Centralized Owner Privileges",
            "Centralized Owner Privileges",
            "MEDIUM"
        ),

        (
            "Hidden Owner Mint Capability",
            "Hidden Owner Mint Capability",
            "HIGH"
        ),

        (
            "Approval For All Abuse Risk",
            "Approval For All Abuse Risk",
            "HIGH"
        ),

        (
            "Unsafe ERC721 Transfer Usage",
            "Unsafe ERC721 Transfer Usage",
            "HIGH"
        ),

        (
            "Missing Zero Address Validation",
            "Missing Zero Address Validation",
            "MEDIUM"
        ),

        (
            "UNAUTHORIZED_TRANSFER",
            "Unauthorized Transfer",
            "HIGH"
        ),

        (
            "TAINTED_UNAUTHORIZED_TRANSFER",
            "Tainted Unauthorized Transfer",
            "HIGH"
        ),

        (
            "OWNERSHIP_CORRUPTION",
            "Ownership Corruption",
            "HIGH"
        )

    ]

    # -------------------------------------------------
    # DETECTOR MATCHING
    # -------------------------------------------------
    for keyword, vuln_type, severity in detector_map:

        if keyword in output:

            vulnerabilities.append({

                "type":
                vuln_type,

                "severity":
                severity
            })

    # -------------------------------------------------
    # SYMBOLIC EXECUTION VULNS
    # -------------------------------------------------
    if "VULNS:" in output:

        vulnerabilities.append({

            "type":
            "Symbolic Execution Attack",

            "severity":
            "CRITICAL"
        })

    # -------------------------------------------------
    # REENTRANCY
    # -------------------------------------------------
    if (
        "REENTRANCY" in output
        or "[REENTRY]" in output
    ):

        vulnerabilities.append({

            "type":
            "Reentrancy Attack",

            "severity":
            "CRITICAL"
        })

    # =====================================================
    # RISK METRICS
    # =====================================================
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

    risk_score = (
        critical_count * 10
        + high_count * 7
        + medium_count * 4
        + low_count * 1
    )

    # =====================================================
    # RESPONSE
    # =====================================================
    return {

        "success": True,

        "vulnerabilities":
        vulnerabilities,

        "raw_output":
        output,

        "symbolic_trace":
        symbolic_trace,

        "attack_paths":
        [
            line.replace(
                "[TRACE] ",
                ""
            )
            for line in symbolic_trace
            if "⚠ Reentrancy" in line
        ],

        "graph_url":"https://nft-security-analyzer.onrender.com/output/call_graph.png",
        "risk_summary": {

            "score":
            risk_score,

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
