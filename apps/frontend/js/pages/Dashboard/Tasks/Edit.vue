<template>
  <div class="my-2 mx-5">
    <BreadCrumb :page-routes="pagesRoutes" :active-link="activeLink"/>
    <div class="m-10">
      <div class="space-y-4 pb-10">
        <form @submit.prevent="updateTask" class="relative bg-white p-10 rounded-xl">
          <div class="space-y-4">
                <div>
                  <h3 class="text-xl leading-6 font-medium text-theme-1">
                    {{ task.name }}
                  </h3>
                  <p class="mt-1 text-sm text-skin-base font-normal">
                     Update information for this task/job by telling it when to run and also customized dates and time.
                  </p>
                </div>
                <div class="space-y-6 sm:space-y-5">
                  <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:pt-2">
                      <label for="name" class="block text-lg font-bold text-skin-inverted-muted sm:mt-px sm:pt-2">
                        Name
                      </label>
                    <div class="sm:col-span-2 relative">
                     <passport-input id="name" v-model="taskForm.name" required/>
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:pt-2">
                      <label for="cron_expression" class="block text-lg font-bold text-skin-inverted-muted sm:mt-px sm:pt-2">
                        Cron Expression
                      </label>
                    <div class="sm:col-span-2 relative">
                     <passport-input id="cron_expression" v-model="taskForm.cron_expression" placeholder="0 0 12 * * ?" required/>
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:pt-2">
                      <label for="start_date" class="block text-lg font-bold text-skin-inverted-muted sm:mt-px sm:pt-2">
                        Start Date
                      </label>
                    <div class="sm:col-span-2 relative">
                      <date-picker
                          :model-config="dateModelConfig"
                          :min-date="start_date"
                          title-position="left"
                          :locale="$i18n.locale"
                          v-model="start_date"
                          :timezone="'Asia/Jerusalem'"
                          mode="dateTime"
                          :minute-increment="5"
                      />
                    </div>
                  </div>
                  <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:items-start sm:pt-2">
                      <label for="end_date" class="block text-lg font-bold text-skin-inverted-muted sm:mt-px sm:pt-2">
                        End Date
                      </label>
                    <div class="sm:col-span-2 relative">
                     <date-picker
                          :model-config="dateModelConfig"
                          :min-date="end_date"
                          title-position="left"
                          :locale="$i18n.locale"
                          v-model="end_date"
                          :timezone="'Asia/Jerusalem'"
                          mode="dateTime"
                          :minute-increment="5"
                      />
                    </div>
                  </div>
                </div>
              </div>
            <div class="flex justify-end mt-5">
              <button
                  type="submit"
                  class="inline-flex items-center bg-yellow-600 font-semibold text-white py-2 px-4 rounded hover:bg-yellow-700 focus:outline-none focus:ring shadow-lg intro-x hover:shadow-none transition-all duration-300 m-2">
                  {{ $t('general.update_task') }}
                  <icon name="pencil-alt" class="w-5 h-5 mx-1"/>
                </button>
            </div>
					</form>
			</div>
    </div>
  </div>
</template>

<script>
import DashboardLayout from "../../../layouts/DashboardLayout";
import i18n from "../../../i18n";
import PassportInput from "../../../global-components/PassportInput";
import DatePicker from "v-calendar/lib/components/date-picker.umd"

export default {
  name: "DashboardDetailsIndex",
  layout: DashboardLayout,
  props: {
    task: Object,
  },
  components: {
    PassportInput,
    DatePicker
  },
  validations() {
        return {
            taskForm: {
                name: { required },
                cron_expression: { required },
                start_date: { required },
                end_date: { required },
            },
        }
    },
  data() {
        return {
           pagesRoutes: [
                {
                    title : i18n.t('menu.dashboard'),
                    link : this.route('dashboard.index')
                },
               {
                    title : i18n.t('menu.tasks'),
                    link : this.route('dashboard.tasks.index')
               },
               {
                    title : this.task.name,
                    link : this.route('dashboard.tasks.detail', this.task.slug)
               },
            ],
          activeLink: i18n.t('general.update_task'),
          taskForm: this.$inertia.form({
            name: null,
            description: null,
          }),
          start_date: new Date(),
          end_date: new Date(),
          dateModelConfig: {
              type: 'string',
              mask: 'YYYY-MM-DD HH:mm',
          },
        }
    },
  methods: {
    updateTask() {
      this.$notify({
        title: i18n.t('general.coming_soon'),
        text: i18n.t('general.coming_soon_text'),
        type: 'warning'
      })
    }
  }
}
</script>
