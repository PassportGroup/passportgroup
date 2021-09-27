<template>
    <div>
        <notifications position="bottom right"/>
        <notifications group="auth" position="top right"/>
        <notifications group="app" position="bottom right"/>
        <notifications group="error" position="top right"/>
    </div>
</template>
<script>
export default {
    watch: {
        "$page.flash": {
            handler() {
                if (this.$page.props.flash.error) {
                    this.$notify(
                        {
                            group: "error",
                            type: "error",
                            title: this.$t('general.error'),
                            text: this.$page.props.flash.error,
                            duration: 5000,
                        }
                    );
                } else if (this.$page.props.flash.success) {
                    this.$notify(
                        {
                            group: "app",
                            type: "success",
                            title: this.$t('general.success'),
                            text: this.$page.props.flash.success,
                            duration: 5000,
                        }
                    );
                } else if (this.$page.props.flash.warning) {
                    this.$notify(
                        {
                            group: "app",
                            type: "warning",
                            title: this.$t('general.warning'),
                            text: this.$page.props.flash.warning,
                            duration: 5000,
                        }
                    );
                } else if (this.$page.props.flash.info) {
                    this.$notify(
                        {
                            group: "app",
                            type: "info",
                            title: this.$t('general.info'),
                            text: this.$page.props.flash.info,
                            duration: 5000,
                        }
                    );
                }
            },
            deep: true
        },
    },
}
</script>
