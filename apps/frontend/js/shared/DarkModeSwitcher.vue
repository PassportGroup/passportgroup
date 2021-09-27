<template>
    <div
        id="passportgroup_theme_toggle"
        v-on:click="toggle"
        class="cursor-pointer flex items-center justify-center rounded-full w-8 h-8 p-1">
        <Icon name="light-bulb" class="flex items-center"/>
    </div>
</template>

<script>
import {mapGetters} from "vuex";
import i18n from "../i18n";

export default {
    name: "DarkModeSwitcher",
    computed: {
        ...mapGetters({theme: "getTheme"}),
    },
    mounted() {
        this.toggleThemeBackground(this.$store.getters.getTheme)
    },
    watch: {
        theme(newTheme) {
            this.toggleThemeBackground(newTheme)
        },
    },
    methods: {
        toggle() {
            // todo remove
            // this.$store.dispatch("toggleTheme");
            this.$notify({
                title: i18n.t('general.coming_soon'),
                text: i18n.t('general.coming_soon_text'),
                type: 'warning'
            })
        },
        toggleThemeBackground(theme) {
            theme === "light" ?
                cash("#passportgroup_theme_toggle").removeClass("bg-yellow-300 bg-opacity-80") :
                cash("#passportgroup_theme_toggle").addClass("bg-yellow-300 bg-opacity-80")
        }
    },
}
</script>

<style scoped>

</style>
