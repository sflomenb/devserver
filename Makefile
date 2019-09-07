build: Dockerfile
	@touch $@
	docker build -t sflomenb/ubuntu .
