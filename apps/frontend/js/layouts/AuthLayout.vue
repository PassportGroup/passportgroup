<template>
    <div>
        <VTNotifications />
        <div class="w-full mx-auto max-w-8xl overflow-hidden h-screen bg-white flex flex-row justify-items-center lg:border lg:border-r lg:border-gray-100 lg:shadow-lg">
            <div class="w-full lg:w-5/12 hidden lg:block bg-blue-100 h-screen relative shadow-lg">
                <div class="flex items-center justify-center my-10">
                    <inertia-link href="/" class="mt-19">
                        <img src="/static/images/passportgroup.png" class="h-28"/>
                    </inertia-link>
                </div>
                <div class="absolute transform top-2/4 left-2/4 -translate-x-2/4 -translate-y-2/4">
                    <img src="/static/images/passportgroup.svg" alt="">
                </div>
            </div>
            <div class="w-full h-full lg:w-7/12 mx-auto">
                <div style="height: 10vh" class="w-full px-4 sticky bg-gradient-to-r from-theme-1 to-theme-2 left-0 top-0 z-40 flex flex-row items-center justify-between">
                    <p v-if="page === 'login'" class="text-center text-sm text-theme-2 font-bold">{{ $t('form.have-account-yet') }} <inertia-link :href="route('login')" class="text-white">{{ $t('menu.login') }}</inertia-link> </p>
                    <p v-else class="text-center text-sm font-bold text-theme-2">{{ $t('form.no-account-yet') }} <inertia-link :href="route('register')" class="text-white">{{ $t('menu.register') }}</inertia-link> </p>
                    <language-switcher />
                </div>
                <div style="height: 90vh" class="flex items-center justify-center my-auto">
                    <div style="max-height: 90vh" class="w-full overflow-y-auto overflow-scroll-container">
                        <div class="w-full md:w-9/12 mx-auto pb-10">
                            <div class="flex block lg:hidden items-center justify-center mb-4">
                                <inertia-link href="/">
                                    <img src="/static/images/passportgroup.png" class="h-24 mt-14"/>
                                </inertia-link>
                            </div>
                            <slot />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import VTNotifications from "../components/VTNotifications";
    import Icon from "../components/Icon";
    import LanguageSwitcher from "../components/LanguageSwitcher";
    export default {
        name: "AuthLayout",
        components: {
            LanguageSwitcher,
            Icon,
            VTNotifications
        },
        props: {
            page: {
                type: String,
                default: 'register'
            }
        },
        mounted() {

        }
    }
</script>

<style scoped>
    .max-w-8xl {
        max-width: 90rem;
    }
</style>