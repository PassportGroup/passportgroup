<template>
    <div>
        <FlashMessages/>
        <div @resize.window="watchScreen()">
            <div class="flex h-screen antialiased text-gray-900 bg-gray-100 dark:bg-dark dark:text-light">
                <!-- Sidebar first column -->
                <!-- Backdrop -->
                <div
                    v-show="isSidebarOpen"
                    @click="isSidebarOpen = false"
                    class="fixed inset-0 z-10 bg-primary-darker md:hidden"
                    style="opacity: 0.5"
                    aria-hidden="true"
                ></div>
                <aside
                    v-show="isSidebarOpen"
                    x-transition:enter="transition-all transform duration-300 ease-in-out"
                    x-transition:enter-start="-translate-x-full opacity-0"
                    x-transition:enter-end="translate-x-0 opacity-100"
                    x-transition:leave="transition-all transform duration-300 ease-in-out"
                    x-transition:leave-start="translate-x-0 opacity-100"
                    x-transition:leave-end="-translate-x-full opacity-0"
                    ref="sidebar"
                    @keydown.escape="window.innerWidth <= 768 ? isSidebarOpen = false : ''"
                    tabindex="-1"
                    class="fixed inset-y-0 z-10 flex flex-shrink-0 bg-white border-r md:static dark:border-primary-darker dark:bg-darker focus:outline-none"
                >
                    <!-- Mini column -->
                    <dashboard-side-menu/>
                </aside>
                <div class="flex flex-1 h-screen overflow-y-scroll">
                    <!-- Main content -->
                    <main class="flex-1">
                        <header class="flex items-center justify-between p-4">
                            <div class="flex items-center space-x-4 md:space-x-0">
                                <!-- Sidebar button -->
                                <button
                                    @click="isSidebarOpen = true; $nextTick(() => { $refs.sidebar.focus() })"
                                    class="p-1 transition-colors duration-200 rounded-md text-primary-lighter bg-primary-50 md:hidden hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:ring"
                                >
                                    <span class="sr-only">Open main manu</span>
                                    <span aria-hidden="true">
                                    <svg
                                        v-show="!isSidebarOpen"
                                        class="w-8 h-8"
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                      <path
                                          stroke-linecap="round"
                                          stroke-linejoin="round"
                                          stroke-width="2"
                                          d="M4 6h16M4 12h16M4 18h16"
                                      />
                                    </svg>
                                    <svg
                                        v-show="isSidebarOpen"
                                        class="w-8 h-8"
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                  </span>
                                </button>
                                <h2 class="text-theme-1 block p-2 text-4xl font-medium tracking-tighter text-black transition duration-500 ease-in-out transform cursor-pointer hover:text-blueGray-500 lg:text-x lg:mr-8">
                                    PassportGroup <span class="text-theme-3 text-2xl">&nbsp;&nbsp;Dashboard </span>
                                </h2>
                            </div>
                            <div class="space-x-2">
                                <!-- Search panel button -->
                                <button
                                    @click="openSearchPanel"
                                    class="p-1 transition-colors duration-200 rounded-md text-primary-lighter bg-primary-50 hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:ring"
                                >
                                    <span class="sr-only">Open search panel</span>
                                    <span aria-hidden="true">
                    <svg
                        class="w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                      <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      />
                    </svg>
                  </span>
                                </button>

                                <!-- User panel button -->
                                <button
                                    @click="openUserPanel"
                                    class="p-1 transition-colors duration-200 rounded-md text-primary-lighter bg-primary-50 xl:hidden hover:text-primary hover:bg-primary-100 dark:hover:text-light dark:hover:bg-primary-dark dark:bg-dark focus:outline-none focus:ring"
                                >
                                    <span class="sr-only">Open user panel</span>
                                    <span aria-hidden="true">
                    <svg
                        class="w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                      <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
                      />
                    </svg>
                  </span>
                                </button>
                            </div>
                        </header>
                        <slot/>
                    </main>
                    <!-- User panel -->
                    <section
                        v-show="isUserPanelOpen"
                        x-transition:enter="transition duration-300 ease-in-out transform"
                        x-transition:enter-start="translate-x-full"
                        x-transition:enter-end="translate-x-0"
                        x-transition:leave="transition duration-300 ease-in-out transform"
                        x-transition:leave-start="translate-x-0"
                        x-transition:leave-end="translate-x-full"
                        @keydown.escape="window.innerWidth <= 1024 ? isUserPanelOpen = false : ''"
                        tabindex="-1"
                        ref="userPanel"
                        class="fixed inset-y-0 top-0 right-0 z-10 flex-shrink-0 bg-white xl:z-0 xl:sticky w-80 dark:bg-darker dark:text-light xl:border-l dark:border-primary-darker focus:outline-none"
                    >
                        <h2 class="sr-only">User panel</h2>
                        <!-- Close button -->
                        <div class="absolute left-0 p-2 transform -translate-x-full xl:hidden">
                            <button
                                @click="isUserPanelOpen = false"
                                class="p-2 rounded-md text-dark dark:text-light focus:outline-none focus:ring"
                            >
                                <svg
                                    class="w-5 h-5"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                        <div class="flex flex-col h-screen">
                            <!-- Panel header -->
                            <div class="flex-shrink-0 px-4">
                                <!-- Settings button -->
                                <div class="flex flex-row items-end justify-end">
                                    <div class="flex flex-row space-x-1 mx-2 mt-2">
