<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img :src="$projectLogoPath" alt="Park Easy Logo" class="me-2" style="height: 30px;" />
        {{ $projectName }}
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <!-- Links for Unauthenticated Users -->
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
          </template>
          <!-- Links for Authenticated Users -->
          <template v-else>
            <!-- User-specific navigation -->
            <template v-if="!authStore.isAdmin">
              <li class="nav-item">
                <router-link class="nav-link" to="/dashboard">Find Parking</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/dashboard">My Bookings</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/dashboard">Account</router-link>
              </li>
            </template>
            <!-- Admin-specific navigation (can be more detailed for admin pages) -->
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/dashboard">Admin Dashboard</router-link>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Management
                </a>
                <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="navbarDropdown">
                  <li><router-link class="dropdown-item" to="/admin/users">Users</router-link></li>
                  <li><router-link class="dropdown-item" to="/admin/reservations">Reservations</router-link></li>
                </ul>
              </li>
            </template>

            <!-- Common authenticated user elements -->
            <li class="nav-item me-2">
              <a class="nav-link" href="#"><i class="fas fa-bell"></i></a>
            </li>
            <li class="nav-item">
              <img src="https://via.placeholder.com/40" class="rounded-circle" alt="User Avatar" style="width: 40px; height: 40px; object-fit: cover;">
            </li>
             <li class="nav-item ms-3">
                <button class="btn btn-outline-primary btn-sm" @click="handleLogout">Logout</button>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Navbar',
  setup() {
    const authStore = useAuthStore();
    const handleLogout = () => {
      authStore.logout();
    };
    return {
      authStore,
      handleLogout
    };
  }
});
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}
.btn-sm {
    margin-top: 2px;
}
.dropdown-item {
  font-size: 0.9rem;
}
.nav-link {
  font-weight: 500;
  color: #333 !important; /* Ensure links are dark on light navbar */
}
.navbar-brand img {
    height: 30px;
    vertical-align: middle;
}
</style>
