<template>
    <div>
        <div id="okCookie" v-if="show" class="okcBeginAnimate z-50">
            <p>{{ $t("general.cookie-msg") }}</p>
            <inertia-link id="privacy-policy" :href="route('privacy.policy')">{{ $t("general.privacy-policy") }}</inertia-link>
            <a id="accept-cookie" href="#" @click="closeCookie">Ok</a>
        </div>
    </div>
</template>

<script>
export default {
    name: "Cookie",
    data() {
        return {
            cookieComponent: null,
            show: false
        }
    },
    watch: {
        show: function(value) {
            if (value) {
                $('#bottom-navigation').addClass('hidden')
            }
            else {
                $('#bottom-navigation').removeClass('hidden')
            }
        }
    },
    methods: {
        createCookieComponent() {
            //check cookies 
            if (document.cookie) {
                let cookieString = document.cookie;
                let cookieList = cookieString.split(";");
                if (cookieList.indexOf("OKCookie=1") === -1) {
                    this.show = true
                    this.$emit('ok-cookie', true)
                }
            }
        },
  
        closeCookie(){
            let cookieExpire = new Date();
            cookieExpire.setFullYear(cookieExpire.getFullYear() + 2);
            document.cookie="OKCookie=1; expires=" + cookieExpire.toGMTString() + ";";
            $('#main-body-content').removeClass('mb-52').addClass('mb-28')
            this.show = false
        }
  
    },
    mounted() {
        this.createCookieComponent()
    }
}
</script>

<style scoped>
    #okCookie {
        background-color:#F2F2F2;
        color:#333333;
        position:fixed;
        bottom:0;
        left:0;
        width:100%;
        padding:10px;
        font-family:sans-serif;
        -moz-box-sizing: border-box;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
        border-top:1px solid #ccc;
    }

    #okCookie p {
        margin:0 0 10px 0; float:left; padding:5px 0px;
    }

    #okCookie #accept-cookie, #okCookie #privacy-policy {
        padding:5px 20px;
        float:right;
        margin-left:10px;
        text-decoration:none;
        border-radius:3px;
        color:white;
    }

    #okCookie #accept-cookie {
        background-color:#39B54A;
        text-shadow:0px 1px 1px #507F2B;
        box-shadow:inset 0px -1px 1px #507F2B;
    }

    #okCookie #accept-cookie:hover {
        background-color:#42ce55
    }

    #okCookie #privacy-policy {
        background-color:#8D9499;
        text-shadow:0px 1px 1px #63666B;
        box-shadow:inset 0px -1px 1px #63666B;
    }

    #okCookie #privacy-policy:hover {
        background-color:#a0a8ae
    }

    .okcBeginAnimate{
        -webkit-animation: myfirst 2s;
        animation: myfirst 2s;
    }

    /* Chrome, Safari, Opera */
    @-webkit-keyframes myfirst {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    /* Standard syntax */
    @keyframes myfirst {
        from {opacity: 0;}
        to {opacity: 1;}
    }

</style>