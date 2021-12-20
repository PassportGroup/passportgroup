<template>
  <div class="my-2 mx-5">
    <BreadCrumb :page-routes="pagesRoutes" :active-link="activeLink"/>
     <form @submit.prevent="filterEmails()" class="flex items-center text-center justify-center mt-10 flex-nowrap w-full">
       <div class="bg-gray-100 shadow:md px-4 w-3/5">
          <litepie-datepicker
             :class="'mx-4 z-9999'"
             placeholder="Enter dates"
             separator=" to "
             :formatter="mailDateFormat"
             :i18n="$i18n.locale"
             v-model="mailRange"/>
          <div v-if="$v.mailRange.$error" class="text-red-600 text-center justify-center pl-4 font-bold mt-1 text-xs">
           <span v-if="!$v.mailRange.required">Please choose dates for mail processing</span>
         </div>
       </div>
       <button class="w-auto flex inline-flex justify-center items-center text-center mx-4 py-2 px-6 bg-yellow-800 text-white cursor-pointer rounded" type="submit">
         <icon name="filter" class="w-4 h-4 mx-2"/>
         {{ $t('general.filter') }} {{ $t('menu.mails') }}
       </button>
     </form>
    <div class="flex flex-col items-center justify-center m-auto my-8">
       <div class="px-0 md:px-4 mt-0 mb-4 w-full">
         <div v-if="mails.length > 0">
           <div v-if="!is_filtering">
             <div class="w-full">
               <div class="flex flex-row justify-end text-xs my-4 space-x-2">
                 <button type="button" :class="isAllSelected ? 'bg-red-700' : 'bg-green-700'" @click="selectAllApproved" class="text-center items-center justify-center font-bold cursor-pointer ml-2 rounded px-2 py-1 text-white">
                   <span>{{ isAllSelected ? 'Clear all' : 'Select All'}}</span>
                 </button>
               </div>
                  <div v-for="mail in mails">
                    <mail-item
                        :mail="mail"
                        @update="onSelect"
                        :selected="selected_mails.includes(mail)"/>
                  </div>
              </div>
           </div>
           <div v-else class="h-full flex items-center justify-center">
             <passport-loader :loading="is_filtering"/>
           </div>
         </div>
         <div v-else>
           <empty-list :content="$t('general.item-not-found', {for: query && query !== 'all' ? `${$t('general.for')} “${query }”.` : $t('general.matching-your-research') })"/>
         </div>
       </div>
    </div>
    <div v-if="showProcessingButton" class="fixed bottom-8 right-5 z-999">
      <button
          v-tippy="{ arrow : true,  animation : 'perspective'}"
          content='Process Mails'
          @click="processMails"
          :disabled="processingMails"
          class="p-0 w-16 h-16 bg-yellow-700 text-white rounded-full hover:bg-yellow-800 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
            <icon v-if="!processingMails" name="send" class="w-8 h-8 inline-block text-center"/>
            <passport-loader v-else :loading="processingMails"/>
      </button>
    </div>
  </div>
</template>

<script>
import DashboardLayout from "../../../layouts/DashboardLayout"
import DateRangePicker from 'vue2-daterange-picker'
import EmptyList from "../../../global-components/EmptyList"
import PassportLoader from "../../../global-components/PassportLoader"
import MailListing from "../../../global-components/MailListing"
import MailItem from "../../../global-components/MailItem"
import i18n from "../../../i18n"
import { required } from "vuelidate/lib/validators"
import LitepieDatepicker from  "vue2-litepie-datepicker"


export default {
  name: "DashboardMailIndex",
  layout: DashboardLayout,
  components: {
    DateRangePicker,
    EmptyList,
    PassportLoader,
    MailListing,
    MailItem,
    LitepieDatepicker,
  },
  props: {
    mails: Array,
  },
  validations() {
        return {
            mailRange: { required },
        }
    },
  filters: {
     dateCell (value) {
      let dt = new Date(value)
      return dt.getDate()
    },
    date (val) {
      return val ? val.toLocaleString() : ''
    }
  },
  watch: {
    'selected_mails': {
      handler(mails) {
        this.showProcessingButton = mails.length > 0;
      }
    }
  },
  data() {
        return {
          pagesRoutes: [
                {
                    title : i18n.t('menu.dashboard'),
                    link : this.route('dashboard.index')
                },
            ],
          activeLink: i18n.t('menu.mails'),
          query: '',
          processingMails: false,
          is_filtering: false,
          isAllSelected: false,
          showProcessingButton: false,
          selected_mails: [],
          mailRange: this.start_date ? {
             startDate: moment(this.start_date).format('DD MMM YYYY'),
             endDate: moment(this.end_date).format('DD MMM YYYY')
           } : [],
          mailDateFormat: {
            date: 'DD MMM YYYY',
            month: 'MMM'
          },
        }
    },
  methods: {
    onSelect(mail) {
      if (this.selected_mails.find(m => m.thread_id === mail.thread_id)) {
       let index = this.selected_mails.indexOf(mail);
       this.selected_mails.splice(index,   1);
     } else {
       this.selected_mails.push(mail);
     }
    },
    selectAllApproved() {
      this.isAllSelected = !this.isAllSelected
      if (this.isAllSelected) {
        this.selected_mails = [...this.mails.filter(m => m.is_approved === true)]
      } else {
        this.selected_mails = []
      }
    },
    filterEmails() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        this.is_filtering = false
      } else {
        this.isAllSelected = false
        this.selected_mails = []
        this.is_filtering = true
        this.$inertia.get(this.route('dashboard.mails.index'), {
          q: this.query,
          start_date: this.mailRange[0],
          end_date: this.mailRange[1],
        }, {
          replace: true,
          preserveState: true,
          preserveScroll: true,
          onStart: () => {
            this.is_filtering = true;
          },
          onFinish: () => {
            this.is_filtering = false;
          },
        })
      }
    },
    processMails() {
      let vm = this
      vm.processingMails = true
      setTimeout(function () {
        vm.processingMails = false
      }, 3000)
    }
  }
}
</script>

<style scoped>
  .slot {
    @apply bg-green-500 text-white;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
</style>