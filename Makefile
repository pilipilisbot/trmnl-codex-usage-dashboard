.PHONY: validate push-sample

PAYLOAD ?= payloads/sample-webhook.json

validate:
	python3 -m json.tool payloads/schema.json >/dev/null
	python3 -m json.tool payloads/sample-webhook.json >/dev/null
	python3 -c 'import sys; sys.path.insert(0, "scripts"); from publish import read_json, validate_payload; validate_payload(read_json("payloads/sample-webhook.json"))'
	test -s templates/full.liquid
	test -s templates/form_fields.yml

push-sample:
	./scripts/push-webhook.sh $(PAYLOAD)
