<template>
    <SliderLayout ref="sliderLayout" @is-open="open">
        <div class="h-full">
            <header id="content-header" :class="$page.props.auth ? 'h-56' : 'h-32'" class="py-auto flex flex-col gap-4 px-4 bg-gradient-to-r from-theme-1 to-theme-2">
                <div class="flex flex-row items-center mt-2 -mx-2 justify-between">
                    <language-switcher position="left-0"/>
                    <button @click="toggleMenu" aria-label="Close Menu" class="h-6 w-6 flex items-center justify-center rounded-full text-white bg-black bg-opacity-60 outline-none focus:outline-none">
                        <Icon name="close" class="h-4 w-4"/>
                    </button>
                </div>
                <div v-if="$page.props.auth">
                    <div class="flex flex-col items-center gap-2 justify-center">
                        <inertia-link :href="route('user.profile', $page.props.auth.username)">
                            <img class="h-24 w-24 object-cover cursor-pointer rounded-full" :src="$page.props.auth.profile_image" :alt="$page.props.auth.username">
                        </inertia-link>
                        <inertia-link :href="route('user.profile', $page.props.auth.username)">
                            <p class="text-white font-bold text-md flex items-center">@{{ $page.props.auth.username }}
                                <span class="text-white" v-if="$page.props.auth.is_verified">
                                    <icon name="badge-check"/>
                                </span>
                            </p>
                        </inertia-link>
                    </div>
                    <div class="flex flex-row flex-wrap items-center justify-between mt-4 mb-2">
                        <inertia-link  :href="route('listing:add')" class="menu-item">
                            <icon class="p-1 h-6 w-6" name="camera"/>
                            {{ $t('menu.sell') }}
                        </inertia-link>
                        <inertia-link  :href="route('listing:wishlist')" class="menu-item">
                            <icon class="p-1 h-6 w-6" name="heart-solid"/>
                            {{ $t('menu.wishlist') }}
                        </inertia-link>
                        <inertia-link :href="route('conversations')" class="menu-item">
                             <icon class="p-1 h-5 w-5" name="chat"/> {{ $t('menu.inbox') }}
                        </inertia-link>
                    </div>
                </div>
                <div v-else class="flex flex-row flex-wrap items-center justify-between gap-3 my-2">
                    <inertia-link :href="route('login')" class="menu-item">
                        <icon name="login"/> {{ $t('menu.login') }}
                    </inertia-link>
                    <inertia-link :href="route('register')" class="menu-item">
                        <icon name="user-add" class="h-6 w-6"/> {{ $t('menu.register') }}
                    </inertia-link>
                    <inertia-link :href="route('listing:add')" class="menu-item">
                        <icon name="camera" class="h-6 w-6"/> {{ $t('menu.sell') }}
                    </inertia-link>
                </div>
            </header>
            <div id="content-body" class="overflow-y-auto overflow-scroll-container">
                <div class="h-full w-full relative" v-if="$store.state.categories_with_children.length > 0">
                    <div class="mx-3">
                        <search-input />
                    </div>
                    <div class="border-b"></div>
                    <div class="pb-5">
                        <p class="text-sm px-3 mt-2 text-gray-700 font-semibold leading-5 uppercase">
                            {{ $t('general.top-categories') }}
                        </p>
                        <ul class="px-3">
                            <li @click="categories_children(index, category)" class="py-2 hover:text-theme-1 text-gray-700 select-none flex items-center justify-between cursor-pointer text-sm" v-for="(category, index) in $store.state.categories_with_children" :key="index">
                                <span> {{ category.name }} </span>
                                <icon v-if="category.children.length > 0" class="h-3 w-3" name="cheveron-right" />
                            </li>
                        </ul>
                    </div>
                </div>
                <div v-else class="p-4 h-full">
                      <div class="animate-pulse flex space-y-4 space-x-4" v-for="i in 3" :key="i">
                            <div class="rounded-full bg-gray-200 h-12 w-12"></div>
                            <div class="flex-1 space-y-4 py-1">
                                <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                                <div class="space-y-2">
                                    <div class="h-4 bg-gray-200 rounded"></div>
                                    <div class="h-4 bg-gray-200 rounded w-5/6"></div>
                                </div>
                            </div>
                      </div>
                </div>
            </div>
            <div v-if="$page.props.auth" id="content-footer" class="h-12 border-t bg-white z-50 px-4 w-full flex items-center sticky bottom-0 left-0">
                 <inertia-link :href="route('logout')" class="flex items-center justify-center text-gray-700 gap-1 text-xs font-bold uppercase block">
                    <icon class="p-1" name="power-off" /> {{ $t('menu.logout') }}
                </inertia-link>
            </div>
            <div :class="sub_categories.length !== 0 ? 'translate-x-0' : 'translate-x-full'" class="bg-white w-full absolute h-screen transform overflow-y-auto overflow-scroll-container top-0 bottom-0 ease-in-out duration-500 z-50">
                <header class="border-b h-16 py-auto flex px-3 bg-gray-50">
                    <div class="flex flex-row items-center mt-2">
                        <button @click="sub_categories = [] " aria-label="Close Categories" class="h-6 flex items-center outline-none focus:outline-none">
                            <Icon name="cheveron-left"/> <span class="ml-2 text-sm">{{ current_category }}</span>
                        </button>
                    </div>
                </header>
                <div>
                    <ul class="px-3">
                        <li @click="$inertia.get('/items/search', { category: category.slug })" class="py-2 hover:text-theme-1 text-gray-700 select-none flex items-center justify-between cursor-pointer text-sm" v-for="(category, index) in sub_categories" :key="index">
                            {{ $t(`categories.${category.slug}`) }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </SliderLayout>
</template>

<script>
import Icon from "../Icon"
import LanguageSwitcher from "../LanguageSwitcher";
import SliderLayout from "./SliderLayout";

export default {
    name: "MenuSlider",
    components: {
        SliderLayout,
        LanguageSwitcher,
        Icon,
    },
    data() {
        return {
            sub_categories: [],
            current_category: null,
            search: null,
            isOpen: false
        }
    },
    watch: {
        isOpen: function(value) {
            if (value) {
                setTimeout(() => {
                    if (this.$page.props.auth) {
                        $('#content-body').css('height', `calc(100vh - ${$('#content-header').height() + $('#content-footer').height()}px)`)
                    }
                    else {
                        $('#content-body').css('height', `calc(100vh - ${$('#content-header').height()}px)`)
                    }

                }, 1000)
            }
        },


    },
    methods: {
        toggleMenu() {
            this.$refs.sliderLayout.toggleMenu()
        },
        open(value) {
            this.isOpen = value
        },
        categories_children(index, category){
            this.current_category = this.$t(`categories.${category.slug}`)
             if (category.children.length > 0) {
                this.sub_categories = category.children
            }
            else {
                this.toggleMenu()
                this.$inertia.get('/items/search', { category: category.slug })
            }
        },
    },

}
</script>

<style scoped>
     .menu-item {
        @apply flex items-center justify-center text-white gap-1 text-xs font-bold uppercase block;
    }
</style>