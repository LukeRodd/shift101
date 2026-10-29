"""Deployment preparation tests that do not need AWS credentials."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / "deploy/aws/deploy.sh").read_text()
WORKFLOW = (ROOT / ".github/workflows/deploy-aws.yml").read_text()
TEMPLATE = (ROOT / "deploy/aws/template.yaml").read_text()


def test_deploy_requires_explicit_cost_acknowledgment():
    assert "DEPLOY_ACKNOWLEDGE_CHARGES" in SCRIPT
    assert "acknowledge_charges" in WORKFLOW
    assert "workflow_dispatch" in WORKFLOW
    assert "push:" not in WORKFLOW


def test_deploy_validates_account_and_budget():
    assert "aws sts get-caller-identity" in SCRIPT
    assert "AWS_EXPECTED_ACCOUNT_ID" in SCRIPT
    assert "aws budgets describe-budget" in SCRIPT
    assert "aws budgets describe-notifications-for-budget" in SCRIPT


def test_deploy_uses_oidc_not_static_aws_keys():
    assert "id-token: write" in WORKFLOW
    assert "configure-aws-credentials" in WORKFLOW
    assert "role-to-assume:" in WORKFLOW
    assert "aws-access-key-id:" not in WORKFLOW
    assert "aws-secret-access-key:" not in WORKFLOW


def test_ai_disabled_until_guardrails_and_review():
    assert "SHIFT101_AI_ENABLED: 'false'" in TEMPLATE
    assert "bedrock:InvokeModel" not in TEMPLATE


def test_publish_has_smoke_tests():
    assert "/api/health" in SCRIPT
    assert "aws s3 sync frontend/" in SCRIPT
    assert "aws cloudfront create-invalidation" in SCRIPT
    assert "curl --fail" in SCRIPT
