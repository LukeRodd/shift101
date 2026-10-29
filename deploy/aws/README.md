# AWS deployment — experimental

Architecture: private S3 bucket + CloudFront for the static frontend; API Gateway HTTP API + AWS Lambda (Python/FastAPI via Mangum); optional Bedrock Nova Micro and Titan Text Embeddings V2. No NAT Gateway, RDS, EC2, or vector database.

**Not deployed.** AWS credentials and a billing account are required. The stack creates billable resources. Start with Bedrock **disabled**. The HTTP API endpoint is separately accessible and unauthenticated; don't enable AI for anonymous traffic.

## Prerequisites
- AWS CLI v2 configured with an authorized deployment role
- AWS SAM CLI
- Python 3.12
- Access to Nova Micro and Titan Embeddings V2 in the chosen AWS region

## Deploy (review charges first)
```bash
sam validate -t deploy/aws/template.yaml
sam build -t deploy/aws/template.yaml
sam deploy --guided --stack-name shift101-demo --capabilities CAPABILITY_IAM
```

Use the outputs `BucketName`, `DistributionId`, and `SiteUrl` from CloudFormation:

```bash
aws s3 sync frontend/ s3://YOUR_BUCKET_NAME/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

The browser requests `/api/*` through CloudFront. Lambda returns the API responses. The website bucket is private and accessible only through CloudFront. Use **Amazon US East (N. Virginia)** initially if both model IDs are available in your AWS account; verify model availability and permissions before enabling.

## AI configuration
Bedrock provider code is present for future work, but **the infrastructure forcibly sets `SHIFT101_AI_ENABLED=false` and does not grant `bedrock:InvokeModel`**. This is a deliberate fail-closed safeguard until checkpoint 05 adds authentication, quotas, abuse detection and spend controls. It cannot be enabled by a deployment parameter. Lambda reserved concurrency and HTTP API throttling are not spending ceilings. The initial demo uses lexical runbook search.

## Costs and security
- At Checkpoint 02, configure an AWS Budget (for example, USD 5/month with 50%, 80%, and 100% notifications) *before* deploying, and review the amount with the account owner. **Budget alerts are not hard spending limits.**
- A public HTTP API is still directly accessible through `execute-api` and CloudFront. Request throttling (2 req/s, burst 5), Lambda concurrency 2 and log retention 7 days lower operational risk but do not prevent sustained billed usage.
- The private S3 bucket uses SSE-S3 encryption, an Origin Access Control and blocks public access. CloudFront adds managed security response headers.
- Limit the IAM role and monitor CloudWatch logs (log retention should be configured before public launch).
- CloudFront, S3, Lambda, API Gateway, data transfer, logs and Bedrock may be billed independently.
- All current incidents and runbooks are synthetic; do not upload confidential documentation.
- The application currently has no authentication or persistent progress; it is not production ready.
