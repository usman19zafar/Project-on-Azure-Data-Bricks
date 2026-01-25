CROSS JOIN — Uzi Learning Framework v1.0
1. PURPOSE
Produce a Cartesian product:
Every left row × every right row.

2. UTILITY
Rare but useful when:

You need to duplicate a small dimension across a fact

You need all combinations of two small datasets

You need to generate permutations

3. WHY
Because sometimes business logic requires all combinations.

Example:
Generate all possible race × driver combinations.

4. WHICH
Cross Join vs Inner Join:

Inner Join → matches only

Cross Join → matches everything with everything

5. WHEN
Use Cross Join only when:

Both datasets are small

You intentionally want a Cartesian product

You understand the explosion in row count

6. HOW
Pattern:

Code
df_left.crossJoin(df_right)
7. CONSTRAINTS
Critical constraints:

Can explode to billions of rows

Can cause out‑of‑memory errors

Must NOT be used on large datasets

Must be used intentionally, never accidentally

8. VALIDATION
Row count = left_count × right_count

Schema = all columns from both sides

No join condition

9. AI PARTNERSHIP
You decide:

whether a Cartesian product is safe

whether the datasets are small

AI writes:

code

count checks

safety warnings

Cross Join in One Line (Uzi v1.0)
Cross Join = every row on the left combined with every row on the right.

FINAL — All Three Joins in One ASCII Table (Uzi v1.0)
Code
+---------------+-------------------------------------------+-------------------------------------------+
| Join Type     | Purpose                                   | Output                                    |
+---------------+-------------------------------------------+-------------------------------------------+
| Semi Join     | Left rows WITH matches                    | Left columns only                         |
| Anti Join     | Left rows WITHOUT matches                 | Left columns only                         |
| Cross Join    | Cartesian product (all combinations)      | All columns, left × right rows            |
+---------------+-------------------------------------------+--------------------------------
