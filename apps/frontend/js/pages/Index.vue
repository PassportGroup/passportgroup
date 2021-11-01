<template>
    <div>
      <section class="text-gray-600 body-font">
        <div class="mx-20 px-2 py-12 flex flex-wrap items-center">
          <div class="w-full md:w-3/5 p-5">
             <span class="text-xl font-semibold flex-shrink-0 text-white bg-green-800 rounded px-3 py-2 sm:text-base lg:text-sm xl:text-base">
               #emailProcessingMadeSimple
             </span>
             <h2 class="my-4 text-4xl font-extrabold leading-10 tracking-tight text-gray-900 sm:leading-none sm:text-6xl lg:text-5xl xl:text-6xl">
               Mail Processing <br class="hidden md:block"/>
               <span class="text-green-700 md:whitespace-pre">      Passport Group</span>
             </h2>
            <h1 class="title-font font-medium text-2xl mt-2">Process large amounts of emails while keeping track of client files</h1>
            <p class="leading-relaxed mt-8">
              Our tool permits you to process any pdf and tool, making sure you keep track of files from drive simultaneously all together with the blue docs.
            </p>
          </div>
          <div class="w-full md:w-2/5 bg-green-100 bg-opacity-40 border rounded-lg p-10 flex flex-col md:ml-auto w-full mt-10 md:mt-0">
            <h2 class="text-xl font-medium title-font mb-6">Sign In</h2>
            <p class="leading-relaxed ">Access your account and get started with processing documents and drive</p>
            <form @submit.prevent="submit">
               <div class="relative mt-5">
                 <label for="email" class="text-base font-semibold leading-7">Email <span class="text-red-700 text-lg">*</span></label>
                 <input type="email" id="email" v-model="form.email" name="email"  placeholder="Account unique identifier" class="w-full px-4 py-2 mt-2 text-base bg-gray-50 transition duration-500 ease-in-out transform border border-gray-300 rounded-lg focus:outline-none focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2">
                 <div class="form-error" v-if="form.errors.email">{{ form.errors.email }}</div>
               </div>
              <div class="relative mt-4">
                <label for="password" class="text-base font-semibold leading-7">Password <span class="text-red-700 text-lg">*</span></label>
                <div class="relative">
                  <input :type="togglePassword ? 'password' : 'text'" required id="password" v-model="form.password" name="password" placeholder="Account password" class="w-full bg-gray-50 px-4 py-2 mt-2 text-base transition duration-500 ease-in-out transform border border-gray-300 rounded-lg focus:outline-none focus:shadow-outline focus:ring-2 ring-offset-current ring-offset-2">
                  <div class="absolute right-1 bottom-2.5 px-2 cursor-pointer"
                       @click="() => this.togglePassword = !togglePassword">
                    <icon :name="togglePassword ? 'eye' : 'eye-off'" class="w-5 h-5" />
                  </div>
                </div>
                <div class="form-error" v-if="form.errors.password">{{ form.errors.password }}</div>
              </div>
                <passport-button
                    :type="'submit'"
                    :loading="form.processing"
                    class="w-full mt-10 text-white bg-gray-800 border-0 py-2 px-4 focus:outline-none hover:bg-green-600 rounded text-lg">
                  Access Portal
                </passport-button>
            </form>
            <p class="text-xs text-gray-500 mt-3">Are you a passport group personnel, login in to start hiking</p>
          </div>
        </div>
      </section>
    </div>
</template>

<script>
import PassportButton from "../global-components/PassportButton"
import MainLayout from "../layouts/MainLayout"

export default {
    name: 'Index',
    layout: MainLayout,
    metaInfo() {
        return {title: this.$t('general.home')}
    },
    props: {
      listings: Array,
      flash: Object,
      errors: Object,
    },
  components: {
      PassportButton
  },
    data() {
        return {
          togglePassword: true,
          form: this.$inertia.form({
            email: null,
            password: null,
            remember: null,
            next: null
          })
        }
    },
    methods: {
      submit() {
            this.form.post(this.route('login'))
        }
    },
}
</script>

