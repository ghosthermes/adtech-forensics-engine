# Ad-Tech Forensics Engine

A headless Playwright-based framework designed for generating defensible, reproducible forensic HAR captures for privacy litigation (CIPA, VPPA, UDTP) and ad-tech compliance auditing.

## Overview
Traditional manual testing fails to meet the evidentiary standards required for modern arbitration and class-action litigation. This engine automates the capture and analysis of network traffic at the protocol level, documenting precisely how third-party trackers (Meta, Google, TikTok, Adobe) exfiltrate PII and persistent identifiers.

## Core Capabilities
- **Forensic Integrity:** Generates hash-verified HAR (HTTP Archive) files with UTC-synchronized timestamps.
- **PII Injection Probe:** Programmatically identifies and interacts with DOM elements (email/phone inputs) to trigger "blur" event listeners used by aggressive scraping scripts.
- **Deobfuscation:** Decodes Base64/JSON-encoded payloads used by Prebid and DFP to obscure cross-site user synchronization.
- **Consent Monitoring:** Synchronous tracking of Consent Management Platform (OneTrust, Optanon) initialization state vs. tracker firing times.

## Workflow
1. **Capture:** `python scripts/capture.py <url>`
   - Headless Chromium execution with human-mimicry (scrolling/delayed wait).
   - Real-time network interception and HAR serialization.
2. **Analysis:** `python scripts/parse_har.py`
   - Automated identification of SHA-256 hashed emails and persistent UUIDs.
   - Domain-specific analysis for high-risk ad-tech endpoints.

## Legal Utility
Designed for litigation support teams to generate reproducible "Technical Findings" reports that survive adversarial scrutiny and expert witness challenges.