build: Dockerfile
	@touch $@
	docker build -t sflomenb/shell .
