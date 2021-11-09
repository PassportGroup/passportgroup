<template>
    <div
        :class="selected ? 'border-green-800 bg-green-800' : 'bg-gray-100 border-gray-400'"
        class="relative my-3 py-10 px-5 focus:outline-none rounded-md bg-opacity-70 border overflow-hidden relative">
      <div
          :class="mail.is_approved ? 'bg-green-500 border-green-500' : 'bg-red-500 border-red-500'"
          class="px-2 py-1 text-xs absolute right-0 top-0 border-l capitalize text-white rounded-tr font-bold"
      >{{ mail.is_approved ? 'approved' : 'not approved' }}</div>
      <h3 class="text-lg font-bold my-2">
        <inertia-link :href="route('dashboard.mails.detail', mail.thread_id)" :class="selected ? 'text-orange-700' : 'text-green-700'" class="underline">{{ mail.subject}}</inertia-link>
        <span class="text-gray-500 mx-2 italic text-xs">- 12 Sep 2021</span><br>
        <span class="mx-2 italic text-xs px-4 py-1 text-white bg-gray-400 rounded">#{{ mail.thread_id }}</span>
      </h3>
      <div class="my-4" v-html="mail.snippet"/>
      <div class="absolute right-0 bottom-1 px-4 py-2 mx-2 mt-12">
        <div class="flex flex-row items-center ltr:justify-end rtl:justify-start text-center">
           <inertia-link :href="route('dashboard.mails.detail', mail.thread_id)" v-tippy="{ arrow : true,  animation : 'perspective'}"
               content='View Mail' class="w-6 h-6 p-1 rounded-full mr-2 transform text-gray-800 bg-gray-300 hover:bg-gray-400 hover:scale-110">
            <icon name="eye" class="cursor-pointer" />
          </inertia-link>
          <template v-if="mail.is_approved">
             <div v-if="!selected" v-on:click="toggleAction('select', mail)" v-tippy="{ arrow : true,  animation : 'perspective'}"
               content='Select Mail' class="w-7 h-7 p-1 items-center text-center justify-center rounded-full mr-2 transform border border-green-700 text-gray-800 hover:text-white bg-gray-300 hover:bg-green-600 hover:scale-110">
              <icon name="check" class="cursor-pointer w-4 h-4" />
            </div>
            <div v-else v-tippy="{ arrow : true,  animation : 'perspective'}"
                 content='Cancel/Decline Mail' v-on:click="toggleAction('select', mail)" class="w-7 h-7 p-1 rounded-full mr-2 transform text-white bg-red-500 hover:bg-red-900 hover:scale-110">
              <icon name="trash" class="cursor-pointer" />
            </div>
          </template>
        </div>
      </div>
    </div>
</template>

<script>

export default {
    name: "MailItem",
    props: {
      mail: Object,
      selected: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      truthValue(value) {
      return Boolean(value)
    },
      toggleAction(action, thread_id) {
        switch (action) {
          case "select":
            this.$emit('update', this.mail)
            break
          case "delete":
            this.$notify({
              type: 'error',
              title: 'Delete Email',
              text: 'Are you sure you want to delete'
            })
            break
          default:
            // viewing the mail
            this.$notify({
              type: 'info',
              title: 'Coming Soon',
              text: 'We are currently working on this feature. You will be notified.'
            })
        }
      }
    }
}
</script>

<style scoped>

</style>
