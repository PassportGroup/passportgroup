<template>
      <div>
          <h1 class="text-2xl font-medium text-center text-gray-700 mb-2 md:mt-8">{{ $t('general.password-reset') }}</h1>
          <form class="px-6 py-5" @submit.prevent="submit">
              <div class="mt-4">
                  <label for="password" class="form-label">{{ $t('form.new-password') }}</label>
                  <input
                      type="password"
                      id="password"
                      v-model="form.password"
                      class="input"
                      :class="{'input-error': $v.form.password.$error}"
                  />
                  <div class="form-error" v-if="!$v.form.password.required && $v.form.password.$error">
                      {{ $t('validation.required', {attribute: $t('validation.attributes.new-password')}) }}
                  </div>
                  <div class="form-error" v-if="!$v.form.password.minLength && $v.form.password.$error">
                      {{ $t('validation.min.string', {attribute: $t('validation.attributes.new-password'), min: $v.form.password.$params.minLength.min}) }}
                  </div>
              </div>

              <div class="mt-4">
                  <label for="repeatPassword" class="form-label">{{ $t('form.confirm-password') }}</label>
                  <input
                      type="password"
                      id="repeatPassword"
                      v-model="form.repeatPassword"
                      class="input"
                      :class="{'input-error': $v.form.password.$error}"
                  />
                  <div class="form-error" v-if="!$v.form.repeatPassword.sameAs && $v.form.repeatPassword.$error">
                      {{ $t('validation.same', {attribute: $t('validation.attributes.new-password'), other: $t('validation.attributes.confirm-password')}) }}
                  </div>
              </div>
              <passport-button :loading="sending" class="mt-4 w-full font-bold" type="submit" bg="bg-gradient-to-r from-theme-1 to-theme-2 hover:from-theme-2 hover:to-theme-1">{{ $t('form.reset') }}</passport-button>
          </form>
      </div>
</template>

<script>
import AuthLayout from "../../layouts/AuthLayout"
import { required, minLength, sameAs } from 'vuelidate/lib/validators'

export default {
    name: 'ResetPassword',
    layout: AuthLayout,
    metaInfo() {
        return {title: this.$t('general.reset-password')}
    },
    props: {
        email: String,
    },
    data() {
        return {
            sending: false,
            form: {
                password: null,
                repeatPassword: null
            }
        }
    },
    validations: {
        form: {
            password: {
                required,
                minLength: minLength(6)
            },
            repeatPassword: {
                sameAsPassword: sameAs(function() {
                    return this.form.password;
                })
            }
        }
    },
    methods: {
        submit(){
            this.$v.$touch()
            if (this.$v.$invalid) {
                this.submitStatus = 'ERROR'
            } else {
                this.$inertia.post(this.route('password.set'),
                    {
                        password: this.form.password,
                        email: this.email
                    },
                    {
                        forceFormData: true,
                        onStart:() => this.sending = true,
                    }
                )
            }
        }
    }
}
</script>