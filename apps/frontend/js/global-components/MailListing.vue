<template>
    <div class="w-full">
        <div v-for="mail in mails">
          <mail-item :mail="mail"/>
        </div>
    </div>
</template>

<script>
import Icon from "./Icon";
import MailItem from "./MailItem";

export default {
    name: 'MailListing',
    components: {
        MailItem,
        Icon
    },
    props: {
        mails: Array,
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