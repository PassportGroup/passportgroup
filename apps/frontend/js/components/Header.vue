<template>
    <div class="sticky top-0 w-full bg-gradient-to-r from-theme-1 h-12 md:h-36 to-theme-2 min-h-min py-1 md:py-4 md:p-0 z-40" id="header">
        <MenuSlider ref="MenuSlider"/>
        <div class="flex md:hidden items-center gap-1.5 mx-2">
            <inertia-link href="/" class="w-10">
                <img src="/static/images/passportgroup.png" class="w-full" alt="Battoh">
            </inertia-link>
            <button @click="$refs.MenuSlider.toggleMenu()" type="button" class="text-sm leading-4 font-medium focus:outline-none transition ease-in-out duration-150">
                <span class="inline-flex bg-clip-text text-white">
                    <icon name="menu" class="h-5 w-5"/>
                </span>
            </button>
        </div>
        <div class="w-full">
            <div class="hidden md:flex flex-nowrap items-center justify-between gap-4 md:gap-10 px-3 my-5 w-auto h-auto">
                <inertia-link href="/">
                    <img src="/static/images/passportgroup.png" class="h-12 w-52" alt="Battoh">
                </inertia-link>
                <form @submit.prevent="searchListing()" class="flex flex-nowrap w-full">
                    <div class="h-10 w-full py-auto rounded-l category" id="category-input">
                        <multiselect
                            placeholder="Category"
                            :options="$store.state.categories"
                            track-by="slug"
                            label="name"
                            v-model="category"
                            :searchable="true"
                        >
                        </multiselect>
                    </div>
                    <input autofocus v-model="query" id="search-input" class="px-3 w-full flex-grow py-3 h-10 hover:bg-gray-30 text-gray-700 border rounded-none focus:outline-none text-sm font-medium" placeholder="Enter your search keyword here.."/>
                    <div class="h-10 w-full location" id="location-input">
                        <multiselect
                            placeholder="Location"
                            :options="$store.state.locations"
                            v-model="location"
                            :searchable="true"
                            track-by="slug"
                            label="name"
                        >
                        </multiselect>
                    </div>
                    <button id="search-btn" class="w-auto px-6 bg-theme-1 text-white cursor-pointer rounded-r" type="submit">
                        {{ $t('menu.search') }}
                    </button>
                </form>
                <div class="flex flex-row items-center gap-4">
                    <inertia-link  :href="route('listing:add')" class="menu-item">
                        <icon class="h-5 w-5" name="camera"/>
                        <span class="ml-0.5">{{ $t('menu.sell') }}</span>
                    </inertia-link>
                    <dropdown v-if="$page.props.auth" placement="bottom-end" :autoclose="false">
                        <div class="relative">
                            <span class="menu-item">
                                <icon name="chat" class="h-5 w-5"/>
                                <span class="ml-0.5">{{ $t('menu.inbox') }}</span>
                            </span>
                            <span
                                v-if="$store.state.notifications_length > 0 && $store.state.notifications[0].unread_count > 0 || $store.state.conversations_length > 0"
                                class="animate-bounce absolute -top-1 right-0 h-2 w-2 inline-flex rounded-full bg-red-500">
                            </span>
                        </div>
                        <div slot="dropdown" class="shadow-xl bg-white mt-1 rounded overflow-hidden">
                            <NotificationBox />
                        </div>
                    </dropdown>
                    <language-switcher dropDownColor="text-white"/>
                    <dropdown v-if="$page.props.auth" placement="bottom-end">
                        <span class="menu-item cursor-pointer select-none">
                            {{ $page.props.auth.username }} <icon class="ml-1" name="cheveron-down"/>
                        </span>
                        <div slot="dropdown" class="shadow-xl mt-2 bg-white rounded overflow-hidden">
                            <profile />
                        </div>
                    </dropdown>
                    <inertia-link v-if="!$page.props.auth" :href="route('login')" class="menu-item capitalize">{{ $t('menu.login') }}</inertia-link>
                    <inertia-link v-if="!$page.props.auth" :href="route('register')" class="menu-item capitalize">{{ $t('menu.register') }}</inertia-link>
                </div>
            </div>
            <div class="hidden sm:flex flex-row flex-nowrap items-center mx-3 relative justify-between" v-if="show_categories">
                <div class="relative" @mouseleave="hideChildren(index)" :key="index" v-for="(category, index) in $store.state.categories.slice(0, categoriesToDisplayPerScreenSize)">
                    <a
                        href="#"
                        @mouseenter="showChildren(index, category.id)"
                        @click="$inertia.get('/items/search', { category: category.slug })"
                        class="text-sm z-40 select-none text-white hover:text-white"
                    >
                        {{ $t(`categories.${category.slug}`) }}
                    </a>
                     <div :id="'category-'+index" :class="index === categoriesToDisplayPerScreenSize - 1 ? 'right-0' : 'left-0'" class="h-auto bg-white hidden shadow-lg z-50 rounded-b top-6 absolute pb-2 w-52">
                         <div class="border-2 border-theme-1 w-full"></div>
                          <ul class="px-3" v-if="sub_categories.length > 0">
                              <li class="py-1 hover:text-theme-1 select-none cursor-pointer flex items-center justify-between text-sm" v-for="(c, index) in sub_categories" :key="index">
                                  <a class="z-50" @click="$inertia.get('/items/search',{category: c.slug})"> {{ $t(`categories.${c.slug}`) }} </a>
                              </li>
                          </ul>
                          <div v-else class="animate-pulse px-2">
                              <div class="flex-1 space-y-2 py-1">
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200 "></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                                  <div class="h-4 bg-gray-200"></div>
                              </div>
                          </div>
                    </div>
                </div>
                <div v-if="$store.state.categories_length > 0 && categoriesToDisplayPerScreenSize !== $store.state.categories_length" class="relative" @mouseleave="hideChildren('more')" >
                    <a
                        href="#"
                        @mouseenter="showChildren('more')"
                        @click="$inertia.get('/items/search', { category: category.slug })"
                        class="text-sm select-none z-40 text-white hover:text-white"
                    >
                        {{ $t('menu.more') }}
                    </a>
                    <div id="category-more" class="h-auto bg-white hidden shadow-lg z-50 rounded-b top-6 right-0 absolute pb-2 w-52">
                        <div class="border-2 border-theme-1 w-full"></div>
                        <ul class="px-3">
                            <li class="py-2 hover:text-theme-1 select-none cursor-pointer flex items-center justify-between text-sm" v-for="(c, index) in $store.state.categories.slice(categoriesToDisplayPerScreenSize, $store.state.categories_length)" :key="index">
                                <a class="z-50" @click="$inertia.get('/items/search',{category: c.slug})"> {{ $t(`categories.${c.slug}`) }} </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Dropdown from '@/components/Dropdown';
