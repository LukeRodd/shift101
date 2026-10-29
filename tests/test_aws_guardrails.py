"""Static guardrail checks for the pre-authentication AWS demo.

These checks are intentionally strict: enabling Bedrock requires an explicit
code review at Checkpoint 05, not just a deployment parameter.
"""
from pathlib import Path

TEMPLATE = (Path(__file__).resolve().parents[1] / "deploy/aws/template.yaml").read_text(encoding="utf-8")


def test_bedrock_is_fail_closed():
    assert "SHIFT101_AI_ENABLED: 'false'" in TEMPLATE
    assert "bedrock:InvokeModel" not in TEMPLATE
    assert "EnableBedrock:" not in TEMPLATE


def test_budget_and_abuse_guardrails_declared():
    assert "ThrottlingRateLimit: 2" in TEMPLATE
    assert "ThrottlingBurstLimit: 5" in TEMPLATE
    assert "ReservedConcurrentExecutions: 2" in TEMPLATE
    assert "RetentionInDays: 7" in TEMPLATE


def test_private_s3_and_secure_cloudfront():
    assert "BlockPublicAcls: true" in TEMPLATE
    assert "BlockPublicPolicy: true" in TEMPLATE
    assert "SigningBehavior: always" in TEMPLATE
    assert "SSEAlgorithm: AES256" in TEMPLATE
    assert "ResponseHeadersPolicyId: 67f7725c-6f97-4210-82d7-5512b31e9d03" in TEMPLATE
    assert "OriginRequestPolicyId: b689b0a8-53d0-40ab-baf2-68738e2966ac" in TEMPLATE
