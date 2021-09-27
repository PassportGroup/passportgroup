<template>
    <div class="overflow-scroll-container">
        <FlashMessages/>
        <portal-target name="dropdown" slim />
        <Header v-if="show_header"/>
        <slot/>
        <cookie @ok-cookie="setMarginProperties"/>
        <Footer/>
    </div>
</template>
<script>
import Footer from "../shared/includes/Footer"
import Header from "../shared/includes/Header"
import FlashMessages from "../shared/helpers/FlashMessages"
import { mapGetters } from "vuex"
import Cookie from "../global-components/Cookie"
export default {
    name: 'MainLayout',
    props: {
        show_header: {
            type: Boolean,
            default: true
        },
    },
    components: {
      FlashMessages,
      Header,
      Footer,
      Cookie,
    },
    computed: {
        ...mapGetters({theme: "getTheme"}),
    },
    watch: {
        theme(newTheme, oldTheme) {
            newTheme === "light" ?
                cash("html").removeClass("dark") :
                cash("html").addClass("dark")
        },
    },
    data() {
        return {
            notification_audio: new Audio('/static/audio/notification_bell.mp3'),
        }
    },
    methods: {
        subscribeToNotifications () {
           let channel = this.$pusher.subscribe('PassportGroup.web.notifications.' + this.$page.props.auth.username)
            channel.bind('notification', data => {
                this.$store.commit('setNotifications', data)
            })
        },
       setMarginProperties(value) {
            if (value) {
                cash('#main-body-content').removeClass('mb-28').addClass('mb-52')
            }
        }
    },
    mounted() {
       if (this.$page.props.auth) {
            this.$store.dispatch('getRecentNotifications')
            this.subscribeToNotifications()
        }
    }
}
</script>