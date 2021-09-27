import dayjs from "dayjs";
import axios from "axios";

export default {
    install(Vue) {
        Vue.prototype.$h = {
            cutText(text, length) {
                if (text.split(" ").length > 1) {
                    let string = text.substring(0, length);
                    let splitText = string.split(" ");
                    splitText.pop();
                    return splitText.join(" ") + "...";
                } else {
                    return text;
                }
            },
            metaData(title, description, image = window.route('index') + '/images/logo.png', url = window.location.href) {
                return {
                    title: title,
                    meta: [{
                        vmid: 'description', name: 'description', content: description
                    }],
                }
            },
            notif(data) {
                let title = data.title
                console.log(data)
                let icon = 'users';
                let bg = 'bg-theme-1';
                let thumbnail = data.sender.thumbnail
                let url = window.route('user.dashboard.notifications') + '?notify_id='
                if (title === 'new-follower') {
                    icon = 'user-add';
                    url = window.route('user.profile', data.sender.username) + '?notify_id='
                } else if (title === 'withdrawals') {
                    icon = 'bank'
                    bg = 'bg-gray-500'
                    url = window.route('user.dashboard', 'withdrawals') + '?=' + data.item.order_id + '&notify_id='
                } else if (title === 'artist-verification') {
                    icon = 'mic'
                    bg = 'bg-teal-500'
                    if (Vue.prototype.$page.props.user_roles[0] === 'admin') {
                        url = window.route('admin.artist_verifications') + '?notify_id='
                    } else {
                        url = window.route('artist.request') + '?notify_id='
                    }
                } else if (title === 'purchases') {
                    icon = 'money'
                    bg = 'bg-gray-500'
                    thumbnail = data.item.thumbnail
                    url = window.route('user.dashboard', 'sales') + '?=' + data.item.order_id + '&notify_id='
                } else if (title === 'likes') {
                    icon = 'like'
                    bg = 'bg-red-500'
                    thumbnail = data.item.thumbnail
                    url = window.route(data.item.class_type + '.show', [data.item.slug, 'likes']) + '?notify_id='
                } else if (title === 'reposts') {
                    icon = 'repost'
                    bg = 'bg-green-500'
                    thumbnail = data.item.thumbnail
                    url = window.route(data.item.class_type + '.show', [data.item.slug, 'reposts']) + '?notify_id='
                } else if (title === 'user-created') {
                    icon = 'settings'
                    if (data.item)
                        url = window.route('user.settings', data.item.username) + '?notify_id='
                } else if (title === 'comments') {
                    icon = 'chat'
                    thumbnail = data.item.thumbnail
                    url = window.route(data.item.class_type + '.show', data.item.slug) + '?notify_id='
                } else {
                    icon = data.item.class_type
                    thumbnail = data.item.thumbnail
                    url = window.route(data.item.class_type + '.show', data.item.slug) + '?notify_id='
                }
                return {'icon': icon, 'url': url, 'bg': bg, thumbnail: thumbnail}
            },
            responsiveCarousel(nberShow = 4, rows = 1, arrows = true, autoplay = false) {
                return {
                    "dots": false,
                    "arrows": arrows,
                    "focusOnSelect": false,
                    "infinite": true,
                    "pauseOnFocus": true,
                    "autoplay": autoplay,
                    "speed": 200,
                    "slidesToShow": nberShow,
                    "slidesToScroll": 1,
                    "rows": rows,
                    "touchThreshold": 3,
                    "responsive": [
                        {
                            "breakpoint": 1024,
                            "settings": {
                                "dots": false,
                                "focusOnSelect": false,
                                "pauseOnFocus": true,
                                "infinite": true,
                                "speed": 500,
                                "slidesToShow": nberShow > 2 ? 3 : 1,
                                "slidesToScroll": 1,
                                "touchThreshold": 3,
                            }
                        },
                        {
                            "breakpoint": 600,
                            "settings": {
                                "dots": false,
                                "focusOnSelect": false,
                                "pauseOnFocus": true,
                                "infinite": true,
                                "speed": 500,
                                "slidesToShow": nberShow > 2 ? 3 : 1,
                                "slidesToScroll": 1,
                                "touchThreshold": 3,
                            }
                        },
                        {
                            "breakpoint": 480,
                            "settings": {
                                "dots": false,
                                "focusOnSelect": false,
                                "pauseOnFocus": true,
                                "infinite": true,
                                "speed": 500,
                                "slidesToShow": nberShow > 2 ? 3 : 1,
                                "slidesToScroll": 1,
                                "touchThreshold": 3,
                            }
                        }
                    ]
                }
            },
            carouselSetting(nberShow = 1, rows = 1) {
                return {
                    "dots": false,
                    "infinite": true,
                    "centerMode": false,
                    "centerPadding": "20px",
                    "slidesToShow": 1,
                    "rows": rows,
                    "slidesToScroll": 1,
                    "variableWidth": true
                }
            },
            formatDate(date, format) {
                return dayjs(date).format(format);
            },
            capitalizeFirstLetter(string) {
                if (string) {
                    return string.charAt(0).toUpperCase() + string.slice(1);
                }
            },
            onlyNumber(number) {
                if (number) {
                    return number.replace(/\D/g, "");
                } else {
                    return "";
                }
            },
            notifyUser(message, title = 'Error', type = "error",) {
                Vue.prototype.$notify(
                    {
                        group: "foo",
                        type: type,
                        title: title,
                        text: message ? message : 'Please ensure to fill all the fields correctly',
                    }, 5000
                )
            },
            formatCurrency(number, separator) {
                if (number) {
                    let splitArray = number.toString().split('.')
                    let decimalPart = ''
                    if (splitArray.length > 1) {
                        number = splitArray[0]
                        decimalPart = '.' + splitArray[1]
                    }
                    let formattedNumber = number.toString().replace(/\D/g, "");
                    let rest = formattedNumber.length % 3;
                    let currency = formattedNumber.substr(0, rest);
                    let thousand = formattedNumber.substr(rest).match(/\d{3}/g);

                    if (thousand) {
                        separator = rest ? separator ? separator : "," : "";
                        currency += separator + thousand.join(",");
                    }

                    return currency + decimalPart;
                } else {
                    return "0";
                }
            },
            formatPrice(price) {
                if (!price) return ""
                return this.formatCurrency(price, ',')
            },
            timeAgo(time) {
                let date = new Date(
                    (time || "").replace(/-/g, "/").replace(/[TZ]/g, " ")
                    ),
                    diff = (new Date().getTime() - date.getTime()) / 1000,
                    dayDiff = Math.floor(diff / 86400);

                if (isNaN(dayDiff) || dayDiff < 0 || dayDiff >= 31)
                    return dayjs(time).format("MMMM DD, YYYY");

                return (
                    (dayDiff === 0 &&
                        ((diff < 60 && "just now") ||
                            (diff < 120 && "1 minute ago") ||
                            (diff < 3600 && Math.floor(diff / 60) + " minutes ago") ||
                            (diff < 7200 && "1 hour ago") ||
                            (diff < 86400 && Math.floor(diff / 3600) + " hours ago"))) ||
                    (dayDiff === 1 && "Yesterday") ||
                    (dayDiff < 7 && dayDiff + " days ago") ||
                    (dayDiff < 31 && Math.ceil(dayDiff / 7) + " weeks ago")
                );
            },
            diffTimeByNow(time) {
                let startDate = dayjs(
                    dayjs()
                        .format("YYYY-MM-DD HH:mm:ss")
                        .toString()
                );
                let endDate = dayjs(
                    dayjs(time)
                        .format("YYYY-MM-DD HH:mm:ss")
                        .toString()
                );

                let duration = dayjs.duration(endDate.diff(startDate));
                let milliseconds = Math.floor(duration.asMilliseconds());

                let days = Math.round(milliseconds / 86400000);
                let hours = Math.round((milliseconds % 86400000) / 3600000);
                let minutes = Math.round(((milliseconds % 86400000) % 3600000) / 60000);
                let seconds = Math.round(
                    (((milliseconds % 86400000) % 3600000) % 60000) / 1000
                );

                if (seconds < 30 && seconds >= 0) {
                    minutes += 1;
                }

                return {
                    days: days.toString().length < 2 ? "0" + days : days,
                    hours: hours.toString().length < 2 ? "0" + hours : hours,
                    minutes: minutes.toString().length < 2 ? "0" + minutes : minutes,
                    seconds: seconds.toString().length < 2 ? "0" + seconds : seconds
                };
            },
            isset(obj) {
                if (obj !== null && obj !== undefined) {
                    if (typeof obj === "object" || Array.isArray(obj)) {
                        return Object.keys(obj).length;
                    } else {
                        return obj.toString().length;
                    }
                }

                return false;
            },
            kNumber(num, digits = 1) {
                if (isNaN(num) || num <= 0) {
                    return isNaN(num) ? "NaN" : 0
                }
                const lookup = [
                    {value: 1, symbol: ""},
                    {value: 1e3, symbol: "k"},
                    {value: 1e6, symbol: "M"},
                    {value: 1e9, symbol: "G"},
                    {value: 1e12, symbol: "T"},
                    {value: 1e15, symbol: "P"},
                    {value: 1e18, symbol: "E"}
                ]
                const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
                var item = lookup.slice().reverse().find(function (item) {
                    return num >= item.value
                });
                return (num / item.value).toFixed(digits).replace(rx, "$1") + item.symbol
            },
            assign(obj) {
                return JSON.parse(JSON.stringify(obj));
            },
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },
            formatTime(secs) {
                let minutes = Math.floor(secs / 60) || 0;
                let seconds = Math.floor(secs - minutes * 60) || 0;
                return (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            },
            randomNumbers(from, to, length) {
                let numbers = [0];
                for (let i = 1; i < length; i++) {
                    numbers.push(Math.ceil(Math.random() * (from - to) + to))
                }

                return numbers
            },
            truncate(str, n) {
                return (str.length > n) ? str.substr(0, n - 1) + '...' : str
            },
            pauseTrack() {
                $("#auxplayPauseTrack").click()
            },
            statusTemplate(status) {
                let bg = 'text-red-800 bg-red-100';
                if (status === 'pending') {
                    bg = 'text-yellow-800 bg-yellow-100'
                } else if (status === 'in-review') {
                    bg = 'text-blue-800 bg-blue-100'
                }
                return bg;
            },
            totalPrice(tracks) {
                let unpaidTracks = tracks.find(track => track.can_play !== true)
                return unpaidTracks.reduce((current, next) => current + next.price, 0)
            },
            async postAjax(url, payload = {}) {
                const request = {
                    method: "post",
                    url: url,
                    parameter: payload
                };
                try {
                    const response = await axios(request);
                    return {'status': 1, 'message': response.data.message, 'data': response.data.data};
                } catch (error) {
                    return {'status': 0, 'message': error.response.data.message, 'data': error.response.data.data}
                }
            },
            async getAjax(url, payload = {}) {
                const request = {
                    method: "get",
                    url: url,
                    parameter: payload
                };
                try {
                    const response = await axios(request);
                    return response.data;
                } catch (error) {
                    console.log(error.response.data.message)
                    return {'status': 0, 'message': error.response.data.message, 'data': error.response.data.data}
                }
            }
        };
    }
};
