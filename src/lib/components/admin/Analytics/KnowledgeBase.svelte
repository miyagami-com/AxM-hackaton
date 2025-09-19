<script>
	import { onMount } from 'svelte';

	let searchTerm = '';
	let selectedCategory = 'all';
	let selectedStatus = 'all';

	const knowledgeItems = [
		{
			id: 1,
			title: 'Titanium White Paint Formulation',
			category: 'Paint Formulas',
			status: 'active',
			lastUpdated: '2 days ago',
			contributor: 'Sarah Chen',
			views: 156,
			rating: 4.8,
			content:
				'Comprehensive guide to titanium white paint formulation including optimal ratios, mixing techniques, and quality control measures...',
			tags: ['paint', 'formulation', 'titanium', 'white', 'quality']
		},
		{
			id: 2,
			title: 'Color Matching Procedures',
			category: 'Color Matching',
			status: 'active',
			lastUpdated: '1 week ago',
			contributor: 'Mike Rodriguez',
			views: 234,
			rating: 4.9,
			content:
				'Step-by-step procedures for accurate color matching including equipment setup, sample preparation, and verification methods...',
			tags: ['color', 'matching', 'procedures', 'equipment', 'verification']
		},
		{
			id: 3,
			title: 'Quality Control Checklist',
			category: 'Quality Control',
			status: 'active',
			lastUpdated: '3 days ago',
			contributor: 'Emma Thompson',
			views: 189,
			rating: 4.7,
			content:
				'Comprehensive quality control checklist covering all stages of paint production from raw materials to finished products...',
			tags: ['quality', 'control', 'checklist', 'production', 'standards']
		},
		{
			id: 4,
			title: 'Equipment Maintenance Schedule',
			category: 'Equipment',
			status: 'pending',
			lastUpdated: '2 weeks ago',
			contributor: 'David Kim',
			views: 98,
			rating: 4.5,
			content:
				'Detailed maintenance schedule for all paint mixing and processing equipment including daily, weekly, and monthly tasks...',
			tags: ['equipment', 'maintenance', 'schedule', 'mixing', 'processing']
		},
		{
			id: 5,
			title: 'Safety Protocols for Chemical Handling',
			category: 'Safety',
			status: 'active',
			lastUpdated: '5 days ago',
			contributor: 'Sarah Chen',
			views: 312,
			rating: 4.9,
			content:
				'Essential safety protocols for handling various chemicals used in paint production including PPE requirements and emergency procedures...',
			tags: ['safety', 'chemicals', 'handling', 'PPE', 'emergency']
		},
		{
			id: 6,
			title: 'Former Employee Knowledge Archive',
			category: 'Archive',
			status: 'archived',
			lastUpdated: '1 month ago',
			contributor: 'System',
			views: 45,
			rating: 4.6,
			content:
				'Preserved knowledge from former employees including specialized techniques, troubleshooting guides, and historical production data...',
			tags: ['archive', 'former', 'employees', 'knowledge', 'preservation']
		}
	];

	const categories = [
		{ name: 'All', value: 'all', count: knowledgeItems.length },
		{
			name: 'Paint Formulas',
			value: 'Paint Formulas',
			count: knowledgeItems.filter((item) => item.category === 'Paint Formulas').length
		},
		{
			name: 'Color Matching',
			value: 'Color Matching',
			count: knowledgeItems.filter((item) => item.category === 'Color Matching').length
		},
		{
			name: 'Quality Control',
			value: 'Quality Control',
			count: knowledgeItems.filter((item) => item.category === 'Quality Control').length
		},
		{
			name: 'Equipment',
			value: 'Equipment',
			count: knowledgeItems.filter((item) => item.category === 'Equipment').length
		},
		{
			name: 'Safety',
			value: 'Safety',
			count: knowledgeItems.filter((item) => item.category === 'Safety').length
		},
		{
			name: 'Archive',
			value: 'Archive',
			count: knowledgeItems.filter((item) => item.category === 'Archive').length
		}
	];

	$: filteredItems = knowledgeItems.filter((item) => {
		const matchesSearch =
			item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
			item.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
			item.tags.some((tag) => tag.toLowerCase().includes(searchTerm.toLowerCase()));
		const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
		const matchesStatus = selectedStatus === 'all' || item.status === selectedStatus;
		return matchesSearch && matchesCategory && matchesStatus;
	});

	function getStatusColor(status) {
		switch (status) {
			case 'active':
				return 'bg-green-500/20 text-green-400 border-green-500/30';
			case 'pending':
				return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
			case 'archived':
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
			default:
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
		}
	}

	function getRatingStars(rating) {
		const stars = [];
		const fullStars = Math.floor(rating);
		const hasHalfStar = rating % 1 >= 0.5;

		for (let i = 0; i < fullStars; i++) {
			stars.push('full');
		}
		if (hasHalfStar) {
			stars.push('half');
		}
		while (stars.length < 5) {
			stars.push('empty');
		}
		return stars;
	}
</script>

