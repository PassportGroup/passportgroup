import Vue from "vue"

Vue.component("PassportPhoneInput", () => import("./PassportPhoneInput"))
Vue.component("Header", () => import("./../shared/includes/Header"))
Vue.component("Footer", () => import("./../shared/includes/Footer"))
Vue.component('Alert', () => import('./Alert'))
Vue.component('Icon', () => import('./Icon'))
Vue.component('PassportButton', (import('./PassportButton')))
Vue.component('PassportLoader', (import('./PassportLoader')))
Vue.component('EmptyList', (import('./EmptyList')))
Vue.component('MailListing', (import('./MailListing')))
Vue.component('MailItem', (import('./MailItem')))
Vue.component('Pagination', (import('./Pagination')))
Vue.component('Cookie', (import('./Cookie')))