# This Week Ship Plan (GMV First)

Week objective: deliver measurable GMV impact within 7 days while reducing realized GMV leakage risk.

## Weekly target outcomes

- Conversion: +0.2 to +0.4 percentage points
- Leakage: -0.1 to -0.2 points (from current baseline)
- Ancillary attach: +0.8 to +1.5 points
- Refund SLA attainment: +10 to +15 points
- Manual finance ops touches: -10%

## Prioritized ship list (60/30/10)

### 60% Near-term GMV wins

1) Checkout fare integrity guardrail (P0)
- GMV impact: protects high-intent bookings, expected +0.8% to +1.5% gross GMV via reduced checkout failures
- Effort/ROI: Medium effort, high ROI (payback in 1-2 weeks)
- Scope this week:
  - Block payment when quote vs ticket fare delta exceeds route threshold
  - Show clear traveler message and 1-click reprice flow
  - Log mismatch events by supplier/route
- Owners: Pricing Platform PM, Checkout Eng Lead, Supply Ops
- Success metric: checkout drop due to fare change down 15%+

2) Refund exception queue v1 with value-at-risk sorting (P0)
- GMV impact: recovers leakage, expected +0.3% to +0.7% realized GMV protection
- Effort/ROI: Medium effort, very high ROI (direct recovery)
- Scope this week:
  - Queue grouped by aging bucket, amount, and supplier
  - SLA tags: <3d, 3-7d, >7d
  - Owner assignment + daily resolution tracker
- Owners: Finance Systems PM, Backend Lead, Finance Ops Manager
- Success metric: >7 day refund backlog reduced 20%+

3) Ancillary attach nudge on top 20 routes (P1)
- GMV impact: +0.2% to +0.5% GMV via AOV/attach lift
- Effort/ROI: Small-Medium effort, high ROI
- Scope this week:
  - Simple bundle prompt (seat + meal + baggage) pre-selected only on high-confidence routes
  - Guardrail: conversion non-inferiority threshold (-0.2 pp max)
  - Segment split: traveler type and route class
- Owners: Growth PM, Flights PM, Frontend Lead
- Success metric: attach up 1 point with no conversion regression

### 30% System improvements

4) Funnel instrumentation hardening (P1)
- GMV impact: indirect, enables faster iteration and cleaner causality
- Effort/ROI: Small effort, medium ROI (compounding)
- Scope this week:
  - Enforce canonical events for search -> itinerary -> traveler -> payment -> confirmation
  - Add event QA checklist and data completeness alert
- Owners: Product Analytics Lead, Data Engineer
- Success metric: event completeness >98% for funnel stages

5) GST/tax pre-validation for cancellation invoices (P1)
- GMV impact: protects realized GMV and month-end close quality
- Effort/ROI: Medium effort, medium-high ROI
- Scope this week:
  - Rule checks for tax code/rate/place-of-supply at credit-note generation
  - Exception list to finance before filing cycle
- Owners: Finance Platform PM, Compliance Analyst
- Success metric: tax exception rate down 25%

### 10% Exploratory bets

6) Enterprise activation trigger test (P2)
- GMV impact: potential +0.2% to +0.6% via faster first booking ramp
- Effort/ROI: Small effort, moderate ROI with learning value
- Scope this week:
  - Trigger CS outreach if no first booking in 7 days from onboarding
  - Test 2 playbooks: policy setup-first vs route recommendations-first
- Owners: CS Ops Manager, Lifecycle PM
- Success metric: first-booking activation +5% in test cohort

## Execution plan (day-by-day)

Monday
- Lock scope, owners, and metrics for P0/P1 items
- Start engineering on fare guardrail and refund queue
- Publish baseline dashboard snapshot

Tuesday
- Ship internal beta of refund queue to finance ops
- Complete fare mismatch thresholds per top routes/suppliers
- Validate instrumentation events in staging

Wednesday
- Release fare guardrail to 20% traffic
- Start ancillary nudge experiment on top 20 routes
- Run leakage review and exception triage

Thursday
- Ramp fare guardrail to 50% if guardrails hold
- Enable tax pre-validation in shadow mode
- Fix top 3 funnel event quality gaps

Friday
- Readout: conversion, leakage recovery, attach, refund SLA
- Decide ramp to 100% or rollback criteria for each launch
- Freeze next-week priorities based on measured ROI

## Trade-offs and risks

- Growth vs margin: aggressive ancillary prompts may hurt conversion; mitigate with strict non-inferiority guardrails
- Speed vs control: fast refund automation can create false positives; keep manual override for high-value cases
- Automation vs operational risk: tax rules may miss edge cases; run shadow mode before enforcement
- Cross-team dependency risk: pricing/supply and finance data latency can slow outcomes; set daily blocker standup

## Weekly KPI scoreboard

- GMV (gross, net, realized)
- Conversion (end-to-end + stage drop-offs)
- AOV and ancillary attach rate
- Leakage % and recovered value
- Refund SLA attainment
- Manual ops touches per 100 bookings

## Decision rules for next week

- If fare-guardrail conversion lift >= +0.2 pp and no payment drop, ramp to 100%
- If ancillary attach lifts but conversion drops >0.2 pp, narrow targeting before scale
- If refund backlog reduction <10%, increase queue automation and staffing for top suppliers
- If tax exceptions persist > baseline, keep shadow mode and add rule refinements
