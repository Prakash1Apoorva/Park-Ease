<template>
  <div class="user-dashboard">
    <!-- Welcome Header -->
    <h1 class="mb-2">Welcome back, {{ authStore.user ? authStore.user.username : 'User' }}</h1>
    <p class="text-muted mb-4">Today is {{ currentDate }}</p>

    <div class="row g-4">
      <!-- Left Column: Current Status -->
      <div class="col-lg-8">
        <div class="card current-status-card p-4 rounded-4 shadow-sm h-100">
          <h4 class="fw-bold mb-3">Current Status</h4>
          <div v-if="activeReservation" class="active-parking-info">
            <h5 class="mb-2 text-primary">{{ activeReservation.lot_name || 'N/A' }}, Spot #{{ activeReservation.spot_number || 'N/A' }}</h5>
            <p class="mb-3">
              Elapsed Time: {{ formatDuration(activeReservation.parking_time) }} | 
              Cost: ${{ activeReservation.cost ? activeReservation.cost.toFixed(2) : calculateCurrentCost(activeReservation).toFixed(2) }}
            </p>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary rounded-pill px-4" @click="extendSession">
                <i class="fas fa-plus"></i> Extend Session
              </button>
              <button class="btn btn-danger rounded-pill px-4" @click="userStore.releaseSpot(activeReservation.reservation_id)">
                <i class="fas fa-stop-circle"></i> End Session
              </button>
            </div>
          </div>
          <div v-else class="text-muted-emphasis text-center py-5">
            <i class="fas fa-car fa-3x mb-3 text-secondary"></i>
            <p class="lead">No active parking session.</p>
            <p>Find a parking spot in your area!</p>
            <button class="btn btn-primary rounded-pill px-4" @click="scrollToAvailableLots">Find Parking</button>
          </div>
        </div>
      </div>

      <!-- Right Column: Quick Stats -->
      <div class="col-lg-4">
        <div class="card p-4 rounded-4 shadow-sm h-100">
          <h4 class="fw-bold mb-3">Quick Stats</h4>
          <div class="row g-3">
            <div class="col-6">
              <div class="stat-item p-3 rounded-3 border">
                <p class="text-muted mb-1 small">Total Bookings</p>
                <h5 class="fw-bold">{{ userStore.analytics ? userStore.analytics.total_reservations : 'N/A' }}</h5>
              </div>
            </div>
            <div class="col-6">
              <div class="stat-item p-3 rounded-3 border border-success border-opacity-50">
                <p class="text-muted mb-1 small">Money Spent</p>
                <h5 class="fw-bold text-success">${{ userStore.analytics ? userStore.analytics.total_spent.toFixed(2) : 'N/A' }}</h5>
              </div>
            </div>
            <div class="col-6">
              <div class="stat-item p-3 rounded-3 border">
                <p class="text-muted mb-1 small">Favorite Lot</p>
                <h5 class="fw-bold">{{ userStore.analytics ? userStore.analytics.favorite_lot : 'N/A' }}</h5>
              </div>
            </div>
            <div class="col-6">
              <div class="stat-item p-3 rounded-3 border border-purple border-opacity-50">
                <p class="text-muted mb-1 small">Current Streak</p>
                <h5 class="fw-bold text-purple">5 days</h5> <!-- Placeholder for now -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="mt-5">
      <h4 class="fw-bold mb-3">Recent Activity <router-link to="/dashboard" class="small text-decoration-none float-end">View All</router-link></h4>
      <div class="d-flex overflow-x-auto pb-3 recent-activity-scroll-container">
        <div class="activity-card flex-shrink-0 me-3 rounded-3 shadow-sm" v-for="res in recentReservations" :key="res.reservation_id">
          <img :src="getLotImage(res.lot_name)" class="img-fluid rounded-top" alt="Parking Lot">
          <div class="p-3">
            <h6 class="fw-bold mb-1 text-truncate">{{ res.lot_name }}</h6>
            <p class="text-muted small mb-0">{{ new Date(res.parking_time).toLocaleDateString() }}</p>
          </div>
        </div>
        <div v-if="!recentReservations.length" class="text-muted-emphasis py-4 px-3">
            No recent activity to display.
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-5">
      <h4 class="fw-bold mb-3">Quick Actions</h4>
      <div class="row g-3">
        <div class="col-lg-4">
          <div class="input-group">
            <span class="input-group-text rounded-start-pill bg-white border-end-0"><i class="fas fa-search text-muted"></i></span>
            <input type="text" class="form-control rounded-end-pill px-3 py-2 border-start-0" placeholder="Find Parking (e.g., Downtown)" aria-label="Find Parking">
          </div>
        </div>
        <div class="col-lg-4">
          <button class="btn btn-outline-primary rounded-pill px-4 py-2 w-100">
            <i class="fas fa-heart me-2"></i>Favorite Lots
          </button>
        </div>
        <div class="col-lg-4">
          <button class="btn btn-outline-secondary rounded-pill px-4 py-2 w-100">
            <i class="fas fa-phone me-2"></i>Emergency Contact
          </button>
        </div>
      </div>
    </div>
    
    <!-- User Dashboard's original content (Available Lots & Parking History) -->
    <!-- This section can be moved to "Find Parking" and "My Bookings" pages in future -->
    <hr class="my-5">
    <div class="row">
      <div class="col-lg-6 mb-4">
        <h3>Available Parking Lots</h3>
        <div class="list-group">
          <div class="list-group-item" v-for="lot in userStore.availableLots" :key="lot.id">
            <h5>{{ lot.prime_location_name }}</h5>
            <p class="mb-2">{{ lot.address }} - Price: ${{ lot.price_per_hour.toFixed(2) }}/hr</p>
            <button class="btn btn-primary" :disabled="lot.available_spots === 0 || activeReservation" @click="userStore.reserveSpot(lot.id)">
              {{ lot.available_spots > 0 ? `Reserve a Spot (${lot.available_spots} available)` : 'No Spots Available' }}
            </button>
          </div>
          <div v-if="!userStore.availableLots.length" class="list-group-item text-muted">No parking lots available at the moment.</div>
        </div>
      </div>
      <div class="col-lg-6 mb-4">
        <h3>My Parking History</h3>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr><th>Lot</th><th>Parked</th><th>Left</th><th>Cost</th></tr>
            </thead>
            <tbody>
              <tr v-for="res in completedReservations" :key="res.reservation_id">
                <td>{{ res.lot_name }}</td>
                <td>{{ new Date(res.parking_time).toLocaleString() }}</td>
                <td>{{ new Date(res.leaving_time).toLocaleString() }}</td>
                <td>{{ res.cost ? '$' + res.cost.toFixed(2) : '-' }}</td>
              </tr>
              <tr v-if="!completedReservations.length" class="text-center text-muted">
                <td colspan="4">No past parking history.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import { useAuthStore } from '@/stores/auth';
