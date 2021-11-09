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
                                :href="route('dashboard.index')">
                              Admin Dashboard
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
                                <div class="relative">
                                    <dropdown placement="bottom-end">
                                        <div class="flex items-center justify-center">
                                            <img
                                                :alt="$page.props.auth.username"
                                                class="w-12 h-12 rounded-full border border-theme-1"
                                                :src="'/static/images' + $page.props.auth.profile_image"  />
                                        </div>
                                        <div slot="dropdown" class="-mt-4 py-2 shadow-xl rounded bg-white dark:bg-dark-2 text-sm relative">
                                            <div class="relative inline-block ">
                                                <!-- Dropdown menu -->
                                                <div class="absolute right-0 z-20 w-64 py-2 overflow-hidden bg-white rounded-md shadow-xl dark:bg-gray-800">
                                                    <inertia-link href="#" class="flex items-center p-3 -mt-2 text-sm text-gray-600 transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <img class="flex-shrink-0 object-cover mx-1 rounded-full w-9 h-9 border border-theme-3" :src="'/static/images' + $page.props.auth.profile_image" :alt="$page.props.auth.username">
                                                        <div class="mx-1">
                                                            <h1 class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ $page.props.auth.username }}</h1>
                                                            <p class="text-sm text-gray-500 dark:text-gray-400">{{ $page.props.auth.email }}</p>
                                                        </div>
                                                    </inertia-link>
                                                    <hr class="border-gray-200 dark:border-gray-700 ">
                                                    <inertia-link href="#" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <svg class="w-5 h-5 mx-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M7 8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8C17 10.7614 14.7614 13 12 13C9.23858 13 7 10.7614 7 8ZM12 11C13.6569 11 15 9.65685 15 8C15 6.34315 13.6569 5 12 5C10.3431 5 9 6.34315 9 8C9 9.65685 10.3431 11 12 11Z" fill="currentColor"></path>
                                                            <path d="M6.34315 16.3431C4.84285 17.8434 4 19.8783 4 22H6C6 20.4087 6.63214 18.8826 7.75736 17.7574C8.88258 16.6321 10.4087 16 12 16C13.5913 16 15.1174 16.6321 16.2426 17.7574C17.3679 18.8826 18 20.4087 18 22H20C20 19.8783 19.1571 17.8434 17.6569 16.3431C16.1566 14.8429 14.1217 14 12 14C9.87827 14 7.84344 14.8429 6.34315 16.3431Z" fill="currentColor"></path>
                                                        </svg>
                                                        <span class="mx-1">view profile</span>
                                                    </inertia-link>
                                                    <inertia-link href="#" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <svg class="w-5 h-5 mx-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M13.8199 22H10.1799C9.71003 22 9.30347 21.673 9.20292 21.214L8.79592 19.33C8.25297 19.0921 7.73814 18.7946 7.26092 18.443L5.42392 19.028C4.97592 19.1709 4.48891 18.9823 4.25392 18.575L2.42992 15.424C2.19751 15.0165 2.27758 14.5025 2.62292 14.185L4.04792 12.885C3.98312 12.2961 3.98312 11.7019 4.04792 11.113L2.62292 9.816C2.27707 9.49837 2.19697 8.98372 2.42992 8.576L4.24992 5.423C4.48491 5.0157 4.97192 4.82714 5.41992 4.97L7.25692 5.555C7.50098 5.37416 7.75505 5.20722 8.01792 5.055C8.27026 4.91269 8.52995 4.78385 8.79592 4.669L9.20392 2.787C9.30399 2.32797 9.71011 2.00049 10.1799 2H13.8199C14.2897 2.00049 14.6958 2.32797 14.7959 2.787L15.2079 4.67C15.4887 4.79352 15.7622 4.93308 16.0269 5.088C16.2739 5.23081 16.5126 5.38739 16.7419 5.557L18.5799 4.972C19.0276 4.82967 19.514 5.01816 19.7489 5.425L21.5689 8.578C21.8013 8.98548 21.7213 9.49951 21.3759 9.817L19.9509 11.117C20.0157 11.7059 20.0157 12.3001 19.9509 12.889L21.3759 14.189C21.7213 14.5065 21.8013 15.0205 21.5689 15.428L19.7489 18.581C19.514 18.9878 19.0276 19.1763 18.5799 19.034L16.7419 18.449C16.5093 18.6203 16.2677 18.7789 16.0179 18.924C15.7557 19.0759 15.4853 19.2131 15.2079 19.335L14.7959 21.214C14.6954 21.6726 14.2894 21.9996 13.8199 22ZM7.61992 16.229L8.43992 16.829C8.62477 16.9652 8.81743 17.0904 9.01692 17.204C9.20462 17.3127 9.39788 17.4115 9.59592 17.5L10.5289 17.909L10.9859 20H13.0159L13.4729 17.908L14.4059 17.499C14.8132 17.3194 15.1998 17.0961 15.5589 16.833L16.3799 16.233L18.4209 16.883L19.4359 15.125L17.8529 13.682L17.9649 12.67C18.0141 12.2274 18.0141 11.7806 17.9649 11.338L17.8529 10.326L19.4369 8.88L18.4209 7.121L16.3799 7.771L15.5589 7.171C15.1997 6.90671 14.8132 6.68175 14.4059 6.5L13.4729 6.091L13.0159 4H10.9859L10.5269 6.092L9.59592 6.5C9.39772 6.58704 9.20444 6.68486 9.01692 6.793C8.81866 6.90633 8.62701 7.03086 8.44292 7.166L7.62192 7.766L5.58192 7.116L4.56492 8.88L6.14792 10.321L6.03592 11.334C5.98672 11.7766 5.98672 12.2234 6.03592 12.666L6.14792 13.678L4.56492 15.121L5.57992 16.879L7.61992 16.229ZM11.9959 16C9.78678 16 7.99592 14.2091 7.99592 12C7.99592 9.79086 9.78678 8 11.9959 8C14.2051 8 15.9959 9.79086 15.9959 12C15.9932 14.208 14.2039 15.9972 11.9959 16ZM11.9959 10C10.9033 10.0011 10.0138 10.8788 9.99815 11.9713C9.98249 13.0638 10.8465 13.9667 11.9386 13.9991C13.0307 14.0315 13.9468 13.1815 13.9959 12.09V12.49V12C13.9959 10.8954 13.1005 10 11.9959 10Z" fill="currentColor"></path>
                                                        </svg>
                                                        <span class="mx-1">Settings</span>
                                                    </inertia-link>
                                                    <inertia-link href="#" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <svg class="w-5 h-5 mx-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M21 19H3C1.89543 19 1 18.1046 1 17V16H3V7C3 5.89543 3.89543 5 5 5H19C20.1046 5 21 5.89543 21 7V16H23V17C23 18.1046 22.1046 19 21 19ZM5 7V16H19V7H5Z" fill="currentColor"></path>
                                                        </svg>
                                                        <span class="mx-1">Keyboard shortcuts</span>
                                                    </inertia-link>
                                                    <hr class="border-gray-200 dark:border-gray-700 ">
                                                    <inertia-link :href="route('dashboard.index')" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <icon name="home" class="w-5 h-5 mx-1 text-red-700"/>
                                                        <span class="mx-1">Dashboard</span>
                                                    </inertia-link>
                                                    <inertia-link :href="'#'" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <svg class="w-5 h-5 mx-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M9 3C6.23858 3 4 5.23858 4 8C4 10.7614 6.23858 13 9 13C11.7614 13 14 10.7614 14 8C14 5.23858 11.7614 3 9 3ZM6 8C6 6.34315 7.34315 5 9 5C10.6569 5 12 6.34315 12 8C12 9.65685 10.6569 11 9 11C7.34315 11 6 9.65685 6 8Z" fill="currentColor"></path>
                                                            <path d="M16.9084 8.21828C16.6271 8.07484 16.3158 8.00006 16 8.00006V6.00006C16.6316 6.00006 17.2542 6.14956 17.8169 6.43645C17.8789 6.46805 17.9399 6.50121 18 6.5359C18.4854 6.81614 18.9072 7.19569 19.2373 7.65055C19.6083 8.16172 19.8529 8.75347 19.9512 9.37737C20.0496 10.0013 19.9987 10.6396 19.8029 11.2401C19.6071 11.8405 19.2719 12.3861 18.8247 12.8321C18.3775 13.2782 17.8311 13.6119 17.2301 13.8062C16.6953 13.979 16.1308 14.037 15.5735 13.9772C15.5046 13.9698 15.4357 13.9606 15.367 13.9496C14.7438 13.8497 14.1531 13.6038 13.6431 13.2319L13.6421 13.2311L14.821 11.6156C15.0761 11.8017 15.3717 11.9248 15.6835 11.9747C15.9953 12.0247 16.3145 12.0001 16.615 11.903C16.9155 11.8059 17.1887 11.639 17.4123 11.416C17.6359 11.193 17.8035 10.9202 17.9014 10.62C17.9993 10.3198 18.0247 10.0006 17.9756 9.68869C17.9264 9.37675 17.8041 9.08089 17.6186 8.82531C17.4331 8.56974 17.1898 8.36172 16.9084 8.21828Z" fill="currentColor"></path>
                                                            <path d="M19.9981 21C19.9981 20.475 19.8947 19.9551 19.6938 19.47C19.4928 18.9849 19.1983 18.5442 18.8271 18.1729C18.4558 17.8017 18.0151 17.5072 17.53 17.3062C17.0449 17.1053 16.525 17.0019 16 17.0019V15C16.6821 15 17.3584 15.1163 18 15.3431C18.0996 15.3783 18.1983 15.4162 18.2961 15.4567C19.0241 15.7583 19.6855 16.2002 20.2426 16.7574C20.7998 17.3145 21.2417 17.9759 21.5433 18.7039C21.5838 18.8017 21.6217 18.9004 21.6569 19C21.8837 19.6416 22 20.3179 22 21H19.9981Z" fill="currentColor"></path>
                                                            <path d="M16 21H14C14 18.2386 11.7614 16 9 16C6.23858 16 4 18.2386 4 21H2C2 17.134 5.13401 14 9 14C12.866 14 16 17.134 16 21Z" fill="currentColor"></path>
                                                        </svg>
                                                        <span class="mx-1">Team</span>
                                                    </inertia-link>
                                                    <hr class="border-gray-200 dark:border-gray-700 ">
                                                    <inertia-link href="#" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <DarkModeSwitcher class="mx-1"/>
                                                        <span class="mx-1">Switch Dark theme</span>
                                                    </inertia-link>
                                                    <inertia-link href="#" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <svg class="w-5 h-5 mx-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M12 22C6.47967 21.9939 2.00606 17.5203 2 12V11.8C2.10993 6.30452 6.63459 1.92794 12.1307 2.00087C17.6268 2.07379 22.0337 6.56887 21.9978 12.0653C21.9619 17.5618 17.4966 21.9989 12 22ZM11.984 20H12C16.4167 19.9956 19.9942 16.4127 19.992 11.996C19.9898 7.57928 16.4087 3.99999 11.992 3.99999C7.57528 3.99999 3.99421 7.57928 3.992 11.996C3.98979 16.4127 7.56729 19.9956 11.984 20ZM13 18H11V16H13V18ZM13 15H11C10.9684 13.6977 11.6461 12.4808 12.77 11.822C13.43 11.316 14 10.88 14 9.99999C14 8.89542 13.1046 7.99999 12 7.99999C10.8954 7.99999 10 8.89542 10 9.99999H8V9.90999C8.01608 8.48093 8.79333 7.16899 10.039 6.46839C11.2846 5.76778 12.8094 5.78493 14.039 6.51339C15.2685 7.24184 16.0161 8.57093 16 9.99999C15.9284 11.079 15.3497 12.0602 14.44 12.645C13.6177 13.1612 13.0847 14.0328 13 15Z" fill="currentColor"></path>
                                                        </svg>
                                                        <span class="mx-1">Help</span>
                                                    </inertia-link>
                                                    <inertia-link href="#" @click.prevent="logout" class="flex items-center p-3 text-sm text-gray-600 capitalize transition-colors duration-200 transform dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white">
                                                        <icon name="logout" class="w-5 h-5 mx-1 text-red-700"/>
                                                        <span class="mx-1">Sign Out</span>
                                                    </inertia-link>
                                                </div>
                                            </div>
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
        gotoRoute(notification, index) {
            this.newNotification = false
            this.$store.dispatch('MARK_READ_NOTIFICATION', index)
            this.$inertia.get(this.$h.notif(notification).url+notification.id)
        },
        logout() {
          this.$inertia.post(this.route('logout'))
        }
    }
}
</script>

