PANTS:=pants
APP_NAME:=microservices
APP_IMAGE:=microservices
CLIENT_APP_NAME:=microservice_client
CLIENT_APP_IMAGE:=microservice-client

SHELL=/bin/bash

.PHONY: all
all:
	$(PANTS) check ::
	$(PANTS) lint ::
	$(PANTS) fmt ::

.PHONY: tailor
tailor:
	$(PANTS) tailor ::

.PHONY: tailor-check
tailor-check:
	$(PANTS) tailor --check ::

.PHONY: fmt
fmt:
	$(PANTS) fmt ::

.PHONY: check
check:
	$(PANTS) check ::

.PHONY: lint
lint:
	$(PANTS) lint ::

.PHONY: generate-lockfiles
generate-lockfiles:
	$(PANTS) generate-lockfiles

.PHONY: generate-lockfiles-mypy
generate-lockfiles-mypy:
	$(PANTS) generate-lockfiles --resolve=mypy

# .PHONY: generate-lockfiles-bandit
# generate-lockfiles-bandit:
# 	$(PANTS) generate-lockfiles --resolve=bandit

# .PHONY: generate-lockfiles-black
# generate-lockfiles-black:
# 	$(PANTS) generate-lockfiles --resolve=black

# .PHONY: generate-lockfiles-docformatter
# generate-lockfiles-docformatter:
# 	$(PANTS) generate-lockfiles --resolve=docformatter

# .PHONY: generate-lockfiles-flake8
# generate-lockfiles-flake8:
# 	$(PANTS) generate-lockfiles --resolve=flake8

# .PHONY: generate-lockfiles-isort
# generate-lockfiles-isort:
# 	$(PANTS) generate-lockfiles --resolve=isort

# .PHONY: generate-lockfiles-pylint
# generate-lockfiles-pylint:
# 	$(PANTS) generate-lockfiles --resolve=pylint

# .PHONY: generate-lockfiles-pytest
# generate-lockfiles-pytest:
# 	$(PANTS) generate-lockfiles --resolve=pytest

# .PHONY: generate-lockfiles-coverage
# generate-lockfiles-coverage:
# 	$(PANTS) generate-lockfiles --resolve=coverage

# .PHONY: generate-lockfiles-grpc
# generate-lockfiles-grpc:
# 	$(PANTS) generate-lockfiles --resolve=grpc

# .PHONY: generate-lockfiles-protobuf
# generate-lockfiles-protobuf:
# 	$(PANTS) generate-lockfiles --resolve=protobuf

run-grpc-server:
	$(PANTS) run src/python/grpc-server:grpc-server

package-grpc-server:
	$(PANTS) package src/python/grpc-server:

.PHONY: test
test-grpc-server:
	$(PANTS) test src/python/grpc-server:


.PHONY: export-codegen
export-codegen:
	$(PANTS) export-codegen :: 

.PHONY: test
test:
	$(PANTS) test ::

.PHONY: fix
fix:
	$(PANTS) fix ::

.PHONY: package
package:
	$(PANTS) package ::

.PHONY: update-build-files
update-build-files:
	$(PANTS) update-build-files ::
