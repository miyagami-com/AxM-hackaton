<script>
	import { getContext, tick, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { user } from '$lib/stores';
	import { page } from '$app/stores';

	import DashboardOverview from './Analytics/DashboardOverview.svelte';
	import EmployeeMonitor from './Analytics/EmployeeMonitor.svelte';
	import ChatAnalytics from './Analytics/ChatAnalytics.svelte';
	import KnowledgeBase from './Analytics/KnowledgeBase.svelte';
	import ActivityFeed from './Analytics/ActivityFeed.svelte';

	const i18n = getContext('i18n');

	let selectedTab;
	$: {
		const pathParts = $page.url.pathname.split('/');
		const tabFromPath = pathParts[pathParts.length - 1];
		selectedTab = [
			'overview',
			'employee-monitor',
			'chat-analytics',
			'knowledge-base',
			'activity-feed'
		].includes(tabFromPath)
			? tabFromPath
			: 'overview';
	}

	$: if (selectedTab) {
		// scroll to selectedTab
		scrollToTab(selectedTab);
	}

	const scrollToTab = (tabId) => {
		const tabElement = document.getElementById(tabId);
		if (tabElement) {
			tabElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
		}
	};

	let loaded = false;

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
		}

		loaded = true;

		const containerElement = document.getElementById('analytics-tabs-container');

		if (containerElement) {
			containerElement.addEventListener('wheel', function (event) {
				if (event.deltaY !== 0) {
					// Adjust horizontal scroll position based on vertical scroll
					containerElement.scrollLeft += event.deltaY;
				}
			});
		}

		// Scroll to the selected tab on mount
		scrollToTab(selectedTab);
	});
</script>

<div class="flex flex-col lg:flex-row w-full h-full pb-2 lg:space-x-4">
	<div
		id="analytics-tabs-container"
		class="mx-[16px] lg:mx-0 lg:px-[16px] flex flex-row overflow-x-auto gap-2.5 max-w-full lg:gap-1 lg:flex-col lg:flex-none lg:w-50 dark:text-gray-200 text-sm font-medium text-left scrollbar-none"
	>
		<button
			id="overview"
			class="px-0.5 py-1 min-w-fit rounded-lg lg:flex-none flex text-right transition {selectedTab ===
			'overview'
				? ''
				: ' text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
			on:click={() => {
				goto('/admin/analytics/overview');
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M8.5 4.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0ZM10.9 12.006c.11.542-.348.994-.9.994H2c-.553 0-1.01-.452-.902-.994a5.002 5.002 0 0 1 9.803 0ZM14.002 12h-1.59a2.556 2.556 0 0 0-.04-.29 6.476 6.476 0 0 0-1.167-2.603 3.002 3.002 0 0 1 3.633 1.911c.18.522-.283.982-.836.982ZM12 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Overview')}</div>
		</button>

		<button
			id="employee-monitor"
			class="px-0.5 py-1 min-w-fit rounded-lg lg:flex-none flex text-right transition {selectedTab ===
			'employee-monitor'
				? ''
				: ' text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
			on:click={() => {
				goto('/admin/analytics/employee-monitor');
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M8 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM3.156 11.763c.16-.629.44-1.21.813-1.72a2.5 2.5 0 0 0-2.725 1.377c-.136.287.102.58.418.58h1.449c.01-.077.025-.156.045-.237ZM12.847 11.763c.02.08.036.16.046.237h1.446c.316 0 .554-.293.417-.579a2.5 2.5 0 0 0-2.722-1.378c.374.51.653 1.09.813 1.72ZM14 7.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0ZM3.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM5 13c-.552 0-1.013-.455-.876-.99a4.002 4.002 0 0 1 7.753 0c.136.535-.324.99-.877.99H5Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Employee Monitor')}</div>
		</button>

		<button
			id="chat-analytics"
			class="px-0.5 py-1 min-w-fit rounded-lg lg:flex-none flex text-right transition {selectedTab ===
			'chat-analytics'
				? ''
				: ' text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
			on:click={() => {
				goto('/admin/analytics/chat-analytics');
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8Zm7.5-3.5a.5.5 0 0 0-1 0v2.793L6.354 5.646a.5.5 0 1 0-.708.708l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5a.5.5 0 0 0-.708-.708L8.5 7.293V4.5Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Chat Analytics')}</div>
		</button>

		<button
			id="knowledge-base"
			class="px-0.5 py-1 min-w-fit rounded-lg lg:flex-none flex text-right transition {selectedTab ===
			'knowledge-base'
				? ''
				: ' text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
			on:click={() => {
				goto('/admin/analytics/knowledge-base');
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M1 2.828c.885-.37 2.154-.769 3.767-.893 1.44-.262 2.87-.262 4.466 0 1.597.262 3.026.262 4.466 0 1.613.124 2.882.523 3.767.893 1.234.324 1.872.755 2.051 1.397.16.562-.158 1.158-.753 1.158l-10.5 0c-.595 0-.913-.596-.753-1.158.179-.642.817-1.073 2.051-1.397Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Knowledge Base')}</div>
		</button>

		<button
			id="activity-feed"
			class="px-0.5 py-1 min-w-fit rounded-lg lg:flex-none flex text-right transition {selectedTab ===
			'activity-feed'
				? ''
				: ' text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'}"
			on:click={() => {
				goto('/admin/analytics/activity-feed');
			}}
		>
			<div class=" self-center mr-2">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 16 16"
					fill="currentColor"
					class="size-4"
				>
					<path
						d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1Z"
					/>
				</svg>
			</div>
			<div class=" self-center">{$i18n.t('Activity Feed')}</div>
		</button>
	</div>

	<div class="flex-1 mt-1 lg:mt-0 px-[16px] lg:pr-[16px] lg:pl-0 overflow-y-scroll">
		{#if selectedTab === 'overview'}
			<DashboardOverview />
		{:else if selectedTab === 'employee-monitor'}
			<EmployeeMonitor />
		{:else if selectedTab === 'chat-analytics'}
			<ChatAnalytics />
		{:else if selectedTab === 'knowledge-base'}
			<KnowledgeBase />
		{:else if selectedTab === 'activity-feed'}
			<ActivityFeed />
		{/if}
	</div>
</div>
