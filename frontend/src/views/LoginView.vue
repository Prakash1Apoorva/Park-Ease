<template>
  <div class="auth-container d-flex">
    <!-- Left Panel: Login Form -->
    <div class="auth-panel auth-form-panel d-flex align-items-center justify-content-center p-4 p-md-5">
      <div class="auth-content w-100" style="max-width: 400px;">
        <div class="text-center mb-5">
          <h2 class="fw-bold">Welcome Back</h2>
          <p class="text-muted">Sign in to access your account</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control rounded-pill px-3 py-2" id="username" v-model="username" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control rounded-pill px-3 py-2" id="password" v-model="password" required>
          </div>
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="rememberMe">
              <label class="form-check-label text-muted" for="rememberMe">
                Remember me
              </label>
            </div>
            <router-link to="/forgot-password" class="text-primary text-decoration-none">Forgot your password?</router-link>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-lg rounded-pill fw-bold">Sign In</button>
          </div>
        </form>

        <div class="text-center mt-4">
          <p class="text-muted">Not a member? <router-link to="/register" class="text-primary text-decoration-none fw-bold">Create an account</router-link></p>
        </div>
      </div>
    </div>

    <!-- Right Panel: Promotional Image & Text -->
    <div class="auth-panel auth-image-panel d-none d-md-flex align-items-center justify-content-center text-white text-center p-5">
      <div>
        <h1 class="display-4 fw-bolder mb-3">Park Smarter, Not Harder</h1>
        <p class="lead" style="max-width: 40rem;">
          Discover seamless parking with ParkEase. Find, reserve, and pay for your spot hassle-free.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

export default {
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore();
    const username = ref('');
    const password = ref('');

    const handleLogin = () => {
      authStore.login({ username: username.value, password: password.value });
    };

    return {
      username,
      password,
      handleLogin
    };
  }
};
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  width: 100%;
  /* REMOVED: position: absolute; top: 0; left: 0; */
}

.auth-panel {
  width: 50%;
}

.auth-form-panel {
  background-color: white;
}

.auth-image-panel {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url('https://plus.unsplash.com/premium_photo-1673886205989-24c637783c60?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D') no-repeat center center;
  background-size: cover;
}

@media (max-width: 767.98px) {
  .auth-panel {
    width: 100%;
    min-height: 50vh;
  }

  .auth-image-panel {
    min-height: 300px;
  }

  .auth-content {
    padding: 20px;
  }
}
</style>
