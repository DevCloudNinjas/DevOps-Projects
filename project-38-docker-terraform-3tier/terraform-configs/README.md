# Three-Tier Terraform Configs

This folder is a compact AWS three-tier example: public web instances behind an ALB, private application/database subnets, and an RDS subnet group placeholder.

## Inputs

The defaults are intentionally demo-sized. Override these before applying in a real account:

```bash
terraform plan \
  -var='admin_cidr_blocks=["203.0.113.10/32"]' \
  -var='web_ingress_cidr_blocks=["0.0.0.0/0"]'
```

- `aws_region`: target AWS region, default `us-east-1`.
- `admin_cidr_blocks`: CIDRs allowed to SSH to the web instances. The default `203.0.113.0/24` is a documentation range and should be replaced.
- `web_ingress_cidr_blocks`: CIDRs allowed to reach HTTP/HTTPS on the public tier.

## Local Checks

Run these without cloud credentials to catch syntax drift:

```bash
terraform fmt -check
terraform validate
```
