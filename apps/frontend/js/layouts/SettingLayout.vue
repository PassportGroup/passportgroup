<template>
    <main-layout current_menu="account">
        <div class="w-full flex flex-col gap-24 z-30 justify-between">
            <div style="background-image: url(/static/images/banner.jpg)" class="w-full z-0 bg-no-repeat bg-cover bg-center h-52 md:h-64 bg-gray-500 bg-opacity-75 justify-center flex items-center relative">
                <div class="absolute left-10 -bottom-20 border-0">
                    <div>
                        <img :src="$page.props.auth.profile_image" class="h-32 w-32 object-cover relative border-4 border-white rounded-full" :alt="$page.props.auth.username">
                        <input type="file" class="absolute hidden opacity-0 z-0" @change="updatePicture($event)" ref="profile_image">
                        <div class="absolute top-2/4 left-2/4 z-0 transform -translate-x-2/4 -translate-y-2/4">
                            <span v-if="!sending" content="change your picture" v-tippy="{ arrow : true, placement: 'bottom' }" class="focus:outline-none text-white z-10 cursor-pointer font-bold" @click="$refs.profile_image.click()">
                                <icon name="camera" class="h-6 w-6"/>
                            </span>
                            <svg v-else class="-ml-1 mr-2 h-5 w-5 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="w-full px-3 md:px-0 md:w-11/12 mx-auto mb-4 flex flex-col md:flex-row items-start justify-between gap-8 mt-24">
            <div class="w-full md:w-4/12 bg-gray-100 rounded h-auto">
                <div class="px-8">
                    <inertia-link :href="route('settings')" class="text-md my-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 0 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 0"
                    >
                        <icon name="user" class="h-6 w-6"></icon>
                        {{ $t('menu.personal-information') }}
                    </inertia-link>
                    <inertia-link :href="route('notifications.settings')" class="text-md text-gray-700 my-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 1 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 1"
                    >
                        <icon name="bell" class="h-6 w-6"></icon>
                        {{ $t('general.notifications') }}
                    </inertia-link>

                    <inertia-link :href="route('account.verification')" v-if="!$page.props.auth.verification" class="text-md text-gray-700 my-5 flex items-center gap-3 cursor-pointer text-red-500"
                         @click="menu = 2"
                    >
                        <icon name="shield-check"></icon>

                        {{ $t('menu.verify-account') }}
                    </inertia-link>

                    <inertia-link :href="route('account.change.phone')" class="text-md text-gray-700 my-5 flex items-center gap-3 cursor-pointer"
                         @click="menu = 3" :class="{'text-red-500': !$page.props.auth.verify_phone, 'text-theme-1': menu === 3 }"
                    >
                        <icon name="phone"></icon>
                        {{ !$page.props.auth.verify_phone ? $t('general.verify-phone-number') : $t('general.change-phone-number') }}
                    </inertia-link>

                    <p v-if="$page.props.auth.verification && ['approved', 'pending'].includes($page.props.auth.verification.status)" class="text-md text-gray-700 my-5 flex items-center gap-3" :class="{'text-info': ['approved', 'pending'].includes($page.props.auth.verification.status)}">
                         <icon name="badge-check"></icon>
                        {{ $page.props.auth.verification.status === 'approved' ? $t('general.id-verified') : 'ID verification in review' }}
                    </p>
                    <inertia-link v-if="$page.props.auth.verification && $page.props.auth.verification.status === 'rejected'" :href="route('account.verification')" class="text-md text-danger my-5 flex items-center gap-3"
                    >
                        <icon name="shield-check"></icon>
                        ID verification rejected
                    </inertia-link>
                </div>
                <div class="py-5 px-8 border-t border-gray-200">
                    <inertia-link :href="route('account.wallet')" class="text-md text-gray-700 mb-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 4 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 4"
                    >
                        <icon name="lock"></icon>
                        {{ $t('general.wallet') }}
                    </inertia-link>
                    <inertia-link :href="route('password.change')" class="text-md text-gray-700 mb-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 5 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 5"
                    >
                        <icon name="lock"></icon>
                        {{ $t('general.change-my-password') }}
                    </inertia-link>
                    <inertia-link :href="route('delete.account')" class="text-md text-gray-700 mt-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 6 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 6"
                    >
                        <icon name="trash"></icon>
                        {{ $t('general.delete-account') }}
                    </inertia-link>
                    <inertia-link :href="route('account.security')" class="text-md text-gray-700 mt-5 flex items-center gap-3 cursor-pointer"
                         :class="menu === 7 ? 'text-theme-1' : 'text-gray-700'"
                         @click="menu = 7"
                    >
                        <icon name="shield-check"></icon>
                        {{ $t('general.security') }}
                    </inertia-link>
                </div>
            </div>
            <div class="w-full md:w-8/12">
                <FlashMessages class="px-2 md:px-6"/>
                <slot></slot>
            </div>
        </div>
    </main-layout>
