// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import qs from 'qs'

import global from '../static/global'

Vue.config.productionTip = false
Vue.prototype.global=global
Vue.prototype.$axios=axios
Vue.prototype.$qs=qs

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  beforeCreate:function(){
    console.log('对像创建完之后执行beforeCreate()')
  },
  created:function(){
    console.log('对像创建完之后执行create()')
  },
  beforeMount:function(){
    console.log('beforeMount()')
  },
  mounted:function(){
    console.log('mounted()')
  },
  beforeUpdate:function(){
    console.log('beforeUpdate()')
  },
  updated:function(){
    console.log('updated()')
  },
  beforeDetroy:function(){
    console.log('beforeDetroy()')
  },
  destroyed:function(){
    console.log('destroyed()')
  },


})
