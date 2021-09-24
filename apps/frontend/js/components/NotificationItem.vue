<template>
     <div class="flex flex-row flex-nowrap hover:bg-white items-start justify-between border-b">
          <div class="flex items-center px-4 py-4">
                <div class="h-16 flex-shrink-0 w-16 relative cursor-pointer">
                    <inertia-link :href="route('user.profile', notification.sender.username)" v-if="notification.sender">
                        <img class="rounded-full object-cover flex-shrink-0 h-16 w-16" :src="notification.sender.profile" :alt="notification.sender.username"/>
                    </inertia-link>
                    <img v-else class="rounded-full object-cover flex-shrink-0 h-16 w-16" src="/static/images/bforbattoh.png" alt="Battoh">
                    <div class="h-6 rounded-full w-6 bg-theme-1 text-white absolute bottom-0 right-0  flex items-center justify-center">
                        <icon
                            :name="notification.type.toLowerCase() === 'message' ? 'message' : notification.type.toLowerCase() === 'follower' ? 'follower' : notification.type.toLowerCase() === 'transaction' ? 'money' : notification.type.toLowerCase() === 'identification' ? 'identification' : 'speakerphone'"
                            :class="{'h-4 w-4' : notification.type.toLowerCase() === 'transaction'}"
                        />
                    </div>
               </div>

                <div class="ml-4 cursor-pointer" @click="gotoTarget(notification)">
                    <p class="text-gray-700 text-sm" v-if="notification.type.toLowerCase() === 'message'" v-html="$t('notifications.new-message-from', {sender: notification.sender.username})"></p>
                    <p class="text-gray-700 text-sm" v-else-if="notification.type.toLowerCase() === 'offer' && notification.notifiable.status.toLowerCase() === 'pending'" v-html="$t('notifications.new-offer-from', {sender: notification.sender.username})"></p>
                    <p class="text-gray-700 text-sm m-0" v-else-if="notification.type.toLowerCase() === 'listing'" v-html="$t('notifications.new-listing-from', {sender: notification.sender.username, listing: notification.notifiable.title})" />
                    <div class="text-gray-700 text-sm" v-else-if="notification.type.toLowerCase() === 'offer' && notification.notifiable.status.toLowerCase() !== 'pending'">
                        <div v-if="notification.sender.username === notification.notifiable.user" v-html="$t('notifications.sender-action-his-offer', {sender: notification.sender.username, status: $t(`general.${notification.notifiable.status}`)})"></div>
                        <div v-else v-html="$t('notifications.sender-action-your-offer', {sender: notification.sender.username, status: notification.notifiable.status})"></div>
                    </div>
                    <p class="text-gray-700 text-sm" v-else-if="notification.type.toLowerCase() === 'follower'" v-html="$t('notifications.new-follower', {follower: notification.sender.username})"></p>
                    <p class="text-gray-700 text-sm" v-else-if="notification.type.toLowerCase() === 'identification' && notification.notifiable.status === 'approved'">
                          {{ $t('notifications.verification-approved') }}
                    </p>
                    <p class="text-gray-700 text-sm" v-else-if="notification.type.toLowerCase() === 'identification' && notification.notifiable.status === 'rejected'">
                          {{ $t('notifications.verification-rejected') }}
                    </p>
                    <div class="text-gray-700 text-sm m-0" v-else-if="notification.type.toLowerCase() === 'transaction'">
                        <div v-if="notification.notifiable.type === 'purchase'">
                            <div v-if="notification.notifiable.status === 'pending'">
                                <div v-if="notification.notifiable.username === notification.recipient.username" v-html="$t('general.purchase-item-of', {item: data.notifiable.listing, amount: intcomma(data.notifiable.amount) })"></div>
                                <div v-else class="text-gray-700 text-sm" v-html="$t('general.item-already-paid', {user: notification.sender.username})"></div>
                            </div>
                            <div v-else-if="notification.notifiable.status === 'delivered'" class="text-gray-700 text-sm" v-html="$t('general.waiting-already-delivered', {user: notification.sender.username})"></div>
                            <div v-else-if="notification.notifiable.status === 'received'" class="text-gray-700 text-sm" v-html="$t('general.transaction-completed-on-item', {item: notification.notifiable.listing})"></div>
                            <div v-else-if="notification.notifiable.status === 'canceled'" class="text-gray-700 text-sm" v-html="$t('general.transaction-canceled-by', {user: notification.sender.username})"></div>
                        </div>
                        <div v-else>
                            <p class="text-gray-700 text-sm" v-html="$t('general.withdrawal-of', {amount: intcomma(notification.notifiable.amount)})"></p>
                        </div>
                    </div>
                    <span class="text-xs text-gray-400">{{ notification.timesince }}</span>
                </div>
          </div>
     </div>
</template>

<script>
import Icon from "./Icon";
import axios from "axios";
export default {
    name: "NotificationItem",
    components: {Icon},
    props: {
        notification: Object,
        index: Number,
    },
    methods: {
        gotoTarget(notification) {
            this.markNotificationAsRead(notification.id)
            if (['message', 'offer'].includes(notification.type)) {
                this.$inertia.get(this.route('conversations', notification.notifiable.listing.slug))
            }
            else if (notification.type === 'follower') {
                this.$inertia.get(this.route('user.profile', notification.sender.username))
            }
            else if (notification.type === 'listing') {
                this.$inertia.get(this.route('listing', notification.notifiable.slug))
            }
            else if (notification.type === 'transaction') {
                if (notification.notifiable.type  === 'withdrawal') {
                    this.$inertia.get(this.route('account.wallet'))
                }
                else {
                    this.$inertia.get(this.route('conversations', notification.notifiable.listing.slug))
                }
            }
        },
        markNotificationAsRead(id) {
             axios.post(this.route('notification.mark.as.read', id))
        }
    }
}
</script>

<style scoped>

</style>