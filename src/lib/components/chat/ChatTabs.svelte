<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';
	
	import { chatId, chats, showSidebar, mobile } from '$lib/stores';
	import { createNewChat, deleteChatById, getChatList } from '$lib/apis/chats';
	
	import Plus from '../icons/Plus.svelte';
	import XMark from '../icons/XMark.svelte';
	import ModelSelector from './ModelSelector.svelte';
	
	const i18n: Writable<i18nType> = getContext('i18n');
	
	// Props for model selector
	export let selectedModels = [''];
	export let shareEnabled = false;
	
	// Get recent chats (limit to show only recent ones as tabs)
	$: recentChats = $chats ? $chats.slice(0, 8) : [];
	
	const switchToChat = async (chat: any) => {
		if (chat.id === $chatId) return;
		
		await goto(`/c/${chat.id}`);
		
		if ($mobile) {
			showSidebar.set(false);
		}
	};
	
	const createNewChatTab = async () => {
		console.log('Creating new chat tab...');
		
		try {
			// Create a temporary chat object for immediate display
			const tempChatId = `temp-${Date.now()}`;
			const tempChat = {
				id: tempChatId,
				title: $i18n.t('New Chat'),
				timestamp: Date.now(),
				time_range: 'Today'
			};
			
			// Add the temporary chat to the chats store immediately
			chats.update(currentChats => {
				if (currentChats) {
					return [tempChat, ...currentChats];
				}
				return [tempChat];
			});
			
			// Navigate to the new chat
			await goto('/');
			
			if ($mobile) {
				showSidebar.set(false);
			}
			
		} catch (error) {
			console.error('Error creating new chat tab:', error);
		}
	};
	
	const closeChat = async (chat: any, event: Event) => {
		event.stopPropagation();
		
		// Don't close if it's the only tab
		if (recentChats.length <= 1) return;
		
		try {
			// If we're closing the active chat, switch to another one first
			if (chat.id === $chatId) {
				const currentIndex = recentChats.findIndex(c => c.id === chat.id);
				const nextChat = recentChats[currentIndex + 1] || recentChats[currentIndex - 1];
				
				if (nextChat) {
					await switchToChat(nextChat);
				}
			}
			
			// Delete the chat from the backend
			await deleteChatById(localStorage.token, chat.id);
			
			// Update the chats store to remove the deleted chat
			chats.update(currentChats => {
				if (currentChats) {
					return currentChats.filter(c => c.id !== chat.id);
				}
				return currentChats;
			});
			
			console.log('Chat closed:', chat.title);
		} catch (error) {
			console.error('Error closing chat:', error);
		}
	};
	
	const truncateTitle = (title: string, maxLength: number = 25) => {
		return title.length > maxLength ? `${title.slice(0, maxLength)}...` : title;
	};
</script>

<!-- Chat Tabs Container -->
<div class="flex items-center bg-transparent px-2 min-h-[48px] relative z-50" style="margin-top: -24px !important;">
	<!-- Chat Tabs -->
	<div class="flex-1 flex items-center overflow-x-auto scrollbar-hidden">
		<div class="flex items-center min-w-0 gap-0">
			{#if recentChats.length === 0}
				<!-- Fallback when no chats - clickable -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div 
					class="flex items-center px-3 py-2 bg-gray-50 dark:bg-gray-800 border-b-2 border-b-blue-500 rounded-t-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
					on:click={createNewChatTab}
				>
					<span class="text-sm font-medium text-gray-700 dark:text-gray-200 italic">
						{$i18n.t('New Chat')}
					</span>
				</div>
			{:else}
				{#each recentChats as chat (chat.id)}
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						class="relative flex items-center min-w-0 max-w-56 group cursor-pointer select-none flex-shrink-0 mx-1
							{chat.id === $chatId 
								? 'bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-600 border-b-0 shadow-sm' 
								: 'bg-gray-50 dark:bg-gray-800 border border-transparent hover:bg-gray-100 dark:hover:bg-gray-700'
							}
							transition-all duration-200 ease-in-out rounded-t-lg"
						on:click={() => switchToChat(chat)}
					>
						<div class="flex items-center px-3 py-2 min-w-0 w-full">
							<!-- Tab Title -->
							<div class="flex-1 min-w-0 mr-2">
								<span class="text-sm font-medium text-gray-700 dark:text-gray-200 truncate block">
									{truncateTitle(chat.title)}
								</span>
							</div>
							
							<!-- Close Button -->
							{#if recentChats.length > 1}
								<button
									class="flex-shrink-0 p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 
										opacity-0 group-hover:opacity-100 transition-opacity duration-200
										{chat.id === $chatId ? 'opacity-60 hover:opacity-100' : ''}"
									on:click={(e) => closeChat(chat, e)}
									title={$i18n.t('Close tab')}
								>
									<XMark className="w-3 h-3 text-gray-500 dark:text-gray-400" />
								</button>
							{/if}
						</div>
					</div>
				{/each}
			{/if}
		</div>
	</div>
	
	<!-- New Chat Button -->
	<div class="flex-shrink-0 ml-2">
		<button
			class="flex items-center justify-center w-8 h-8 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 
				transition-colors duration-200 border border-gray-300 dark:border-gray-600 bg-blue-50 dark:bg-blue-900"
			on:click={createNewChatTab}
			title={$i18n.t('New chat')}
		>
			<Plus className="w-4 h-4 text-blue-600 dark:text-blue-300" />
		</button>
	</div>
</div>

<!-- Model Selector Section - Below tabs -->
<div class="bg-gray-50 dark:bg-gray-800 px-4 py-2 relative z-40">
	<div class="max-w-md">
		<ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
	</div>
</div>

<style>
	.scrollbar-hidden {
		-ms-overflow-style: none;
		scrollbar-width: none;
	}
	.scrollbar-hidden::-webkit-scrollbar {
		display: none;
	}
</style>