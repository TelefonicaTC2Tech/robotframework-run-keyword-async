current_dir = $(shell pwd)

.PHONY: help
help:	## Show a list of available commands
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: test
test:	
	docker run -v $(current_dir)/test:/root/test -t robot-async


.PHONY: build
build:	## Run unitary test and coverage badge
	docker build . -t robot-async
