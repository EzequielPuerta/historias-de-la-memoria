# Historias de la Memoria

## Link

https://historias-de-la-memoria.vercel.app

## Django: Running Locally

```bash
python manage.py runserver
```

Your Django application is now available at `http://localhost:8000`.

## Svelte: Running Locally

```bash
cd svelte-front
npm run dev
```

## Build

```bash
cd svelte-front
npm run build
cd ..
python manage.py collectstatic
```
