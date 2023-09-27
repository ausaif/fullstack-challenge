<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <v-icon icon="mdi-office-building-marker-outline" />
      ENODO
    </v-app-bar-title>
    <v-spacer></v-spacer>

    <v-sheet v-show="store.isAuthenticated">
      <v-btn class="mr-2" to="/" text> Home </v-btn>
      <v-btn class="mr-2" to="/favorites"> Favorites </v-btn>
      <v-btn @click.prevent.stop="logout()" text> Log out </v-btn>
    </v-sheet>
  </v-app-bar>
</template>

<script setup>
import { useAppStore } from "@/store/app";
import { useRouter } from "vue-router";

const store = useAppStore();
const router = useRouter();

const logout = () => {
  store.logout();
  router.push({
    name: "LoginScreen",
  });
};
</script>
