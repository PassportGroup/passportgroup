<template>
    <div class="relative z-50">
        <button
            type="button"
            :class="getLanguageColor"
            class="flex items-center border-none outline-none focus:outline-none focus:border-transparent"
            @click="toggleVisibility"
            @keydown.space.exact.prevent="toggleVisibility"
            @keydown.esc.exact="hideDropdown"
            @keydown.shift.tab="hideDropdown"
            @keydown.up.exact.prevent="startArrowKeys"
            @keydown.down.exact.prevent="startArrowKeys"
        >
            <img :src="`/static/flags/${$i18n.locale}.svg`" alt="flag" class="fill-current h-4 w-4 ltr:mr-1 rtl:ml-1">
            <span class="ml-1 text-sm font-bold whitespace-no-wrap">{{ $i18n.locale.toUpperCase() }}</span>
            <icon name="cheveron-down" class="mx-1.5"/>
        </button>
        <transition name="dropdown-fade">
            <ul v-on-clickaway="hideDropdown" v-if="isVisible" ref="dropdown"
                class="absolute z-50 font-normal bg-white shadow overflow-hidden rounded w-36 border mt-2 py-1" :class="position">
                <li v-for="locale in locales" :key="locale.code">
                    <a href="#"
                       @click.prevent="setLocale(locale.code)"
                       ref="account"
                       class="flex items-center px-4 py-2 text-sm whitespace-no-wrap hover:bg-gray-100 dark:hover:bg-dark-3"
                       @keydown.up.exact.prevent=""
                       @keydown.tab.exact="focusNext(false)"
                       @keydown.down.exact.prevent="focusNext(true)"
                       @keydown.esc.exact="hideDropdown">
                        <img :alt="locale.code" :src="`/static/flags/${locale.code}.svg`" class="h-4 w-4">
                        <span class="ltr:ml-2 rtl:mr-2 capitalize">{{locale.name}}</span>
                    </a>
                </li>
            </ul>
        </transition>
    </div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway';
import { getSupportedLocales } from "@/utils/i18n/supported-locales"
import {loadLocaleMessagesAsync} from "@/i18n";
import {setDocumentDirectionPerLocale, setDocumentLang, setDocumentTitle} from "@/utils/i18n/document";
export default {
    name: "LanguageSwitcher",
    mixins: [ clickaway ],
    props: {
        dropDownColor: null,
        position: {
            type: String,
            default: 'right-0'
        }
    },
    data() {
        return {
            isVisible: false,
            focusedIndex: 0,
            locales: getSupportedLocales(),
        }
    },
    computed: {
        getLanguageColor() {
            return this.dropDownColor !== null ? this.dropDownColor : "text-black";
        },
    },
    methods: {
        toggleVisibility() {
            this.isVisible = !this.isVisible;
        },
        hideDropdown() {
            this.isVisible = false;
            this.focusedIndex = 0
        },
        startArrowKeys() {
            if (this.isVisible) {
                this.$refs.account.focus()
                this.$refs.dropdown.children[0].children[0].focus()
            }
        },
        focusPrevious(isArrowKey) {
            this.focusedIndex = this.focusedIndex - 1;
            if (isArrowKey) {
                this.focusItem()
            }
        },
        focusNext(isArrowKey) {
            this.focusedIndex = this.focusedIndex + 1;
            if (isArrowKey) {
                this.focusItem()
            }
        },
        focusItem() {
            this.$refs.dropdown.children[this.focusedIndex].children[0].focus()
        },
        setLocale(locale) {
            let data = new FormData
            data.append('locale', locale)
            data.append('next', window.location.pathname.replace(this.$i18n.locale.toLowerCase()+"/", ''))
            this.$inertia.post(this.route('locale.set'), data)
            loadLocaleMessagesAsync(locale).then(() => {
                setDocumentLang(locale)
                setDocumentDirectionPerLocale(locale)
                setDocumentTitle(this.$t('general.document-title'))
                this.$moment.locale(locale)
                this.$i18n.locale = locale
            })

            this.hideDropdown()
        }
    }
}
</script>
