import { useState, useEffect } from "react"
import jsPDF from "jspdf"
import {
  useNodesState,
  useEdgesState
} from "reactflow"

import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
  Position

  
} from "reactflow"
import "reactflow/dist/style.css"

import {
  UploadCloud,
  Shield,
  ShieldAlert,
  Activity,
  GitBranch,
  Terminal,
  Bug,
  FileText
} from "lucide-react"
import { motion } from "framer-motion"



function App() {

  const [file, setFile] =
    useState<File | null>(null)

  const [loading, setLoading] =
    useState(false)

  const [vulnerabilities, setVulnerabilities] =
    useState<any[]>([])

  const [rawOutput, setRawOutput] =
    useState("")

  const [symbolicTrace, setSymbolicTrace] =
    useState<string[]>([])
  
  const [attackPaths, setAttackPaths] =
  useState<string[]>([])

 

  const [riskSummary, setRiskSummary] =
    useState<any>(null)

const [
  nodes,
  setNodes,
  onNodesChange
] = useNodesState([])

const [
  edges,
  setEdges,
  onEdgesChange
] = useEdgesState([])
const [showStatic, setShowStatic] =
  useState(true)

const [showSymbolic, setShowSymbolic] =
  useState(true)

const [showGraph, setShowGraph] =
  useState(true)

const [showRaw, setShowRaw] =
  useState(false)

const [activeSection, setActiveSection] =
  useState("top")
  // ANALYZE CONTRACT
  // =====================================================
  const analyzeContract = async () => {

    if (!file) {

      alert("Please select Solidity file")

      return
    }

    const formData = new FormData()

    formData.append("file", file)

    try {

      setLoading(true)

      const response = await fetch(
        "https://nft-security-analyzer.onrender.com/analyze",
        {
          method: "POST",
          body: formData
        }
      )

      const data = await response.json()

      setVulnerabilities(
        data.vulnerabilities || []
      )

      setRawOutput(
        data.raw_output || ""
      )

      setSymbolicTrace(
        data.symbolic_trace || []
      )
      setAttackPaths(
  data.attack_paths || []
)



      setRiskSummary(
        data.risk_summary || null
      )
      
// =================================================
// BUILD INTERACTIVE GRAPH
// =================================================

const generatedNodes: any[] = []

const generatedEdges: any[] = []
let entryY = 120
let externalY = 120
let reentryY = 120

generatedNodes.push(

  // =================================================
  // ENTRY CLUSTER
  // =================================================

  {
    id: "cluster-entry",

    type: "group",

    position: {
      x: 0,
      y: 0
    },

    style: {

      width: 420,
      zIndex: 0,

height: 2200,
      overflow: "visible",

      background:
        "linear-gradient(180deg, rgba(15,23,42,0.82), rgba(2,6,23,0.92))",

      border:
        "2px solid rgba(34,197,94,0.18)",

      borderRadius: "24px",

      boxShadow:
        "0 0 40px rgba(34,197,94,0.08)"
    },

data: {
  label: "🟢 ENTRY FLOW\n\nExecution & Validation"
}
  },

  // =================================================
  // EXTERNAL CLUSTER
  // =================================================

  {
    id: "cluster-external",

    type: "group",

    position: {
      x: 620,
      y: 0
    },

    style: {

      width: 420,
      zIndex: 0,

height: 2200,

      overflow: "visible",

      background:
        "linear-gradient(180deg, rgba(15,23,42,0.82), rgba(2,6,23,0.92))",

      border:
        "2px solid rgba(59,130,246,0.18)",

      borderRadius: "24px",

      boxShadow:
        "0 0 40px rgba(59,130,246,0.08)"
    },

    data: {
      label: "🔵 EXTERNAL CALLS"
    }
  },

  // =================================================
  // REENTRANCY CLUSTER
  // =================================================

  {
    id: "cluster-reentry",

    type: "group",

    position: {
      x: 1240,
      y: 0
    },

    style: {

      width: 420,
      zIndex: 0,

height: 2200,

      overflow: "visible",

      background:
        "linear-gradient(180deg, rgba(15,23,42,0.82), rgba(2,6,23,0.92))",

      border:
        "2px solid rgba(239,68,68,0.18)",

      borderRadius: "24px",

      boxShadow:
        "0 0 40px rgba(239,68,68,0.08)"
    },

    data: {
      label: "🔴 REENTRANCY"
    }
  }
)

// =================================================
// FLOW TRACKERS
// =================================================

let previousEntryNode: string | null = null

let previousExternalNode: string | null = null

let previousReentryNode: string | null = null

let previousGlobalNode: string | null = null

let previousGlobalCluster: string | null = null

// =================================================
// NODE SPACING
// =================================================



// =================================================
// TRACE LOOP
// =================================================
;(
  data.symbolic_trace || []
).forEach(

  (
    trace: string,
    index: number
  ) => {

    const nodeId =
      `node-${index}`

    let clusterId =
      "cluster-entry"

    // =================================================
    // DETECT CLUSTER
    // =================================================

    if (

      trace.includes("[CALL]")

      ||

      trace.includes("External")

    ) {

      clusterId =
        "cluster-external"
    }

    else if (

      trace.includes("[REENTRY]")

      ||

      trace.includes("Reentrancy")

    ) {

      clusterId =
        "cluster-reentry"
    }

    // =================================================
    // POSITIONING
    // =================================================

    let nodeY = entryY

    if (
      clusterId === "cluster-external"
    ) {

      nodeY = externalY

      externalY += 150
    }

    else if (
      clusterId === "cluster-reentry"
    ) {

      nodeY = reentryY

      reentryY += 150
    }

    else {

      nodeY = entryY

      entryY += 150
    }

    // =================================================
    // CREATE NODE
    // =================================================

    generatedNodes.push({

      id: nodeId,

      parentNode: clusterId,

      extent: "parent",

      sourcePosition: Position.Bottom,

      targetPosition: Position.Top,

      position: {

        x: 30,

        y: nodeY
      },

      data: {
        label: trace
      },

      style: {

        width: 300,
        zIndex: 10,

        minHeight: 90,

        padding: "16px",

        borderRadius: "18px",

        color: "white",

        fontWeight: "700",
        lineHeight: "1.5",
wordBreak: "break-word",
textAlign: "center",
justifyContent: "center",

        fontSize: "13px",

        display: "flex",

        alignItems: "center",

        boxShadow:

          clusterId === "cluster-reentry"

            ? "0 0 24px rgba(239,68,68,0.22)"

            : clusterId === "cluster-external"

            ? "0 0 24px rgba(59,130,246,0.22)"

            : "0 0 24px rgba(34,197,94,0.18)",

        border:

          clusterId === "cluster-reentry"

            ? "1px solid rgba(239,68,68,0.35)"

            : clusterId === "cluster-external"

            ? "1px solid rgba(59,130,246,0.35)"

            : "1px solid rgba(34,197,94,0.35)",

        background:

          clusterId === "cluster-reentry"

            ? "linear-gradient(145deg,#450a0a,#7f1d1d)"

            : clusterId === "cluster-external"

            ? "linear-gradient(145deg,#172554,#2563eb)"

            : "linear-gradient(145deg,#052e16,#166534)"
      }
    })

    // =================================================
    // INTERNAL FLOW
    // =================================================

    let previousNode = null

    let edgeColor = "#22c55e"

    if (
      clusterId === "cluster-entry"
    ) {

      previousNode =
        previousEntryNode

      previousEntryNode =
        nodeId

      edgeColor =
        "#22c55e"
    }

    else if (
      clusterId === "cluster-external"
    ) {

      previousNode =
        previousExternalNode

      previousExternalNode =
        nodeId

      edgeColor =
        "#3b82f6"
    }

    else {

      previousNode =
        previousReentryNode

      previousReentryNode =
        nodeId

      edgeColor =
        "#ef4444"
    }

    // =================================================
    // INTERNAL EDGE
    // =================================================

    if (previousNode) {

      generatedEdges.push({

        id:
          `edge-${index}`,

        source:
          previousNode,

        target:
          nodeId,

        animated: true,

        type: "bezier",
        pathOptions: {
  curvature: 0.45
},

        markerEnd: {

          type: MarkerType.ArrowClosed,

          color: edgeColor
        },

        style: {

          stroke:
            edgeColor,

          strokeWidth: 3
        }
      })
    }

    // =================================================
    // CROSS-CLUSTER FLOW
    // =================================================

    if (

      previousGlobalNode

      &&

      previousGlobalCluster !== clusterId

    ) {

      generatedEdges.push({

        id:
          `cross-edge-${index}`,

        source:
          previousGlobalNode,

        target:
          nodeId,

        animated: true,

        type: "bezier",
        pathOptions: {
  curvature: 0.45
},

        markerEnd: {

          type: MarkerType.ArrowClosed,

          color: "#38bdf8"
        },

style: {

  stroke: "#38bdf8",

  strokeWidth: 2,

  strokeDasharray: "12 8",

  opacity: 0.28
}
      })
    }

    previousGlobalNode =
      nodeId

    previousGlobalCluster =
      clusterId
  }
)

setNodes(generatedNodes)

setEdges(generatedEdges)

    } catch (err) {

      console.error(err)

      alert("Analysis failed")
    }

    setLoading(false)
  }


  // =====================================================
  // DOWNLOAD PDF REPORT
  // =====================================================
  const downloadPdfReport = () => {

    const doc = new jsPDF()

    let y = 20

    doc.setFontSize(20)

    doc.text(
      "NFT Security Analysis Report",
      20,
      y
    )

    y += 20

    doc.setFontSize(14)

    doc.text(
      `Risk Score: ${riskSummary?.score || 0}`,
      20,
      y
    )

    y += 10

    doc.text(
      `Critical: ${riskSummary?.critical || 0}`,
      20,
      y
    )

    y += 10

    doc.text(
      `High: ${riskSummary?.high || 0}`,
      20,
      y
    )

    y += 10

    doc.text(
      `Medium: ${riskSummary?.medium || 0}`,
      20,
      y
    )

    y += 10

    doc.text(
      `Low: ${riskSummary?.low || 0}`,
      20,
      y
    )

    y += 20

    doc.setFontSize(16)

    doc.text(
      "Vulnerabilities",
      20,
      y
    )

    y += 15

    doc.setFontSize(12)

    vulnerabilities.forEach((vuln: any) => {

      doc.text(
        `• ${vuln.type} (${vuln.severity})`,
        25,
        y
      )

      y += 10
    })

    y += 10

    doc.setFontSize(16)

    doc.text(
      "Symbolic Execution Trace",
      20,
      y
    )

    y += 15

    doc.setFontSize(10)

    symbolicTrace
      .slice(0, 20)
      .forEach((trace: string) => {

        doc.text(
          trace,
          25,
          y
        )

        y += 8

        if (y > 270) {

          doc.addPage()

          y = 20
        }
      })

    doc.save(
      "nft_security_report.pdf"
    )
  }
 // =====================================================
//   // DOWNLOAD JSON REPORT
//   // =====================================================
  const downloadJsonReport = () => {

    const report = {

      riskSummary,

      vulnerabilities,

      symbolicTrace,

      rawOutput
    }

    const blob = new Blob(
      [
        JSON.stringify(
          report,
          null,
          2
        )
      ],
      {
        type: "application/json"
      }
    )

    const url =
      URL.createObjectURL(blob)

    const a =
      document.createElement("a")

    a.href = url

    a.download =
      "nft_security_report.json"

    a.click()

    URL.revokeObjectURL(url)
  }

  // =====================================================
  // DOWNLOAD TXT REPORT
  // =====================================================
  const downloadTxtReport = () => {

    const textReport = `
NFT SECURITY ANALYSIS REPORT
====================================

RISK SCORE:
${riskSummary?.score || 0}

------------------------------------
VULNERABILITIES
------------------------------------

${vulnerabilities.map((v: any) => `
- ${v.type}
  Severity: ${v.severity}
`).join("\n")}

------------------------------------
SYMBOLIC EXECUTION TRACE
------------------------------------

${symbolicTrace.join("\n")}

------------------------------------
RAW ANALYZER OUTPUT
------------------------------------

${rawOutput}
`

    const blob = new Blob(
      [textReport],
      {
        type: "text/plain"
      }
    )

    const url =
      URL.createObjectURL(blob)

    const a =
      document.createElement("a")

    a.href = url

    a.download =
      "nft_security_report.txt"

    a.click()

    URL.revokeObjectURL(url)
  }

 /* ===================================================== */
/* ACTIVE SIDEBAR TRACKING */
/* ===================================================== */

useEffect(() => {

  const handleScroll = () => {

    const sections = [
      "top",
      "risk",
      "static",
      "symbolic",
      "graph",
      "logs"
    ]

    let current = "top"

    sections.forEach((id) => {

      const element =
        document.getElementById(id)

      if (element) {

        const rect =
          element.getBoundingClientRect()

        if (rect.top <= 140) {

          current = id
        }
      }
    })

    setActiveSection(current)
  }

  window.addEventListener(
    "scroll",
    handleScroll
  )

  return () =>
    window.removeEventListener(
      "scroll",
      handleScroll
    )

}, [])

/* ===================================================== */
/* MAIN RETURN */
/* ===================================================== */

return (

  <>

    {
      loading && (

        <div className="loading-overlay">

          <div className="scanner-box">

            <div className="scanner-glow"></div>

            <div className="scanner-spinner"></div>

            <h1>
              Scanning Smart Contract
            </h1>

            <p>
              Running Static Analysis,
              Symbolic Execution,
              CFG Generation,
              and Vulnerability Detection...
            </p>

            <div className="scan-steps">

              <div className="scan-step active">
                ✓ Parsing Solidity
              </div>

              <div className="scan-step active">
                ✓ Detecting Vulnerabilities
              </div>

              <div className="scan-step">
                ⟳ Running Symbolic Execution
              </div>

              <div className="scan-step">
                ⟳ Building CFG Graph
              </div>

              <div className="scan-step">
                ⟳ Generating Report
              </div>

            </div>

          </div>

        </div>
      )
    }

    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "white",
        fontFamily: "Arial",
        display: "flex"
      }}
    >
      
    {/* ================================================= */}
    {/* SIDEBAR */}
    {/* ================================================= */}

    <div
      className="sidebar"
      style={{
        position: "sticky",
        top: 0,
        height: "100vh",
        borderRight: "1px solid #1e293b"
      }}
    >

      {/* LOGO */}
      <div className="sidebar-logo">

        <Shield
          size={54}
          color="#38bdf8"
        />

        <div>

          <h1>
            NFT SECURE
          </h1>

          <p>
            Analyzer
          </p>

        </div>

      </div>

      {/* NAVIGATION */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "14px"
        }}
      >

        {/* DASHBOARD */}
        <a
          href="#top"
          className={
            activeSection === "top"
              ? "sidebar-link active"
              : "sidebar-link"
          }
          style={{
            textDecoration: "none"
          }}
        >

          <Activity size={24} />

          Dashboard

        </a>

        {/* RISK */}
        <a
          href="#risk"
          className={
            activeSection === "risk"
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >

          <ShieldAlert size={24} />

          Risk Summary

        </a>

        {/* STATIC */}
        <a
          href="#static"
          className={
            activeSection === "static"
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >

          <Activity size={24} />

          Static Analysis

        </a>

        {/* SYMBOLIC */}
        <a
          href="#symbolic"
          className={
            activeSection === "symbolic"
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >

          <Bug size={24} />

          Symbolic Trace

        </a>

        {/* GRAPH */}
        <a
          href="#graph"
          className={
            activeSection === "graph"
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >

          <GitBranch size={24} />

          CFG Graph

        </a>

        {/* LOGS */}
        <a
          href="#logs"
          className={
            activeSection === "logs"
              ? "sidebar-link active"
              : "sidebar-link"
          }
        >

          <FileText size={24} />

          Raw Logs

        </a>

      </div>

    </div>

    {/* ================================================= */}
    {/* MAIN CONTENT */}
    {/* ================================================= */}

    <div
      id="top"
      style={{
        flex: 1,
        padding: "40px"
      }}
    >
{/* ================================================= */}
{/* HEADER */}
{/* ================================================= */}
<div className="hero-header">

  {/* LEFT SIDE */}
  <div>

    <h1 className="hero-title">
      NFT Security Analyzer
    </h1>

    <p className="hero-subtitle">
      Hybrid Static + Symbolic NFT Vulnerability Detection
    </p>

  </div>

  {/* RIGHT SIDE */}
  <div className="top-bar">

    {/* VERSION */}
    <div className="version-pill">
      ● v2.1.0
    </div>

    {/* NOTIFICATION */}
    <div className="top-icon">
      🔔
    </div>

    {/* PROFILE */}
    <div className="top-icon">
      👤
    </div>

  </div>

</div>
{/* ================================================= */}
{/* RISK DASHBOARD */}
{/* ================================================= */}
{
  riskSummary && (

    <motion.div
      id="risk"
      className="glass-card"
      initial={{
        opacity: 0,
        y: 30
      }}
      animate={{
        opacity: 1,
        y: 0
      }}
      transition={{
        duration: 0.5
      }}
      style={{
        marginBottom: "40px",
        border:
          riskSummary.score >= 15
            ? "2px solid rgba(239,68,68,0.45)"
            : riskSummary.score >= 7
            ? "2px solid rgba(249,115,22,0.45)"
            : "2px solid rgba(34,197,94,0.45)"
      }}
    >

      {/* TOP HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <div>

          <h2 className="section-title">

            <ShieldAlert size={24} />

            Security Risk Summary

          </h2>

          <p
            style={{
              color: "#94a3b8",
              marginTop: "10px",
              fontSize: "16px"
            }}
          >
            AI-powered hybrid NFT vulnerability analysis
          </p>

        </div>

        {/* RISK BADGE */}
        <motion.div
          whileHover={{
            scale: 1.05
          }}
          style={{
            padding: "14px 24px",
            borderRadius: "999px",
            fontWeight: "700",
            fontSize: "18px",
            background:
              riskSummary.score >= 15
                ? "rgba(239,68,68,0.15)"
                : riskSummary.score >= 7
                ? "rgba(249,115,22,0.15)"
                : "rgba(34,197,94,0.15)",
            color:
              riskSummary.score >= 15
                ? "#f87171"
                : riskSummary.score >= 7
                ? "#fb923c"
                : "#4ade80",
            border:
              riskSummary.score >= 15
                ? "1px solid rgba(239,68,68,0.4)"
                : riskSummary.score >= 7
                ? "1px solid rgba(249,115,22,0.4)"
                : "1px solid rgba(34,197,94,0.4)"
          }}
        >

          {
            riskSummary.score >= 15
              ? "HIGH RISK"
              : riskSummary.score >= 7
              ? "MEDIUM RISK"
              : "LOW RISK"
          }

        </motion.div>

      </div>

      {/* SCORE SECTION */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "40px",
          flexWrap: "wrap",
          marginBottom: "40px"
        }}
      >

        {/* SCORE CIRCLE */}
        <motion.div
          animate={{
            scale: [1, 1.03, 1]
          }}
          transition={{
            duration: 3,
            repeat: Infinity
          }}
          style={{
            width: "220px",
            height: "220px",
            borderRadius: "50%",
            border:
              riskSummary.score >= 15
                ? "10px solid #ef4444"
                : riskSummary.score >= 7
                ? "10px solid #f59e0b"
                : "10px solid #22c55e",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            background: "rgba(255,255,255,0.03)",
            boxShadow:
              riskSummary.score >= 15
                ? "0 0 40px rgba(239,68,68,0.25)"
                : riskSummary.score >= 7
                ? "0 0 40px rgba(249,115,22,0.25)"
                : "0 0 40px rgba(34,197,94,0.25)"
          }}
        >

          <motion.h1
            initial={{
              scale: 0.5,
              opacity: 0
            }}
            animate={{
              scale: 1,
              opacity: 1
            }}
            transition={{
              duration: 0.5
            }}
            style={{
              fontSize: "64px",
              margin: 0
            }}
          >
            {riskSummary.score}
          </motion.h1>

          <p
            style={{
              color: "#94a3b8",
              marginTop: "10px",
              fontSize: "18px"
            }}
          >
            Risk Score
          </p>

        </motion.div>

        {/* DESCRIPTION */}
        <div
          style={{
            flex: 1,
            minWidth: "280px"
          }}
        >

          <h2
            style={{
              fontSize: "32px",
              marginBottom: "20px"
            }}
          >
            Contract Security Status
          </h2>

          <p
            style={{
              color: "#cbd5e1",
              fontSize: "18px",
              lineHeight: "1.8"
            }}
          >
            This analysis combines static analysis and symbolic execution
            to detect NFT smart contract vulnerabilities including
            reentrancy, authorization flaws, ownership issues,
            unchecked external calls, and state inconsistencies.
          </p>

        </div>

      </div>

      {/* RISK METRIC CARDS */}
      <div className="risk-grid">

        {/* CRITICAL */}
        <motion.div
          className="risk-card critical"
          initial={{
            opacity: 0,
            y: 20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          transition={{
            duration: 0.4
          }}
          whileHover={{
            scale: 1.04
          }}
        >

          <h3>
            Critical
          </h3>

          <motion.h1
            initial={{
              scale: 0.5,
              opacity: 0
            }}
            animate={{
              scale: 1,
              opacity: 1
            }}
          >
            {riskSummary.critical}
          </motion.h1>

        </motion.div>

        {/* HIGH */}
        <motion.div
          className="risk-card high"
          initial={{
            opacity: 0,
            y: 20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          transition={{
            duration: 0.5,
            delay: 0.1
          }}
          whileHover={{
            scale: 1.04
          }}
        >

          <h3>
            High
          </h3>

          <motion.h1>
            {riskSummary.high}
          </motion.h1>

        </motion.div>

        {/* MEDIUM */}
        <motion.div
          className="risk-card medium"
          initial={{
            opacity: 0,
            y: 20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          transition={{
            duration: 0.5,
            delay: 0.2
          }}
          whileHover={{
            scale: 1.04
          }}
        >

          <h3>
            Medium
          </h3>

          <motion.h1>
            {riskSummary.medium}
          </motion.h1>

        </motion.div>

        {/* LOW */}
        <motion.div
          className="risk-card low"
          initial={{
            opacity: 0,
            y: 20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          transition={{
            duration: 0.5,
            delay: 0.3
          }}
          whileHover={{
            scale: 1.04
          }}
        >

          <h3>
            Low
          </h3>

          <motion.h1>
            {riskSummary.low}
          </motion.h1>

        </motion.div>

      </div>

    </motion.div>
  )
}
{/* ================================================= */}
{/* FILE UPLOAD */}
{/* ================================================= */}

<div className="glass-card">

  {/* HIDDEN FILE INPUT */}
  <input
    id="file-upload"
    type="file"
    accept=".sol"
    style={{
      display: "none"
    }}
    onChange={(e) => {

      if (e.target.files) {

        setFile(
          e.target.files[0]
        )
      }
    }}
  />

  {/* MAIN LAYOUT */}
  <div className="upload-layout">

    {/* LEFT SIDE */}
    <label
      htmlFor="file-upload"
      className="upload-zone"
    >

      <UploadCloud
        size={58}
        color="#38bdf8"
      />

      <div>

        <h2>
          Drag & Drop Solidity File
        </h2>

        <p>
          or click to browse
        </p>

        {
          file && (

            <div className="file-pill">

              {file.name}

            </div>
          )
        }

      </div>

    </label>

    {/* RIGHT SIDE */}
    <div className="button-grid">

      <button
        className="action-button"
        onClick={analyzeContract}
        style={{
          background: "#2563eb"
        }}
      >

        {
          loading
            ? "Analyzing..."
            : "Analyze Contract"
        }

      </button>

      <button
        className="action-button"
        onClick={downloadJsonReport}
        style={{
          background: "#16a34a"
        }}
      >
        Download JSON
      </button>

      <button
        className="action-button"
        onClick={downloadTxtReport}
        style={{
          background: "#9333ea"
        }}
      >
        Download TXT
      </button>

      <button
        className="action-button"
        onClick={downloadPdfReport}
        style={{
          background: "#dc2626"
        }}
      >
        Download PDF
      </button>

    </div>

  </div>

</div>

 {/* ================================================= */}
{/* STATIC ANALYSIS */}
{/* ================================================= */}
<div
  id="static"
  className="glass-card dashboard-section"
>

  {/* SECTION HEADER */}
  <div className="section-header">

<h2
  onClick={() =>
    setShowStatic(!showStatic)
  }
  className="section-title"
  style={{
    cursor: "pointer"
  }}
>

  <Activity size={22} />

  {
    showStatic
      ? "▼"
      : "▶"
  }

  {" "}

  Static Analysis Findings

</h2>

    <div className="status-pill red">

      {
        vulnerabilities.length
      }

      {" "}
      Issues

    </div>

  </div>

  {/* CONTENT */}
  {
    showStatic && (
      <>

        {/* EMPTY STATE */}
        {
          vulnerabilities.length === 0 && (

            <div
              style={{
                marginTop: "24px",
                padding: "24px",
                borderRadius: "18px",
                background:
                  "rgba(34,197,94,0.08)",
                border:
                  "1px solid rgba(34,197,94,0.18)",
                color:
                  "#4ade80"
              }}
            >

              ✅ No vulnerabilities detected

            </div>
          )
        }

        {/* VULNERABILITIES */}
        {
          vulnerabilities.map((vuln, index) => (

            <div
              key={index}
              className="vulnerability-card"
              style={{
                marginTop: "24px",
                borderLeft:
                  vuln.severity === "CRITICAL"
                    ? "6px solid #ef4444"
                    : vuln.severity === "HIGH"
                    ? "6px solid #f97316"
                    : vuln.severity === "MEDIUM"
                    ? "6px solid #eab308"
                    : "6px solid #22c55e"
              }}
            >

              {/* TOP ROW */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "16px"
                }}
              >

                <h3
                  style={{
                    margin: 0,
                    fontSize: "24px"
                  }}
                >
                  {vuln.type}
                </h3>

                {/* SEVERITY BADGE */}
                <div
                  style={{
                    padding: "10px 18px",
                    borderRadius: "999px",
                    fontWeight: "700",
                    fontSize: "14px",
                    background:
                      vuln.severity === "CRITICAL"
                        ? "rgba(239,68,68,0.12)"
                        : vuln.severity === "HIGH"
                        ? "rgba(249,115,22,0.12)"
                        : vuln.severity === "MEDIUM"
                        ? "rgba(234,179,8,0.12)"
                        : "rgba(34,197,94,0.12)",
                    color:
                      vuln.severity === "CRITICAL"
                        ? "#f87171"
                        : vuln.severity === "HIGH"
                        ? "#fb923c"
                        : vuln.severity === "MEDIUM"
                        ? "#fde047"
                        : "#4ade80",
                    border:
                      vuln.severity === "CRITICAL"
                        ? "1px solid rgba(239,68,68,0.22)"
                        : vuln.severity === "HIGH"
                        ? "1px solid rgba(249,115,22,0.22)"
                        : vuln.severity === "MEDIUM"
                        ? "1px solid rgba(234,179,8,0.22)"
                        : "1px solid rgba(34,197,94,0.22)"
                  }}
                >

                  {vuln.severity}

                </div>

              </div>

              {/* DESCRIPTION */}
              <p
                style={{
                  marginTop: "18px",
                  color: "#cbd5e1",
                  lineHeight: "1.8",
                  fontSize: "16px"
                }}
              >
                Potential vulnerability detected during static analysis.
                Review this issue carefully before deployment.
              </p>

            </div>
          ))
        }

      </>
    )
  }

</div>

 {/* ================================================= */}
{/* SYMBOLIC EXECUTION */}
{/* ================================================= */}
<div
  id="symbolic"
  className="glass-card dashboard-section"
>

  {/* SECTION HEADER */}
  <div className="section-header">

<h2
  onClick={() =>
    setShowSymbolic(
      !showSymbolic
    )
  }
  className="section-title"
  style={{
    cursor: "pointer"
  }}
>

  <Bug size={22} />

  {
    showSymbolic
      ? "▼"
      : "▶"
  }

  {" "}

  Symbolic Execution Trace

</h2>
    <div className="status-pill blue">

      {
        symbolicTrace.length
      }

      {" "}
      Steps

    </div>

  </div>

  {/* CONTENT */}
  {
    showSymbolic && (
      <>

        {/* EMPTY STATE */}
        {
          symbolicTrace.length === 0 ? (

            <div
              style={{
                marginTop: "24px",
                padding: "24px",
                borderRadius: "18px",
                background:
                  "rgba(59,130,246,0.08)",
                border:
                  "1px solid rgba(59,130,246,0.18)",
                color:
                  "#60a5fa"
              }}
            >

              ⚡ No symbolic execution trace found

            </div>

          ) : (

            <div
              style={{
                marginTop: "28px",
                display: "flex",
                flexDirection: "column",
                gap: "18px"
              }}
            >

              {
                symbolicTrace.map(
                  (trace, index) => {

let color = "#38bdf8"

let bg =
  "rgba(56,189,248,0.08)"

let border =
  "1px solid rgba(56,189,248,0.18)"

let label =
  "EXECUTION TRACE"
if (
  trace.includes("⚠")
) {

  color = "#ef4444"

  bg =
    "rgba(239,68,68,0.08)"

  border =
    "1px solid rgba(239,68,68,0.18)"

  label =
    "SECURITY WARNING"

}

else if (
  trace.includes("External contract")
) {

  color = "#facc15"

  bg =
    "rgba(250,204,21,0.08)"

  border =
    "1px solid rgba(250,204,21,0.18)"

  label =
    "EXTERNAL INTERACTION"

}

else if (
  trace.includes("[PATH BLOCKED]")
) {

  color = "#60a5fa"

  bg =
    "rgba(59,130,246,0.08)"

  border =
    "1px solid rgba(59,130,246,0.18)"

  label =
    "BLOCKED EXECUTION"

}
                    return (

                      <div
                        key={index}
                        className="trace-card"
                        style={{
                          background: bg,
                          border
                        }}
                      >

                        {/* TOP ROW */}
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            flexWrap: "wrap",
                            gap: "16px",
                            marginBottom: "18px"
                          }}
                        >

                          <h3
                            style={{
                              margin: 0,
                              color,
                              fontSize: "18px"
                            }}
                          >

                            Step #{index + 1}

                          </h3>

                          <div
                            style={{
                              padding: "8px 16px",
                              borderRadius: "999px",
                              background:
                                "rgba(255,255,255,0.05)",
                              color,
                              fontWeight: "700",
                              fontSize: "13px"
                            }}
                          >

                            {label}

                          </div>

                        </div>

                        {/* TRACE CONTENT */}
                        <pre
                          style={{
                            margin: 0,
                            color: "#e2e8f0",
                            whiteSpace: "pre-wrap",
                            lineHeight: "1.8",
                            fontSize: "15px"
                          }}
                        >
                          {trace}
                        </pre>

                      </div>
                    )
                  }
                )
              }

            </div>
          )
        }

      </>
    )
  }

</div>
{/* ================================================= */}
{/* CFG GRAPH */}
{/* ================================================= */}
<div
  id="graph"
  className="glass-card dashboard-section"
>

  {/* SECTION HEADER */}
  <div className="section-header">

<h2
  onClick={() =>
    setShowGraph(!showGraph)
  }
  className="section-title"
  style={{
    cursor: "pointer"
  }}
>

  <GitBranch size={22} />

  {
    showGraph
      ? "▼"
      : "▶"
  }

  {" "}

  CFG / Execution Graph

</h2>

    <div className="status-pill green">

      {
        nodes.length
      }

      {" "}
      Nodes

    </div>

  </div>

  {/* CONTENT */}
  {
    showGraph && (
      <>

        {
            nodes.length > 0 ? (

            <div
              className="graph-wrapper"
              style={{
                marginTop: "30px"
              }}
            >

              {/* GRAPH HEADER */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: "16px",
                  marginBottom: "20px"
                }}
              >

                <div>

                  <h3
                    style={{
                      margin: 0,
                      fontSize: "24px"
                    }}
                  >
                    Smart Contract Control Flow
                  </h3>

                  <p
                    style={{
                      color: "#94a3b8",
                      marginTop: "8px"
                    }}
                  >
                    Interactive execution graph generated from symbolic analysis
                  </p>

                </div>

                {/* GRAPH STATUS */}
                <div
                  style={{
                    padding: "10px 18px",
                    borderRadius: "999px",
                    background:
                      "rgba(34,197,94,0.12)",
                    border:
                      "1px solid rgba(34,197,94,0.22)",
                    color:
                      "#4ade80",
                    fontWeight: "700",
                    fontSize: "14px"
                  }}
                >

                  ● Graph Active

                </div>

              </div>

              {/* GRAPH CONTAINER */}
              <div
                className="graph-container"
                style={{
  height: "1400px",
  borderRadius: "28px",
  overflow: "hidden",
  background:
  "radial-gradient(circle at center, #0f172a 0%, #020617 100%)",
backgroundSize: "400% 400%",
animation: "gradientMove 18s ease infinite"
}}
              >

<ReactFlow
  nodes={nodes}
  edges={edges}
  fitView
  fitViewOptions={{
    padding: 0.4
  }}
  proOptions={{
  hideAttribution: true
}}
defaultEdgeOptions={{
  type: "bezier",
  animated: true
}}
minZoom={0.4}
maxZoom={1.5}
onNodesChange={onNodesChange}
onEdgesChange={onEdgesChange}
>

  <MiniMap
    zoomable
    pannable
    nodeColor="#38bdf8"
      maskColor="rgba(2,6,23,0.55)"

  />

  <Background
    gap={24}
    size={1}
    color="rgba(56,189,248,0.12)"
  />

  <Controls />

</ReactFlow>

              </div>

            </div>

          ) : (

            <div
              style={{
                marginTop: "24px",
                padding: "24px",
                borderRadius: "18px",
                background:
                  "rgba(34,197,94,0.08)",
                border:
                  "1px solid rgba(34,197,94,0.18)",
                color:
                  "#4ade80"
              }}
            >

              🌐 No graph generated yet

            </div>
          )
        }

      </>
    )
  }

</div>
{/* ================================================= */}
{/* ATTACK CHAIN VISUALIZATION */}
{/* ================================================= */}
{
  attackPaths.length > 0 && (

    <div
      className="glass-card dashboard-section"
      style={{
        marginTop: "40px"
      }}
    >

      {/* HEADER */}
      <div className="section-header">

        <h2 className="section-title">

          <ShieldAlert size={22} />

          Attack Chain Visualization

        </h2>

        <div className="status-pill red">

          {
            attackPaths.length
          }

          {" "}
          Attack Paths

        </div>

      </div>

      {/* ATTACK CHAINS */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "20px",
          marginTop: "28px"
        }}
      >

        {
          attackPaths.map(
            (
              path,
              index
            ) => (

              <motion.div
                key={index}
                initial={{
                  opacity: 0,
                  y: 20
                }}
                animate={{
                  opacity: 1,
                  y: 0
                }}
                transition={{
                  duration: 0.4
                }}
                whileHover={{
                  scale: 1.01
                }}
                style={{

                  padding: "24px",

                  borderRadius: "20px",

                  background:
                    "linear-gradient(145deg,#450a0a,#7f1d1d)",

                  border:
                    "1px solid rgba(239,68,68,0.25)",

                  boxShadow:
                    "0 0 30px rgba(239,68,68,0.16)"
                }}
              >

                <h3
                  style={{
                    marginTop: 0,
                    color: "#fca5a5",
                    marginBottom: "18px"
                  }}
                >

                  Exploit Flow #{index + 1}

                </h3>

                <div
                  style={{
                    color: "#fee2e2",
                    fontSize: "16px",
                    lineHeight: "2",
                    fontWeight: "700",
                    wordBreak: "break-word"
                  }}
                >

                  {path}

                </div>

              </motion.div>
            )
          )
        }

      </div>

    </div>
  )
}

{/* ================================================= */}
{/* RAW ANALYZER OUTPUT */}
{/* ================================================= */}
<div
  id="logs"
  className="glass-card dashboard-section"
  style={{
    marginTop: "40px",
    marginBottom: "40px"
  }}
>

  {/* SECTION HEADER */}
  <div className="section-header">

<h2
  onClick={() =>
    setShowRaw(!showRaw)
  }
  className="section-title"
  style={{
    cursor: "pointer"
  }}
>

  <Terminal size={22} />

  {
    showRaw
      ? "▼"
      : "▶"
  }

  {" "}

  Full Analyzer Output

</h2>

    <div className="status-pill purple">

      RAW LOGS

    </div>

  </div>

  {/* CONTENT */}
  {
    showRaw && (

      <div
        className="raw-output-container"
      >

        {/* TERMINAL HEADER */}
        <div className="terminal-header">

          <div
            style={{
              display: "flex",
              gap: "10px"
            }}
          >

            <div className="terminal-dot red"></div>

            <div className="terminal-dot yellow"></div>

            <div className="terminal-dot green"></div>

          </div>

          <div
            style={{
              color: "#94a3b8",
              fontSize: "14px"
            }}
          >
            analyzer.log
          </div>

        </div>

        {/* RAW CONTENT */}
        <pre
          className="raw-output-text"
        >
          {rawOutput}
        </pre>

      </div>
    )
  }

</div>

      </div>

    </div>
    </>
  )
}
export default App
