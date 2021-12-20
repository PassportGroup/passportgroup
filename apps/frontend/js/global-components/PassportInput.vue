<template>
    <div :class="error ? 'has-error' : '' " class="mt-2 capitalize">
        <label v-if="label" :for="id">
            <span v-html="label"/>
            <span v-if="required" class="text-red-600 text-sm lowercase font-semibold">*</span><br>
        </label>
        <div v-if="type === 'text-area'" class="relative">
          <textarea
              class="mt-1 py-2.5 px-3 focus:ring-green-500 focus:border-green-500 block w-full border border-gray-300 rounded"
              :class="customClass"
              :disabled="disabled"
              :readonly="read_only"
              @input="$emit('input', $event.target.value)"
              :id="id" :cols="cols" :rows="rows" v-bind="$attrs" :minlength="minLength" :placeholder="placeholder" :required="required">{{ value }}</textarea>
        </div>
        <div v-else class="relative">
            <input :id="id" ref="input"
                   :disabled="disabled"
                   :readonly="read_only"
                   v-bind="$attrs" :minlength="minLength" :placeholder="placeholder" :required="required" :type="this.isPassword ? this.togglePassword ? 'password' : 'text' : this.type"
                   :value="value" class="mt-1 py-2.5 px-3 focus:ring-green-500 focus:border-green-500 block w-full border border-gray-300 rounded" :class="customClass" @input="$emit('input', $event.target.value)"/>
            <div v-if="isPassword" class="absolute right-1 bottom-4 px-3 cursor-pointer"
                 @click="changeType(togglePassword)">
                <icon :name="togglePassword ? 'eye' : 'eye-off'" class="w-5 h-5" />
            </div>
        </div>
        <div v-if="description" v-html="description" class="text-xs lowercase p-1"/>
        <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </div>
</template>

<script>
export default {
    name: "PassportInput",
    inheritAttrs: false,
    props: {
        id: {
            type: String,
            default() {
                return `text-input-${this._uid}`
            },
        },
        customClass: {
            type: String,
            default: 'dark:bg-dark-2 dark:border dark:border-white px-3 py-2'
        },
        type: {
            type: String,
            default: 'text',
        },
        cols: {
          type: Number,
          default: 30
        },
        rows: {
          type: Number,
          default: 7
        },
        value: String,
        label: String,
        description: String,
        error: String,
        required: Boolean,
        minLength: String,
        placeholder: String,
        disabled: {
          type: Boolean,
          default: false
        },
        read_only: {
          type: Boolean,
          default: false
        },
    },
    data() {
        return {
            isPassword: this.type === "password",
            togglePassword: true
        }
    },
    methods: {
        focus() {
            this.$refs.input.focus()
        },
        select() {
            this.$refs.input.select()
        },
        changeType() {
            this.togglePassword = !this.togglePassword
        }
    }
}
</script>
