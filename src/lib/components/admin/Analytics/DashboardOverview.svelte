<script>
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import { getContext } from 'svelte';
	import { getUsers } from '$lib/apis/users';
	import { getChatListByUserId, getChatById } from '$lib/apis/chats';

	const i18n = getContext('i18n');

	let aiUsageChart;
	let topicsChart;
	let chartContainer1;
	let chartContainer2;

	// User data
	let activeUsersCount = 0;
	let loading = true;
	let realTopicsData = [];

	const aiUsageData = [
		{ name: 'Mon', interactions: 245, efficiency: 87 },
		{ name: 'Tue', interactions: 312, efficiency: 91 },
		{ name: 'Wed', interactions: 189, efficiency: 83 },
		{ name: 'Thu', interactions: 278, efficiency: 89 },
		{ name: 'Fri', interactions: 356, efficiency: 94 },
		{ name: 'Sat', interactions: 167, efficiency: 78 },
		{ name: 'Sun', interactions: 134, efficiency: 76 }
	];

	const topicsData = [
		{ name: 'Paint Formulas', value: 35, color: '#8b5cf6' },
		{ name: 'Color Matching', value: 28, color: '#a855f7' },
		{ name: 'Quality Control', value: 18, color: '#c084fc' },
		{ name: 'Equipment Issues', value: 12, color: '#d8b4fe' },
		{ name: 'Safety Protocols', value: 7, color: '#e9d5ff' }
	];

	const recentActivities = [
		{
			user: 'Sarah Chen',
			action: 'Asked about titanium white ratios',
			time: '2 min ago',
			type: 'query'
		},
		{
			user: 'Mike Rodriguez',
			action: 'Completed color matching training',
			time: '15 min ago',
			type: 'training'
		},
		{
			user: 'Emma Thompson',
			action: 'Flagged quality issue in batch #4521',
			time: '32 min ago',
			type: 'alert'
		},
		{
			user: 'David Kim',
			action: 'Accessed former employee knowledge base',
			time: '1 hr ago',
			type: 'knowledge'
		}
	];

	onMount(() => {
		Chart.register(...registerables);

		// AI Usage Trends Chart
		if (chartContainer1) {
			aiUsageChart = new Chart(chartContainer1, {
				type: 'line',
				data: {
					labels: aiUsageData.map((d) => d.name),
					datasets: [
						{
							label: 'Interactions',
							data: aiUsageData.map((d) => d.interactions),
							borderColor: '#8b5cf6',
							backgroundColor: 'rgba(139, 92, 246, 0.1)',
							tension: 0.4,
							fill: true
						},
						{
							label: 'Efficiency %',
							data: aiUsageData.map((d) => d.efficiency),
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

		// Topics Pie Chart
		if (chartContainer2) {
			updateTopicsChart();
		}

		// Fetch user data
		loadUsers();
	});

	async function loadUsers() {
		try {
			loading = true;

			// Fetch all users using pagination
			let allUsers = [];
			let page = 1;
			let hasMore = true;

			while (hasMore) {
				const response = await getUsers(localStorage.token, '', 'created_at', 'asc', page);
				if (response && response.users) {
					allUsers = allUsers.concat(response.users);
					hasMore = response.users.length === 30; // PAGE_ITEM_COUNT is 30
					page++;
				} else {
					hasMore = false;
				}
			}

			// Count users with role "user"
			activeUsersCount = allUsers.filter((user) => user.role === 'user').length;

			// Fetch real topics data from user chats
			await loadRealTopicsData(allUsers);

			loading = false;
		} catch (err) {
			console.error('Error loading users:', err);
			loading = false;
		}
	}

	async function loadRealTopicsData(users) {
		try {
			// Get topics from all users' recent chats
			const allTopics = [];

			for (const user of users.slice(0, 10)) {
				// Limit to first 10 users for performance
				const userTopics = await getUserChatTopics(user.id);
				allTopics.push(...userTopics);
			}

			// Count topic frequency and create chart data
			const topicCounts = {};
			allTopics.forEach((topic) => {
				if (
					topic &&
					topic !== 'No recent chats' &&
					topic !== 'No recent user messages' &&
					topic !== 'Error loading topics'
				) {
					// Extract key words from the topic
					const words = topic
						.toLowerCase()
						.replace(/[^\w\s]/g, '')
						.split(/\s+/)
						.filter((word) => word.length > 3)
						.slice(0, 3); // Take first 3 meaningful words

					const keyPhrase = words.join(' ');
					if (keyPhrase) {
						topicCounts[keyPhrase] = (topicCounts[keyPhrase] || 0) + 1;
					}
				}
			});

			// Convert to chart data format
			const colors = ['#8b5cf6', '#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff'];
			realTopicsData = Object.entries(topicCounts)
				.sort(([, a], [, b]) => b - a)
				.slice(0, 5)
				.map(([name, value], index) => ({
					name,
					value,
					color: colors[index % colors.length]
				}));

			// Update the chart with real data
			updateTopicsChart();
		} catch (err) {
			console.warn('Error loading real topics data:', err);
			realTopicsData = topicsData; // Fallback to mock data
			updateTopicsChart();
		}
	}

	async function getUserChatTopics(userId) {
		try {
			// Get the latest chats for this user
			const chats = await getChatListByUserId(localStorage.token, userId, 1, {
				order_by: 'updated_at',
				direction: 'desc'
			});

			if (!chats || chats.length === 0) {
				return ['No recent chats'];
			}

			// Get the latest 3 chats and extract user messages
			const latestChats = chats.slice(0, 3);
			const topics = [];

			for (const chat of latestChats) {
				try {
					const chatData = await getChatById(localStorage.token, chat.id);
					if (
						chatData &&
						chatData.chat &&
						chatData.chat.history &&
						chatData.chat.history.messages
					) {
						const messages = Object.values(chatData.chat.history.messages);

						// Find the latest user message in this chat
						const userMessages = messages
							.filter((msg) => msg.role === 'user' && msg.content)
							.sort((a, b) => (b.created_at || 0) - (a.created_at || 0));

						if (userMessages.length > 0) {
							const latestUserMessage = userMessages[0];
							// Extract a topic from the message (first sentence or first 50 chars)
							const content = latestUserMessage.content.trim();
							const topic = content.length > 50 ? content.substring(0, 50) + '...' : content;
							topics.push(topic);
						}
					}
				} catch (chatErr) {
					console.warn(`Error fetching chat ${chat.id}:`, chatErr);
				}
			}

			// If no topics found, return default
			return topics.length > 0 ? topics : ['No recent user messages'];
		} catch (err) {
			console.warn(`Error fetching chat topics for user ${userId}:`, err);
			return ['Error loading topics'];
		}
	}

	function updateTopicsChart() {
		if (chartContainer2) {
			// Destroy existing chart if it exists
			if (topicsChart) {
				topicsChart.destroy();
			}

			// Use real data if available, otherwise fallback to mock data
			const dataToUse = realTopicsData.length > 0 ? realTopicsData : topicsData;

			topicsChart = new Chart(chartContainer2, {
				type: 'doughnut',
				data: {
					labels: dataToUse.map((d) => d.name),
					datasets: [
						{
							data: dataToUse.map((d) => d.value),
							backgroundColor: dataToUse.map((d) => d.color),
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
	}

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
			default:
				return 'bg-gray-500/20 text-gray-400';
		}
	}
</script>

<div class="p-6 space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-balance">AI Integration Dashboard</h1>
			<p class="text-muted-foreground text-pretty">
				Monitor employee AI interactions and business knowledge retention
			</p>
		</div>
		<div class="flex items-center gap-2">
			<div
				class="px-3 py-1 rounded-full border border-green-400 text-green-400 text-sm flex items-center gap-1"
			>
				<div class="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
				Live Monitoring
			</div>
			<button
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
			>
				Export Report
			</button>
		</div>
	</div>

	<!-- Key Metrics -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Employees</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM3.156 11.763c.16-.629.44-1.21.813-1.72a2.5 2.5 0 0 0-2.725 1.377c-.136.287.102.58.418.58h1.449c.01-.077.025-.156.045-.237ZM12.847 11.763c.02.08.036.16.046.237h1.446c.316 0 .554-.293.417-.579a2.5 2.5 0 0 0-2.722-1.378c.374.51.653 1.09.813 1.72ZM14 7.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0ZM3.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM5 13c-.552 0-1.013-.455-.876-.99a4.002 4.002 0 0 1 7.753 0c.136.535-.324.99-.877.99H5Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">{loading ? '...' : activeUsersCount}</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+2</span> from last week
			</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Daily AI Interactions</h3>
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
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Knowledge Retention</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">94.2%</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">From 12 former employees</p>
		</div>

		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="flex items-center justify-between mb-2">
				<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Efficiency Score</h3>
				<svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 16 16">
					<path
						d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z"
					/>
				</svg>
			</div>
			<div class="text-2xl font-bold">89.4%</div>
			<p class="text-xs text-gray-500 dark:text-gray-400">
				<span class="text-green-400">+5.2%</span> this month
			</p>
		</div>
	</div>

	<!-- Charts Section -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- AI Usage Trends -->
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">AI Usage Trends</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Daily interactions and efficiency over the past week
				</p>
			</div>
			<div class="h-80">
				<canvas bind:this={chartContainer1}></canvas>
			</div>
		</div>

		<!-- Top Discussion Topics -->
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Top Discussion Topics</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Most frequently discussed topics with AI
				</p>
			</div>
			<div class="h-80">
				<canvas bind:this={chartContainer2}></canvas>
			</div>
			<div class="mt-4 space-y-2">
				{#each realTopicsData.length > 0 ? realTopicsData : topicsData as topic, index}
					<div class="flex items-center justify-between text-sm">
						<div class="flex items-center gap-2">
							<div class="w-3 h-3 rounded-full" style="background-color: {topic.color}"></div>
							<span>{topic.name}</span>
						</div>
						<span class="font-medium">{topic.value}%</span>
					</div>
				{/each}
			</div>
		</div>
	</div>

	<!-- Recent Activity & Alerts -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- Recent Activity -->
		<div
			class="lg:col-span-2 p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">Recent Activity</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">
					Latest employee interactions with AI systems
				</p>
			</div>
			<div class="space-y-4">
				{#each recentActivities as activity, index}
					<div class="flex items-start gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
						<div class="p-2 rounded-full {getActivityColor(activity.type)}">
							<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 16 16">
								<path d={getActivityIcon(activity.type)} />
							</svg>
						</div>
						<div class="flex-1">
							<p class="font-medium">{activity.user}</p>
							<p class="text-sm text-gray-500 dark:text-gray-400">{activity.action}</p>
							<p class="text-xs text-gray-400 dark:text-gray-500 flex items-center gap-1 mt-1">
								<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
									/>
								</svg>
								{activity.time}
							</p>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<!-- System Status -->
		<div
			class="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
		>
			<div class="mb-4">
				<h3 class="text-lg font-semibold">System Status</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400">AI integration health metrics</p>
			</div>
			<div class="space-y-4">
				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>OCR Processing</span>
						<span class="text-green-400">98%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 98%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Knowledge Base</span>
						<span class="text-green-400">94%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 94%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Response Time</span>
						<span class="text-yellow-400">87%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
						<div class="bg-yellow-400 h-2 rounded-full" style="width: 87%"></div>
					</div>
				</div>

				<div>
					<div class="flex justify-between text-sm mb-2">
						<span>Data Retention</span>
						<span class="text-green-400">99%</span>
					</div>
					<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
						<div class="bg-green-400 h-2 rounded-full" style="width: 99%"></div>
					</div>
				</div>

				<div class="pt-4 border-t border-gray-200 dark:border-gray-600">
					<p class="text-sm text-gray-500 dark:text-gray-400 mb-2">Former Employee Data</p>
					<div class="text-2xl font-bold text-blue-500">12 Profiles</div>
					<p class="text-xs text-gray-500 dark:text-gray-400">Knowledge preserved and accessible</p>
				</div>
			</div>
		</div>
	</div>
</div>
