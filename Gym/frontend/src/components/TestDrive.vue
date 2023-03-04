<template>
    <section>
        <b-field label="Select datetime">
        <b-datetimepicker
            placeholder="Select a date"
            icon="calendar-today"
            :timepicker="timepicker"
            >
        </b-datetimepicker>
    </b-field>
    </section>
</template>

<script>
export default {
  name: "TestDrive",
  methods: {
            clickMe() {
                this.$buefy.notification.open('Clicked!!')
            },
            clearDate () {
            this.selected = null
        }
        },
  data() {
        return {
            selected: new Date(),
            showWeekNumber: false,
            locale: undefined // Browser locale
        }
    },
}
</script>

<style scoped>

</style>