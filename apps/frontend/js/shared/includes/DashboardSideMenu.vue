<template>
    <nav class="flex flex-col flex-shrink-0 h-full px-2 py-4 border-r dark:border-primary-darker">
        <!-- Brand -->
        <div class="flex-shrink-0 flex flex-col items-center justify-center">
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('menu.profile')"
                :href="'#'"
                class="block text-xl font-bold tracking-wider uppercase text-primary-dark dark:text-light">
                <img :alt="$page.props.auth.username" :src="'/static/images' + $page.props.auth.profile_image"
                     class="text-center justify-center items-center rounded-full object-contain w-10 h-10 items-center justify-center border border-theme-1"/>
            </inertia-link>
        </div>
        <div class="flex flex-col items-center justify-center flex-1 space-y-4">
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('menu.dashboard')"
                :href="route('dashboard.mails.index')"
                class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                <span class="sr-only">{{ $t('menu.dashboard') }}</span>
                <icon name="gmail" class="w-7 h-7"/>
            </inertia-link>
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('menu.notifications')"
                :href="'#'"
                :class="newNotification ? 'animate-wiggle' : ''"
                class="relative p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                <span class="sr-only">Notifications</span>
                <icon name="bell" class="w-7 h-7"/>
                <div class="absolute inset-0 right-2 -top-1.5">
                    <span style="font-size: 9px !important;" class="inline-flex items-center px-1.5 border-1 border-white rounded-full font-semibold bg-red-500 text-white">
                      {{$h.kNumber($page.props.auth.unread_messages) }}
                    </span>
                </div>
            </inertia-link>
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('menu.medical_vouchers')"
                :href="'#'"
                class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                <span class="sr-only">Mails Processor</span>
                <icon name="document-report" class="w-7 h-7"/>
            </inertia-link>
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('general.new_voucher')"
                :href="'#'"
                class="p-2 text-white duration-200 rounded-full bg-orange-600 hover:text-white hover:bg-theme-3 focus:outline-none">
                <span class="sr-only">{{ $t('general.dashboard') }}</span>
                <icon name="home" class="w-8 h-8"/>
            </inertia-link>
            <template v-if="hasRole('super_admin|admin')">
                <inertia-link
                    v-tippy="{ arrow : true,  animation : 'perspective'}"
                    :content="$t('menu.users')"
                    :href="'#'"
                    class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                    <span class="sr-only">Users</span>
                    <icon name="users" class="w-7 h-7"/>
                </inertia-link>
                <inertia-link
                    v-tippy="{ arrow : true,  animation : 'perspective'}"
                    :content="$t('menu.settings')"
                    :href="'#'"
                    class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                    <span class="sr-only">Settings</span>
                    <icon name="settings" class="w-7 h-7"/>
                </inertia-link>
            </template>
            <inertia-link
                v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="$t('menu.website')"
                :href="route('home')"
                class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                <span class="sr-only">Website</span>
                <icon name="website" class="w-7 h-7"/>
            </inertia-link>
        </div>
        <!-- Sidebar footer -->
        <!-- prevent default just to prevent form submission in this demo -->
        <form @submit.prevent="logout" action="#" class="flex items-center justify-center flex-shrink-0">
            <!-- Logout button -->
            <button
                class="p-2 transition-colors duration-200 rounded-full text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:bg-primary-100 dark:focus:bg-primary-dark focus:ring-primary-darker">
                <span class="sr-only">Logout</span>
                <svg
                    class="w-7 h-7"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                </svg>
            </button>
        </form>
    </nav>
</template>

<script>
export default {
    name: "DashboardSideMenu",
    data() {
        return {
            newNotification: false,
        }
    },
    created() {
        let vm = this
        if (this.$page.props.auth.user) {
            // let userId = String(this.$page.props.auth.user.id)
            // Echo.private('App.Models.Insurance.InsuranceUser.' + userId)
            //     .notification((notification) => {
            //     console.log(notification)
            //     vm.newNotification = true
            //     // vm.$store.commit('ADD_NOTIFICATIONS', notification)
            // });
        }
    },
    methods: {
        url() {
            return location.pathname.substr(1);
        },
        isUrl(...urls) {
            if (urls[0] === '') {
                return this.url() === ''
            }
            return urls.filter(url => this.url().startsWith(url)).length
        },
        logout() {
            this.$inertia.post(this.route('logout'))
        }
    }
}
</script>

<style scoped>

</style>
