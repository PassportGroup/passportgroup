<template>
    <div class="flex flex-inline p-2 mx-auto capitalize text-xs">
        <template v-if="pageRoutes != null" v-for="pageRoute in pageRoutes">
            <div class="rounded cursor-pointer px-2 py-1 bg-gray-400 bg-opacity-30 hover:bg-gray-700 hover:text-white">
                <inertia-link :href="pageRoute.link">
                    {{ pageRoute.title }}
                </inertia-link>
            </div>
            <Icon name="arrow-narrow-right" class="flex w-6 h-4 align-middle items-center mt-1 text-theme-1"/>
        </template>
        <template v-if="activeLink != null" class="ml-1">
            <div class="rounded px-2 py-1 bg-theme-1 bg-opacity-20">
                <span class="text-theme-1">
                    {{ activeLink }}
                </span>
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        name: "Breadcrumb",
        props: {
            pageRoutes: {
                type: Array,
                required: false
            },
            activeLink: {
                type: String,
                required: true
            }
        },
    }
</script>

<style scoped>

</style>
