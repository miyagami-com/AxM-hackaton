<script>
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import { getUsers } from '$lib/apis/users';
	import { getChatListByUserId, getChatById } from '$lib/apis/chats';

	let selectedEmployee = 0;
	let searchTerm = '';
	let filterStatus = 'all';
	let sortBy = 'interactions';
	let employeeChart;
	let employees = [];
	let loading = true;
	let error = null;

	// Mock data for demonstration (will be replaced by real data)
	const mockWeeklyData = [
		{ day: 'Mon', interactions: 15, efficiency: 94 },
		{ day: 'Tue', interactions: 22, efficiency: 97 },
		{ day: 'Wed', interactions: 18, efficiency: 95 },
		{ day: 'Thu', interactions: 25, efficiency: 98 },
		{ day: 'Fri', interactions: 20, efficiency: 96 },
		{ day: 'Sat', interactions: 8, efficiency: 92 },
		{ day: 'Sun', interactions: 5, efficiency: 90 }
	];

	// Mock topics for demonstration
	const mockTopics = [
		['System Administration', 'Analytics', 'Development'],
		['General Questions', 'Help & Support', 'Technical Issues'],
		['Product Features', 'User Interface', 'Customization'],
		['API Usage', 'Integration', 'Documentation'],
		['Troubleshooting', 'Configuration', 'Best Practices']
	];

	let departmentStats = [];

	let chartContainer;

	$: filteredEmployees = employees.filter((emp) => {
		const matchesSearch =
			emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
			emp.role.toLowerCase().includes(searchTerm.toLowerCase());
		const matchesStatus = filterStatus === 'all' || emp.status === filterStatus;
		return matchesSearch && matchesStatus;
	});

	$: currentEmployee = employees[selectedEmployee];

	onMount(async () => {
		Chart.register(...registerables);
		await loadUsers();
	});

	async function loadUsers() {
		try {
			loading = true;
			error = null;

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

			// Transform user data to employee format and fetch chat topics
			employees = await Promise.all(
				allUsers.map(async (user, index) => {
					// Generate some mock analytics data for demonstration
					// In a real implementation, you would fetch actual chat/interaction data
					const aiInteractions = Math.floor(Math.random() * 200) + 50;
					const efficiency = Math.floor(Math.random() * 20) + 80;
					const lastActiveMinutes = getLastActiveMinutes(user.last_active_at);

					// Fetch real chat topics for this user
					const topTopics = await getUserChatTopics(user.id);

					return {
						id: user.id,
						name: user.name || 'Unknown User',
						role: user.role || 'User',
						avatar: user.profile_image_url || '/user.png',
						status: getRandomStatus(),
						aiInteractions: aiInteractions,
						efficiency: efficiency,
						lastActive: formatLastActive(lastActiveMinutes),
						topTopics: topTopics,
						weeklyData: generateMockWeeklyData(aiInteractions, efficiency)
					};
				})
			);

			// Update department stats based on actual users
			updateDepartmentStats();

			// Update chart if we have employees
			if (employees.length > 0) {
				updateChart();
			}
		} catch (err) {
			console.error('Error loading users:', err);
			error = err.message;
		} finally {
			loading = false;
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

	function getRandomStatus() {
		const statuses = ['active', 'away', 'offline'];
		return statuses[Math.floor(Math.random() * statuses.length)];
	}

	function getLastActiveMinutes(lastActiveAt) {
		if (!lastActiveAt) return Math.floor(Math.random() * 60) + 1;

		const now = Date.now() / 1000; // Convert to seconds
		const lastActive = lastActiveAt;
		const diffMinutes = Math.floor((now - lastActive) / 60);

		return Math.max(1, diffMinutes);
	}

	function formatLastActive(minutes) {
		if (minutes < 60) {
			return `${minutes} min ago`;
		} else if (minutes < 1440) {
			// Less than 24 hours
			const hours = Math.floor(minutes / 60);
			return `${hours} hr ago`;
		} else {
			const days = Math.floor(minutes / 1440);
			return `${days} day${days > 1 ? 's' : ''} ago`;
		}
	}

	function generateMockWeeklyData(baseInteractions, baseEfficiency) {
		return mockWeeklyData.map((day) => ({
			...day,
			interactions: Math.floor(day.interactions * (baseInteractions / 100)),
			efficiency: Math.max(60, Math.min(100, day.efficiency + (baseEfficiency - 90)))
		}));
	}

	function updateDepartmentStats() {
		// Group users by role and calculate stats
		const roleGroups = {};
		employees.forEach((emp) => {
			const role = emp.role;
			if (!roleGroups[role]) {
				roleGroups[role] = {
					employees: 0,
					totalInteractions: 0,
					totalEfficiency: 0
				};
			}
			roleGroups[role].employees++;
			roleGroups[role].totalInteractions += emp.aiInteractions;
			roleGroups[role].totalEfficiency += emp.efficiency;
		});

		// Convert to department stats format
		departmentStats = Object.entries(roleGroups).map(([role, stats]) => ({
			name: role,
			employees: stats.employees,
			avgInteractions: Math.round(stats.totalInteractions / stats.employees),
			avgEfficiency: Math.round(stats.totalEfficiency / stats.employees)
		}));
	}

	function updateChart() {
		if (chartContainer && currentEmployee) {
			if (employeeChart) {
				employeeChart.destroy();
			}

			employeeChart = new Chart(chartContainer, {
				type: 'line',
				data: {
					labels: currentEmployee.weeklyData.map((d) => d.day),
					datasets: [
						{
							label: 'Interactions',
							data: currentEmployee.weeklyData.map((d) => d.interactions),
							borderColor: '#8b5cf6',
							backgroundColor: 'rgba(139, 92, 246, 0.1)',
							tension: 0.4,
							fill: true,
							yAxisID: 'y'
						},
						{
							label: 'Efficiency %',
							data: currentEmployee.weeklyData.map((d) => d.efficiency),
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
	}

	$: if (currentEmployee) {
		updateChart();
	}

	function getStatusColor(status) {
		switch (status) {
			case 'active':
				return 'bg-green-500/20 text-green-400 border-green-500/30';
			case 'away':
				return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
			default:
				return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
		}
	}

	function getInitials(name) {
		return name
			.split(' ')
			.map((n) => n[0])
			.join('');
	}
</script>

<div class="p-6 space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-balance">Employee AI Usage Monitor</h1>
			<p class="text-muted-foreground text-pretty">
				Track individual employee interactions with AI systems
			</p>
		</div>
		<div class="flex items-center gap-2">
			<button
				on:click={loadUsers}
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors flex items-center gap-2"
			>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
					/>
				</svg>
				Refresh
			</button>
			<button
				class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
			>
				Export Data
			</button>
			<button
				class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
			>
				Generate Report
			</button>
		</div>
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
			<span class="ml-2 text-gray-600 dark:text-gray-400">Loading employee data...</span>
		</div>
	{:else if error}
		<div
			class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
		>
			<div class="flex items-center">
				<svg class="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
					<path
						fill-rule="evenodd"
						d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
						clip-rule="evenodd"
					/>
				</svg>
				<span class="text-red-800 dark:text-red-200">Error: {error}</span>
			</div>
		</div>
	{:else}
		<!-- Department Overview -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
			{#each departmentStats as dept, index}
				<div
					class="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
				>
					<div class="mb-2">
						<h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">{dept.name}</h3>
					</div>
					<div class="text-2xl font-bold">{dept.employees}</div>
					<p class="text-xs text-gray-500 dark:text-gray-400 mb-2">employees</p>
					<div class="space-y-1">
						<div class="flex justify-between text-xs">
							<span>Avg Interactions</span>
							<span class="font-medium">{dept.avgInteractions}</span>
						</div>
						<div class="flex justify-between text-xs">
							<span>Avg Efficiency</span>
							<span class="font-medium">{dept.avgEfficiency}%</span>
						</div>
					</div>
				</div>
			{/each}
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Employee List -->
			<div
				class="lg:col-span-1 p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
			>
				<div class="mb-4">
					<h3 class="text-lg font-semibold">Employee List</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">
						Click on an employee to view detailed analytics
					</p>
				</div>

				<!-- Search and Filters -->
				<div class="space-y-2 mb-4">
					<div class="relative">
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
							placeholder="Search employees..."
							bind:value={searchTerm}
							class="w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						/>
					</div>
					<div class="flex gap-2">
						<select
							bind:value={filterStatus}
							class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							<option value="all">All Status</option>
							<option value="active">Active</option>
							<option value="away">Away</option>
							<option value="offline">Offline</option>
						</select>
						<select
							bind:value={sortBy}
							class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							<option value="interactions">Interactions</option>
							<option value="efficiency">Efficiency</option>
							<option value="name">Name</option>
						</select>
					</div>
				</div>

				<div class="space-y-3">
					{#each filteredEmployees as employee, index}
						<div
							class="p-3 rounded-lg border cursor-pointer transition-colors {selectedEmployee ===
							index
								? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
								: 'border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700/50'}"
							on:click={() => (selectedEmployee = index)}
						>
							<div class="flex items-center gap-3">
								<div
									class="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-sm font-medium"
								>
									{getInitials(employee.name)}
								</div>
								<div class="flex-1 min-w-0">
									<div class="flex items-center gap-2">
										<p class="font-medium truncate">{employee.name}</p>
										<span
											class="px-2 py-1 text-xs rounded-full border {getStatusColor(
												employee.status
											)}"
										>
											{employee.status}
										</span>
									</div>
									<p class="text-xs text-gray-500 dark:text-gray-400 truncate">{employee.role}</p>
									<div class="flex items-center gap-4 mt-1">
										<span class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
											<svg class="h-3 w-3" fill="currentColor" viewBox="0 0 16 16">
												<path
													d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8Zm7.5-3.5a.5.5 0 0 0-1 0v2.793L6.354 5.646a.5.5 0 1 0-.708.708l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5a.5.5 0 0 0-.708-.708L8.5 7.293V4.5Z"
												/>
											</svg>
											{employee.aiInteractions}
										</span>
										<span class="text-xs text-gray-500 dark:text-gray-400"
											>{employee.efficiency}% efficiency</span
										>
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Employee Details -->
			{#if currentEmployee}
				<div
					class="lg:col-span-2 p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
				>
					<div class="flex items-center justify-between mb-4">
						<div class="flex items-center gap-3">
							<div
								class="h-12 w-12 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-lg font-medium"
							>
								{getInitials(currentEmployee.name)}
							</div>
							<div>
								<h3 class="text-lg font-semibold">{currentEmployee.name}</h3>
								<p class="text-sm text-gray-500 dark:text-gray-400">{currentEmployee.role}</p>
							</div>
						</div>
						<div class="flex items-center gap-2">
							<span
								class="px-2 py-1 text-xs rounded-full border {getStatusColor(
									currentEmployee.status
								)}"
							>
								{currentEmployee.status}
							</span>
							<button class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
								<svg class="h-4 w-4" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
									/>
								</svg>
							</button>
						</div>
					</div>

					<!-- Key Metrics -->
					<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
						<div class="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
							<div class="flex items-center gap-2 mb-2">
								<svg class="h-4 w-4 text-blue-500" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8Zm7.5-3.5a.5.5 0 0 0-1 0v2.793L6.354 5.646a.5.5 0 1 0-.708.708l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5a.5.5 0 0 0-.708-.708L8.5 7.293V4.5Z"
									/>
								</svg>
								<span class="text-sm font-medium">AI Interactions</span>
							</div>
							<div class="text-2xl font-bold">{currentEmployee.aiInteractions}</div>
							<p class="text-xs text-gray-500 dark:text-gray-400">This week</p>
						</div>

						<div class="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
							<div class="flex items-center gap-2 mb-2">
								<svg class="h-4 w-4 text-green-400" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5A.5.5 0 0 0 8 12Z"
									/>
								</svg>
								<span class="text-sm font-medium">Efficiency</span>
							</div>
							<div class="text-2xl font-bold">{currentEmployee.efficiency}%</div>
							<p class="text-xs text-gray-500 dark:text-gray-400">Average score</p>
						</div>

						<div class="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
							<div class="flex items-center gap-2 mb-2">
								<svg class="h-4 w-4 text-blue-400" fill="currentColor" viewBox="0 0 16 16">
									<path
										d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
									/>
								</svg>
								<span class="text-sm font-medium">Last Active</span>
							</div>
							<div class="text-lg font-bold">{currentEmployee.lastActive}</div>
							<p class="text-xs text-gray-500 dark:text-gray-400">Recent activity</p>
						</div>
					</div>

					<!-- Weekly Performance Chart -->
					<div class="mb-6">
						<h4 class="text-sm font-medium mb-3">Weekly Performance</h4>
						<div class="h-64">
							<canvas bind:this={chartContainer}></canvas>
						</div>
					</div>

					<!-- Top Topics -->
					<div>
						<h4 class="text-sm font-medium mb-3">Top Discussion Topics</h4>
						<div class="space-y-3">
							{#each currentEmployee.topTopics as topic, index}
								<div
									class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50"
								>
									<span class="font-medium">{topic}</span>
									<span
										class="px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-full"
									>
										{Math.floor(Math.random() * 50) + 10} queries
									</span>
								</div>
							{/each}
						</div>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
