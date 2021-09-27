import Vue from "vue";
import Vuex from "vuex";
import theme from "./theme";
import pagination from "./pagination";
import notifications from "./notifications";

Vue.use(Vuex);
export default new Vuex.Store({
    state: {
        //
    },
    getters: {
        //
    },
    modules: {
        main: theme,
        pagination: pagination,
        notifications: notifications,
    }
});
