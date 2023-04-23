<template>
  <div class="main">
     <div class="header">
       <h1> Главная страница !</h1>
     </div>
    <input v-model="message" placeholder="отредактируй меня">
    <p>Введённое сообщение: {{ message }}</p>
    <button class="button" @click="addUser"> Добавить </button>
       {{users.name}}
    <ul>
      <li v-for="item in users"  v-bind:key="item.age" >{{ item.name }}</li>
   </ul>

  </div>
</template>


<script>
   import axios from "axios";

   export default {
     name: "PageHome",
     methods: {
       addUser() {
         // axios.get('/api/users/').then(res => {
         //   console.log(res.data); // Результат ответа от сервера
         //   this.users = res.data;
         // });

         // axios.post('/api/info', {"Name": "Kirill"}).then(res => {
         //    console.log(res); // Результат ответа от сервера
         // });

         axios.post("/api/info", {"Name": this.message, "age": "32"}).then(res => {
           console.log(res.data); // Результат ответа от сервера
           this.users = res.data;
         });
       }
     },
     data() {
       return {
         message: 'Hello!!!',
         users: []
       }
     }
   }

</script>


<style>
.header
{
  text-align: center;
}
</style>