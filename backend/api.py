from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import subprocess
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://localhost:5173",
"http://127.0.0.1:5173",
"https://nft-security-analyzer.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            timeout=300
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
    # EXTRACT FINAL RISK SCORE
    # =====================================================
    risk_score = 0

    for line in output.split("\n"):

        if "Overall Risk Score:" in line:

            try:

                risk_score = int(
                    line.split(":")[1].strip()
                )

            except:

                risk_score = 0
    critical_count = len([
        v for v in vulnerabilities
        if v["severity"] == "CRITICAL"
    ])

    high_count = len([
        v for v in vulnerabilities
        if v["severity"] == "HIGH"
    ])

    medium_count = len([
        v for v in vulnerabilities
        if v["severity"] == "MEDIUM"
    ])

    low_count = len([
        v for v in vulnerabilities
        if v["severity"] == "LOW"
    ])
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

        "graph_url":
        "https://nft-security-analyzer.onrender.com/output/call_graph.png",

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
@app.get("/")
def home():
    return {
        "status": "backend running"
    }
