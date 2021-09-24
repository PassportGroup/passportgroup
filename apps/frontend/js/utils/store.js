export default class Store {

    constructor(expire_in = null) {
        this.expire_in = expire_in !== null ? Math.abs(expire_in) : 1
    }

    addStorage(key, value) {
        let now = new Date()
        let schedule = new Date()
        schedule.setDate(now.getDate() + this.expire_in)
        let data = {
            value: value,
            expire_in: schedule
        }
        localStorage.setItem(key, JSON.stringify(data))

    }

    getStorage(key) {
        if (this.keyExist(key)) {
            let now = Date.now()
            let data = JSON.parse(localStorage.getItem(key))
            if (data !== null && data.expire_in >= now) {
                localStorage.removeItem(key)
            }
            return data.value
        }
        return []

    }

    keyExist(key) {
        return localStorage.getItem(key) !== null
    }
}