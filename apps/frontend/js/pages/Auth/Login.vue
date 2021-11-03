<template>
    <div class="mb-4">
        <h1 class="text-xl font-bold text-center md:text-2xl font-medium text-gray-700 mb-2 md:mt-8">{{ $t('general.login-title') }}</h1>
        <form class="px-6 py-5" @submit.prevent="submit">
            <div class="mt-6">
               <label for="email" class="form-label">{{ $t('form.email') }}</label>
                <input type="password" id="email" autocomplete="off" v-model="form.email" :placeholder="$t('form.email-placeholder')" class="input pb-8"/>
                <div class="form-error" v-if="$page.props.errors && $page.props.errors.email">{{ $page.props.errors.email[0].message }}</div>
            </div>
            <div class="mt-6">
                <label for="password" class="form-label">{{ $t('form.password') }}</label>
                <input type="password" id="password" autocomplete="off" v-model="form.password" :placeholder="$t('form.password-placeholder')" class="input pb-8"/>
                <div class="form-error" v-if="$page.props.errors && $page.props.errors.password">{{ $page.props.errors.password[0].message }}</div>
            </div>
            <label class="my-4 select-none flex items-center" for="remember">
                <input id="remember" v-model="form.remember" class="mr-1 input input--switch" type="checkbox">
                <span class="text-xs text-gray-700">{{ $t('form.remember-me') }}</span>
            </label>
            <p class="text-sm text-gray-700 mb-4 font-bold text-right cursor-pointer">{{ $t('form.forgot-password') }} <inertia-link :href="route('password.forgot')" class="text-theme-1">{{ $t('general.click-here') }}</inertia-link></p>
            <passport-button class="w-full capitalize font-bold" :loading="sending" type="submit" bg="bg-gradient-to-r from-theme-1 to-theme-2 hover:from-theme-2 hover:to-theme-1">{{ $t('form.login') }}</passport-button>
        </form>
    </div>
    
</template>

<script>
import AuthLayout from "../../layouts/AuthLayout"

export default {
    name: 'Login',
    layout: AuthLayout,
    metaInfo() {
        return {title: this.$t('menu.login')}
    },
    props: {
        flash: Object,
        errors: Object,
    },
    data() {
        return {
            sending: false,
            url: new URL(window.location.href),
            form: {
                phone_number: null,
                password: null,
                remember: null,
                next: null
            }
        }
    },
    methods: {
        submit(){

            this.form.post(this.route('login'), this.form , {
                onStart: () => {
                    this.sending = true
                },
                onFinish: () => {
                    this.sending = false
                }
            })
        }
    },
    mounted() {
        this.form.next = this.url.searchParams.get('next')
    }
}
</script>

<style scoped>

</style>