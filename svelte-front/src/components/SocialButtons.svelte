<script>
	import { Email, Reddit, LinkedIn, Telegram, WhatsApp, Facebook, X } from 'svelte-share-buttons-component';

	const url = 'https://historias-de-la-memoria.vercel.app';
	const title = 'Historias de la Memoria';
	const desc = 'Porque las víctimas del Terrorismo de Estado no son solamente un número, son caras, nombres, hijos, padres, amores, amistades, historias que nos recuerdan lo importante de mantener viva la Memoria.';
</script>

<div>
    <Email subject="{title}" body="{desc} {url}" />
    <Reddit class="share-button" {title} {url} />
    <LinkedIn class="share-button" {url} />
    <Telegram class="share-button" text={title} {url} />
    <WhatsApp class="share-button" text="{title} {url}" />
    <Facebook class="share-button" quote="{title}" {url} />
    <X class="share-button" text="{title}" {url} hashtags="HDeLaMemoria,NuncaMás,TerrorismoDeEstado" via="username" related="other,users" />
</div>
