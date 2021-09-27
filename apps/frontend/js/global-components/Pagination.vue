
<template>
  <div v-if="links.length > 2">
    <div class="flex flex-wrap items-center justify-start mt-6 -mb-1">
      <template v-for="(link, key) in links">
        <div v-if="link.url === null" :key="key" class="mr-1 mb-1 px-3 py-2 text-sm leading-4 text-gray-400 border rounded" v-html="link.label" ></div>
        <inertia-link v-else :key="key" class="mr-1 mb-1 px-3 py-2 text-sm leading-4 rounded hover:bg-white focus:border-theme-1 focus:text-theme-1" :class="!link.active ? 'bg-white border': 'bg-theme-1 text-white font-bold'" :href="link.url" v-html="link.label" />
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    links: Array,
  },
}
</script>