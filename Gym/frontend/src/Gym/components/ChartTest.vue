<template>
  <div class="test">

 </div>
</template>

<script>
export default {
  name: "ChartTest",
  props: ['zag'],
  data (){
        return  {
                  message : 'Hello'
                }
  },
  methods:{
    clickMe (){
      alert(this.zag);
    }
  }
}
</script>

<style scoped>

</style>