</template>

<script>
import FlashMessages from "../components/FlashMessages";
import Icon from "../components/Icon";
import MainLayout from "./MainLayout";
export default {
    name: "SettingLayout",
    props: {
        current_menu: {
            type: Number,
            default: 0
        },
    },
    components: {
        MainLayout,
        Icon,
        FlashMessages
    },
    data() {
        return {
            camera_open: false,
            facingMode: 'user',
            sending: false,
            selfie_image: null,
            error: null,
            menu: null,
        }
    },
    methods: {
        takeSelfie(){
            if ('mediaDevices' in navigator) {
                let video = document.getElementById('video')
                let self = this
                navigator.mediaDevices.enumerateDevices().then(devices => {
                    const cameras = devices.filter((device) => device.kind === 'videoinput')
                    if (cameras.length === 0) {
                      alert('No camera found on this device.')
                    }
                    else {
                        const camera = cameras[cameras.length - 1]
                        // Create stream and get video track
                        alert(self.facingMode)
                        navigator.mediaDevices.getUserMedia({
                            video: {
                                deviceId: camera.deviceId,
                                facingMode: self.facingMode,
                            }
                        }).then(stream => {
                            self.camera_open = true
                            video.srcObject = stream
                            video.play()
                            const track = stream.getVideoTracks()[0]
                            //Create image capture object and get camera capabilities
                            const imageCapture = new ImageCapture(track)
                            const photoCapabilities = imageCapture.getPhotoCapabilities().then(() => {
                                //todo: check if camera has a torch
                                /*document.getElementById("switch_torch").addEventListener('click', function(){
                                  track.applyConstraints({
                                    advanced: [{torch: false}]
                                  })
                                })*/
                                // Elements for taking the snapshot
                                let canvas = document.getElementById('canvas')
                                let video = document.getElementById('video')

                                // Trigger photo take
                                document.getElementById("take_picture").addEventListener("click", function() {
                                    canvas.setAttribute('width', 500)
                                    canvas.setAttribute('height', 500)
                                    canvas.getContext('2d').drawImage(video, 0, 0, 500, 500)
                                    self.selfie_image = canvas.toDataURL('image/png')
                                    canvas.removeAttribute('width')
                                    canvas.removeAttribute('height')
                                    self.camera_open = false
                                    stream.getTracks()[0].stop()
                                })

                                // turn off camera
                                document.getElementById("turn_off_camera").addEventListener("click", function() {
                                    self.camera_open = false
                                    stream.getTracks()[0].stop()
                                })

                                document.addEventListener('keydown', e => {
                                    if (e.keyCode === 27){
                                        self.camera_open = false
                                        stream.getTracks()[0].stop()
                                    }
                                })
                            })
                        })
                    }
                })
            }
            else {
                alert('Sorry your device do not support media devices')
            }
        },

        switchCamera() {
            this.facingMode = this.facingMode === 'user' ? 'environment' : 'user'
            this.takeSelfie()
        },

        uploadSelfie(){
            if (!this.selfie_image) {
                this.error = this.$t('general.take-selfie')
            }
            else {
                let data = new FormData
                data.append('identification_picture', this.selfie_image)
                this.$inertia.post(this.route('verify.profile'), data, {
                    onStart: () => this.sending = true,
                    onFinish: () => {
                        this.sending = false
                        this.selfie_image = null
                    }
                })
            }
        },

        updatePicture(e) {
            let file = e.target.files[0]
            let extension = file.name.split('.').reverse()[0].toLowerCase()
            const extensions = ['jpg', 'jpeg', 'png']

            if (extensions.includes(extension)) {
                 let data = {
                     picture: file,
                 }
                this.$inertia.post(this.route('settings'), data,  {
                    forceFormData: true,
                    onStart: () => this.sending = true,
                    onFinish: () => {
                        this.sending = false
                    }
                })
            }
            else {
                this.$notify(
                    {
                        group: "foo",
                        type: "error",
                        title: 'Error',
                        text: this.$t('validation.mimes', {attribute: this.$t('validation.attributes.image'), values: extensions.join(", ")})
                    }, 5000
                )
            }

        }

    },
    mounted() {
        this.menu = this.current_menu
    }
}
</script>

<style scoped>

</style>