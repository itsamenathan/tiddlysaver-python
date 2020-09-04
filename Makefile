NAME = itsamenathan/tiddlysaver-python
VERSION = 1.0.2

.PHONY: all build test tag_latest release ssh

all: build

build:
	docker build -t $(NAME):$(VERSION) --rm --no-cache=true --pull=true .

test:
	docker run --rm -p 8000:800 $(NAME):$(VERSION)

release:
	@if ! grep -q '## \[$(VERSION)\]' CHANGELOG.md; then echo 'Please note the release date in Changelog.md.' && false; fi
	@echo "*** Don't forget to create a tag. git tag v$(VERSION) && git push origin v$(VERSION)"

