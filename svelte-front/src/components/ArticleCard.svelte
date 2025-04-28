<script lang="ts">
    import {push} from "svelte-spa-router"

    export let title;
    export let slug;
    export let is_new = false;
    export let abstract;
    export let tags;
    export let photo;
    export let alt_photo = "";
</script>

<div class="card bg-primary w-70 shadow-lg">
    <button
        on:click={() => push(`#/articulo/${slug}`)}
        tabindex="0"
        class="w-full text-left"
    >
        <figure>
            <img
                src={photo}
                alt={alt_photo}
            />
        </figure>
        <div class="card-body h-60">
            <h2 class="card-title">
                {title}
                {#if is_new}
                    <div class="badge badge-secondary">Nuevo</div>
                {/if}
            </h2>
            <p>{abstract}</p>
            <div class="card-actions justify-end">
                {#each tags as tag}
                    <div class="badge badge-outline">{tag}</div>
                {/each}
            </div>
        </div>
    </button>
</div>
