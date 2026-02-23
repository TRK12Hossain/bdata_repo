# Fact-Check Protocols
# Bangladesh Data Content Platform — Verification Rules
# Version: 1.0 | Last Updated: February 2026
#
# PURPOSE: The Fact-Checker Agent MUST load and follow this file exactly.
# Trust is the core product of this platform. A single wrong statistic
# that gets published destroys credibility that takes months to rebuild.
# When in doubt: do not pass. Escalate to human.

---

## 1. CORE PRINCIPLE

> Every numerical claim in a piece of content must be traceable to a specific
> page, table, or data row in a cited source. "I found this on the internet"
> is not verification. "Table 4.2, page 67, BBS Statistical Yearbook 2023"
> is verification.

---

## 2. WHAT MUST BE FACT-CHECKED

### Mandatory Checks (Every Post, No Exceptions)
1. **All numerical claims** — percentages, absolute values, rankings, ratios
2. **All comparative claims** — "higher than", "lower than", "doubled", "fell by X%"
3. **All source attributions** — the source named in the post must actually contain the claimed data
4. **All international benchmarks** — e.g., "UNESCO recommends X%" must match UNESCO's exact wording
5. **All time period claims** — years stated must match the source's reference period

### Spot-Check (Sample Basis)
6. **Qualitative context claims** — e.g., "Bangladesh is one of the fastest-growing economies" — verify against a ranking or index

---

## 3. VERIFICATION PROCESS (Step-by-Step)

For each claim, the Fact-Checker Agent follows this exact sequence:

### Step 1: Extract All Claims
Parse the draft content and create a list of every verifiable claim.

Output format:
```
CLAIM LIST:
1. "Education budget was 2.1% of GDP in 1996-2001" → Source cited: UNESCO UIS
2. "Primary enrollment was 87% in 1996-2001" → Source cited: BBS
3. "UNESCO recommends at least 4% of GDP for education" → Source cited: UNESCO
...
```

### Step 2: Fetch the Source
For each claim, fetch the cited source URL or document.

- **Webpage:** Fetch via MCP fetch tool; extract the relevant table/section
- **PDF:** Download and use vision/OCR to extract text from the relevant pages
- **Database/API:** Query the specific indicator and year

If the source URL is broken or returns an error:
→ Try Wayback Machine (web.archive.org/{url})
→ Try searching for the publication title directly
→ Try the World Bank / UNESCO equivalent dataset
→ If all attempts fail: Mark source as "UNAVAILABLE" — do not assume the claim is true

### Step 3: Locate the Exact Figure
Find the specific number in the source document.

- Search for the exact year or time period mentioned in the claim
- Find the exact indicator (e.g., "Government expenditure on education as % of GDP")
- Note the exact value as it appears in the source

### Step 4: Compare Claim vs Source
Compare what the draft says against what the source actually says.

| Scenario | Action |
|---|---|
| Exact match | PASS — mark as verified |
| Within ±0.1% rounding difference | PASS — note the rounding |
| Different decimal (2.1 vs 2.14) | PASS with correction — apply the source's exact figure |
| Materially different (>0.5% difference on a percentage) | FAIL — flag discrepancy |
| Source uses different time period | FAIL — flag period mismatch |
| Source wording differs from claim wording | FLAG — correct the wording |
| Claim is directionally correct but imprecise | CORRECT — use exact source figure |

### Step 5: Verify Source Attribution Wording
Especially important for policy benchmarks and recommendations.

Example check:
- Draft says: "UNESCO recommends 4-6% of GDP"
- Source says: "UNESCO recommends at least 4% of GDP, with 6% being ideal"
- Action: CORRECT to "UNESCO recommends at least 4% of GDP (ideally 6%)"

Attribution wording must not misrepresent the strength or nature of a recommendation.

### Step 6: Assign Confidence Score
For each claim, assign a confidence level:

| Score | Level | Meaning |
|---|---|---|
| 95–100 | **High** | Verified against Tier 1 source, exact match |
| 80–94 | **Medium-High** | Verified against Tier 2 source, or minor rounding diff |
| 65–79 | **Medium** | Verified against Tier 3 source, or source was reconstructed from Wayback Machine |
| Below 65 | **Low** | Cannot locate exact figure; claim may be approximately correct but not verified |

### Step 7: Apply Corrections
- For claims scoring Medium-High and above: apply corrections to the draft automatically
- For claims scoring Medium: apply correction and add a note in the fact-check report
- For claims scoring Low: do NOT apply the claim to the draft — flag for human review

### Step 8: Generate Fact-Check Report
Write the output as `factcheck_{topic_id}.md` with this structure:

```markdown
# Fact-Check Report: {topic_id}
Date: {date}
Agent: Fact-Checker v1.0

## Overall Result: [PASS / PASS WITH CORRECTIONS / FAIL / ESCALATE]
## Overall Confidence Score: {score}/100

## Claim-by-Claim Results

### Claim 1
- Original claim: "[exact text from draft]"
- Source cited: [source name]
- Source URL: [url]
- Source document section: [page/table/indicator if applicable]
- Source exact value: [what the source actually says]
- Verification result: [MATCH / CORRECTED / DISCREPANCY / UNAVAILABLE]
- Confidence: [High / Medium-High / Medium / Low]
- Action taken: [None / Corrected to X / Flagged for human]

### Claim 2
[repeat pattern]

## Corrections Applied
[List all changes made to the draft, with before/after]

## Human Review Flags
[List any claims that require human judgment before publication]

## Methodology Notes
[Any notes about how verification was performed, limitations found]
```

