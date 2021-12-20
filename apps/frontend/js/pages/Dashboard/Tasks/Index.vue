<template>
  <div class="my-2 mx-5">
    <BreadCrumb :page-routes="pagesRoutes" :active-link="activeLink"/>
    <div class="m-10">
      <div v-for="task in tasks" class="space-y-4 pb-5 mb-5">
				<div>
					<div class="relative bg-white p-10 rounded-xl">
            <inertia-link :href="route('dashboard.tasks.detail', task.slug)"
                class="text-xl underline text-gray-700 font-bold my-2">{{ task.name }}</inertia-link>
            <div class="flex flex-wrap mt-2">
              <span class="px-3 py-1 cursor-pointer bg-green-200 hover:bg-green-300 rounded-full text-xs font-semibold text-green-600">
                Running - {{ task.start_date | moment('ddd DD/M/YYYY hh:mm A') }} - <span class="text-yellow-700">{{ task.end_date | moment('ddd DD/M/YYYY hh:mm A') }}</span>
              </span>
            </div>
            <div v-html="task.excerpt" class="mt-2 text-sm text-gray-600 leading-relaxed"/>
						<span
                :class="$i18n.locale === 'he' ? '-right-6' : '-left-6'"
                class="absolute bg-green-500 w-14 h-14 flex items-center justify-center font-bold text-green-50 rounded-full -top-6">
              <icon name="play"  v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="'Run task'" class="h-6 w-6 mx-2 cursor-pointer text-white focus:outline-none"/>
            </span>
						<div
                :class="$i18n.locale === 'he' ? 'left-0' : 'right-0'"
                class="absolute top-0 flex p-4 space-x-2">
               <inertia-link :href="route('dashboard.tasks.detail', task.slug)"
                  v-tippy="{ arrow : true,  animation : 'perspective'}" :content="'View task'">
                <icon name="eye"  class="h-6 w-6 cursor-pointer mx-2 text-gray-600"/>
              </inertia-link>
              <icon name="refresh"  v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="'Restart task'" class="h-6 w-6 mx-2 cursor-pointer text-green-600"/>
              <inertia-link :href="route('dashboard.tasks.update', task.slug)"
                  v-tippy="{ arrow : true,  animation : 'perspective'}" :content="'Edit task'">
                <icon name="pencil-alt"   class="h-6 w-6 cursor-pointer mx-2 text-yellow-700"/>
              </inertia-link>
						</div>
            <div class="border-t mt-4 flex flex-row justify-between">
              <div class="rounded p-4">
                <div class="flex flex-wrap">
                  <span v-for="parameter in task.extra_parameters" class="px-3 py-1 mx-1 bg-yellow-200 hover:bg-yellow-300 rounded text-xs font-semibold text-yellow-600">
                    <span v-if="parameter.records">Records: {{ parameter.records }}</span>
                    <span v-else>{{ parameter }}</span>
                  </span>
                </div>
              </div>
              <div class="p-4 italic text-gray-500 text-sm">
                Last Updated: {{ task.updated_at | moment('DD/M/YYYY hh:mm A') }}
              </div>
            </div>
					</div>
				</div>
			</div>
    </div>
  </div>
</template>

<script>
import DashboardLayout from "../../../layouts/DashboardLayout";
import i18n from "../../../i18n";

export default {
  name: "DashboardTasksIndex",
  layout: DashboardLayout,
  props: {
    tasks: Array,
  },
  data() {
        return {
           pagesRoutes: [
                {
                    title : i18n.t('menu.dashboard'),
                    link : this.route('dashboard.index')
                },
            ],
          activeLink: i18n.t('menu.tasks'),
        }
    },
  methods: {
    //
  }
}
</script>
