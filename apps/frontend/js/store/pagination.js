import axios from "axios";

export default {
    state: {
        results: [],
        url: '',
        page: 1,
        is_complete: false,
        filterPage: {
            period: 'all',
            genre: 'all',
        },
        pageSize: 10,
        infiniteId: +new Date()
    },
    getters: {
        results: state => {
            return state.results
        },
        is_complete: state => {
            return state.is_complete
        },
        infiniteId: state => {
            return state.infiniteId
        },
        url: state => {
            return state.url
        },
    },
    mutations: {
        INIT_REQUEST(state, payload) {
            state.url = payload.url
            state.results = []
            state.page = 1
            state.infiniteId += 1
            if (payload.filter) {
                state.filterPage = payload.filter
            }
        },
        CHANGE_PAGE_SIZE(state, page_size) {
            state.pageSize = page_size
        },

        CHANGE_FILTER_PARAMETER(state, filter) {
            state.filterPage = filter
        },

        AJAX_REQUEST(state, $state) {
            let parameters =  { page: state.page, page_size: state.pageSize}
            axios.get(state.url, {
                params: {...parameters, ...state.filterPage}
            }).then(res => {
                let data = res.data['listings']
                if (data !== 0) {
                    state.results = [...state.results, ...data]
                }
                if (data.length < state.pageSize) {
                    $state.complete()
                    state.is_complete = true
                } else {
                    state.page += 1
                    $state.loaded()
                }
            }).catch(error => {
                console.log(error)
            })
        }
    },
    actions: {
        GET_DATA({commit}, $state) {
            commit('AJAX_REQUEST', $state)
        },
        INIT_DATA({commit}, payload) {
            commit('INIT_REQUEST', payload)
        },
        SET_PAGE_SIZE({commit}, page_size) {
            commit('CHANGE_PAGE_SIZE', page_size)
        },
    }
}