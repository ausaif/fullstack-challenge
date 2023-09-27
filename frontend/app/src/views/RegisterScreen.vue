<template>
  <v-sheet class="pa-2" rounded>
    <v-img src="@/assets/neighborhood.jpg" cover max-height="650">
      <v-card class="mx-auto mt-8 px-6 py-4" max-width="344">
        <v-card-title class="text-h5 text-success">Register</v-card-title>
        <v-form v-model="form" @submit.prevent="onSubmit">
          <v-text-field
            v-model="firstName"
            :readonly="loading"
            density="compact"
            :rules="[required]"
            variant="outlined"
            class="mb-2"
            clearable
            label="First Name"
          >
          </v-text-field>
          <v-text-field
            v-model="lastName"
            :readonly="loading"
            density="compact"
            :rules="[required]"
            variant="outlined"
            class="mb-2"
            clearable
            label="Last Name"
          >
          </v-text-field>
          <v-text-field
            v-model="username"
            :readonly="loading"
            density="compact"
            :rules="[required]"
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
            clearable
            variant="outlined"
            label="Password"
            placeholder="Enter your password"
          ></v-text-field>
          <v-text-field
            v-model="email"
            :readonly="loading"
            density="compact"
            :rules="[required]"
            variant="outlined"
            label="Email"
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
            Sign Up
          </v-btn>
        </v-form>
        <br />
        <div>
          <span class="text-body-1"
            >Already have an account?
            <v-btn to="/login" color="primary" density="compact" variant="text"
              >Click Here</v-btn
            >
            to login.</span
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
const firstName = ref(null);
const lastName = ref(null);
const username = ref(null);
const password = ref(null);
const email = ref(null);
const loading = ref(false);

const store = useAppStore();

const router = useRouter();

const onSubmit = async () => {
  if (!form.value) return;
  loading.value = true;
  const resp = await fetch(`${import.meta.env.VITE_API_BASE_URL}/register`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
      firstname: firstName.value,
      lastname: lastName.value,
      email: email.value,
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
