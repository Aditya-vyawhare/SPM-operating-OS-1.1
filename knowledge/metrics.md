# Core Metrics Dictionary (GMV Operating System)

Use these definitions consistently in PRDs, reviews, and experiments.

## GMV

Definition:

- Total gross value of confirmed bookings (flights, hotels, bus, train) in a period before cancellations and refunds.

Formula:

- GMV = sum(confirmed booking amount)

Cut views by:

- mode, route type (domestic/international), customer segment, company tier, source channel

## Conversion Rate

Definition:

- Percent of booking sessions that end in a confirmed booking.

Formula:

- Conversion rate = confirmed bookings / booking-intent sessions

Track funnel checkpoints:

- search -> itinerary view -> traveler details -> payment -> confirmation

## AOV (Average Order Value)

Definition:

- Average GMV per confirmed booking.

Formula:

- AOV = GMV / confirmed bookings

## Repeat Rate

Definition:

- Percent of active customers (or companies) who make another booking in the defined repeat window.

Formula:

- Repeat rate = repeat bookers in window / active bookers in base window

Standard windows:

- 30-day traveler repeat
- 90-day company repeat

## Ancillary Attach Rate

Definition:

- Percent of bookings with one or more ancillaries (seat, meal, baggage, insurance, flex change).

Formula:

- Attach rate = bookings with ancillary / confirmed bookings

## Cancellation/Refund Leakage Percentage

Definition:

- Percent of GMV lost due to unrecovered or incorrectly processed cancellations/refunds.

Formula:

- Leakage % = unrecovered cancellation/refund value / GMV

Leakage categories:

- supplier refund shortfall
- missed refund claim
- delayed credit note
- incorrect fee reversal

## Guardrail metrics

- Take rate (revenue / GMV)
- Contribution margin
- Payment success rate
- Refund SLA attainment
- Manual ops touches per 100 bookings