import Profile from '@/components/dropdowns/Profile';
import Icon from "./Icon";
import MenuSlider from "./Sliders/MenuSlider";
import axios from "axios";
import NotificationBox from "./dropdowns/Notifications";
import LanguageSwitcher from "./LanguageSwitcher";

export default {
    name: "Header",
    components: {
        LanguageSwitcher,
        NotificationBox,
        MenuSlider,
        Icon,
        Dropdown,
        Profile
    },
    props: {
      show_categories: {
          type: Boolean,
          default: true
      },

    },
    data(){
        return {
            show_menu: false,
            location: null,
            locations_options: [],
            query: null,
            category: null,
            sub_categories: [],
            notification_audio: new Audio('/static/audio/notification_bell.mp3'),
            screen_width: document.body.clientWidth,
            isLoading: false
        }
    },
    computed: {
        categoriesToDisplayPerScreenSize(){
            if (this.screen_width <= 640) {
                return 3
            }
            else if (this.screen_width > 641 && this.screen_width <= 900) {
                return 4
            }
            else if (this.screen_width > 900 && this.screen_width <= 1000) {
                return 5
            }
            else if (this.screen_width > 1000 && this.screen_width <= 1100) {
                return 6
            }
            else if (this.screen_width > 1100 && this.screen_width <= 1300) {
                return 7
            }
            else if (this.screen_width > 1300) {
                return 8
            }
        },
    },
    methods: {
        toggleBottomNavigation(value) {
            $('#bottom-navigation').toggleClass('hidden')
        },
        showChildren(index, parent = null) {
            $('#category-'+index).removeClass('hidden')
            if (parent) {
                if (this.$localstorage.keyExist(`category_${parent}`)) {
                    this.sub_categories = this.$localstorage.getStorage(`category_${parent}`)
                }
                else {
                    axios.get(`${this.route('listing:categories')}?parent=${parent}`)
                    .then(res => {
                        if (res.data['categories'].length > 0) {
                            this.sub_categories = res.data['categories']
                            this.$localstorage.addStorage(`category_${parent}`, this.sub_categories)
                        }
                        else {
                            this.hideChildren(index)
                        }
                    })
                    .catch( res => this.hideChildren(index))
                }
            }
        },
        hideChildren(index) {
            $('#category-'+index).addClass('hidden')
        },
        searchListing(){
            let data = {
                category: this.category && this.category.slug ? this.category.slug : 'all'
            }

            if (this.query) data.query = this.query
            if (this.location) data.location = this.location
            this.$inertia.get(this.route('listing:search'), data)
        },

        searchLocation(query) {
             this.isLoading = true
             axios.get(this.route('listing:locations', query))
             .then(res => {
                 if (res.data['locations'].length > 0) this.locations_options = res.data['locations']
                 this.isLoading = false
            })
             .catch(err => {
                this.isLoading = false
            })
        }

    },
    created() {
        let self = this
        window.addEventListener("resize", function () {
            self.screen_width = document.documentElement.clientWidth
        })
    }
}
</script>

<style scoped>
    .menu-item {
        @apply flex items-center text-white font-bold text-sm uppercase block;
    }

    @media screen and (max-width: 971px){
        #category-input {
            @apply hidden;
        }
        #location-input {
            @apply hidden;
        }
        #search-input {
            @apply rounded-l border-l;
        }
    }
    .stop-scrolling {
        height: 100%;
        overflow: hidden;
    }

    .header-bg {
        background: rgb(1,60,75);
        background: linear-gradient(90deg, rgba(1,60,75,1) 9%, rgba(0,175,151,1) 45%, rgba(1,79,88,1) 99%);
    }

</style>