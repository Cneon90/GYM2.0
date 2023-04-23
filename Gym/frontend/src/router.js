import Vue from "vue";
import VueRouter from "vue-router";
// import HelloWorld from "@/components/HelloWorld";
// import TestDrive from "@/components/TestDrive";
//
import PageHome from "@/Gym/page/PageHome";
import MyCabinet from "@/Gym/page/MyCabinet";
// import PageHome from "@/Gym/page/PageHome";

Vue.use(VueRouter);

export default new VueRouter({
  routes: [
      { path: '/home',  component: PageHome },
      { path: '/my',  component: MyCabinet  },
  ],
    mode: "history",
});
