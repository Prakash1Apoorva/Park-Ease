import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingView.vue'),
      meta: { guest: true } // Mark as a guest-only route
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true } // Mark as a guest-only route
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { guest: true } // Mark as a guest-only route
    },
    // --- User Routes ---
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/UserDashboardView.vue'),
      meta: { requiresAuth: true, roles: ['user'] }
    },
    {
      path: '/payment/:reservationId/:cost',
      name: 'payment',
      component: () => import('../views/PaymentView.vue'),
      props: true, // This allows the component to receive params as props
      meta: { requiresAuth: true, roles: ['user'] }
    },
    // --- Admin Routes ---
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboardView.vue'),
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/admin/lots/:id',
      name: 'admin-lot-detail',
      component: () => import('../views/AdminLotDetailView.vue'),
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/admin/users',
      name: 'admin-user-list',
      component: () => import('../views/AdminUserListView.vue'),
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/admin/reservations',
      name: 'admin-reservation-list',
      component: () => import('../views/AdminReservationListView.vue'),
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    { 
      path: '/:pathMatch(.*)*', 
      name: 'ErrorPage',
      component: () => import('../views/ErrorPage.vue') 
    }
  ]
})

// --- THE MODIFIED NAVIGATION GUARD ---
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Fetch profile on page load if needed
  if (authStore.token && !authStore.user) {
    await authStore.fetchProfile();
  }

  // Case 1: Route requires authentication
  if (to.meta.requiresAuth) {
    if (authStore.isAuthenticated) {
      // User is authenticated, check role
      const requiredRoles = to.meta.roles;
      if (requiredRoles && !requiredRoles.includes(authStore.user.role)) {
        // Wrong role, redirect to appropriate dashboard
        return next(authStore.isAdmin ? { name: 'admin-dashboard' } : { name: 'dashboard' });
      }
      // Correct role, allow access
      return next();
    } else {
      // User is not authenticated, redirect to login
      return next({ name: 'login' });
    }
  } 
  // Case 2: Route is for guests (login, register, landing)
  else if (to.meta.guest) {
    if (authStore.isAuthenticated) {
      // If a logged-in user tries to visit a guest page, redirect them to their dashboard
      return next(authStore.isAdmin ? { name: 'admin-dashboard' } : { name: 'dashboard' });
    }
    // If not logged in, allow access
    return next();
  } 
  // Case 3: Any other route (like the 404 page)
  else {
    return next();
  }
});

export default router
