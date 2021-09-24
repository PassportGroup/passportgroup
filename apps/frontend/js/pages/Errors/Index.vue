<template>
   <main-layout>
        <div class="container mx-auto px-8 absolute top-1/4 md:top-1/2 left-1/4 md:left-1/2 transform -translate-x-1/4 -translate-y-1/4 md:-translate-x-2/4 md:-translate-y-2/4">
            <div class="flex flex-col items-center justify-center">
                <h1 class="text-4xl text-gray-900 font-bold my-3">{{ status }}</h1>
                <p class="text-2xl text-gray-800 font-light my-3 uppercase text-center">{{ description }}</p>
                <a href="/" class="py-2 min-w-min px-6 text-white bg-theme-1 rounded mt-3 uppercase shadow-xl font-bold">
                    {{ $t('general.home') }}
                </a>
            </div>
        </div>
    </main-layout>
</template>

<script>
import MainLayout from "../../layouts/MainLayout";
export default {
    name: "500",
    metaInfo() {
       return {
           title: this.title
       }
    },
    props: {
        status: Number
    },
    computed: {
        title() {
            return {
                503: this.$t('errors.503-title'),
                500: this.$t('errors.500-title'),
                404: this.$t('errors.404-title'),
                403: this.$t('errors.403-title'),
            }[this.status]
        },
        description() {
            return {
                503: this.$t('errors.503-content'),
                500: this.$t('errors.500-content'),
                404: this.$t('errors.404-content'),
                403: this.$t('errors.403-content'),
            }[this.status]
        },
    },
    components: {
        MainLayout
    }
}
</script>

<style scoped>

</style>