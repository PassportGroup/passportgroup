import Vue from "vue"
import VueMeta from "vue-meta"
import axios from "axios"
import PortalVue from 'portal-vue'
import { createInertiaApp, Link } from '@inertiajs/inertia-vue'
import { InertiaProgress } from "@inertiajs/progress"
import VueTelInput from 'vue-tel-input'
import Vuelidate from 'vuelidate'
import VueTippy, { TippyComponent } from "vue-tippy"
import VuePusher from 'vue-pusher'
import VueSweetalert2 from 'vue-sweetalert2'
import Notifications from "vue-notification"
import './utils/modal'
import Store from './utils/store'
import store from "./store/index"
import i18n from "./i18n"
const moment = require('moment')
require('moment/locale/es')
import InfiniteLoading from 'vue-infinite-loading';
import Multiselect from 'vue-multiselect'

Vue.config.productionTip = false
Vue.use(InfiniteLoading, { /* options */ });
Vue.use(VueSweetalert2)
Vue.use(VueTippy)
Vue.component("tippy", TippyComponent)
Vue.use(require('vue-moment'), { moment })
Vue.prototype.$moment.locale(i18n.locale)
Vue.use(VueMeta)
Vue.use(Notifications)
Vue.use(PortalVue)
Vue.use(VueTelInput)
Vue.use(Vuelidate)


Vue.use(VuePusher, {
  api_key: process.env.MIX_PUSHER_APP_KEY,
  options: {
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    authTransport: 'jsonp',
  }
})
VuePusher.logToConsole = (process.env.MIX_APP_ENV !== "production")

InertiaProgress.init({delay: 250, color: '#fa8f05'})

let customRoute = (...args) => {
  return '/' + i18n.locale.toString().toLowerCase() + window.reverseUrl(...args)
}
Vue.mixin({ methods: { route: customRoute } })

Vue.prototype.$localstorage = new Store()
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFToken"

Vue.component('multiselect', Multiselect)
Vue.component("inertia-link", Link)

createInertiaApp({
    resolve: name => require(`./pages/${name}`),
    setup({ el, app, props }) {
        new Vue({
            store,
            i18n,
            metaInfo: {
                titleTemplate: title => title ? `${title} | ${process.env.MIX_APP_NAME}` : process.env.MIX_APP_NAME,
                htmlAttrs: {
                    lang: 'en',}
                },
            render: h => h(app, props),
        }).$mount(el)
    },
})