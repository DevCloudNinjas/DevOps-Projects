package l2cloudpilot

default allow = false
allow { input.region == input.approved_region; input.ttl_minutes <= 120; input.public == false; input.persistent == false; required_tags(input.tags) }
required_tags(tags) { tags.owner != ""; tags.request_id != ""; tags.expires_at != ""; tags.managed_by == "l2-cloud-pilot" }
deny[msg] { input.resource_type == "iam:*"; msg := "wildcard IAM/resource type denied" }
deny[msg] { input.public == true; msg := "public exposure denied" }
deny[msg] { input.persistent == true; msg := "persistent storage denied" }
allowed_resource_type { input.resource_type == "one-disposable-fixture-resource" }
deny[msg] { not allowed_resource_type; msg := "resource type outside disposable allow-list denied" }
deny[msg] { input.shared_dependency == true; msg := "shared dependency denied" }
deny[msg] { input.production_dependency == true; msg := "production dependency denied" }
deny[msg] { input.tags.expires_at == ""; msg := "expiry tag required" }
