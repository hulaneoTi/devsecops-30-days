# AWS sandbox (Week 4)

One EC2 instance running the app container, built to be created and destroyed in each study session.

| Choice | Why |
| --- | --- |
| IMDSv2 only | Blocks SSRF-style theft of instance credentials |
| Encrypted root volume | Data at rest is encrypted |
| No SSH, access via SSM Session Manager | No open port 22, no keys to leak |
| Inbound only from `allowed_cidr` | App reachable from my IP only |
| Default security group locked | Nothing attaches to it by accident |
| Container runs read-only, no capabilities | Smaller blast radius if the app is compromised |
| GitHub OIDC, no stored AWS keys | Short-lived credentials per workflow run |

## One-time setup

1. **Billing alarm first.** AWS Billing → Budgets → create a $5 monthly budget with email alerts.
2. **State bucket.** Create an S3 bucket (versioning on, public access blocked) for the Terraform state.
3. **OIDC for GitHub.** IAM → Identity providers → add `token.actions.githubusercontent.com` (audience `sts.amazonaws.com`). Create a role trusted only by this repo:

   ```json
   "Condition": {
     "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
     "StringLike": { "token.actions.githubusercontent.com:sub": "repo:hulaneoTi/devsecops-30-days:*" }
   }
   ```

   Give it only the permissions this code needs (EC2, VPC, IAM role/instance profile, SSM parameter read, the state bucket).
4. **GitHub secrets** (Settings → Secrets and variables → Actions): `AWS_ROLE_ARN`, `TF_STATE_BUCKET`, `ALLOWED_CIDR` (your IP with `/32`).
5. **Approval gate.** Settings → Environments → create `aws-sandbox` with yourself as required reviewer.
6. **Public image.** After the first pipeline run on `main`, set the GHCR package `devsecops-30-days` to public so the instance can pull it.

## Use

Actions → *Terraform deploy (AWS sandbox)* → Run workflow → `plan`, `apply` or `destroy`.

Always finish a session with `destroy`.

## Run locally

```bash
cp backend.hcl.example backend.hcl            # fill in
cp terraform.tfvars.example terraform.tfvars  # fill in
terraform init -backend-config=backend.hcl
terraform plan
```
