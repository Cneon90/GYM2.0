<template>
  <div class="panel">
    {{ this.ChartLabels }}
    {{ this.ChartData }}
    <button @click="beng"> ggett </button>
    <Bar
      id="my-chart-id"
      v-bind:options="chartOptions"
      v-bind:data="chartData"
    />
 </div>

</template>

<script>

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'WeekChart',
  components: {Bar},
  props: ['ChartLabels', 'ChartData'],
  data() {
    return {
      chartData: {
        title: {
          display: true,
          text: 'Chart.js Bar Chart'
        },
        labels: this.ChartLabels,
        datasets: [{data: this.ChartData}]
      },
      chartOptions: {
        responsive: true
      }
    }
  },
  methods: {
    beng() {

    }
  },
  watch: {
    data: {

    },

      deep: true
    }
}
</script>

<style scoped>


</style>