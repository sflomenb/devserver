NAME   := sflomenb/shell
TAG    := $$(git rev-parse HEAD)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build: Dockerfile
	@touch $@
	docker build -t ${IMG} .
	docker tag ${IMG} ${LATEST}

.PHONY: test
test:
	bundle exec rspec spec/devserver_spec.rb

.PHONY: push
push:
	@docker push ${NAME}

.PHONY: copy
copy:
	cp bootstrap.sh scripts/*.py /Users/sflomenb/Library/Mobile\ Documents/iCloud\~com\~omz-software\~Pythonista3/Documents/devserver/
