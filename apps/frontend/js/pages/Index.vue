<template>
    <main-layout menu="home" :categories="main_categories">
        <listing-list ref="listingList" class="px-2 md:px-8 mt-2" :listings="results" :is_full_screen="true"/>
        <infinite-loading  @infinite="getInitialData" :identifier="infiniteId">
            <div slot="spinner" class="my-20">
                <passport-loader :loading="true"/>
            </div>
            <div slot="no-more"></div>
            <div slot="no-results">
                 <empty-list v-if="results.length === 0" :content="$t('general.no-mails')"/>
            </div>
        </infinite-loading>
    </main-layout>
</template>

<script>
import MainLayout from '@/layouts/MainLayout';
import EmptyList from "../components/EmptyList";
import PassportLoader from "../components/PassportLoader";
import ListingList from "../components/ListingList";
import {mapGetters} from "vuex";

export default {
    name: 'Index',
    metaInfo() {
        return {title: this.$t('general.home')}
    },
    props: {
        listings: Array,
        main_categories: Array,
        flash: Object,
    },
    computed: {
        ...mapGetters([
            'infiniteId',
            'results',
            'is_complete',
        ])
    },
    components: {
      PassportLoader,
        EmptyList,
        ListingList,
        MainLayout,
    },
    data() {
        return {
        }
    },
    methods: {
        getInitialData($state) {
            this.$store.dispatch('GET_DATA', $state)
        },
    },
    mounted() {
        this.$store.dispatch('INIT_DATA', {url: '/'})
        document.addEventListener('scroll', () => {
            this.$redrawVueMasonry('listings')
        })
    }
}
</script>