<div class="p-6 space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-balance">Knowledge Base Management</h1>
			<p class="text-muted-foreground text-pretty">
				Manage and organize company knowledge, procedures, and best practices
			</p>
		</div>
		<div class="flex items-center gap-2">
			<button
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
			>
				Import Knowledge
			</button>
			<button
				class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
			>
				Add New Article
			</button>
		</div>
	</div>

	<!-- Stats Overview -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Articles</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M1 2.828c.885-.37 2.154-.769 3.767-.893 1.44-.262 2.87-.262 4.466 0 1.597.262 3.026.262 4.466 0 1.613.124 2.882.523 3.767.893 1.234.324 1.872.755 2.051 1.397.16.562-.158 1.158-.753 1.158l-10.5 0c-.595 0-.913-.596-.753-1.158.179-.642.817-1.073 2.051-1.397Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">{knowledgeItems.length}</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+3</span> this month
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Articles</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z" />
				</svg>
			</div>
			<div class="text-2xl font-bold">
				{knowledgeItems.filter((item) => item.status === 'active').length}
			</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Currently available</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Views</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">
				{knowledgeItems.reduce((sum, item) => sum + item.views, 0)}
			</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+12%</span> this week
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Rating</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">
				{(
					knowledgeItems.reduce((sum, item) => sum + item.rating, 0) / knowledgeItems.length
				).toFixed(1)}
			</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Out of 5.0</p>
		</div>
	</div>

	<!-- Search and Filters -->
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
				placeholder="Search knowledge base..."
				bind:value={searchTerm}
				class="w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
			/>
		</div>
		<select
			bind:value={selectedCategory}
			class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
		>
			{#each categories as category}
				<option value={category.value}>{category.name} ({category.count})</option>
			{/each}
		</select>
		<select
			bind:value={selectedStatus}
			class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
		>
			<option value="all">All Status</option>
			<option value="active">Active</option>
			<option value="pending">Pending</option>
			<option value="archived">Archived</option>
		</select>
	</div>

	<!-- Knowledge Items Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
		{#each filteredItems as item}
			<div
				class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
			>
				<div class="flex items-start justify-between mb-3">
					<div class="flex-1">
						<h3 class="text-lg font-semibold mb-1">{item.title}</h3>
						<div class="flex items-center gap-2 mb-2">
							<span
								class="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full"
							>
								{item.category}
							</span>
							<span class="px-2 py-1 text-xs border rounded-full {getStatusColor(item.status)}">
								{item.status}
							</span>
						</div>
					</div>
					<button class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
						<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 16 16">
							<path
								d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
							/>
						</svg>
					</button>
				</div>

				<p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">{item.content}</p>

				<div class="flex flex-wrap gap-1 mb-4">
					{#each item.tags as tag}
						<span
							class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded"
						>
							#{tag}
						</span>
					{/each}
				</div>

				<div
					class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4"
				>
					<div class="flex items-center gap-4">
						<span class="flex items-center gap-1">
							<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
								<path
									d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z"
								/>
							</svg>
							{item.views} views
						</span>
						<span class="flex items-center gap-1">
							<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
								<path
									d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
								/>
							</svg>
							{item.lastUpdated}
						</span>
					</div>
					<div class="flex items-center gap-1">
						{#each getRatingStars(item.rating) as star}
							{#if star === 'full'}
								<svg class="h-3 w-3 text-yellow-400" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
									/>
								</svg>
							{:else if star === 'half'}
								<svg class="h-3 w-3 text-yellow-400" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M5.354 5.119 7.538.792A.516.516 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.537.537 0 0 1 16 6.32a.548.548 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.52.52 0 0 1-.746-.592l.83-4.73L.173 6.765a.55.55 0 0 1-.172-.403.58.58 0 0 1 .085-.302.513.513 0 0 1 .37-.245l4.898-.696zM8 12.027a.5.5 0 0 1 .232.056l3.686 1.894-.694-3.957a.565.565 0 0 1 .162-1.163l2.974-.422-2.14-2.037a.56.56 0 0 1-.163-.505l.694-3.957-3.686 1.894a.503.503 0 0 1-.464 0L4.35 5.12l.694 3.957a.56.56 0 0 1-.163.505L2.816 11.4l2.974.422a.565.565 0 0 1 .162 1.163l-.694 3.957 3.686-1.894a.5.5 0 0 1 .232-.056z"
									/>
								</svg>
							{:else}
								<svg class="h-3 w-3 text-gray-300" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
									/>
								</svg>
							{/if}
						{/each}
						<span class="ml-1">{item.rating}</span>
					</div>
				</div>

				<div class="flex items-center justify-between">
					<div class="text-xs text-gray-500 dark:text-gray-400">
						By {item.contributor}
					</div>
					<div class="flex gap-2">
						<button
							class="px-3 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
						>
							Edit
						</button>
						<button
							class="px-3 py-1 text-xs bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
						>
							View
						</button>
					</div>
				</div>
			</div>
		{/each}
	</div>

	{#if filteredItems.length === 0}
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
					d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
				/>
			</svg>
			<h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">
				No knowledge articles found
			</h3>
			<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
				Try adjusting your search or filter criteria.
			</p>
		</div>
	{/if}
</div>
