<template>
  <div class="fund">    
    <button @click="fund_data">生成基金数据</button>
    <ul>
      <li v-for="fund in funddata">
        {{fund}}
      </li>
    </ul>
    </div>
  </div>  
</template>

<script>
export default {
  name: 'fund',
  data () {
    return {
      msg: '定投 帮你 选基金',
      user:'',
      pwd:'',
      picked: '',
      selected:'',
      options: [
      { text: 'One', value: 'A' },
      { text: 'Two', value: 'B' },
      { text: 'Three', value: 'C' }
      ],
      funddata:[]
    }
  },
  methods: {
    fund_data: function () {
      this.$axios.get(this.global.host+"fundata")
      .then(res=>{
        if(res.status==200){
          this.funddata=res.data.split(',');
        }
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
