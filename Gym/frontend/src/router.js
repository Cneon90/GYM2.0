import Vue from "vue";
import VueRouter from "vue-router";
import HelloWorld from "@/components/HelloWorld";
import TestDrive from "@/components/TestDrive";

Vue.use(VueRouter);

export default new VueRouter({
  routes: [
      { path: '/home',  component: HelloWorld },
      { path: '/my',  component: TestDrive }
  ],
  mode: "history",

});