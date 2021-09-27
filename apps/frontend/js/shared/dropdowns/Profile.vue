<template>
    <div class="h-auto bg-white w-64">
        <div class="absolute -top-1 right-1 arrow-up"></div>
        <div class="border-b px-4 py-6 flex flex-row items-center">
            <inertia-link class="flex-shrink-0" :href="route('user.profile', $page.props.auth.username)">
                <img class="h-16 w-16 object-cover rounded-full" :src="$page.props.auth.profile_image" alt="">
            </inertia-link>
            <div class="ml-3">
                <inertia-link :href="route('user.profile', $page.props.auth.username)">
                    <p class="text-gray-700 font-semibold text-lg" v-if="$page.props.auth.full_name">{{ $page.props.auth.full_name }}</p>
                    <p class="text-gray-700 font-semibold text-lg" v-else>{{ $page.props.auth.username}}</p>
                </inertia-link>
                <p class="text-gray-500 text-xs mt-1 capitalize">{{ $t('general.on-battoh-since') }} {{ $page.props.auth.date_joined | moment('dddd, MMMM Do YYYY') }}</p>
            </div>
        </div>
        <div class="md:h-1/2">
            <inertia-link :href="route('user.profile', $page.props.auth.username)" class="menu-item">
                <icon class="mr-3 text-theme-1 h-6 w-6" name="camera"/> {{ $t('general.manage-listings') }}
            </inertia-link>
            <inertia-link :href="route('listing:wishlist')" class="menu-item">
                <icon class="mr-3 text-theme-1" name="heart-solid" /> {{ $t('general.wishlist') }}
            </inertia-link>
            <inertia-link :href="route('conversations')" class="menu-item">
                 <icon class="mr-3 text-theme-1 h-6 w-6" name="chat"/> {{ $t('menu.inbox') }}
            </inertia-link>
            <inertia-link :href="route('user.profile', $page.props.auth.username)" class="menu-item">
                <icon class="mr-3 text-theme-1 h-6 w-6" name="user" /> {{ $t('general.my-profile') }}
            </inertia-link>
            <inertia-link :href="route('settings')" class="menu-item">
                <icon class="mr-3 text-theme-1" name="cog" /> {{ $t('general.account-settings') }}
            </inertia-link>
            <a href="/secure.portal/v2/admin" target="_blank" class="menu-item" v-if="$page.props.auth.is_admin">
                <icon class="mr-3 text-theme-1 h-6 w-6" name="user" /> {{ $t('general.dashboard') }}
            </a>
            <inertia-link :href="route('logout')" class="menu-item">
                <icon class="mr-3 text-theme-1" name="power-off" /> {{ $t('menu.logout') }}
            </inertia-link>
        </div>
    </div>
</template>

<script>
import Icon from "../Icon";
export default {
    components: {
        Icon
    }
}
</script>

<style scoped>
    .menu-item {
        @apply text-gray-700 px-4 py-4 border-b capitalize block m-0 text-sm flex flex-row items-center;
    }
    .arrow-up {
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-bottom: 15px solid white;
    }
</style>