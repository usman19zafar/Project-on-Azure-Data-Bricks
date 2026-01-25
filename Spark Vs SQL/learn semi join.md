SEMI JOIN — Uzi Learning Framework v1.0
1. PURPOSE
Return only the left rows that have a match on the right — but do NOT return any right‑side columns.

2. UTILITY
Use Semi Join when you want to filter the left dataset based on existence in the right dataset.

Examples:

“Give me circuits that have races.”

“Give me drivers that appear in results.”

“Give me products that have sales.”

It’s a filter, not a merge.

3. WHY
Why does Semi Join exist?

Because sometimes you only care about which left rows have matches, not the right‑side data.

It’s a relational existence check.

4. WHICH
Semi Join vs Inner Join:

Inner Join → returns columns from both sides

Semi Join → returns only left columns

5. WHEN
Use Semi Join when:

You only need left‑side columns

You want a fast existence check

You want to avoid duplicate columns

You want a clean left‑side dataset filtered by right‑side matches

You do not use it when you need right‑side data.

6. HOW
Pattern (not memorized):

Code
df_left.join(df_right, condition, "left_semi")
7. CONSTRAINTS
Cannot select right‑side columns

Will error if you try

Only returns left‑side schema

Not useful when you need combined data

8. VALIDATION
Row count = number of left rows that have matches

Schema = only left columns

No NULLs (because unmatched rows are removed)

9. AI PARTNERSHIP
You decide:

join key

join type

expected behavior

AI writes:

syntax

renaming

validation code

Semi Join in One Line (Uzi v1.0)
Semi Join = Inner Join that returns only the left rows and left columns.
