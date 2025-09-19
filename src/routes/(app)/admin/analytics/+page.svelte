<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import Analytics from '$lib/components/admin/Analytics.svelte';

	onMount(() => {
		goto('/admin/analytics/overview');
	});
</script>

<Analytics />
