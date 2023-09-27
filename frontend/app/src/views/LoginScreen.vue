<template>
  <v-sheet class="pa-2" rounded>
    <v-img src="@/assets/neighborhood.jpg" cover max-height="650">
      <v-card class="mx-auto mt-8 px-6 py-4" max-width="344">
        <v-card-title class="text-h5 text-success">Login</v-card-title>
        <v-form v-model="form" @submit.prevent="onSubmit">
          <v-text-field
            v-model="username"
            :readonly="loading"
            density="compact"
            :rules="[required]"
            prepend-icon="mdi-account"
            variant="outlined"
            class="mb-2"
            clearable
            label="Username"
          >
          </v-text-field>
          <v-text-field
            v-model="password"
            :readonly="loading"
            density="compact"
            :rules="[required]"
            prepend-icon="mdi-form-textbox-password"
            clearable
            variant="outlined"
            label="Password"
            placeholder="Enter your password"
            type="password"
          ></v-text-field>
          <br />
          <v-btn
            :disabled="!form"
            :loading="loading"
            block
            color="success"
            size="large"
            type="submit"
            variant="elevated"
          >
            Sign In
          </v-btn>
        </v-form>
        <br />
        <div>
          <span class="text-body-1"
            >Don't have an account?
            <v-btn
              to="/register"
              color="primary"
              density="compact"
              variant="text"
              >Click Here</v-btn
            >
            to register.</span
          >
        </div>
      </v-card>
    </v-img>
  </v-sheet>
</template>
<script setup>
import { ref } from "vue";
import { useAppStore } from "@/store/app";
import { useRouter } from "vue-router";

const form = ref(false);
const username = ref(null);
const password = ref(null);
const loading = ref(false);

const store = useAppStore();

const router = useRouter();

const onSubmit = async () => {
  if (!form.value) return;
  loading.value = true;
  const resp = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  });
  if (resp.ok) {
    const content = await resp.json();
    store.authenticate(content["x-token"]);
    router.push({
      name: "HomeScreen",
    });
  } else {
    store.setAlert(
      "Something went wrong while logging in. Please refresh and try again."
    );
  }
  loading.value = false;
};

const required = async (v) => {
  return !!v || "Field is required";
};
</script>
