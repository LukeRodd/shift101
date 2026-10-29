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
sam deploy --guided --stack-name shift101-demo --capabilities CAPABILITY_IAM --parameter-overrides EnableBedrock=false
```

Use the outputs `BucketName`, `DistributionId`, and `SiteUrl` from CloudFormation:

```bash
aws s3 sync frontend/ s3://YOUR_BUCKET_NAME/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

The browser requests `/api/*` through CloudFront. Lambda returns the API responses. The website bucket is private and accessible only through CloudFront. Use **Amazon US East (N. Virginia)** initially if both model IDs are available in your AWS account; verify model availability and permissions before enabling.

## AI configuration
Bedrock provider is selected using `SHIFT101_AI_PROVIDER=bedrock`. `EnableBedrock=false` keeps the model endpoint off. Do not set it to true for a public demo until authentication, per-user budgets/quotas, abuse detection and monitoring have been implemented. Lambda reserved concurrency is not a spend ceiling. The first demo can use lexical runbook search without Bedrock.

## Costs and security
- Set an AWS Budget with alerts *before* deploying. Budgets notify and do not automatically stop charges.
- Limit the IAM role and monitor CloudWatch logs (log retention should be configured before public launch).
- CloudFront, S3, Lambda, API Gateway, data transfer, logs and Bedrock may be billed independently.
- All current incidents and runbooks are synthetic; do not upload confidential documentation.
- The application currently has no authentication or persistent progress; it is not production ready.
