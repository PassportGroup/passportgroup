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
                                :href="route('mails.index')">
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
                                                :content="$page.props.auth.full_name"
                                                class="border-none outline-none focus:outline-none focus:border-transparent">
                                            <img :src="$page.props.auth.img" alt="avatar"
                                                 class="w-10 h-10 rounded-full items-center align-center content-center">
                                            <span v-if="$page.props.auth.is_verified === 1"
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
                                        <div slot="dropdown"
                                             class="mt-1 py-2 shadow-xl rounded bg-white dark:bg-dark-2 text-sm relative z-50">
                                            <div class="absolute -top-2 right-1 arrow-up"></div>
                                            <div class="border-b">
                                                <div class="flex items-center mx-4 mb-4">
                                                    <img :src="$page.props.auth.img" alt="avatar"
                                                         class="w-10 rounded-full border-2 border-gray-300"/>
                                                    <div class="leading-5 ml-2">
                                                        <h4 class="text-sm font-semibold">{{
                                                                $page.props.auth.full_name
                                                            }}</h4>
                                                        <h5 class="text-xs font-semibold">{{
                                                                $page.props.auth.email
                                                            }}</h5>
                                                        <h5 v-if="$page.props.auth.is_active === 0 "
                                                            class="font-semibold items-center justify-center flex mt-1 rounded bg-opacity-2 py-1 text-red-800 bg-red-100 px-2">
                                                            <span class="text-xs"> {{ $t('general.email-not-verified') }}</span>
                                                        </h5>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="border-b">
                                                <inertia-link
                                                    :href="route('user.profile', $page.props.auth.username)"
                                                    class="px-4 py-2 hover:bg-gray-100  dark:hover:bg-dark-3 flex">
                                                    <svg class="w-5 h-5" fill="none" stroke="currentColor"
                                                         strokeLinecap="round" strokeLinejoin="round" strokeWidth="1"
                                                         viewBox="0 0 24 24">
                                                        <path
                                                            d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                                    </svg>
                                                    <div class="pl-3">
                                                        <p class="text-sm font-medium leading-none">{{ $t('general.my-profile') }}</p>
                                                        <p class="text-xs text-gray-500">{{ $t('general.my-profile-note') }}</p>
                                                    </div>
                                                </inertia-link>
                                            </div>
                                            <div v-if="hasRole('admin')"
                                                 class="flex items-center justify-center my-2 mx-4">
                                                <inertia-link v-tippy="{arrow : true,  animation : 'perspective'}"
                                                              :href="route('upload.index')"
                                                              class="mx-4 mt-auto text-white text-xs transition duration-500 ease-in-out transform border-0 rounded bg-theme-1 hover:bg-gray-900 focus:outline-none focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2"
                                                              content="Upload">
                                                    <div class="flex items-center uppercase w-full px-6 py-2">
                                                        <svg class="w-4 h-4 ml-2 mr-2" fill="none" stroke="currentColor"
                                                             viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                            <path
                                                                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                                                                stroke-linecap="round" stroke-linejoin="round"
                                                                stroke-width="2"></path>
                                                        </svg>
                                                        Process Nationality
                                                    </div>
                                                </inertia-link>
                                            </div>
                                            <inertia-link :href="route('index')" as="button"
                                                          class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-3 flex w-full focus:outline-none outline-none"
                                                          method="post">
                                                <div class="text-red-700">
                                                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24">
                                                        <path
                                                            d="M13 4.00894C13.0002 3.45665 12.5527 3.00876 12.0004 3.00854C11.4481 3.00833 11.0002 3.45587 11 4.00815L10.9968 12.0116C10.9966 12.5639 11.4442 13.0118 11.9965 13.012C12.5487 13.0122 12.9966 12.5647 12.9968 12.0124L13 4.00894Z"
                                                            fill="currentColor"/>
                                                        <path
                                                            d="M4 12.9917C4 10.7826 4.89541 8.7826 6.34308 7.33488L7.7573 8.7491C6.67155 9.83488 6 11.3349 6 12.9917C6 16.3054 8.68629 18.9917 12 18.9917C15.3137 18.9917 18 16.3054 18 12.9917C18 11.3348 17.3284 9.83482 16.2426 8.74903L17.6568 7.33481C19.1046 8.78253 20 10.7825 20 12.9917C20 17.41 16.4183 20.9917 12 20.9917C7.58172 20.9917 4 17.41 4 12.9917Z"
                                                            fill="currentColor"/>
                                                    </svg>
                                                </div>
                                                <div class="pl-3">
                                                    <p class="text-sm font-medium leading-none">
                                                        {{ $t('general.logout') }}
                                                    </p>
                                                </div>
                                            </inertia-link>
                                        </div>
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