import { onMounted, computed } from 'vue';

export default {
  name: 'UserDashboardView',
  setup() {
    const userStore = useUserStore();
    const authStore = useAuthStore();

    onMounted(() => {
      userStore.fetchAvailableLots();
      userStore.fetchReservations();
      userStore.fetchAnalytics();
    });

    const activeReservation = computed(() =>
      userStore.reservations.find(r => r.leaving_time === 'Active')
    );

    const completedReservations = computed(() =>
      userStore.reservations.filter(r => r.leaving_time !== 'Active')
    );

    const recentReservations = computed(() => {
      // Show only completed reservations for recent activity, limit to 5
      return userStore.reservations
        .filter(r => r.leaving_time !== 'Active')
        .sort((a, b) => new Date(b.parking_time) - new Date(a.parking_time))
        .slice(0, 5);
    });

    const currentDate = computed(() => {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date().toLocaleDateString(undefined, options);
    });

    const calculateCurrentCost = (reservation) => {
      if (!reservation || !reservation.parking_time || !reservation.spot || !reservation.spot.lot) {
        return 0;
      }
      const parkTime = new Date(reservation.parking_time);
      const now = new Date();
      const durationSeconds = (now - parkTime) / 1000;
      const durationHours = Math.ceil(durationSeconds / 3600);
      const cost = durationHours * reservation.spot.lot.price;
      return isNaN(cost) ? 0 : cost;
    };

    const formatDuration = (parkingTime) => {
      const parkTime = new Date(parkingTime);
      const now = new Date();
      const diffSeconds = Math.floor((now - parkTime) / 1000);
      
      const hours = Math.floor(diffSeconds / 3600);
      const minutes = Math.floor((diffSeconds % 3600) / 60);

      return `${hours}h ${minutes}m`;
    };

    const extendSession = () => {
      // Placeholder for extending session functionality
      alert('Extend Session functionality coming soon!');
    };

    const scrollToAvailableLots = () => {
      // Simple scroll to the available lots section
      const availableLotsSection = document.querySelector('.list-group');
      if (availableLotsSection) {
        availableLotsSection.scrollIntoView({ behavior: 'smooth' });
      }
    };

    const getLotImage = (lotName) => {
      // Simple function to map lot names to placeholder images
      // You'd replace this with actual image URLs from your backend or assets
      const images = {
        'Downtown Central Parking': 'https://images.unsplash.com/photo-1519782558-8687b1c3c97e?auto=format&fit=crop&q=80&w=400&h=200',
        'Uptown Premium Parking': 'https://images.unsplash.com/photo-1522814234509-b684a270f20d?auto=format&fit=crop&q=80&w=400&h=200',
        'Midtown Lot C': 'https://images.unsplash.com/photo-1595180425712-42171120f2b0?auto=format&fit=crop&q=80&w=400&h=200',
        'Westside Lot D': 'https://images.unsplash.com/photo-1582255734731-f1b212f483b8?auto=format&fit=crop&q=80&w=400&h=200',
        'Eastside Lot E': 'https://images.unsplash.com/photo-1563889053894-3990f230869a?auto=format&fit=crop&q=80&w=400&h=200',
        'Park Easy Lot F': 'https://images.unsplash.com/photo-1568270597274-1234a9b6c0e0?auto=format&fit=crop&q=80&w=400&h=200',
      };
      return images[lotName] || 'https://images.unsplash.com/photo-1532581291347-9b45eece0865?auto=format&fit=crop&q=80&w=400&h=200'; // Default placeholder
    };


    return {
      authStore,
      userStore,
      activeReservation,
      completedReservations,
      recentReservations,
      currentDate,
      calculateCurrentCost,
      formatDuration,
      extendSession,
      scrollToAvailableLots,
      getLotImage
    };
  }
};
</script>

<style scoped>
/* Custom Styles for Dashboard Layout and Components */
.user-dashboard {
  background-color: #f8f9fa; /* Light grey background for the dashboard area */
  padding: 20px; /* Some padding around the entire dashboard */
}

.current-status-card {
  background: linear-gradient(135deg, #e0f2f7 0%, #c9e6f2 100%); /* Light blue gradient */
  color: #333;
}

.current-status-card h4 {
  color: #212529;
}

.active-parking-info h5 {
  font-size: 1.5rem;
  color: #007bff;
}

.stat-item {
  background-color: #fff;
}

/* Custom border colors for stat items */
.border-purple {
  border-color: #6f42c1 !important;
}

.text-purple {
  color: #6f42c1 !important;
}

.recent-activity-scroll-container {
  overflow-y: hidden; /* Hide vertical scrollbar */
  -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}

.recent-activity-scroll-container::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.activity-card {
  width: 250px; /* Fixed width for activity cards */
  background-color: #fff;
  border: 1px solid #e0e0e0;
}

.activity-card img {
  height: 150px; /* Fixed height for activity card images */
  object-fit: cover;
}

.input-group .form-control.rounded-end-pill {
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
}
.input-group .input-group-text.rounded-start-pill {
    border-top-right-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
}
</style>
