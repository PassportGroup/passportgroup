<template>
    <div class="w-full mx-auto max-w-8xl">
        <portal-target name="dropdown" slim/>
        <VTNotifications />
        <Header v-if="show_header"/>
        <div class="mb-28" id="main-body-content">
            <slot></slot>
        </div>
        <cookie @ok-cookie="setMarginProperties"/>
        <div id="bottom-navigation" class="fixed bottom-0 left-0 right-0 h-12 bg-gradient-to-r from-theme-1 to-theme-2 text-white flex items-center justify-between block md:hidden px-4 border-t border-gray-50 shadow-lg z-40">
            <inertia-link href="/">
                <div class="flex flex-col items-center justify-center font-bold text-xs" :class="menu && menu === 'home' ? 'text-theme-3' : 'text-white'">
                    <icon name="home" class="h-5 w-5"/>
                    <span>{{ $t('menu.home') }}</span>
                </div>
             </inertia-link>
            <inertia-link :href="route('inbox')">
                <div class="flex flex-col items-center justify-center font-bold text-xs relative" :class="menu && menu === 'inbox' ? 'text-theme-3' : 'text-white'">
                    <icon name="message" class="h-5 w-5"/>
                    <span>{{ $t('menu.inbox') }}</span>
                    <span
                        v-if="$store.state.notifications_length > 0 && $store.state.notifications[0].unread_count > 0 || $store.state.conversations_length > 0"
                        class="absolute top-0 right-1 h-2 w-2 inline-flex rounded-full bg-red-500">
                    </span>
                </div>
            </inertia-link>
            <inertia-link :href="route('listing:add')">
                <div class="flex flex-col items-center justify-center font-bold text-xs" :class="menu && menu === 'post' ? 'text-theme-3' : 'text-white'">
                    <icon name="camera" class="h-5 w-5"/>
                    <span>{{ $t('menu.post') }}</span>
                </div>
            </inertia-link>
            <inertia-link :href="route('settings')">
                <div class="flex flex-col items-center justify-center font-bold text-xs" :class="menu === 'account' ? 'text-theme-3' : 'text-white'">
                    <icon name="user" class="h-5 w-5"/>
                    <span>{{ $t('menu.account') }}</span>
                </div>
            </inertia-link>
        </div>
    </div>
</template>
<script>
import Footer from '@/components/Footer';
import Header from "@/components/Header";
import VTNotifications from "../components/VTNotifications";
import Icon from "../components/Icon";
import axios from "axios";
import Cookie from "../components/Cookie";

export default {
    name: 'MainLayout',
    props: {
        show_header: {
            type: Boolean,
            default: true
        },
        categories: {
            type: Array,
            default: null
        },
        menu: {
            type: String,
            default: 'home'
        }
    },
    components: {
        Cookie,
        Icon,
        VTNotifications,
        Header,
        Footer
    },
    data() {
        return {
            pathname: window.location.pathname,
            notifications: [],
            messages: [],
            notification_audio: new Audio('/static/audio/notification_bell.mp3'),
        }
    },
    methods: {
        subscribe2NewNotifications () {
            let channel = this.$pusher.subscribe('PassportGroup.web.notifications.'+this.$page.props.auth.username)
            channel.bind('notification', data => {
                this.$store.commit('setNotifications', data)
            })
        },
        subscribe2NewMessages () {
            let channel = this.$pusher.subscribe('PassportGroup.new.message.'+this.$page.props.auth.username)
            channel.bind('message', data => {
                this.$store.dispatch('getRecentConversation')
            })
        },
        setMarginProperties(value) {
            if (value) {
                $('#main-body-content').removeClass('mb-28').addClass('mb-52')
            }
        }
    },
    mounted() {
        if (this.categories) {
            this.$store.commit('setCategories', this.categories)
        }
        else {
            this.$store.dispatch('getMainCategories')
        }

        this.$store.dispatch('getAllLocations')
        this.$store.dispatch('getCategoriesWithChildren')
        if (this.$page.props.auth) {
            this.$store.dispatch('getRecentConversation')
            this.$store.dispatch('getRecentNotifications')
            this.subscribe2NewNotifications()
            this.subscribe2NewMessages()
        }
    }
}
</script>

<style scoped>
    .max-w-8xl {
        max-width: 1450px;
    }
</style>