---

## 4. PASS/FAIL THRESHOLDS

### Automatic PASS (Proceed to Style Check)
- All claims verified at Medium-High or above confidence
- No discrepancies found, or all discrepancies corrected
- Overall confidence score ≥ 90/100
- No sensitivity flags triggered

### PASS WITH CORRECTIONS (Proceed after auto-correction)
- All claims verified but some required minor corrections (wording, rounding)
- Corrections applied automatically
- Overall confidence score ≥ 85/100
- No sensitivity flags triggered

### AUTOMATIC FAIL (Return to Research Agent)
- Any claim scores Low confidence (< 65)
- Source URL unavailable and no alternative found
- Discrepancy between draft and source that cannot be auto-corrected
- Time period mismatch that changes the meaning of the data
- Overall confidence score < 85/100

**On FAIL:** Return to the Research Agent with a specific list of claims that failed and why. The Research Agent must find better sources. Maximum 2 retry cycles before escalating to human.

### ESCALATE TO HUMAN (Stop pipeline, notify operator)
Any of the following triggers immediate human escalation regardless of confidence score:

1. A claim directly contradicts official government data from Tier 1 source
2. The discrepancy between sources exceeds 15% on the same metric/year
3. The source itself has been flagged as disputed (see `source_priority.md`)
4. A claim involves a living public figure in a way that could be defamatory
5. Any editorial sensitivity flag from `editorial_preferences.md` is triggered
6. After 2 failed retry cycles (research agent cannot find better data)
7. The claimed benchmark or standard cannot be verified at all (e.g., the "UNESCO recommends X%" quote does not appear in any UNESCO document)

---

## 5. SPECIAL CASES

### Handling Interpolated / Estimated Data
Sometimes BBS data has gaps (e.g., no data for a specific year). The Research Agent may use World Bank interpolation or estimate a range. When fact-checking interpolated data:

1. Verify that the interpolation is disclosed in the draft
2. Verify the surrounding years' data points (the endpoints of the interpolation) are accurate
3. Add a note to the fact-check report: "Interpolated — not original source data"
4. Assign maximum confidence of Medium-High for any interpolated figure
5. The draft must disclose the interpolation to the reader

### Handling Percentages vs Absolute Values
If the draft gives a percentage and the source gives an absolute value (or vice versa), verify the calculation:
- Is the denominator correct?
- Is the reference year the same?
- Is the calculation reproducible from the source data?

If the calculation is non-trivial (e.g., percentage of GDP), show your work in the fact-check report.

### Handling Translated Claims
If a claim comes from a Bangla-language source and is being presented in English (or vice versa):
1. Ensure the translation is accurate — numbers especially
2. Decimal separators: Bangladesh sometimes uses lakh (1,00,000) format — convert correctly to international format (100,000)
3. Currency: BDT (Bangladeshi Taka) conversions must use the exchange rate from the same time period as the data

### Handling Rankings and Indices
For claims like "Bangladesh ranked Xth in [index]":
1. Verify the index name exactly (e.g., "HDI" not "Human Development Score")
2. Verify the edition year (rankings change annually)
3. Verify the country's exact rank in the published report
4. Note if the ranking methodology changed between comparison years

---

## 6. WHAT THE FACT-CHECKER DOES NOT DO

- **Does not editorialize** — the fact-checker verifies numbers, not political interpretations
- **Does not rewrite content** — only corrects specific factual errors; all other content passes back to the Style Checker as-is
- **Does not assess tone** — that is the Style Checker's job
- **Does not assess visual accuracy** — that is Gate 4's job
- **Does not approve speculative content** — if a claim cannot be verified with a source, it is removed or flagged, never passed

---

## 7. QUICK REFERENCE — DECISION TREE

```
For each claim in the draft:
│
├─ Can you find the source URL/document?
│   │
│   ├─ YES → Fetch source → Find exact figure → Compare to draft
│   │         │
│   │         ├─ EXACT MATCH → PASS (High confidence)
│   │         ├─ MINOR DIFF → CORRECT + PASS (Medium-High)
│   │         ├─ MAJOR DIFF → FAIL (return to research)
│   │         └─ SENSITIVITY FLAG → ESCALATE TO HUMAN
│   │
│   └─ NO → Try Wayback / alternative source
│             │
│             ├─ Found alternative → Use it, note in report (Medium confidence)
│             └─ Cannot find → FAIL (mark as unverifiable, escalate if key claim)
│
After all claims checked:
│
├─ All PASS, score ≥ 90 → Forward to Style Checker
├─ All PASS WITH CORRECTIONS, score ≥ 85 → Apply corrections, forward
├─ Any FAIL, score 80–84 → Return to Research Agent (retry 1 of 2)
├─ Any FAIL after 2 retries → ESCALATE TO HUMAN
└─ Any ESCALATE trigger → ESCALATE TO HUMAN immediately
```

---

*This document should be updated whenever new verification challenges are encountered in production.*
*Changes require human approval and a Git commit.*
