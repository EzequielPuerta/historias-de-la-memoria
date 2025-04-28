<script lang="ts">
    import { inject } from '@vercel/analytics';
    import Router from "svelte-spa-router";
    import Home from './routes/Home.svelte';
    import Article from './routes/Article.svelte';
    import NotFound404 from './routes/NotFound404.svelte';

    let routes = {
        "/": Home,
        "/articulo/:slug": Article,
        "/404": NotFound404,
        "*": NotFound404,
    }

    inject();
</script>

<main>
    <div class="navbar bg-primary shadow-sm">
        <a href="/" class="btn btn-ghost text-xl">Historias de la Memoria</a>
    </div>

    <div class="max-w-screen-lg mx-auto p-8">
        <Router {routes}/>
    </div>
</main>
