# Skill: Revenue Leakage Detection

Use this skill when leakage is suspected in fares, refunds, ancillaries, or tax reconciliation.

## Objective

Detect, quantify, and prioritize leakage recovery opportunities with a repeatable workflow.

## Signals to collect

- Booking confirmation amount
- Supplier issued amount (ticket/invoice)
- Payment captured amount
- Cancellation and refund events
- Ancillary order and settlement records
- Tax/GST lines in customer and supplier invoices

## Method

## 1) Build reconciliation keys

- PNR/ticket ID for flights
- booking ID + supplier reference for hotels
- order ID + invoice ID + payment ID for all modes

## 2) Run deterministic checks

- Fare mismatch: booked vs issued vs settled
- Refund mismatch: expected refund vs received refund
- Ancillary mismatch: sold vs charged vs settled
- Tax mismatch: booked tax rules vs invoiced tax lines

## 3) Run anomaly detection

Flag outliers for:

- route-level fare deltas
- supplier-level refund delay
- sudden ancillary realization drops
- unusual tax correction patterns

## 4) Prioritize by value at risk

Score each issue:

- leakage value
- recoverability probability
- compliance risk
- aging (time sensitivity)

## 5) Drive action

- Auto-close low-risk, low-value mismatches inside tolerance
- Route high-value cases to finance ops queue
- Escalate systemic root causes to product/engineering

## Standard outputs

- Leakage by category (% GMV and absolute value)
- Top 10 recoverable cases
- Root-cause themes with owner and ETA
- Weekly prevention actions
