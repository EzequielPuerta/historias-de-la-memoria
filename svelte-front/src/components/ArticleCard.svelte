<script lang="ts">
    import {push} from "svelte-spa-router"

    export let title: string;
    export let slug: string;
    export let is_new: boolean = false;
    export let date: Date;
    export let abstract: string;
    export let tags: string[] = [];
    export let photo: string;
    export let alt_photo: string = "";
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
                class="w-full h-auto"
            />
            <div class="absolute top-2 right-2 bg-black bg-opacity-90 text-white text-xs px-2 py-1 rounded">
                {date.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' })}
            </div>
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
