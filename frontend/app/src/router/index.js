// Composables
import { createRouter, createWebHistory } from "vue-router";
import { useAppStore } from "@/store/app";

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "HomeScreen",
        component: () => import("@/views/HomeScreen.vue"),
      },
    ],
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/favorites",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "HomeScreenUser",
        component: () => import("@/views/HomeScreenUser.vue"),
      },
    ],
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    component: () => import("@/layouts/default/Default.vue"),
    name: "Login",
    children: [
      {
        path: "",
        name: "LoginScreen",
        component: () => import("@/views/LoginScreen.vue"),
      },
    ],
  },
  {
    path: "/register",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "RegisterScreen",
        component: () => import("@/views/RegisterScreen.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to) => {
  const store = useAppStore();
  if (to.meta.requiresAuth && !store.isAuthenticated) return "/login";
});

export default router;
