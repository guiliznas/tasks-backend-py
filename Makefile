test:
	pytest tests/ -v

shell:
	flask --app server shell