run:
	@(\
			source venv/bin/activate; \
			scripts/main.sh; \
	)

test:
	@(\
			source venv/bin/activate; \
			scripts/test.sh; \
	)

