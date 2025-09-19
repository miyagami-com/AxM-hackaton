<script>
	import { onMount } from 'svelte';

	let selectedFilter = 'all';
	let searchTerm = '';

	const activities = [
		{
			id: 1,
			type: 'query',
			user: 'Sarah Chen',
			action: 'Asked about titanium white ratios',
			details: 'Query about optimal titanium white ratios for semi-gloss paint formulation',
			timestamp: '2 min ago',
			status: 'completed',
			priority: 'normal',
			department: 'Production',
			tags: ['paint', 'formulation', 'titanium-white']
		},
		{
			id: 2,
			type: 'training',
			user: 'Mike Rodriguez',
			action: 'Completed color matching training',
			details: 'Successfully completed advanced color matching certification course',
			timestamp: '15 min ago',
			status: 'completed',
			priority: 'high',
			department: 'Quality Control',
			tags: ['training', 'certification', 'color-matching']
		},
		{
			id: 3,
			type: 'alert',
			user: 'Emma Thompson',
			action: 'Flagged quality issue in batch #4521',
			details: 'Detected viscosity inconsistency in batch #4521, requires immediate attention',
			timestamp: '32 min ago',
			status: 'pending',
			priority: 'urgent',
			department: 'Quality Control',
			tags: ['quality', 'alert', 'viscosity', 'batch-4521']
		},
		{
			id: 4,
			type: 'knowledge',
			user: 'David Kim',
			action: 'Accessed former employee knowledge base',
			details: 'Retrieved archived knowledge from former senior technician John Smith',
			timestamp: '1 hr ago',
			status: 'completed',
			priority: 'normal',
			department: 'Production',
			tags: ['knowledge', 'archive', 'former-employee']
		},
		{
			id: 5,
			type: 'system',
			user: 'AI System',
			action: 'Automated quality check completed',
			details: 'Automated quality control scan completed for 15 batches, all passed',
			timestamp: '1 hr ago',
			status: 'completed',
			priority: 'normal',
			department: 'System',
			tags: ['automation', 'quality-check', 'batch-scan']
		},
		{
			id: 6,
			type: 'maintenance',
			user: 'Maintenance Team',
			action: 'Scheduled equipment maintenance',
			details: 'Scheduled maintenance for Mixer #3 due to unusual noise reported',
			timestamp: '2 hrs ago',
			status: 'scheduled',
			priority: 'high',
			department: 'Maintenance',
			tags: ['maintenance', 'mixer-3', 'scheduled']
		},
		{
			id: 7,
			type: 'query',
			user: 'Lisa Wang',
			action: 'Asked about safety protocols',
			details: 'Inquiry about proper PPE requirements for chemical handling',
			timestamp: '3 hrs ago',
			status: 'completed',
			priority: 'normal',
			department: 'Safety',
			tags: ['safety', 'PPE', 'chemical-handling']
		},
		{
			id: 8,
			type: 'alert',
			user: 'System',
			action: 'Temperature threshold exceeded',
			details: 'Paint mixing temperature exceeded safe operating range in Tank #2',
			timestamp: '4 hrs ago',
			status: 'resolved',
			priority: 'urgent',
			department: 'System',
			tags: ['temperature', 'alert', 'tank-2', 'safety']
		},
		{
			id: 9,
			type: 'training',
			user: 'Alex Johnson',
			action: 'Started safety certification',
			details: 'Began mandatory safety certification course for new employees',
			timestamp: '5 hrs ago',
			status: 'in-progress',
			priority: 'high',
			department: 'Safety',
			tags: ['training', 'safety', 'certification', 'new-employee']
		},
		{
			id: 10,
			type: 'knowledge',
			user: 'Sarah Chen',
			action: 'Updated paint formula database',
			details: 'Added new titanium white formulation to the knowledge base',
			timestamp: '6 hrs ago',
			status: 'completed',
			priority: 'normal',
			department: 'R&D',
			tags: ['knowledge', 'formula', 'titanium-white', 'database']
		}
	];

	const filterOptions = [
		{ name: 'All Activities', value: 'all', count: activities.length },
		{ name: 'Queries', value: 'query', count: activities.filter((a) => a.type === 'query').length },
		{
			name: 'Training',
			value: 'training',
			count: activities.filter((a) => a.type === 'training').length
		},
		{ name: 'Alerts', value: 'alert', count: activities.filter((a) => a.type === 'alert').length },
		{
			name: 'Knowledge',
			value: 'knowledge',
			count: activities.filter((a) => a.type === 'knowledge').length
		},
		{
			name: 'System',
			value: 'system',
			count: activities.filter((a) => a.type === 'system').length
		},
		{
			name: 'Maintenance',
			value: 'maintenance',
			count: activities.filter((a) => a.type === 'maintenance').length
		}
	];

	$: filteredActivities = activities.filter((activity) => {
		const matchesSearch =
			activity.user.toLowerCase().includes(searchTerm.toLowerCase()) ||
			activity.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
			activity.details.toLowerCase().includes(searchTerm.toLowerCase()) ||
			activity.tags.some((tag) => tag.toLowerCase().includes(searchTerm.toLowerCase()));
		const matchesFilter = selectedFilter === 'all' || activity.type === selectedFilter;
		return matchesSearch && matchesFilter;
	});

	function getActivityIcon(type) {
		switch (type) {
			case 'query':
				return 'M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z';
			case 'training':
				return 'M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z';
			case 'alert':
				return 'M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z';
			case 'knowledge':
				return 'M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1Z';
			case 'system':
				return 'M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646Z';
			case 'maintenance':
				return 'M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1Z';
			default:
				return 'M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z';
		}
	}

	function getActivityColor(type) {
		switch (type) {
			case 'query':
				return 'bg-blue-500/20 text-blue-400';
			case 'training':
				return 'bg-green-500/20 text-green-400';
			case 'alert':
				return 'bg-red-500/20 text-red-400';
			case 'knowledge':
				return 'bg-purple-500/20 text-purple-400';
			case 'system':
				return 'bg-gray-500/20 text-gray-400';
			case 'maintenance':
				return 'bg-orange-500/20 text-orange-400';
			default:
				return 'bg-gray-500/20 text-gray-400';
		}
	}

	function getStatusColor(status) {
		switch (status) {
			case 'completed':
				return 'bg-green-500/20 text-green-400 border-green-500/30';
			case 'pending':
				return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
			case 'in-progress':
				return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
			case 'scheduled':
				return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
			case 'resolved':
				return 'bg-green-500/20 text-green-400 border-green-500/30';
			default:
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
		}
	}

	function getPriorityColor(priority) {
		switch (priority) {
			case 'urgent':
				return 'bg-red-500/20 text-red-400 border-red-500/30';
			case 'high':
				return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
			case 'normal':
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
			default:
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
		}
	}

	function getDepartmentColor(department) {
		switch (department) {
			case 'Production':
				return 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400';
			case 'Quality Control':
				return 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400';
			case 'Safety':
				return 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400';
			case 'Maintenance':
				return 'bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400';
			case 'R&D':
				return 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400';
			case 'System':
				return 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400';
			default:
				return 'bg-gray-100 dark:bg-gray-900/30 text-gray-600 dark:text-gray-400';
		}
	}
