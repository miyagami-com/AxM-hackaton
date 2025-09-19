<script>
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

	let selectedTimeRange = '24h';
	let selectedTopic = 'all';
	let searchTerm = '';
	let chatVolumeChart;
	let sentimentChart;

	const chatVolumeData = [
		{ time: '00:00', volume: 12, sentiment: 0.8 },
		{ time: '02:00', volume: 8, sentiment: 0.7 },
		{ time: '04:00', volume: 5, sentiment: 0.9 },
		{ time: '06:00', volume: 23, sentiment: 0.6 },
		{ time: '08:00', volume: 45, sentiment: 0.8 },
		{ time: '10:00', volume: 67, sentiment: 0.7 },
		{ time: '12:00', volume: 89, sentiment: 0.9 },
		{ time: '14:00', volume: 78, sentiment: 0.8 },
		{ time: '16:00', volume: 56, sentiment: 0.6 },
		{ time: '18:00', volume: 34, sentiment: 0.7 },
		{ time: '20:00', volume: 21, sentiment: 0.8 },
		{ time: '22:00', volume: 15, sentiment: 0.9 }
	];

	const topicTrendsData = [
		{ topic: 'Paint Formulas', thisWeek: 245, lastWeek: 198, growth: 23.7 },
		{ topic: 'Color Matching', thisWeek: 189, lastWeek: 167, growth: 13.2 },
		{ topic: 'Quality Control', thisWeek: 156, lastWeek: 143, growth: 9.1 },
		{ topic: 'Equipment Issues', thisWeek: 134, lastWeek: 156, growth: -14.1 },
		{ topic: 'Safety Protocols', thisWeek: 98, lastWeek: 89, growth: 10.1 },
		{ topic: 'Production Planning', thisWeek: 87, lastWeek: 92, growth: -5.4 }
	];

	const sentimentData = [
		{ name: 'Positive', value: 68, color: '#10b981' },
		{ name: 'Neutral', value: 24, color: '#6b7280' },
		{ name: 'Negative', value: 8, color: '#ef4444' }
	];

	const recentChats = [
		{
			id: 1,
			employee: 'Sarah Chen',
			timestamp: '2 min ago',
			topic: 'Paint Formulas',
			query: "What's the optimal ratio for titanium white in semi-gloss paint?",
			response:
				'For semi-gloss paint, titanium white should comprise 15-20% of the total pigment load...',
			sentiment: 'positive',
			resolved: true,
			duration: '2m 34s',
			followUp: false
		},
		{
			id: 2,
			employee: 'Mike Rodriguez',
			timestamp: '8 min ago',
			topic: 'Quality Control',
			query: 'How do I test viscosity for batch #4521?',
			response: 'Use the Ford Cup #4 viscometer at 25°C. Target range is 85-95 seconds...',
			sentiment: 'neutral',
			resolved: true,
			duration: '1m 45s',
			followUp: true
		},
		{
			id: 3,
			employee: 'Emma Thompson',
			timestamp: '15 min ago',
			topic: 'Equipment Issues',
			query: 'Mixer #3 is making unusual noise during operation',
			response: 'This could indicate bearing wear. Check the maintenance schedule and...',
			sentiment: 'negative',
			resolved: false,
			duration: '4m 12s',
			followUp: true
		},
		{
			id: 4,
			employee: 'David Kim',
			timestamp: '23 min ago',
			topic: 'Color Matching',
			query: 'Customer wants to match Sherwin Williams SW 6204',
			response: 'SW 6204 (Sea Salt) can be matched using our base formula B-342...',
			sentiment: 'positive',
			resolved: true,
			duration: '3m 18s',
			followUp: false
		}
	];

	const commonQuestions = [
		{
			question: "What's the drying time for acrylic paint?",
			frequency: 45,
			category: 'Paint Properties'
		},
		{ question: 'How to fix paint separation issues?', frequency: 38, category: 'Quality Control' },
		{ question: 'Optimal temperature for paint mixing?', frequency: 32, category: 'Production' },
		{ question: 'Safety protocols for chemical handling?', frequency: 29, category: 'Safety' },
		{ question: 'Color matching for custom orders?', frequency: 26, category: 'Color Matching' }
	];

	let chartContainer1;
	let chartContainer2;

	$: filteredChats = recentChats.filter((chat) => {
		const matchesSearch =
			chat.query.toLowerCase().includes(searchTerm.toLowerCase()) ||
			chat.employee.toLowerCase().includes(searchTerm.toLowerCase());
		const matchesTopic =
			selectedTopic === 'all' || chat.topic.toLowerCase().includes(selectedTopic.toLowerCase());
		return matchesSearch && matchesTopic;
	});

	onMount(() => {
		Chart.register(...registerables);

		// Chat Volume Chart
		if (chartContainer1) {
			chatVolumeChart = new Chart(chartContainer1, {
				type: 'line',
				data: {
					labels: chatVolumeData.map((d) => d.time),
					datasets: [
						{
							label: 'Volume',
							data: chatVolumeData.map((d) => d.volume),
							borderColor: '#8b5cf6',
							backgroundColor: 'rgba(139, 92, 246, 0.1)',
							tension: 0.4,
							fill: true
						},
						{
							label: 'Sentiment',
							data: chatVolumeData.map((d) => d.sentiment * 100),
							borderColor: '#10b981',
							backgroundColor: 'rgba(16, 185, 129, 0.1)',
							tension: 0.4,
							yAxisID: 'y1'
						}
					]
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					plugins: {
						legend: {
							labels: {
								color: '#9CA3AF'
							}
						}
					},
					scales: {
						x: {
							grid: {
								color: '#374151'
							},
							ticks: {
								color: '#9CA3AF'
							}
						},
						y: {
							type: 'linear',
							display: true,
							position: 'left',
							grid: {
								color: '#374151'
							},
							ticks: {
								color: '#9CA3AF'
							}
						},
						y1: {
							type: 'linear',
							display: true,
							position: 'right',
							grid: {
								drawOnChartArea: false
							},
							ticks: {
								color: '#9CA3AF'
							}
						}
					}
				}
			});
		}

		// Sentiment Chart
		if (chartContainer2) {
			sentimentChart = new Chart(chartContainer2, {
				type: 'doughnut',
				data: {
					labels: sentimentData.map((d) => d.name),
					datasets: [
						{
							data: sentimentData.map((d) => d.value),
							backgroundColor: sentimentData.map((d) => d.color),
							borderWidth: 0
						}
					]
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					plugins: {
						legend: {
							position: 'bottom',
							labels: {
								color: '#9CA3AF',
								padding: 20
							}
						}
					}
				}
			});
		}
	});

	function getSentimentColor(sentiment) {
		switch (sentiment) {
			case 'positive':
				return 'border-green-500/30 text-green-400';
			case 'negative':
				return 'border-red-500/30 text-red-400';
			default:
				return 'border-gray-500/30 text-gray-400';
		}
	}

	function getStatusColor(resolved) {
		return resolved ? 'text-green-400' : 'text-yellow-400';
	}
