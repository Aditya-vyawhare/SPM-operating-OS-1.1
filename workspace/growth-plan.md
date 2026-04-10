# 30-60-90 Day GMV Growth Plan (Dice Corporate Travel)

This plan aligns Product, Engineering, Supply, and Finance around one objective: grow GMV while improving realized revenue quality.

## Baseline snapshot (start of quarter)

- Current quarterly GMV: 400 Cr
- Current take rate: 3.0%
- Current leakage: 2.1% of GMV
- Daily bookings: 900
- Current conversion (search -> confirmed): 6.8%
- Current AOV: 49,500 INR
- Current ancillary attach rate: 18%
- Current repeat rate (30-day traveler): 22%
- Top constraints:
  - Fare mismatch at checkout causing high-intent drop-offs
  - Slow refund reconciliation and exception resolution
  - Weak enterprise onboarding activation in first 30 days

## Quarter target

- GMV growth target: +20% (400 Cr -> 480 Cr)
- Realized GMV protection target: leakage from 2.1% -> 1.2%
- Take rate target: 3.0% -> 3.3%

## Day 0-30: Diagnose and stabilize high-leakage/high-dropoff points

### Goals

- Establish a trusted baseline for conversion, AOV, repeat, and leakage by mode
- Ship quick wins that reduce conversion loss and manual finance effort

### Initiatives

- Funnel instrumentation hardening
  - Owner: Product Analytics + Engineering
  - Output: stage-wise drop-off dashboard for flight/hotel/bus/train
- Checkout fare integrity alerts
  - Owner: Pricing Platform + Supply
  - Output: real-time fare mismatch flag before payment submit
- Refund exception queue v1
  - Owner: Finance Ops + Backend
  - Output: SLA queue by aging/value-at-risk with owner assignment
- Enterprise onboarding activation playbook
  - Owner: Customer Success + Product
  - Output: 14-day launch checklist for top 20 new accounts

### Targets by day 30

- Conversion lift: +0.4 to +0.6 percentage points
- Leakage reduction: 0.2 points (2.1% -> 1.9%)
- Time-to-reconcile improvement: 25% faster for refund exceptions
- First-booking activation for new enterprises: +10%

## Day 31-60: Scale high-ROI interventions with controlled experiments

### Goals

- Scale proven changes and shut down low-yield work
- Increase AOV and ancillary realization without hurting conversion

### Initiatives

- A/B test ancillary bundles on top business routes
  - Owner: Growth PM + Flights Product + Design
  - Tests: bundle framing, price anchor, default selection
- Policy-aware checkout simplification
  - Owner: Traveler Experience + Admin Controls
  - Output: pre-validated policy badges and auto-filled traveler profiles
- Automated finance mismatch alerts
  - Owner: Finance Systems + Data
  - Output: daily anomaly alerts for fare/refund/tax mismatches
- Enterprise reactivation workflow for inactive accounts
  - Owner: CS Ops + CRM
  - Output: account-level triggers and outreach cadence

### Targets by day 60

- AOV lift: +3.0% to +4.0%
- Ancillary attach lift: +3 to +4 points (18% -> 21%-22%)
- Refund leakage reduction: additional 0.3 points (to 1.6%)
- Checkout completion lift: +0.5 points

## Day 61-90: Institutionalize the GMV growth engine

### Goals

- Convert tactical wins into repeatable operating systems
- Make leakage prevention and growth optimization part of weekly cadence

### Initiatives

- AI-assisted reconciliation workflow (invoice + refund + ancillary)
  - Owner: Finance Platform + Data Science
  - Output: confidence-based auto-resolution for low-risk mismatches
- Account-level retention plays
  - Owner: CS + Product Marketing
  - Output: route-specific offers and travel policy optimization reviews
- Executive GMV command center dashboard
  - Owner: BI + Product Ops
  - Output: single view for GMV drivers, take rate, leakage, and recovery backlog
- Quarterly growth operating rhythm
  - Owner: Product Leadership
  - Output: weekly growth review and monthly portfolio reallocation

### Targets by day 90

- Repeat rate lift: +3 to +4 points (22% -> 25%-26%)
- Net GMV lift: +18% to +22% vs baseline quarter
- Manual ops touch reduction: 35% in finance exception handling
- Leakage reduction: to 1.2% of GMV

## Effort vs ROI tracker (current view)

| Initiative | Effort | Expected GMV Impact | Owner | Status |
| --- | --- | --- | --- | --- |
| Checkout fare integrity alerts | M | +2.0% to +3.5% via conversion protection | Pricing Platform Lead | In progress |
| Refund exception queue + automation | M | +0.6% to +1.0% via leakage recovery | Finance Systems Lead | In progress |
| Ancillary bundle experiments | S-M | +2.0% to +3.0% via AOV and attach | Growth PM | Planned |
| Policy-aware checkout simplification | M | +1.5% to +2.5% via completion lift | Traveler Experience PM | Planned |
| Enterprise onboarding activation playbook | S | +1.0% to +2.0% via faster account ramp | CS Operations Manager | In progress |
| AI-assisted reconciliation workflow | L | +1.0% to +1.8% via sustained leakage control | Finance Platform PM | Planned |

## Risks and dependencies

- Key risks:
  - Aggressive upsell can hurt conversion if targeting is weak
  - Reconciliation automation quality may create false positives early
  - Cross-team dependencies can delay quarter outcomes
- External dependencies:
  - Supplier API reliability for fare and refund events
  - Payment gateway reconciliation data latency
  - Finance ops bandwidth for transition period
- Mitigation plans:
  - Use staged rollouts with strict guardrails
  - Keep manual override for all finance decisions in phase 1
  - Weekly dependency review with Product, Finance, Supply, and Engineering

## Weekly operating cadence

- Monday: growth KPI review (conversion, AOV, attach, repeat)
- Wednesday: leakage and reconciliation review (value-at-risk, recovery)
- Friday: experiment readout and next-week prioritization
