<template>
    <header ref="headerRef"
            class="w-full dark:bg-dark-2 bg-white sticky top-0 z-50 inset-x-0 h-18 border-b border-gray-200 shadow-md items-center">
        <div class="py-2 w-full dark:bg-dark-2 flex flex-col">
            <div id="mainNavBar" class="flex items-center justify-between mx-8">
                <div aria-label="Passport Group Payments" class="inline-flex items-center justify-start" title="Passport Group Payments">
                    <div
                        class="md:hidden p-1 h-8 w-8 bg-transparent items-center justify-center rounded-full align-middle outline-none focus:outline-none">
                        <Icon class="w-5 h-5 text-theme-1" name="menu-alt-2"/>
                    </div>
                    <inertia-link :href="'/'" aria-label="Portuguese Nationality Status"
                                  class="inline-flex items-center justify-start outline-none focus:outline-none"
                                  title="PassportGroup">
                        <Icon class="w-28 md:w-36 h-16 text-theme-4" name="logo"/>
                    </inertia-link>
                </div>
                <div>
                    <ul class="flex items-center justify-end space-x-3 md:space-x-5 lg:space-x-8 md:flex">
                      <li class="flex flex-row space-x-2">
                            <DarkModeSwitcher class="ltr:mr-2 rtl:ml-2"/>
                            <inertia-link
                                v-if="$page.props.auth"
                                class="ltr:mr-2 rtl:ml-2 py-2 px-4 rounded bg-gray-900 hover:bg-yellow-700 text-center text-white"
                                :href="route('mails.index')">
                              Mail Dashboard
                            </inertia-link>
                            <inertia-link
                                v-if="!$page.props.auth"
                                class="ltr:mr-2 rtl:ml-2 py-2 px-4 rounded bg-gray-900 hover:bg-yellow-700 text-center text-white"
                                :href="route('login')">
                              Login
                            </inertia-link>
                        </li>
                        <li :class="$page.props.auth ? 'mt-1.5' : ''" class="flex flex-row mx-2 hidden md:block space-x-2">
                            <LanguageSwitcher drop-down-color="text-gray-700"/>
                        </li>
                        <li>
                            <div v-if="$page.props.auth" class="flex">
                                <dropdown placement="bottom-end">
                                    <button :class="newNotification ? 'animate-wiggle' : ''"
                                            class="relative py-1 px-2 mt-2 items-center justify-center rounded-full align-middle outline-none focus:outline-none"
                                            content="notifications"
                                            name="notifications">
                                        <Icon class="w-5 h-5" name="bell"/>
                                        <span v-show="newNotification"
                                             class="w-2 h-2 rounded-full bg-red-500 border border-white absolute inset-0 mt-1 mr-1 m-auto">
                                        </span>
                                    </button>
                                    <div slot="dropdown"
                                         class="py-2 shadow-xl rounded bg-white dark:bg-dark-2 text-sm relative z-50">
                                        <div class="absolute -top-2 right-1 arrow-up"></div>
                                        <div class="flex justify-between mt-4 mb-1 px-3">
                                            <h1 class="font-bold text-lg text-left">Notifications</h1>
                                            <inertia-link :href="route('home')"
                                                          class="text-right text-theme-1 hover:text-gray-800">
                                                {{ $t('general.view-all') }}
                                            </inertia-link>
                                        </div>
                                        <div class="rounded-md text-sm overflow-y-auto overflow-x-hidden overflow-scroll-container max-h-98 w-96">
                                           kansdkjankdnjasd
                                        </div>
                                    </div>
                                </dropdown>
                                <span
                                    class="flex-inline font-bold text-sm mr-2 ml-2 mt-3 text-center content-center justify-center hidden md:block ">
                                    {{ $page.props.auth.username }}
                                </span>
                                <div class="inline-block rounded-full ring-2 ring-white relative w-10 h-10">
                                    <dropdown placement="bottom-end">
                                        <button v-tippy="{ arrow : true,  animation : 'perspective'}"
                                                :content="$page.props.auth.username"
                                                class="border-none outline-none focus:outline-none focus:border-transparent">
                                            <img :src="$page.props.auth.profile_image" alt="avatar"
                                                 class="w-10 h-10 rounded-full items-center align-center content-center">
                                            <span v-if="$page.props.auth.verify_email === true"
                                                 class="absolute -bottom-2 right-0 h-5 w-5 my-1 border-2 border-white rounded-full bg-theme-1 z-2">
                                                <svg class="rounded-full text-white" fill="none" stroke="currentColor"
                                                     viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                        d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                                                        stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"></path>
                                                </svg>
                                            </span>
                                        </button>
                                    </dropdown>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </header>
</template>
<script>
import Dropdown from "./Dropdown"
import LanguageSwitcher from "../LanguageSwitcher"
import { mixin as clickaway } from 'vue-clickaway'
import {mapGetters} from "vuex"
import DarkModeSwitcher from "../DarkModeSwitcher"

export default {
    name: "Header",
    mixins: [clickaway],
    components: {
      Dropdown,
      DarkModeSwitcher,
      LanguageSwitcher,
    },
    data() {
        return {
            newNotification: false,
            notificationPage: 0,
            notificationPageSize: 10,
        }
    },
    computed: {
        ...mapGetters([
            'passport_notifications',
            'getTheme'
        ])
    },
    methods: {
        allNotifications($state) {
            this.notificationPage = this.notificationPage + 1;
            this.newNotification = false
            axios.get(this.route('api.notifications.data'), {
                params: {
                    page: this.notificationPage,
                    page_size: this.notificationPageSize,
                }
            }).then(res => {
                res.data && (this.$store.commit('CONCAT_NOTIFICATIONS', res.data))
                if (res.data.length < 10) {
                    $state.complete()
                } else {
                    $state.loaded()
                }
            }).catch(error => {
                console.log(error.response)
            });
        },
        submit() {
            this.$inertia.post(this.route("logout"));
        },
        gotoRoute(notification, index) {
            this.newNotification = false
            this.$store.dispatch('MARK_READ_NOTIFICATION', index)
            this.$inertia.get(this.$h.notif(notification).url+notification.id)
        },
    }
}
</script>

