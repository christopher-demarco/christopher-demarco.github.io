CONTAINER_NAME ?= cmd-pages-preview

.PHONY: run clean

run:
	bundle install && bundle exec jekyll serve

clean:
	rm -rf vendor _site .jekyll-cache
