import Vue from 'vue';
import axios from "axios";
import {REMOTE_URL} from "../common/base.js";
import {
    Message
} from "element-ui";

axios.defaults.baseURL = REMOTE_URL;
axios.defaults.timeout = 60 * 1000;

const _axios = axios.create();
const _incomeAxios = axios.create();

_axios.interceptors.request.use(
    function (config) {
        let token = localStorage.getItem("token");
        config.headers["Authorization"] = token;
        console.log('发送请求：', config);
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

_incomeAxios.interceptors.request.use(
    function (config) {
        let token = localStorage.getItem("token");
        config.headers["Authorization"] = token;
        console.log('发送请求：', config);
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

_axios.interceptors.response.use(
    function (rsp) {
        console.log('响应报文：', rsp);
        let {headers} = rsp;
        if (headers['content-type'] == 'application/octet-stream;charset=UTF-8') {
            return rsp;
        }
        if (headers['content-type'] == 'application/vnd.ms-excel') {
            return rsp;
        }

        let res = rsp.data;
        if (typeof (res.success) == 'undefined') {
            return rsp;
        }
        if (!res.success && res.statusCode != -1) {
            Message({
                type: 'error',
                message: res.message
            });
            return rsp;
        }
        return rsp;
    },
    function (err) {
        Message({
            type: 'error',
            message: '请求时发生网络错误！'
        });
        console.log('处理请求时发生错误：', err);
    }
);
_incomeAxios.interceptors.response.use(
    function (rsp) {
        console.log('响应报文：', rsp);
        let res = rsp.data;
        if (!res.success) {
            Message({
                type: 'error',
                message: res.message
            });
            return res;
        }
        //console.log(`业务内容：${JSON.stringify(res)}`);
        return res;
    },
    function (error) {
        Message({
            type: 'error',
            message: `请求时发生网络错误！`
        });
        console.log(`处理请求时发生错误：${JSON.stringify(error)}`);
    }
);

Plugin.install = function (Vue) {
    Vue.axios = _axios;
    Vue.incomeAxios = _incomeAxios;
    window.axios = _axios;
    window.incomeAxios = _incomeAxios;
    Object.defineProperties(Vue.prototype, {
        axios: {
            get() {
                return _axios;
            }
        },
        incomeAxios: {
            get() {
                return _incomeAxios;
            }
        },
        $axios: {
            get() {
                return _axios;
            }
        },
        $incomeAxios: {
            get() {
                return _incomeAxios;
            }
        }
    });
};

Vue.use(Plugin);

export default {
    axios: _axios,
    incomeAxios: _incomeAxios
};