<script>
    import { onMount } from 'svelte';
    import { push } from 'svelte-spa-router';
    import { articles } from '../articles/index.js';

    let ArticleComponent = null;
    let articleMetadata = null;
    export let params = {};

    async function loadArticle(slug) {
        ArticleComponent = null;
        try {
            const module = await import(`../articles/${slug}.svelte`);
            ArticleComponent = module.default;
            articleMetadata = articles.find(a => a.slug === slug);
        } catch (error) {
            push('/404');
        }
    }

    onMount(() => {
        if (params.slug) {
            loadArticle(params.slug);
        }
    });
</script>

{#if ArticleComponent}
    <h1>{articleMetadata.abstract}</h1>
    <div class="divider textarea-xl pt-10">{articleMetadata.date.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
    <div class="pt-10 pb-16 sm:py-16">
        <img
            src={articleMetadata.photo}
            alt={articleMetadata.alt_photo}
            class="w-full h-auto"
        />
    </div>
    <div class="divider whitespace-normal break-words text-center pb-16">{articleMetadata.caption}</div>
    <svelte:component this={ArticleComponent} />
{:else}
    <div class="flex justify-center p-8">
        <span class="loading loading-spinner loading-lg"></span>
    </div>
{/if}
