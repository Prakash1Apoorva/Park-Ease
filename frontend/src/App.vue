<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <!-- Navbar is only visible if it's NOT an authentication page -->
    <Navbar v-if="!isAuthPage" />
    
    <!--
      The main content area.
      - If it's a landing page, it takes full width (no 'container' class).
      - If it's an auth page, it takes full width (no 'container' class).
      - Otherwise (for dashboards, etc.), it uses the 'container my-5' classes.
    -->
    <main :class="{ 'container my-5': !isLandingPage && !isAuthPage }">
      <RouterView />
    </main>
    
    <!-- Footer is only visible if it's NOT an authentication page -->
    <Footer v-if="!isAuthPage" />
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

export default {
  components: {
    Navbar,
    Footer,
    RouterView
  },
  setup() {
    const route = useRoute();
    
    // Checks if the current route is the landing page
    const isLandingPage = computed(() => route.name === 'landing');

    // Checks if the current route is either the login or register page
    const isAuthPage = computed(() => route.name === 'login' || route.name === 'register');

    return {
      isLandingPage,
      isAuthPage
    };
  }
};
</script>

<style>
/* You can add global styles here if needed */
/* Ensure body and html take full height for min-vh-100 to work */
html, body, #app {
  height: 100%;
}
</style>
