import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import pagination from "./pagination";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        notifications: [],
        notifications_length: 0,
    },
    mutations: {
        setNotifications(state, data) {
            if (Array.isArray(data)) {
                state.notifications = data
                state.notifications_length = data.length
            }
            else {
                state.notifications.unshift(data)
                state.notifications_length += 1
            }
        },
    },
    actions: {
        getRecentNotifications(context) {
            let notifications = []
            axios.get('/notifications/unread/')
            .then(res => {
                context.commit('setNotifications', res.data['notifications'])
            })
        },
    },
    modules: {
        pagination: pagination,
    }
})