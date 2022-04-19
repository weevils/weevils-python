test:
	pytest


test-with-local-api:
	WEEVILS_CLIENT_TEST_API=http://localhost:8000/ pytest
