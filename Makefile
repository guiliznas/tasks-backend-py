test:
	pytest tests/ -v

shell:
	flask --app server shell

migration/create:
	flask --app server db migrate
migration/upgrade:
	flask --app server db upgrade