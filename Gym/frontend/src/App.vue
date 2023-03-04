<template>

 <section>
  <router-view></router-view>
 </section>



</template>

<script>



export default {
  name: 'App',
  components: {

  },
    methods: {
            clickMe() {
              this.$http.get("/api/info").then(res => {
              // Вывод на экран ответа сервера
              console.log(res.data);
              this.result = res.data;
    })
            }
        },
  fetchData() {
      this.$http.get('/api/info')
        .then(response => { console.log(response) }) .catch(error => { console.log(error) })
    },
 data() {
    return {
      message: 'ttgh',
      result: 5,
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
