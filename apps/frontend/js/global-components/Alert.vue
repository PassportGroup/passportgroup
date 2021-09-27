<template>
    <div class="alert flex flex-row items-center p-2 border-b-2" :class="bg">
        <icon class="flex items-center flex-shrink-0 rounded-full h-6 w-6" :name="icon" />
        <div class="ml-2">
            <div class="text-xs">
                <div v-html="message"></div>
            </div>
        </div>
    </div>
</template>

<script>
import Icon from "./Icon";
export default {
    name: "Alert",
    components: {Icon},
    props: {
        icon: {
            type: String,
            default: 'info'
        },
        type: {
            type: String,
            default: 'info'
        },
        message: String
    },
    computed: {
        bg() {
            return {
                'warning': 'bg-yellow-200 text-yellow-200',
                'success': 'bg-green-200 text-green-200',
                'error': 'bg-red-200 text-red-700',
                'info': 'bg-blue-200 text-blue-500',
            }[this.type]
        }
    },
    data() {
        return {

        }
    }
}
</script>

<style scoped>

</style>