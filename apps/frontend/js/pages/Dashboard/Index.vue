<template>
    <div class="mt-2">
      <div class="grid grid-cols-1 gap-8 p-4 lg:grid-cols-2 xl:grid-cols-4">
            <a
                href="#"
                class="flex items-center justify-between p-4 -intro-y bg-white box zoom-in rounded-md dark:bg-darker">
                <div>
                    <h6 class="text-xs my-1 font-medium leading-none tracking-wider text-gray-500 uppercase dark:text-primary-light">
                        <span class="rounded px-3 py-0.5 text-xs text-green-700 bg-green-200">Mails Processed</span>
                    </h6>
                    <span class="text-xl font-semibold">{{ $h.kNumber(5600) }}</span>
                    <span class="inline-block px-2 py-px ml-2 text-xs text-green-500 bg-green-100 rounded-md">
                      +4.4%
                    </span>
                </div>
                <div><icon name="gmail" class="w-8 h-8 text-gray-300"/></div>
            </a>
            <a
                :href="'#'"
                class="flex items-center justify-between p-4 -intro-y bg-white box zoom-in rounded-md dark:bg-darker">
                <div>
                    <h6 class="text-xs my-1 font-medium leading-none tracking-wider text-gray-500 uppercase dark:text-primary-light">
                        Users
                    </h6>
                    <span class="text-xl font-semibold">{{ $h.kNumber(4) }}</span>
                    <span class="inline-block px-2 py-px ml-2 text-xs text-green-500 bg-green-100 rounded-md">
                      +3.1%
                    </span>
                </div>
                <div><icon name="users" class="w-10 h-10 text-gray-300"/></div>
            </a>
            <a
                :href="'#'"
                class="flex items-center justify-between p-4 intro-y bg-white box zoom-in rounded-md dark:bg-darker">
                <div>
                    <h6 class="text-xs my-1 font-medium leading-none tracking-wider text-gray-500 uppercase dark:text-primary-light">
                        Partners
                    </h6>
                    <span class="text-xl font-semibold">{{ $h.kNumber(50) }}</span>
                    <span class="inline-block px-2 py-px ml-2 text-xs text-green-500 bg-green-100 rounded-md">
                      +2.6%
                    </span>
                </div>
                <div><icon name="office-building" class="w-12 h-12 text-gray-300"/></div>
            </a>
        </div>
    </div>
</template>

<script>
import DashboardLayout from "../../layouts/DashboardLayout"

export default {
  name: "DashboardIndex",
  layout: DashboardLayout,
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
