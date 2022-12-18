dev/server:
	flask --app server --debug run

prod/server:
	flask --app server

test:
	pytest tests/ -v

shell:
	flask --app server shell

migration/create:
	flask --app server db migrate
migration/upgrade:
	flask --app server db upgrade