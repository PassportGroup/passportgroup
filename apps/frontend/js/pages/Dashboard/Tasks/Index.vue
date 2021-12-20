<template>
  <div class="my-2 mx-5">
    <BreadCrumb :page-routes="pagesRoutes" :active-link="activeLink"/>
    <div class="m-10">
      <div class="space-y-4 pb-10">
				<div>
					<div class="relative bg-white p-10 rounded-xl">
            <p class="text-xl underline text-gray-700 font-bold my-2">Update Passport status</p>
            <div class="flex flex-wrap">
              <span class="px-3 py-1 bg-green-200 hover:bg-green-300 rounded-full text-xs font-semibold text-green-600">
                Running - 14/12/2021 6:19pm
              </span>
            </div>
            <p class="mt-2 text-sm text-gray-600 leading-relaxed">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eum impedit ipsam nam quam! Ab accusamus aperiam distinctio doloribus, praesentium quasi reprehenderit soluta unde?</p>
						<span
                :class="$i18n.locale === 'he' ? '-right-6' : '-left-6'"
                class="absolute bg-green-500 w-14 h-14 flex items-center justify-center font-bold text-green-50 rounded-full -top-6">
              <icon name="play"  v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="'Run task'" class="h-6 w-6 mx-2 cursor-pointer text-white focus:outline-none"/>
            </span>
						<div
                :class="$i18n.locale === 'he' ? 'left-0' : 'right-0'"
                class="absolute top-0 flex p-4 space-x-2">
               <inertia-link :href="route('dashboard.tasks.detail', 'my-task')"
                  v-tippy="{ arrow : true,  animation : 'perspective'}" :content="'View task'">
                <icon name="eye"  class="h-6 w-6 cursor-pointer mx-2 text-gray-600"/>
              </inertia-link>
              <icon name="refresh"  v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="'Restart task'" class="h-6 w-6 mx-2 cursor-pointer text-green-600"/>
              <inertia-link :href="route('dashboard.tasks.update', 'sadas')"
                  v-tippy="{ arrow : true,  animation : 'perspective'}" :content="'Edit task'">
                <icon name="pencil-alt"   class="h-6 w-6 cursor-pointer mx-2 text-yellow-700"/>
              </inertia-link>
						</div>
					</div>
				</div>
			</div>
    </div>
    <table class="table-auto">
  <thead>
    <tr>
      <th>Song</th>
      <th>Artist</th>
      <th>Year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>The Sliding Mr. Bones (Next Stop, Pottersville)</td>
      <td>Malcolm Lockyer</td>
      <td>1961</td>
    </tr>
    <tr>
      <td>Witchy Woman</td>
      <td>The Eagles</td>
      <td>1972</td>
    </tr>
    <tr>
      <td>Shining Star</td>
      <td>Earth, Wind, and Fire</td>
      <td>1975</td>
    </tr>
  </tbody>
</table>
  </div>
</template>

<script>
import DashboardLayout from "../../../layouts/DashboardLayout";
import i18n from "../../../i18n";

export default {
  name: "DashboardTasksIndex",
  layout: DashboardLayout,
  props: {
    mails: Array,
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
