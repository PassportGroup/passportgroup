<template>
  <div class="my-2 mx-5">
    <BreadCrumb :page-routes="pagesRoutes" :active-link="activeLink"/>
    <div class="m-10">
      <div class="space-y-4 pb-10">
				<div>
					<div class="relative bg-white p-10 rounded-xl">
            <span
                :class="$i18n.locale === 'he' ? '-right-6' : '-left-6'"
                class="absolute bg-green-500 w-14 h-14 flex items-center justify-center font-bold text-green-50 rounded-full -top-6">
              <icon name="play"  v-tippy="{ arrow : true,  animation : 'perspective'}"
                :content="'Run task'" class="h-6 w-6 mx-2 cursor-pointer text-white focus:outline-none"/>
            </span>
						<div
                :class="$i18n.locale === 'he' ? 'left-0' : 'right-0'"
                class="absolute top-0 flex p-4 space-x-2">
                <button
                    @click="deleteTask"
                    class="inline-flex items-center bg-red-600 font-semibold text-white py-2 px-4 rounded hover:bg-red-700 focus:outline-none focus:ring shadow-lg intro-x hover:shadow-none transition-all duration-300 m-2">
                  {{ $t('general.delete_task') }}
                  <icon name="thrash" class="w-5 h-5 mx-1"/>
                </button>
						</div>
            <p class="text-xl underline text-gray-700 font-bold my-2">Update Passport status</p>
            <div class="flex flex-wrap">
              <span class="px-3 py-1 bg-green-200 hover:bg-green-300 rounded-full text-xs font-semibold text-green-600">
                Running - 14/12/2021 6:19pm
              </span>
            </div>
            <p class="my-4 text-sm text-gray-600 leading-relaxed">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Eum impedit ipsam nam quam! Ab accusamus aperiam distinctio doloribus, praesentium quasi reprehenderit soluta unde?</p>
            <hr/>
            <div class="flex flex-col space-y-4">
              <div class="overflow-x-auto mt-6">
                <table class="table-auto border-collapse w-full">
                  <tbody class="text-sm font-normal text-gray-700">
                    <tr class="hover:bg-gray-100 border-b border-gray-200 py-10">
            <td class="px-4 py-4">Intro to CSS</td>
            <td class="px-4 py-4">Adam</td>
            <td class="px-4 py-4">858</td>
          </tr>
                  </tbody>
                </table>
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
  name: "DashboardDetailsIndex",
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
    deleteTask() {
      this.$notify({
        title: i18n.t('general.coming_soon'),
        text: i18n.t('general.coming_soon_text'),
        type: 'warning'
      })
    }
  }
}
</script>
