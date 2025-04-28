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

    <footer class="footer flex flex-col sm:flex-row justify-between items-center bg-neutral text-neutral-content p-4">
        <aside class="flex items-center gap-2">
            <img src="/static/favicon.png" alt="Logo" class="w-8 h-8">
            <p>Historias de la Memoria - 2025</p>
        </aside>
        <nav class="mt-2 sm:mt-0">
            <a
                href="https://twitter.com/HDeLaMemoria"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Twitter icon"
                class="hover:text-blue-400"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    class="fill-current">
                    <path
                        d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z">
                    </path>
                </svg>
            </a>
        </nav>
    </footer>
</main>
