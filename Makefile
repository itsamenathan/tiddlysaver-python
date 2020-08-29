NAME = itsamenathan/tiddlysaver-python
VERSION = 1.0.0

.PHONY: all build test tag_latest release ssh

all: build

build:
	docker build -t $(NAME):$(VERSION) --rm --no-cache=true --pull=true .

test:
	docker run --rm -p 8000:800 $(NAME):$(VERSION)

tag_latest:
	docker tag -f $(NAME):$(VERSION) $(NAME):latest

release: tag_latest
	@if ! docker images $(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	@if ! grep -q '## \[$(VERSION)\]' CHANGELOG.md; then echo 'Please note the release date in Changelog.md.' && false; fi
	#docker push $(NAME)
	#@echo "*** Don't forget to create a tag. git tag v$(VERSION) && git push origin v$(VERSION)"

