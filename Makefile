CONTAINER_NAME ?= cmd-pages-preview

.PHONY: preview stop clean

preview:
	docker run --name "$(CONTAINER_NAME)" --volume="$$PWD:/srv/jekyll" -p 4000:4000 jekyll/jekyll sh -c 'bundle config set --local path "vendor/bundle" >/dev/null && bundle install && bundle exec jekyll serve --host 0.0.0.0 --watch --drafts --force_polling'

stop:
	docker kill "$(CONTAINER_NAME)" && docker rm "$(CONTAINER_NAME)"

clean:
	rm -rf vendor _site .jekyll-cache Gemfile.lock
