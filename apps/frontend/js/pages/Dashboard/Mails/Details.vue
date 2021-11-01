<template>
  <div class="container p-5 my-2">
    <div class="font-medium text-gray-500 mb-1 md:mb-4">
      <div class="flex flex-wrap items-center text-xs md:text-lg justify-start gap-1">
        <inertia-link href="/" class="menu-item font-bold">{{ $t('menu.home') }} <icon name="cheveron-right" /> </inertia-link>
        <inertia-link :href="route('mails.index')" class="menu-item font-bold">All Mails <icon name="cheveron-right" /> </inertia-link>
        <span>{{ mail.threadId }}</span>
      </div>
    </div>
    <div v-if="mail">
      <div class="relative my-3 py-10 px-5 bg-gray-100 border-gray-400 focus:outline-none rounded-md bg-opacity-70 border overflow-hidden relative">
      <div :class="isApproved() ? 'bg-green-500 border-green-500' : 'bg-red-500 border-red-500'" class="px-2 py-1 text-xs absolute right-0 top-0 border-l capitalize text-white rounded-tr font-bold">
        {{ isApproved() ? 'approved' : 'not approved' }}
      </div>
      <h3 class="text-lg font-bold my-2">
        <span class="underline text-green-700">{{ getMailSubject() }}</span>
        <span class="text-gray-500 mx-2 italic text-xs">- {{ getMailDate() }}</span><br>
        <span class="mx-2 italic text-xs px-4 py-1 text-white bg-gray-400 rounded">#{{ mail.threadId }}</span>
      </h3>
      <div class="my-4" v-html="mail.snippet"/>
    </div>
    </div>
  </div>
</template>

<script>
import MainLayout from "../../../layouts/MainLayout";

export default {
  name: "MailDetails",
  layout: MainLayout,
  props: {
    mail: Object,
  },
  data() {
    return {
      //
    }
  },
  methods: {
    getMailDate() {
      return this.mail.payload['headers'].find(header => header['name'].toLowerCase() === 'date').value
    },
    getMailSubject() {
      return this.mail.payload['headers'].find(header => header['name'].toLowerCase() === 'subject').value
    },
    isApproved() {
      return this.mail.snippet.includes("approved")
    }
  }
}
</script>

<style scoped>
 .menu-item {
        @apply flex items-center justify-center gap-1 hover:text-theme-1;
    }
</style>