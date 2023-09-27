// Utilities
import { defineStore } from "pinia";
import cookie from "js-cookie";

export const useAppStore = defineStore("app", {
  state: () => ({
    alert: null,
    xToken: null,
  }),
  getters: {
    isAuthenticated() {
      if (this.xToken !== null) {
        return true;
      }
      const token = cookie.get("x-token");
      if (token !== undefined) {
        this.setXToken(token);
        return true;
      }
      return false;
    },
  },
  actions: {
    setXToken(xToken) {
      this.xToken = xToken;
    },
    authenticate(xToken) {
      cookie.set("x-token", xToken, { expires: 1 });
      this.xToken = xToken;
    },
    logout() {
      cookie.remove("x-token");
      this.xToken = null;
    },
    setAlert(alert) {
      this.alert = alert;
    },
  },
});
