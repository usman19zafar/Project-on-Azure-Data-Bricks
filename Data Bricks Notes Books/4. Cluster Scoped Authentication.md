Cluster Scoped Authentication (Databricks)

1. What We Did Before (Session‑Scoped Authentication)
Spark configs + secrets (access key, SAS, SP) were set inside the notebook.

Notebook executed on a cluster → cluster used those secrets to access ADLS.

Authentication was valid only for that notebook session.

Detaching the notebook required re-authentication.

This model = Session Scoped Authentication.

2. What We Want Now (Cluster‑Scoped Authentication)
Instead of configuring secrets in each notebook,
configure them once at the cluster level.

Every notebook attached to that cluster automatically inherits access.

Authentication happens when the cluster starts, not per notebook.

3. How Cluster‑Scoped Authentication Works
Add Spark configs + secrets directly in Cluster → Edit → Advanced Options → Spark Config.

These configs run at cluster startup.

Cluster authenticates to ADLS before any notebook runs.

All notebooks on that cluster can access the storage without setting configs.

4. Steps to Configure Cluster‑Scoped Authentication
Step 1 — Open Cluster Settings
Go to Compute → Your Cluster → Edit

Expand Advanced Options → Spark Config

Step 2 — Add Spark Config
Example (Access Key):

Code
fs.azure.account.key.<storage-account>.dfs.core.windows.net <access-key>
Name = Spark config key

Value = secret

Space separates them (name-value pair)

Step 3 — Restart Cluster
After adding configs → click Confirm and Restart

Cluster restarts with new authentication settings.

Step 4 — Use Notebook Without Configs
Remove Spark configs from notebook.

Run:

```python
dbutils.fs.ls("abfss://<container>@<storage-account>.dfs.core.windows.net/")
```
Files should list successfully.

Step 5 — Clean Up
Remove Spark config from cluster after lesson.

Restart cluster again.

5. Drawbacks of Cluster‑Scoped Authentication
All notebooks on that cluster get full access.

Cannot restrict access per user or per notebook.

Forces you to create separate clusters for different permission groups.

Not ideal for large teams or mixed roles (e.g., engineers vs analysts).

Not widely used in industry due to security + governance limitations.

6. When Cluster‑Scoped Authentication Is Acceptable
Small teams

Single permission group

Training environments

Temporary development clusters

Quick demos or POCs

7. When NOT to Use It
Enterprise environments

Multi-team clusters

Mixed access requirements

Production workloads

When using Unity Catalog (better alternatives exist)

8. Supported Authentication Methods for Cluster Scope
You can store any of these in cluster Spark config:

Access Key

SAS Token

Service Principal (Client ID + Secret + Tenant ID)

Two‑Word Logic (Your Style)
Session Scoped → Notebook Auth  
Cluster Scoped → Startup Auth

If you want, I can also produce:

an ASCII diagram comparing Session vs Cluster Scoped

a DAIS‑10 style decision matrix for choosing authentication methods

a GitHub‑ready version of these notes

Just tell me the direction you want.

an ASCII diagram comparing Session vs Cluster Scoped
Here you go, Usman — a clean, side‑by‑side ASCII comparison of Session‑Scoped vs Cluster‑Scoped authentication.
Designed exactly in your architect‑grade workbook style.

```Code
+--------------------------------------------------+--------------------------------------------------+
|              SESSION‑SCOPED AUTH                 |              CLUSTER‑SCOPED AUTH                 |
+--------------------------------------------------+--------------------------------------------------+
| Notebook sets Spark configs                      | Cluster sets Spark configs                       |
| (access key, SAS, SP creds)                      | (access key, SAS, SP creds)                      |
+--------------------------------------------------+--------------------------------------------------+
| Authentication happens WHEN notebook runs         | Authentication happens WHEN cluster starts      |
+--------------------------------------------------+--------------------------------------------------+
| Only that notebook session gets access            | ALL notebooks attached to the cluster get access|
+--------------------------------------------------+--------------------------------------------------+
| Access ends when notebook detaches                | Access persists as long as cluster is running   |
+--------------------------------------------------+--------------------------------------------------+
| Good for mixed‑access environments                | Not good for mixed‑access environments          |
| (engineers vs analysts)                           | (everyone on cluster gets same permissions)     |
+--------------------------------------------------+--------------------------------------------------+
| More secure, more granular                        | Less secure, broad access                       |
+--------------------------------------------------+--------------------------------------------------+
| Common in production                              | Rare in production                              |
+--------------------------------------------------+--------------------------------------------------+
| Per‑notebook control                              | Per‑cluster control                             |
+--------------------------------------------------+--------------------------------------------------+
| Example Flow:                                     | Example Flow:                                   |
| Notebook → Spark Config → ADLS                    | Cluster → Spark Config → ADLS                   |
+--------------------------------------------------+--------------------------------------------------+
```
DAIS‑10 style decision matrix for choosing between the two
Here it is, Usman — a DAIS‑10 style decision matrix, clean, decisive, architect‑grade.
This is exactly the kind of artifact you’d include in a governance workbook: crisp rows, binary choices, and a clear recommendation path.

DAIS‑10 Decision Matrix: Session‑Scoped vs Cluster‑Scoped Authentication

```Code
+-------------------------------+---------------------------+----------------------------+
| DAIS‑10 Criterion             | Session‑Scoped Auth       | Cluster‑Scoped Auth        |
+-------------------------------+---------------------------+----------------------------+
| 1. Identity Boundary          | Per‑notebook              | Per‑cluster                |
|                               | (fine‑grained)            | (broad access)             |
+-------------------------------+---------------------------+----------------------------+
| 2. Access Control             | Strong, user‑specific     | Weak, shared by all users  |
+-------------------------------+---------------------------+----------------------------+
| 3. Least Privilege            | Easy to enforce           | Hard to enforce            |
+-------------------------------+---------------------------+----------------------------+
| 4. Multi‑Team Suitability     | Excellent                 | Poor                       |
|                               | (engineers vs analysts)   | (everyone gets same perms) |
+-------------------------------+---------------------------+----------------------------+
| 5. Security Posture           | High                      | Medium/Low                 |
+-------------------------------+---------------------------+----------------------------+
| 6. Operational Flexibility    | High                      | Low                        |
|                               | (notebooks independent)   | (cluster locked to one use)|
+-------------------------------+---------------------------+----------------------------+
| 7. Scalability                | Scales with teams         | Scales only with clusters  |
+-------------------------------+---------------------------+----------------------------+
| 8. Governance & Auditability  | Strong                    | Weak                       |
+-------------------------------+----------------------------+---------------------------+
| 9. Secret Exposure Risk       | Lower                     | Higher                     |
|                               | (stored in scopes)        | (stored in cluster config) |
+-------------------------------+----------------------------+---------------------------+
| 10. Industry Adoption         | Common                    | Rare                       |
+-------------------------------+----------------------------+---------------------------+
| **Recommended Use Case**      | Production, multi‑team    | Small teams, POCs, demos   |
|                               | secure workloads          | uniform access needs       |
+-------------------------------+---------------------------+----------------------------+

```
Two‑Word Logic (DAIS‑10 Summary)
Session‑Scoped → Granular Security  
Cluster‑Scoped → Shared Access
