<template>
    <div class="w-full">
        <div v-for="listing in listings">
          <listing-item :class="index === 0 ? 'mr-1' : 'ml-1'" :listing="listing"/>
        </div>
    </div>
</template>

<script>
import Icon from "./Icon";
import ListingItem from "./ListingItem";

export default {
    name: 'ListingList',
    components: {
        ListingItem,
        Icon
    },
    props: {
        listings: Array,
    },
    data() {
        return {
          //
        }
    },
    methods: {
        //
    }
}
</script>

<style scoped>

</style>