.PHONY: validate push-sample

PAYLOAD ?= payloads/sample-webhook.json

validate:
	python3 -m json.tool payloads/sample-webhook.json >/dev/null
	python3 -m json.tool payloads/schema.json >/dev/null
	test -s templates/full.liquid

push-sample:
	./scripts/push-webhook.sh $(PAYLOAD)
