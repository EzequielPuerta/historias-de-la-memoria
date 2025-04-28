runserver:
	python3 manage.py runserver

build:
	cd svelte-front && npm run build
	python manage.py collectstatic --noinput
	$(MAKE) runserver

tailwind-init:
	cd svelte-front && pnpm run tailwind:init
