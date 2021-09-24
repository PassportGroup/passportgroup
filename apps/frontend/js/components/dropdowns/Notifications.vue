<template>
    <div class="h-auto bg-white w-full md:w-96 z-50">
        <div>
              <div class="px-4 pt-3 bg-white shadow-lg font-medium text-md flex items-center justify-between">
                  <div
                      class="pb-1 cursor-pointer flex items-center gap-1"
                      :class="menu === 'messages' ? 'border-b-2 pb-1 border-theme-1 text-theme-1' : 'text-gray-400'"
                       @click="menu = 'messages'"
                  >
                      {{ $t('general.messages') }}
                       <span class="z-50 font-bold text-xs bg-theme-1 text-white rounded-full h-4 w-4 flex items-center justify-center">
                        {{ conversations.length < 99 ? conversations.length : '99+' }}
                       </span>
                  </div>
                  <div
                      class="pb-1 cursor-pointer flex items-center gap-1"
                      :class="menu === 'notifications' ? 'border-b-2 pb-1 border-theme-1 text-theme-1' : 'text-gray-400'"
                      @click="menu = 'notifications'"
                  >
                      {{ $t('general.notifications') }}
                      <span class="z-50 font-bold text-xs bg-theme-1 text-white rounded-full h-4 w-4 flex items-center justify-center">
                        {{ notifications.length < 99 ? notifications.length : '99+' }}
                      </span>
                  </div>
              </div>
              <div v-if="menu === 'notifications'">
                  <div v-if="notifications.length > 0" class="max-h-96 bg-gray-50 overflow-scroll-container overflow-y-auto w-full">
                       <div  v-for="(notification, index) in notifications" :key="index">
                            <notification-item @delete="deleteNotification" :notification="notification" :index="index"/>
                       </div>
                  </div>
                  <div v-else class="flex items-center bg-gray-50 gap-3 flex-col py-8">
                        <icon name="bell" class="h-16 w-16 text-gray-600"/>
                        <p>{{ $t('notifications.no-unread-notifications-msg') }}</p>
                  </div>
              </div>
                    <div v-else>
                        <div v-if="conversations.length > 0" class="max-h-96 bg-gray-50 overflow-scroll-container overflow-y-auto overflow-x-hidden w-full">
                            <div v-for="(conversation, index) in conversations" :key="index">
                                <div class="flex flex-row flex-nowrap p-4 hover:bg-white items-center border-b">
                                    <inertia-link :href="route('user.profile', conversation.last_unread_message.user)" class="h-16 w-16 relative flex-shrink-0">
                                        <img class="rounded-full object-cover flex-shrink-0 h-16 w-16 cursor-pointer" :src="conversation.last_unread_message.user_profile" :alt="conversation.last_unread_message.user"/>
                                        <img class="h-8 w-8 rounded-full object-cover absolute -bottom-1 -right-2" :src="conversation.subject.image" :alt="conversation.subject.title">
                                    </inertia-link>
                                    <div class="ml-4 cursor-pointer w-full" @click="gotoConversation(conversation)">
                                          <div class="text-gray-700 text-sm">
                                              <div class="flex items-center justify-between w-full">
                                                  <strong>{{ conversation.last_unread_message.user }}</strong>
                                                  <span class="text-xs text-gray-400">{{ conversation.last_unread_message.timestamp | moment('from', 'now') }}</span>
                                              </div>
                                              <div class="flex items-center justify-between">
                                                  <p class="truncate w-56" v-if="conversation.last_unread_message.type.toLowerCase() === 'text'">{{ conversation.last_unread_message.message }}</p>
                                                  <p v-else class="truncate w-56">New offer of {{ conversation.last_unread_message.offer.price }}</p>
                                                  <span class="z-50 font-bold text-xs bg-red-600 text-white rounded-full h-4 w-4 flex items-center justify-center">
                                                        {{ conversation.unread_messages }}
                                                  </span>
                                              </div>
                                          </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="flex items-center bg-gray-50 gap-3 flex-col py-8">
                            <icon name="chat" class="h-16 w-16 text-gray-600"/>
                            <p> {{ $t('notifications.no-unread-msg') }}</p>
                        </div>
                    </div>
              <div class="border-b px-4 py-2 bg-white shadow-lg text-center">
                  <inertia-link :href="route('inbox')" class="text-center hover:underline text-sm text-theme-1 cursor-pointer">{{ $t('general.view-all') }}</inertia-link>
              </div>
        </div>
    </div>
</template>

<script>
import Icon from "../Icon";
import NotificationItem from "../NotificationItem";

export default {
  name: "NotificationBox",
  components: {
      NotificationItem,
      Icon
  },

  data() {
      return {
          menu: 'messages',
          notifications: [],
          conversations: [],
      }
  },
  methods: {
      deleteNotification(index) {
          this.notifications.splice(index, 1)
      },
      gotoConversation(conversation) {
          this.$inertia.get(this.route('conversations', conversation.subject.slug))
      }
  },
  mounted() {
      this.notifications = this.$store.state.notifications
      this.conversations = this.$store.state.conversations
  }
}
</script>
