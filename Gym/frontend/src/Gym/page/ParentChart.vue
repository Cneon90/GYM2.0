<template>
  <div class="main">
    <h1>  Index </h1>
    <WeekChart
      v-bind:chart-labels= this.names
      v-bind:chart-data=this.hel
    />
    <button class="button" @click="meClick"> ha </button>
  </div>

</template>

<script>
import WeekChart from "@/Gym/components/WeekChart";
export default {
  name: "PageHome",
  components: {WeekChart},
    data () {
    return {
       names : ['kirill','danil'],
       hel : [25,30]
    }
  },
  methods: {
     increment(){
       this.$store.dispatch('increment');
     },
     decrement(){
       this.$store.dispatch('decrement');
     },
    meClick (){
      this.hel.push(20);
    }
  }
}
</script>

<style scoped>

</style>