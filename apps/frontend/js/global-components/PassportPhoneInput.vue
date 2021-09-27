<template>
    <div>
        <label>{{ $t('general.phone-number')}}<span class="text-theme-6 text-xs mb-2">*{{$t('forms.required')}}</span></label>
        <vue-tel-input
            v-model="phone"
            @validate="onValidate"
            v-bind="bindProps"/>
    </div>
</template>

<script>

import { VueTelInput } from 'vue-tel-input'
import i18n from "../i18n";

export default {
    name: "PassportPhoneInput",
    components: {
        VueTelInput
    },
    props: {
        id: String,
        placeholder: {
            type: String,
            default: ''
        },
        default: String,
        required: {
            type: Boolean,
            default: false
        },
        readonly: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            phone: this.default,
            bindProps: {
                mode: "international",
                autocomplete: "on",
                defaultCountry: "CM",
                required: true,
                onlyCountries: ['CM'],
                validCharactersOnly: true,
                inputOptions: {
                    placeholder: this.placeholder,
                    required: this.required,
                    readonly: this.readonly,
                    styleClasses: "w-full px-4 text-base bg-gray-100 dark:bg-dark-2 border dark:border-dark-2 border-transparent rounded-lg focus:outline-none"
                },
                styleClasses: "w-full block outline-none py-1 mt-2 dark:bg-dark-2 border dark:border-dark-2 focus:outline-none border-none ring-transparent text-base bg-gray-100"
            },
        }
    },
    methods: {
        onValidate(phoneObject) {
            this.$emit("update", phoneObject)
        },
    }
}
</script>

<style src="vue-tel-input/dist/vue-tel-input.css"></style>

