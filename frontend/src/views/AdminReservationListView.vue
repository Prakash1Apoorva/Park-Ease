<template>
  <div>
    <h1 class="mb-4">All Reservations</h1>
     <div v-if="adminStore.reservations.length" class="card">
        <div class="table-responsive">
            <table class="table table-striped table-hover mb-0">
                <thead>
                    <tr><th>Res ID</th><th>User</th><th>Lot</th><th>Spot</th><th>Parked</th><th>Status</th><th>Cost</th></tr>
                </thead>
                <tbody>
                    <tr v-for="res in adminStore.reservations" :key="res.reservation_id">
                        <td>{{ res.reservation_id }}</td>
                        <td>{{ res.username }}</td>
                        <td>{{ res.lot_name }}</td>
                        <td>#{{ res.spot_number }}</td>
                        <td>{{ new Date(res.parking_time).toLocaleString() }}</td>
                        <td>
                            <span class="badge" :class="res.leaving_time === 'Active' ? 'bg-success' : 'bg-secondary'">
                                {{ res.leaving_time === 'Active' ? 'Active' : 'Completed' }}
                            </span>
                        </td>
                        <td>{{ res.cost ? '$' + res.cost.toFixed(2) : '-' }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <LoadingSpinner v-else-if="loading" />
    <p v-else class="text-muted">No reservations found.</p>
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin';
import { onMounted, ref } from 'vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

export default {
    name: 'AdminReservationListView',
    components: { LoadingSpinner },
    setup() {
        const adminStore = useAdminStore();
        const loading = ref(true);
        onMounted(async () => {
            await adminStore.fetchAllReservations();
            loading.value = false;
        });
        return { adminStore, loading };
    }
}
</script>
