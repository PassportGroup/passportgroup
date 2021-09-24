<template>
    <div>
        <div class="px-4 relative w-full h-full">
            <div class="w-full">
                <h1 class="font-bold text-gray-700 py-2 text-sm">{{ $t('general.categories') }}</h1>
                <span class="font-medium text-gray-700 pl-1 select-none py-1 text-sm block w-full cursor-pointer"
                    v-for="(category, index) in categories.slice(0, categoriesToDisplay)"
                    :key="index"
                    @click="filterByCategory(category.slug)"
                >
                    {{ $t(`categories.${category.slug}`) }}
                    <span class="italic text-xs text-gray-500">({{category.total_listings}})</span>
                </span>
                <div class="mt-2 mb-4">
                    <p v-if="categories.length > 8" @click="show_more = !show_more" class="font-medium m-0 text-sm cursor-pointer text-gray-700">
                        <span class="flex items-center justify-start gap-0" v-if="!show_more"><icon name="plus"/>{{ $t('general.show-more') }}</span>
                        <span class="flex items-center justify-start gap-1" v-else><icon name="minus"/>{{ $t('general.show-less') }}</span>
                    </p>
                </div>
            </div>
            <hr />
            <div class="w-full my-3">
                <div class="flex items-center mb-4 justify-between">
                    <h1 class="font-bold text-md">{{ $t('general.filters') }}</h1>
                    <span @click="clearFilter" v-if="canClearFilter" class="text-sm cursor-pointer font-medium text-theme-1">
                        {{ $t('general.clear-filters') }}
                    </span>
                </div>
                <div>
                    <h1 class="text-sm font-bold">{{ $t('general.price-range') }}</h1>
                     <div class="grid grid-cols-7 gap-1 items-center pb-3 pt-4">
                         <input
                             type="text" v-model="filter.min_price"
                             class="px-1 py-1 border focus:outline-none border-gray-200 h-9 rounded text-center text-sm col-span-2"
                             step="0.01"
                             placeholder="Min"
                             :title="$t('general.min-price')"
                         />
                         <div class="text-gray-600 text-center">{{ $t('general.to') }}</div>
                         <input
                             type="text" v-model="filter.max_price"
                             class="px-1 py-1 border focus:outline-none border-gray-200 h-9 rounded text-center text-sm col-span-2"
                             step="0.01"
                             placeholder="Max"
                             :title="$t('general.max-price')"
                         />
                         <button @click="filterByPriceRange" class="px-2 py-1 h-9 focus:outline-none hover:bg-theme-1 hover:text-white rounded border border-theme-1 bg-white text-theme-1 font-bold w-10 col-span-2">
                             {{ $t('general.go') }}
                         </button>
                    </div>
                </div>
                <hr />
                <div class="mt-3">
                    <h1 class="text-sm font-bold capitalize">{{ $t('general.condition') }}</h1>
                    <div class="mt-2">
                        <span class="form-label flex items-center gap-2">
                             <input
                                 type="checkbox"
                                 @change="filterByCondition"
                                 v-model="filter.condition"
                                 value="brand new"
                             />
                             {{ $t('general.brand-new') }}
                        </span>
                        <span class="form-label flex items-center gap-2">
                             <input
                                 type="checkbox"
                                 v-model="filter.condition"
                                 @change="filterByCondition"
                                 value="clean"
                             />
                            {{ $t('general.clean-card') }}
                        </span>
                        <span class="form-label flex items-center gap-2">
                             <input
                                 type="checkbox"
                                 v-model="filter.condition"
                                 @change="filterByCondition"
                                 value="fairly used"
                             />
                            {{ $t('general.fairly-used-card') }}
                        </span>
                         <span class="form-label flex items-center gap-2">
                             <input
                                 type="checkbox"
                                 class="text-theme-1"
                                 v-model="filter.condition"
                                 @change="filterByCondition"
                                 value="dirty"
                             />
                             {{ $t('general.dirty-card') }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Icon from "./Icon";
    export default {
        name: 'CustomFilter',
        components: {
            Icon
        },
        props: {
            categories: Array,
        },
        data() {
            return {
                show_more: false,
                url: new URL(window.location.href),
                filter: {
                    condition: [],
                    min_price: null,
                    max_price: null,
                }
            }
        },
        computed: {
            categoriesToDisplay(){
                return this.show_more ? this.categories.length : 8
            },
        },
        methods: {
            canClearFilter(){
                return this.filter.min_price || this.filter.max_price || this.filter.condition.length > 0
            },
            filterByPriceRange() {
                this.url.searchParams.set('min_price', this.filter.min_price)
                this.url.searchParams.set('max_price', this.filter.max_price)
                let new_url = String(this.url).split(window.location.origin).reverse()[0]
                this.$inertia.visit(new_url, {
                    method: 'get',
                    replace: false,
                    preserveState: true,
                    preserveScroll: true,
                    onStart: () => {
                        this.$emit('is-filtering', true)
                    },
                    onFinish:() => {
                        this.$emit('is-filtering', false)
                    },
                })
            },

            filterByCondition() {
                if (this.filter.condition.length > 0) {
                    this.url.searchParams.set('condition', this.filter.condition.join(','))
                }
                else {
                     this.url.searchParams.delete('condition')
                }

                let new_url = String(this.url).split(window.location.origin).reverse()[0]
                this.$inertia.visit(new_url, {
                    method: 'get',
                    replace: false,
                    preserveState: true,
                    preserveScroll: true,
                    onStart: () => {
                        this.$emit('is-filtering', true)
                    },
                    onFinish:() => {
                        this.$emit('is-filtering', false)
                    },
                })
            },

            filterByCategory(category) {
                this.url.searchParams.set('category', category)

                let new_url = String(this.url).split(window.location.origin).reverse()[0]
                this.$inertia.visit(new_url, {
                    method: 'get',
                    replace: false,
                    preserveState: true,
                    preserveScroll: true,
                    onStart: () => {
                        this.$emit('is-filtering', true)
                    },
                    onFinish:() => {
                        this.$emit('is-filtering', false)
                    },
                })
            },

            clearFilter() {
                this.$inertia.get(this.route('listing:search'))
            }
        }
    }
</script>

<style scoped>
    .form-label{
        @apply text-sm block font-medium text-gray-700;
    }
    


</style>