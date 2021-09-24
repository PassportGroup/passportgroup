<template>
    <div class="my-2 focus:outline-none rounded-md bg-white border overflow-hidden relative">
        <inertia-link class="z-10" :href="'#'">
            <div v-if="listing.status.toLowerCase() === 'sold'" class="flex flex-shrink-0 items-center justify-center bg-white bg-opacity-30 h-16 w-16 rounded-full absolute top-1/3 left-2/4 transform -translate-x-2/4 -translate-y-1/3">
                <h1 class="font-bold text-white text-sm uppercase ">{{ $t('general.sold') }}</h1>
            </div>
        </inertia-link>
    </div>
</template>

<script>
import Icon from "./Icon";
import axios from "axios";

export default {
    name: "ListingItem",
    components: { Icon },
    props: {
        listing: Object
    },
    methods: {
        saveListing() {
          console.log('about to save this email')
            if (this.$page.props.auth === null){
                let _next = window.location.pathname
                this.$inertia.get(`/login/?next=${_next}`)
            }
            else {
                let data = new FormData
                data.append('slug', this.listing.slug)
                axios.post(this.route('listing:wishlist'), data)
                .then(response => {
                    this.listing.in_wishlist = !this.listing.in_wishlist
                    this.$notify({
                        group: "foo",
                        type: "success",
                        title: this.$t('general.success'),
                        text: response.data.message
                    })
                })
                .catch( error => {
                    console.log('something went wrong')
                })
            }
        }
    }
}
</script>

<style scoped>

</style>
=======
    }
}
</script>
>>>>>>> Stashed changes