</script>

<div class="p-6 space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-balance">Activity Feed</h1>
			<p class="text-muted-foreground text-pretty">
				Real-time monitoring of all system activities and user interactions
			</p>
		</div>
		<div class="flex items-center gap-2">
			<div
				class="px-3 py-1 rounded-full border border-green-400 text-green-400 text-sm flex items-center gap-1"
			>
				<div class="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
				Live Feed
			</div>
			<button
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
			>
				Export Log
			</button>
		</div>
	</div>

	<!-- Stats Overview -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Activities</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">{activities.length}</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Today</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Alerts</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">
				{activities.filter((a) => a.type === 'alert' && a.status === 'pending').length}
			</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Require attention</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Completed Tasks</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z" />
				</svg>
			</div>
			<div class="text-2xl font-bold">
				{activities.filter((a) => a.status === 'completed').length}
			</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">This session</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">System Health</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">98%</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Uptime</p>
		</div>
	</div>

	<!-- Filters and Search -->
	<div class="flex flex-col lg:flex-row gap-4">
		<div class="relative flex-1">
			<svg
				class="absolute left-2 top-2.5 h-4 w-4 text-gray-400"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
				/>
			</svg>
			<input
				type="text"
				placeholder="Search activities..."
				bind:value={searchTerm}
				class="w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
			/>
		</div>
		<select
			bind:value={selectedFilter}
			class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
		>
			{#each filterOptions as option}
				<option value={option.value}>{option.name} ({option.count})</option>
			{/each}
		</select>
	</div>

	<!-- Activity Feed -->
	<div class="space-y-4">
		{#each filteredActivities as activity}
			<div
				class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
			>
				<div class="flex items-start gap-4">
					<div class="p-3 rounded-full {getActivityColor(activity.type)}">
						<svg class="h-5 w-5" fill="currentColor" viewBox="0 0 16 16">
							<path d={getActivityIcon(activity.type)} />
						</svg>
					</div>

					<div class="flex-1 min-w-0">
						<div class="flex items-start justify-between mb-2">
							<div class="flex-1">
								<div class="flex items-center gap-2 mb-1">
									<h3 class="font-semibold text-lg">{activity.user}</h3>
									<span
										class="px-2 py-1 text-xs rounded-full {getDepartmentColor(activity.department)}"
									>
										{activity.department}
									</span>
								</div>
								<p class="text-gray-900 dark:text-white font-medium">{activity.action}</p>
								<p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{activity.details}</p>
							</div>
							<div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
								<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
									/>
								</svg>
								{activity.timestamp}
							</div>
						</div>

						<div class="flex items-center gap-2 mb-3">
							<span class="px-2 py-1 text-xs border rounded-full {getStatusColor(activity.status)}">
								{activity.status}
							</span>
							<span
								class="px-2 py-1 text-xs border rounded-full {getPriorityColor(activity.priority)}"
							>
								{activity.priority}
							</span>
						</div>

						<div class="flex flex-wrap gap-1">
							{#each activity.tags as tag}
								<span
									class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
								>
									#{tag}
								</span>
							{/each}
						</div>
					</div>

					<div class="flex flex-col gap-2">
						<button class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
							<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 16 16">
								<path
									d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
								/>
							</svg>
						</button>
						{#if activity.type === 'alert' && activity.status === 'pending'}
							<button
								class="px-3 py-1 text-xs bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
							>
								Resolve
							</button>
						{/if}
					</div>
				</div>
			</div>
		{/each}
	</div>

	{#if filteredActivities.length === 0}
		<div class="text-center py-12">
			<svg
				class="mx-auto h-12 w-12 text-gray-400"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
				/>
			</svg>
			<h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No activities found</h3>
			<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
				Try adjusting your search or filter criteria.
			</p>
		</div>
	{/if}
</div>
