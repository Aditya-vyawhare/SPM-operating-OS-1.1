# Revenue Leakage Map (Dice Travel)

Leakage is unrecovered value between expected and realized booking economics.

## Primary leakage points

## 1) Airline pricing mismatch

How it happens:

- Fare shown to traveler differs from ticketed supplier fare
- Markup/commission misapplied during final ticketing

Typical impact:

- 0.4% to 1.0% of flight GMV

Detection strategy:

- Compare quote snapshot vs issued ticket fare
- Alert when difference exceeds route-specific tolerance
- Reconcile by PNR/ticket within T+1

## 2) Refund errors

How it happens:

- Partial refunds not captured
- Supplier refunds received but not mapped to booking
- Incorrect fee reversals during cancellation/reissue

Typical impact:

- 0.5% to 1.2% of refundable booking GMV

Detection strategy:

- Link cancellation events to supplier credit notes and bank settlement
- Flag aged refund cases beyond SLA
- Run exception queues by amount and aging bucket

## 3) Missed ancillaries

How it happens:

- Ancillary sold but not charged or not invoiced
- Supplier ancillary settlement not reconciled to traveler invoice

Typical impact:

- 0.2% to 0.6% of total GMV (higher for air-heavy mix)

Detection strategy:

- Compare ancillary order events vs payment capture vs supplier settlement
- Daily report on ancillary attach-to-realization gap

## 4) GST/tax issues

How it happens:

- Wrong tax code, rate, or place of supply
- Credit note tax mismatch leading to claim loss

Typical impact:

- 0.1% to 0.4% of GMV and delayed close risk

Detection strategy:

- Rule-based tax validation at invoice creation
- Auto-match invoice tax lines with booking and supplier docs
- Pre-filing exception checks for finance

## Estimated annualized leakage model

Given baseline volume (~800 bookings/day), even 1.5% leakage can represent significant lost GMV realization and margin erosion.

Scenario ranges:

- Low case: 1.2% leakage
- Base case: 2.0% leakage
- High case: 3.2% leakage

## Leakage control operating cadence

- Daily: exception queue triage for fare/refund mismatches
- Weekly: root-cause breakdown and top vendor/routing anomalies
- Monthly: leakage trend by category, recovered value, and prevention actions

## System controls to implement

- Real-time mismatch checks at confirmation and settlement
- AI-assisted reconciliation for refunds and ancillaries
- Threshold-based auto-resolution for low-risk mismatches
- Full audit log for finance and compliance
