# Parrot-proxy
HTTP Request Analyzer &amp; Replay Tool
A modular HTTP replay, fuzzing and reconnaissance automation framework written in Python.

Captures HTTP requests, stores them locally, replays them with mutations, analyzes responses for anomalies, and generates findings and reports. The project was build to automate common bug bounty and web app reconnaissance workflows.

---

## Features
### Request Capture
    * Import raw HTTP requests
    * Store requests in a local database
    * Retrieve and replay captured traffic

### Replay Engine
    * Replay saved requests
    * Modify parameters, headers, and request bodies
    * Async replay support
    * Concurrent execution

### Fuzzing
    * Query parameter fuzzing
    * Header fuzzing
    * JSON body fuzzing
    * Payload mutation workflows

### Analysis
    * Response comparison
    * Reflection detection
    * Context-aware reflection analysis
    * Response clustering
    * Anomaly detection
    * Vulnerability heuristics

### Detection Engine
    * SQL error detection
    * XSS reflection detection
    * Path traversal indicators
    * SSTI indicators
    * Custom YAML-based signatures

### Reporing
    * Markdown report generation
    * Campaign summaries
    * Finding exports

### Workflow Automation
    * YAML campaign definitions
    * Multi-stage recon workflows
    * Automated replay pipelines
    
---

## Architecture

---

## Tech Stack

---

## Installation

---

## Quick Start