<script>
    import { push } from 'svelte-spa-router';
    import { onMount } from 'svelte';

    let ArticleComponent = null;
    export let params = {};

    async function loadArticle(slug) {
        ArticleComponent = null;
        try {
            const module = await import(`../articles/${slug}.svelte`);
            ArticleComponent = module.default;
        } catch (err) {
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
    <svelte:component this={ArticleComponent} />
{:else}
    <div class="flex justify-center p-8">
        <span class="loading loading-spinner loading-lg"></span>
    </div>
{/if}
