NAME   := sflomenb/shell
TAG    := $$(git rev-parse HEAD)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build: Dockerfile
	@touch $@
	docker build -t ${IMG} .
	docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}
