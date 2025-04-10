build:
	cd svelte-front && npm run build
	python manage.py collectstatic --noinput
	python3 manage.py runserver