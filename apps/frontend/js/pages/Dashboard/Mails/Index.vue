<template>
  <div class="container p-5 my-2 text-white">
     <form @submit.prevent="filterEmails()" class="flex items-center text-center justify-center mt-10 flex-nowrap w-full">
       <input v-model="query" type="text" placeholder="Search Emails" class="text-white w-72 bg-gray-700 py-2 px-4 ltr:border-r rtl:border-l border-gray-500 outline-none focus:outline-none">
       <div class="bg-gray-700 px-4">
         <date-range-picker
             class="max-w-md"
            ref="mailPicker"
            :showWeekNumbers="true"
            v-model="mailRange">
           <!--    header slot-->
            <div slot="header" slot-scope="header" class="slot">
              <h3>Select Date range</h3> <span v-if="header.in_selection"> - in selection</span>
            </div>
            <!--    input slot (new slot syntax)-->
            <template slot="input" slot-scope="picker" class="w-full w-72 flex text-gray-200 bg-gray-700 rounded-r">
              <span class="text-gray-200 text-italic" v-if="picker.startDate === null && picker.endDate === null">
                Select date range
              </span>
              <span v-else>
                {{ picker.startDate | date }} - {{ picker.endDate | date }}
              </span>
            </template>
            <!--    date slot-->
            <template #date="data">
              <span class="small text-gray-900">{{ data.date | dateCell }}</span>
            </template>
            <!--    ranges (new slot syntax) -->
            <template #ranges="ranges">
              <div class="ranges text-gray-900">
                <ul>
                  <li v-for="(range, name) in ranges.ranges" :key="name" @click="ranges.clickRange(range)">
                    <b>{{ name }}</b> <small class="text-muted">{{ range[0].toDateString() }} -
                    {{ range[1].toDateString() }}</small>
                  </li>
                </ul>
              </div>
            </template>
            <!--    footer slot-->
            <div slot="footer" slot-scope="data" class="slot py-2 px-4">
              <div>
                <b class="text-black">Chosen Dates </b> {{ data.rangeText }}
              </div>
              <div style="margin-left: auto">
                <a @click="data.clickApply" v-if="!data.in_selection" class="cursor-pointer px-4 text-xs rounded py-1 bg-gray-800">Apply</a>
              </div>
            </div>
       </date-range-picker>
       </div>
       <button class="w-auto flex inline-flex justify-center items-center text-center mx-4 py-2 px-6 bg-yellow-800 text-white cursor-pointer rounded" type="submit">
         <icon name="filter" class="w-4 h-4 mx-2"/>
         Filter Mails
       </button>
     </form>
    <div class="flex flex-col items-center justify-center m-auto my-8">
       <div class="px-0 md:px-4 mt-0 mb-4 w-full md:w-4/5">
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
    <div v-if="showProcessingButton" class="fixed bottom-16 right-8">
      <button
          @click="processMails"
          :disabled="processingMails"
          class="p-0 w-16 h-16 bg-yellow-700 rounded-full hover:bg-yellow-800 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
            <icon v-if="!processingMails" name="send" class="w-8 h-8 inline-block text-center"/>
            <passport-loader v-else :loading="processingMails"/>
      </button>
    </div>
  </div>
</template>

<script>
import MainLayout from "../../../layouts/MainLayout"
import DateRangePicker from 'vue2-daterange-picker'
import EmptyList from "../../../global-components/EmptyList"
import PassportLoader from "../../../global-components/PassportLoader"
import MailListing from "../../../global-components/MailListing"
import MailItem from "../../../global-components/MailItem"

export default {
  name: "MailIndex",
  layout: MainLayout,
  components: {
    DateRangePicker,
    EmptyList,
    PassportLoader,
    MailListing,
    MailItem,
  },
  props: {
    mails: Array,
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
          query: '',
          processingMails: false,
          is_filtering: false,
          isAllSelected: false,
          showProcessingButton: false,
          mailRange: {
            startDate: null,
            endDate: null
          },
          selected_mails: []
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
      this.is_filtering = true
      this.$inertia.get(this.route('mails.index'), {
        q: this.query,
        start_date: this.mailRange.startDate,
        end_date: this.mailRange.endDate,
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