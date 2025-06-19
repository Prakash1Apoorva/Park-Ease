<template>
  <div>
    <h1 class="mb-4">Admin Dashboard</h1>
    <!-- Analytics Section -->
    <div class="row mb-4">
      <div class="col-lg-8 mb-4">
        <h3>Revenue by Lot</h3>
        <div class="card" style="height: 300px;">
          <div class="card-body d-flex justify-content-center align-items-center">
            <BarChart v-if="chartData.datasets[0].data.length" :chartData="chartData" />
            <p v-else class="text-muted">No revenue data to display yet.</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4 mb-4">
        <h3>Key Stats</h3>
        <div v-if="adminStore.analytics" class="d-flex flex-column">
          <div class="card text-center bg-primary text-white mb-2">
            <div class="card-header">Total Revenue</div>
            <div class="card-body"><h4 class="card-title">${{ adminStore.analytics.kpis.total_revenue.toFixed(2) }}</h4></div>
          </div>
          <div class="card text-center bg-info text-white">
            <div class="card-header">Spots Occupied</div>
            <div class="card-body"><h4 class="card-title">{{ adminStore.analytics.kpis.occupied_spots_now }} / {{ adminStore.analytics.kpis.total_spots }}</h4></div>
          </div>
        </div>
        <div v-else class="text-center p-5 text-muted">
          Loading stats...
        </div>
      </div>
    </div>
    <hr>
    <!-- Lot Management -->
    <div class="row">
      <div class="col-lg-7 mb-4">
        <h3>Parking Lots</h3>
        <div class="list-group">
          <router-link v-for="lot in adminStore.lots" :key="lot.id" :to="`/admin/lots/${lot.id}`" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <div>
              <strong>{{ lot.prime_location_name }}</strong> <small class="text-muted">({{lot.address}})</small>
            </div>
            <span class="badge bg-primary rounded-pill">{{ lot.available_spots }} / {{ lot.number_of_spots }} Available</span>
          </router-link>
        </div>
      </div>
      <div class="col-lg-5 mb-4">
        <h3>Create New Lot</h3>
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="handleCreateLot">
              <div class="mb-2"><input type="text" class="form-control" placeholder="Location Name" v-model="newLot.prime_location_name" required></div>
              <div class="mb-2"><input type="number" class="form-control" placeholder="Price per Hour" v-model="newLot.price" step="0.01" min="0.01" required></div>
              <div class="mb-2"><input type="text" class="form-control" placeholder="Address" v-model="newLot.address" required></div>
              <div class="mb-2"><input type="text" class="form-control" placeholder="Pin Code" v-model="newLot.pin_code" required></div>
              <div class="mb-2"><input type="number" class="form-control" placeholder="Number of Spots" v-model="newLot.number_of_spots" min="1" required></div>
              <button type="submit" class="btn btn-success w-100">Create Lot</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin';
import { onMounted, reactive, computed } from 'vue';
import BarChart from '@/components/BarChart.vue';

export default {
    name: 'AdminDashboardView',
    components: { BarChart },
    setup() {
        const adminStore = useAdminStore();
        const newLot = reactive({
            prime_location_name: '',
            price: null,
            address: '',
            pin_code: '',
            number_of_spots: null
        });

        onMounted(() => {
            adminStore.fetchLots();
            adminStore.fetchAnalytics();
        });
        
        const chartData = computed(() => ({
            labels: adminStore.analytics?.revenue_by_lot?.labels || [],
            datasets: [
                {
                    label: 'Revenue ($)',
                    backgroundColor: '#0d6efd',
                    data: adminStore.analytics?.revenue_by_lot?.data || []
                }
            ]
        }));

        const handleCreateLot = () => {
            adminStore.createLot(newLot);
            Object.keys(newLot).forEach(key => { newLot[key] = null });
            newLot.prime_location_name = '';
            newLot.address = '';
            newLot.pin_code = '';
        };

        return { adminStore, newLot, handleCreateLot, chartData };
    }
}
</script>
