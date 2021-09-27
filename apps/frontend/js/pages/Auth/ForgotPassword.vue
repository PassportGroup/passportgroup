<template>
    <div class="w-full px-4">
        <h1 class="text-xl font-bold text-left md:text-2xl font-medium text-gray-700 mb-6 md:mt-8"> {{ $t('form.forgot-password') }}</h1>
        <form @submit.prevent="submit">
            <alert icon="info" :message="$t('general.reset-by-email-help-msg')"/>
            <label for="email" class="form-label">{{ $t('form.email') }}</label>
                <input type="email" id="email" required autocomplete="off" v-model="email" :placeholder="$t('form.email-placeholder')" class="input"/>
                <div class="pt-5 flex justify-end">
                    <passport-button :loading="isLoading" bg="w-full bg-gradient-to-r from-theme-1 to-theme-2 hover:from-theme-2 hover:to-theme-1 text-center" type="submit">
                        {{ $t('form.request-password-reset') }}
                    </passport-button>
                </div>
        </form>
    </div>
</template>

<script>

import AuthLayout from "../../layouts/AuthLayout"

export default {
    name: "ForgotPassword",
    layout: AuthLayout,
    props: {
        errors: Object
    },
    data() {
        return {
            email: null,
            isLoading: false,
        }
    },
    methods: {
        submit() {
          this.$inertia.post(
              this.route('password.forgot'),
              { email: this.email },
              {
                forceFormData: true,
                onStart: () => this.isLoading = true,
                onFinish: () => {
                  this.isLoading = false
                }
              }
          )
        }
    },

}
</script>

<style scoped>

</style>
