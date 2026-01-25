ANTI JOIN — Uzi Learning Framework v1.0
1. PURPOSE
Return left rows that do NOT have a match on the right.

2. UTILITY
Use Anti Join to find missing relationships.

Examples:

Circuits with no races

Drivers with no results

Products with no sales

Customers with no orders

This is extremely useful for data quality, gap analysis, and audit logic.

3. WHY
Because real data is incomplete.
Anti Join exposes what’s missing.

4. WHICH
Anti Join vs Semi Join:

Semi Join → rows WITH matches

Anti Join → rows WITHOUT matches

Opposites.

5. WHEN
Use Anti Join when:

You want to detect missing data

You want to find orphan records

You want to validate referential integrity

You want to identify gaps in ingestion

6. HOW
Pattern:

Code
df_left.join(df_right, condition, "left_anti")
7. CONSTRAINTS
Cannot select right‑side columns

Only returns left‑side schema

Only returns unmatched rows

8. VALIDATION
Row count = number of left rows with no match

Schema = only left columns

All join‑key values should NOT appear in right dataset

9. AI PARTNERSHIP
You decide:

what “missing” means

which side is primary

AI writes:

join code

validation checks

Anti Join in One Line (Uzi v1.0)
Anti Join = return left rows that do NOT exist on the right.
