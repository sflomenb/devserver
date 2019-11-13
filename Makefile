NAME   := sflomenb/shell
TAG    := $$(git rev-parse HEAD)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build: Dockerfile
	@touch $@
	docker build -t ${IMG} .
	docker tag ${IMG} ${LATEST}

test:
	bundle exec rspec spec/devserver_spec.rb

push:
	@docker push ${NAME}
