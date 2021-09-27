import axios from "axios";

export default {
    state: {
        notifications: [],
        notifications_length: 0,
    },
    getters: {

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
            }).catch(error => {
                console.log(error)
            })
        },
    }
}