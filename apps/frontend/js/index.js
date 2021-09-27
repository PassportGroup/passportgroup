import Vue from "vue"
import VueMeta from "vue-meta"
import axios from "axios"
import PortalVue from 'portal-vue'
import { createInertiaApp, Link } from '@inertiajs/inertia-vue'
import { InertiaProgress } from "@inertiajs/progress"
import VueTelInput from 'vue-tel-input'
import Vuelidate from 'vuelidate'
import VuePusher from 'vue-pusher'
import VueSweetalert2 from 'vue-sweetalert2'
import Notifications from "vue-notification"
import RolesPermissions from "./shared/helpers/RolesPermissions"
import i18n from "./i18n"
import  "./utils"
import store from "./store"
import "./global-components"
import InfiniteLoading from 'vue-infinite-loading'

window.Vue = Vue;
Vue.config.productionTip = false
Vue.use(InfiniteLoading);
Vue.use(VueSweetalert2)
Vue.use(VueMeta)
Vue.use(Notifications)
Vue.use(PortalVue)
Vue.use(VueTelInput)
Vue.use(Vuelidate)
Vue.use(VueMeta)
Vue.mixin(RolesPermissions)

Vue.use(VuePusher, {
  api_key: process.env.MIX_PUSHER_APP_KEY,
  options: {
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    authTransport: 'jsonp',
  }
})
Pusher.logToConsole = (process.env.MIX_APP_ENV !== "production");

InertiaProgress.init({delay: 250, color: '#fa8f05'})

let customRoute = (...args) => {
  return '/' + i18n.locale.toString().toLowerCase() + window.reverseUrl(...args)
}
Vue.mixin({ methods: { route: customRoute } })

axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFToken"

Vue.component("inertia-link", Link)

createInertiaApp({
    resolve: name => require(`./pages/${name}`),
    setup({ el, app, props }) {
        new Vue({
            store,
            i18n,
            metaInfo: {
                titleTemplate: title => title ? `${title} | ${process.env.MIX_APP_NAME}` : process.env.MIX_APP_NAME,
                htmlAttrs: { lang: 'en', }
                },
            render: h => h(app, props),
        }).$mount(el)
    },
})