</script>

<div class="p-6 space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-balance">Chat Analytics System</h1>
			<p class="text-muted-foreground text-pretty">
				Analyze employee conversations and AI interaction patterns
			</p>
		</div>
		<div class="flex items-center gap-2">
			<select
				bind:value={selectedTimeRange}
				class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
			>
				<option value="24h">Last 24h</option>
				<option value="7d">Last 7 days</option>
				<option value="30d">Last 30 days</option>
				<option value="90d">Last 90 days</option>
			</select>
			<button
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors flex items-center gap-2"
			>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
					/>
				</svg>
				Export
			</button>
		</div>
	</div>

	<!-- Key Metrics -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Conversations</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8Zm7.5-3.5a.5.5 0 0 0-1 0v2.793L6.354 5.646a.5.5 0 1 0-.708.708l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5a.5.5 0 0 0-.708-.708L8.5 7.293V4.5Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">1,247</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+18%</span> from yesterday
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Response Time</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">1.8s</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">-0.3s</span> improvement
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Resolution Rate</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z" />
				</svg>
			</div>
			<div class="text-2xl font-bold">94.2%</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+2.1%</span> this week
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Satisfaction Score</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">4.6/5</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">Based on 892 ratings</p>
		</div>
	</div>

	<!-- Charts Section -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- Chat Volume Over Time -->
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Chat Volume & Response Quality</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					24-hour conversation patterns with sentiment analysis
				</p>
			</div>
			<div class="h-80">
				<canvas bind:this={chartContainer1}></canvas>
			</div>
		</div>

		<!-- Sentiment Distribution -->
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Conversation Sentiment</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Overall mood and satisfaction in AI interactions
				</p>
			</div>
			<div class="h-80">
				<canvas bind:this={chartContainer2}></canvas>
			</div>
			<div class="mt-4 space-y-2">
				{#each sentimentData as item, index}
					<div class="flex items-center justify-between text-sm">
						<div class="flex items-center gap-2">
							<div class="w-3 h-3 rounded-full" style="background-color: {item.color}"></div>
							<span>{item.name}</span>
						</div>
						<span class="font-medium">{item.value}%</span>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Topic Trends -->
	<div class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
		<div class="mb-4">
			<h3 class="text-lg font-semibold">Topic Trends</h3>
			<p class="text-sm text-gray-500 dark:text-gray-400">Weekly comparison of discussion topics</p>
		</div>
		<div class="space-y-4">
			{#each topicTrendsData as topic, index}
				<div
					class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50"
				>
					<div class="flex-1">
						<div class="flex items-center justify-between mb-2">
							<span class="font-medium">{topic.topic}</span>
							<div class="flex items-center gap-4">
								<span class="text-sm text-gray-500 dark:text-gray-400"
									>{topic.thisWeek} conversations</span
								>
								<span
									class="px-2 py-1 text-xs rounded-full border {topic.growth > 0
										? 'border-green-500/30 text-green-400'
										: 'border-red-500/30 text-red-400'}"
								>
									{topic.growth > 0 ? '+' : ''}{topic.growth.toFixed(1)}%
								</span>
							</div>
						</div>
						<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
							<div
								class="bg-blue-500 h-2 rounded-full"
								style="width: {(topic.thisWeek /
									Math.max(...topicTrendsData.map((t) => t.thisWeek))) *
									100}%"
							></div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Recent Conversations -->
	<div class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
		<div class="mb-4">
			<h3 class="text-lg font-semibold">Recent Conversations</h3>
			<p class="text-sm text-gray-500 dark:text-gray-400">Live feed of employee AI interactions</p>
		</div>

		<!-- Search and Filters -->
		<div class="flex gap-4 mb-4">
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
					placeholder="Search conversations..."
					bind:value={searchTerm}
					class="w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
				/>
			</div>
			<select
				bind:value={selectedTopic}
				class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
			>
				<option value="all">All Topics</option>
				<option value="paint formulas">Paint Formulas</option>
				<option value="color matching">Color Matching</option>
				<option value="quality control">Quality Control</option>
				<option value="equipment">Equipment Issues</option>
				<option value="safety">Safety Protocols</option>
			</select>
		</div>

		<div class="max-h-96 overflow-y-auto space-y-4">
			{#each filteredChats as chat}
				<div
					class="p-4 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700/50"
				>
					<div class="flex items-start justify-between mb-3">
						<div class="flex items-center gap-3">
							<div class="font-medium">{chat.employee}</div>
							<span
								class="px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-full"
							>
								{chat.topic}
							</span>
							<span
								class="px-2 py-1 text-xs border rounded-full {getSentimentColor(chat.sentiment)}"
							>
								{chat.sentiment}
							</span>
						</div>
						<div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
							<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
								<path
									d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
								/>
							</svg>
							{chat.timestamp}
						</div>
					</div>

					<div class="space-y-3">
						<div>
							<p class="text-sm font-medium text-blue-400 mb-1">Question:</p>
							<p class="text-sm">{chat.query}</p>
						</div>

						<div>
							<p class="text-sm font-medium text-purple-400 mb-1">AI Response:</p>
							<p class="text-sm text-gray-500 dark:text-gray-400">{chat.response}</p>
						</div>

						<div
							class="flex items-center justify-between pt-2 border-t border-gray-200 dark:border-gray-600"
						>
							<div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
								<span>Duration: {chat.duration}</span>
								<span class="flex items-center gap-1 {getStatusColor(chat.resolved)}">
									{#if chat.resolved}
										<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
											<path
												d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z"
											/>
										</svg>
									{:else}
										<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
											<path
												d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"
											/>
										</svg>
									{/if}
									{chat.resolved ? 'Resolved' : 'Pending'}
								</span>
								{#if chat.followUp}
									<span class="text-blue-400">Follow-up needed</span>
								{/if}
							</div>
							<button
								class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors flex items-center gap-1"
							>
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
									/>
								</svg>
								View Full
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Common Questions -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Most Common Questions</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Frequently asked questions across all employees
				</p>
			</div>
			<div class="space-y-3">
				{#each commonQuestions as item, index}
					<div
						class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50"
					>
						<div class="flex-1">
							<p class="font-medium text-sm">{item.question}</p>
							<p class="text-xs text-gray-500 dark:text-gray-400">{item.category}</p>
						</div>
						<span
							class="px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-full"
						>
							{item.frequency}
						</span>
					</div>
				{/each}
			</div>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Topic Resolution Rates</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Success rates by conversation category
				</p>
			</div>
			<div class="space-y-4">
				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Paint Formulas</span>
						<span class="text-green-400">98%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 98%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Color Matching</span>
						<span class="text-green-400">95%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 95%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Quality Control</span>
						<span class="text-green-400">92%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 92%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Equipment Issues</span>
						<span class="text-yellow-400">87%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
						<div class="bg-yellow-400 h-2 rounded-full" style="width: 87%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Safety Protocols</span>
						<span class="text-green-400">99%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 99%"></div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
