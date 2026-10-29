#!/usr/bin/env bash
# Shift101 AWS demo deployment. Run only after checkpoint approval and AWS configuration.
set -Eeuo pipefail

: "${AWS_REGION:?Define AWS_REGION (e.g. us-east-1)}"
: "${AWS_EXPECTED_ACCOUNT_ID:?Define AWS_EXPECTED_ACCOUNT_ID (12 digits)}"
: "${AWS_BUDGET_NAME:?Define AWS_BUDGET_NAME (existing budget with notifications)}"

if [[ "${DEPLOY_ACKNOWLEDGE_CHARGES:-}" != "YES" ]]; then
  echo "Deployment blocked: set DEPLOY_ACKNOWLEDGE_CHARGES=YES after reviewing costs." >&2
  exit 1
fi
if [[ ! "${AWS_EXPECTED_ACCOUNT_ID}" =~ ^[0-9]{12}$ ]]; then
  echo "Invalid AWS account ID." >&2
  exit 1
fi

account="$(aws sts get-caller-identity --query Account --output text)"
if [[ "$account" != "$AWS_EXPECTED_ACCOUNT_ID" ]]; then
  echo "AWS account mismatch. Deployment refused." >&2
  exit 1
fi

echo "Checking account budget and alert notifications..."
budget_type="$(aws budgets describe-budget --account-id "$account" --budget-name "$AWS_BUDGET_NAME" --query 'Budget.BudgetType' --output text)"
budget_unit="$(aws budgets describe-budget --account-id "$account" --budget-name "$AWS_BUDGET_NAME" --query 'Budget.BudgetLimit.Unit' --output text)"
budget_period="$(aws budgets describe-budget --account-id "$account" --budget-name "$AWS_BUDGET_NAME" --query 'Budget.TimeUnit' --output text)"
budget_amount="$(aws budgets describe-budget --account-id "$account" --budget-name "$AWS_BUDGET_NAME" --query 'Budget.BudgetLimit.Amount' --output text)"
notifications="$(aws budgets describe-notifications-for-budget --account-id "$account" --budget-name "$AWS_BUDGET_NAME" --query 'length(Notifications)' --output text)"
if [[ "$budget_type" != "COST" || "$budget_unit" != "USD" || "$budget_period" != "MONTHLY" || ! "$notifications" =~ ^[1-9][0-9]*$ ]]; then
  echo "Require a monthly USD cost budget with at least one alert notification." >&2
  exit 1
fi
python - "$budget_amount" <<'PY'
from decimal import Decimal, InvalidOperation
import sys
try:
    amount = Decimal(sys.argv[1])
except InvalidOperation:
    raise SystemExit("Invalid budget amount")
if not Decimal("0") < amount <= Decimal("10"):
    raise SystemExit("Budget threshold must be > 0 and <= USD 10/month")
PY
echo "Budget verified (notification budget, NOT a hard cost cap)."

stack="shift101-demo"
sam validate --lint --template-file deploy/aws/template.yaml
sam build --template-file deploy/aws/template.yaml
sam deploy \
  --stack-name "$stack" \
  --region "$AWS_REGION" \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset

output() {
  aws cloudformation describe-stacks \
    --stack-name "$stack" \
    --region "$AWS_REGION" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue | [0]" \
    --output text
}
bucket="$(output BucketName)"
distribution="$(output DistributionId)"
site_url="$(output SiteUrl)"
api_url="$(output ApiUrl)"

for item in "$bucket" "$distribution" "$site_url" "$api_url"; do
  if [[ -z "$item" || "$item" == "None" ]]; then
    echo "Missing expected CloudFormation output." >&2
    exit 1
  fi
done

echo "Uploading static frontend to private S3 bucket..."
aws s3 sync frontend/ "s3://$bucket/" --delete --region "$AWS_REGION"
aws cloudfront create-invalidation --distribution-id "$distribution" --paths '/*' > /dev/null

echo "Checking the API health route..."
curl --fail --show-error --silent --retry 6 --retry-delay 5 "$api_url/api/health" | python -c 'import json,sys; assert json.load(sys.stdin)["status"] == "ok"'
echo "Checking the CloudFront homepage (propagation can take time)..."
curl --fail --show-error --silent --location --retry 12 --retry-delay 10 --retry-all-errors "$site_url/" | grep -q 'Shift101'
echo "AWS demo deployed: $site_url"
echo "Bedrock remains disabled; no production users or real incidents are configured."