<!--                                        <LanguageSwitcher :locale-link="'waspito_insurance.locale.set'"/>-->
                                        <inertia-link href="#" @click.prevent="logout">
                                            <div
                                                v-tippy="{ arrow : true,  animation : 'perspective'}"
                                                :content="$t('menu.logout')"
                                                class="transition-colors duration-200 rounded-full focus:outline-none">
                                                <span class="sr-only">Logout</span>
                                                <svg
                                                    class="w-6 h-6"
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
                                            </div>
                                        </inertia-link>
                                    </div>
                                    <DarkModeSwitcher/>
                                </div>
                            </div>
                            <!-- Panel content -->
                            <div class="flex-1 p-4 space-y-2 overflow-y-hidden hover:overflow-y-auto">
                                <!-- content -->
                                <div class="flex flex-col items-center">
                                    <!-- User avatar -->
                                    <img
                                        class="w-full h-28 p-2 rounded-full dark:opacity-70 object-contain"
                                        :src="'/static/images' + $page.props.auth.profile_image"
                                        :alt="$page.props.auth.username"
                                    />
                                    <h2 class="text-xl font-bold text-gray-600">PassportGroup</h2>
                                    <h2 class="text-x2 font-bold text-gray-600">{{ $page.props.auth.email }}</h2>

                                    <div class="my-3">
                                        <inertia-link :href="'#'"
                                                      class="uppercase inline-flex items-center justify-center font-bold py-2 px-4 mx-2 text-theme-3 hover:text-white border border-theme-3 hover:border-theme-3 waspito-button transition duration-1000 ease-in-out transform outline-none focus:outline-none">
                                            <icon name="doctor" class="flex mx-2 w-5 h-5 text-theme-3 hover:text-white"/>
                                            View Profile
                                        </inertia-link>
                                    </div>
                                </div>
                                <div class="space-y-2 p-2">
                                    <div class="bg-green-100 mt-5 bg-opacity-40 flex h-72 w-full rounded">
                                      <div class="overflow-y-scroll overflow-scroll-container py-3 p-2 flex-1">
                                         <h3 class="text-theme-1 font-bold text-sm underline my-2">Recent Activities</h3>
                                          <a v-for="activity in 3" href="#" class="block">
                                              <div class="flex px-4 space-x-4">
                                                  <div class="relative flex-shrink-0">
                                                          <inertia-link
                                                              :href="'#'"
                                                              class="relative z-50 inline-block overflow-visible rounded-ful">
                                                              <img class="object-contain rounded-full w-9 h-9 border border-theme-3"
                                                                   :src="'/static/images/' + $page.props.auth.profile_image"
                                                                   :alt="'Unknown user'"/>
                                                          </inertia-link>
                                                      <div class="absolute h-24 p-px -mt-3 -ml-px bg-gray-200 left-1/2 dark:bg-primary-darker"></div>
                                                  </div>
                                                  <div class="flex-1 overflow-hidden pb-2 mb-2">
                                                      <h5 class="text-sm font-medium text-theme-1 dark:text-light">New Mail Processed</h5>
                                                      <p class="text-xs font-normal text-gray-700 flex-wrap dark:text-primary-lighter">
                                                        The mail <strong>#Ta3428sadqw</strong> has been successfully processed.
                                                      </p>
                                                      <span class="text-sm font-normal text-gray-400 dark:text-primary-light">3rd Nov, 2021</span>
                                                  </div>
                                              </div>
                                          </a>
                                      </div>
                                    </div>
                                    <div class="flex items-center justify-end">
                                        <a href="#" class="flex inline-flex items-center text-theme-1 hover:underline">
                                            All activities
                                            <icon name="arrow-narrow-right" class="ml-1 w-4 h-4"/>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <!-- Panel footer -->
                            <footer class="flex items-center justify-between flex-shrink-0 px-4 py-2 border-t dark:border-primary-darker">
                                <div class="float-right text-sm">Designed by
                                    <a href="https://twitter.com/muarachmann" target="_blank" class="text-theme-1 hover:underline">
                                        Mua Rachmann
                                    </a>
                                </div>
                            </footer>
                        </div>
                    </section>
                </div>

                <!-- Panels -->
                <!-- Search panel -->
                <!-- Backdrop -->
                <div
                    class="fixed inset-0 z-10 bg-dark-1 transition duration-300 ease-in-out opacity-0"
                    v-show="isSearchPanelOpen"
                    @click="isSearchPanelOpen = false"
                    style="opacity: 0.5"
                    aria-hidden="true"
                ></div>
                <!-- Panel -->
                <section
                    :class="!isSearchPanelOpen ? '-translate-x-full' : 'translate-x-0'"
                    @keydown.escape="isSearchPanelOpen = false"
                    class="fixed inset-y-0 z-999 w-full duration-500 ease-in-out transform sm:duration-500 max-w-xs bg-white shadow-xl dark:bg-darker dark:text-light sm:max-w-md focus:outline-none"
                >
                    <div :class="!isSearchPanelOpen ? '-translate-x-full' : 'translate-x-full'" class="absolute right-0 p-2 transform ">
                        <!-- Close button -->
                        <button @click="isSearchPanelOpen = false" class="p-2 text-white rounded-md focus:outline-none focus:ring">
                            <svg
                                class="w-5 h-5"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <h2 class="sr-only">Search panel</h2>
                    <!-- Panel content -->
                    <div class="flex flex-col h-screen">
                        <!-- Panel header (Search input) -->
                        <div
                            class="relative flex-shrink-0 px-4 py-8 text-gray-400 border-b dark:border-primary-darker dark:focus-within:text-light focus-within:text-gray-700"
                        >
              <span class="absolute inset-y-0 inline-flex items-center px-4">
                <svg
                    class="w-5 h-5"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                  <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </span>
                            <input
                                ref="searchInput"
                                type="text"
                                class="w-full py-2 pl-10 pr-4 border rounded-full dark:bg-dark dark:border-transparent dark:text-light focus:outline-none focus:ring"
                                placeholder="Search..."
                            />
                        </div>

                        <!-- Panel content (Search result) -->
                        <div class="flex-1 px-4 pb-4 space-y-4 overflow-y-hidden h hover:overflow-y-auto">
                            <h3 class="py-2 text-sm font-semibold text-gray-600 dark:text-light">History</h3>
                            <p class="px=4">Search results</p>
                            <!--  -->
                            <!-- Search content -->
                            <!--  -->
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<script>
import DarkModeSwitcher from "../shared/DarkModeSwitcher";
import LanguageSwitcher from "../shared/LanguageSwitcher";
import DashboardSideMenu from "../shared/includes/DashboardSideMenu";
import FlashMessages from "../shared/helpers/FlashMessages";
export default {
    name: "DashboardLayout",
    components: {
        FlashMessages,
        DashboardSideMenu,
        LanguageSwitcher,
        DarkModeSwitcher
    },
    data() {
        return {
            isNotificationsPanelOpen: false,
            isSidebarOpen: window.innerWidth >= 768,
            isUserPanelOpen: window.innerWidth >= 1280,
            isSettingsPanelOpen: false,
            isSearchPanelOpen: false,
        }
    },
    onIdle() {
        this.$swal({
            title: 'Session Timeout',
            input: 'password',
            inputLabel: 'Password',
            inputPlaceholder: 'Enter your password',
            inputAttributes: {
                autocapitalize: 'off',
                autocorrect: 'off',
                autocomplete: 'off',
            },
            dismiss: false,
        }).then((result) => {
            console.log(result)
        })
    },
    methods: {
        watchScreen() {
            if (window.innerWidth <= 768) {
                this.isSidebarOpen = false
                this.isUserPanelOpen = false
            } else if (window.innerWidth >= 768 && window.innerWidth < 1280) {
                this.isSidebarOpen = true
                this.isUserPanelOpen = false
            } else if (window.innerWidth >= 1280) {
                this.isSidebarOpen = true
                this.isUserPanelOpen = true
            }
        },
        toggleSidebarMenu() {
            this.isSidebarOpen = !this.isSidebarOpen
        },
        openUserPanel() {
            this.isUserPanelOpen = true
            this.$nextTick(() => {
                this.$refs.userPanel.focus()
            })
        },
        openSettingsPanel() {
            this.isSettingsPanelOpen = true
            this.$nextTick(() => {
                this.$refs.settingsPanel.focus()
            })
        },
        openNotificationsPanel() {
            this.isNotificationsPanelOpen = true
            this.$nextTick(() => {
                this.$refs.notificationsPanel.focus()
            })
        },
        openSearchPanel() {
            this.isSearchPanelOpen = true
            this.$nextTick(() => {
                this.$refs.searchInput.focus()
            })
        },
        logout() {
            this.$inertia.post(this.route('waspito_insurance.dashboard.logout', this.$page.props.company.slug))
        }
    }
}
</script>

<style scoped>

</style>
