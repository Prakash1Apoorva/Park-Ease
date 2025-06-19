<template>
  <div v-if="adminStore.currentLotDetails">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4">
      <h1 class="mb-3 mb-md-0 text-break">{{ lotData.prime_location_name }}</h1>
      <div class="align-self-start align-self-md-auto">
        <button class="btn btn-primary me-2" data-bs-toggle="modal" data-bs-target="#editLotModal">
          <i class="fas fa-edit"></i> Edit
        </button>
        <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteLotModal">
          <i class="fas fa-trash"></i> Delete
        </button>
      </div>
    </div>
    
    <div class="card p-3 mb-4">
      <h4>Lot Details</h4>
      <p><strong>Address:</strong> {{ adminStore.currentLotDetails.address }}</p>
      <p><strong>Price:</strong> ${{ adminStore.currentLotDetails.price.toFixed(2) }}/hr</p>
    </div>

    <h4>Spot Status ({{ adminStore.currentLotDetails.spots.length }} total)</h4>
    <div class="row">
      <div class="col-6 col-sm-4 col-md-3 col-lg-2 mb-3" v-for="spot in adminStore.currentLotDetails.spots" :key="spot.id">
        <div class="card text-center h-100" :class="spot.status === 'A' ? 'bg-success-subtle border-success' : 'bg-danger-subtle border-danger'">
          <div class="card-body p-2">
            <h5 class="card-title mb-1">Spot #{{ spot.spot_number }}</h5>
            <p class="card-text fw-bold small">{{ spot.status === 'A' ? 'Available' : 'Occupied' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <LoadingSpinner v-else />

  <!-- Modals -->
  <ConfirmModal id="deleteLotModal" title="Delete Parking Lot" message="Are you sure you want to permanently delete this lot and all its spots? This action cannot be undone." @confirmed="handleDeleteLot" />

  <div class="modal fade" id="editLotModal" tabindex="-1" aria-labelledby="editLotModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editLotModalLabel">Edit Lot Details</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleUpdateLot">
            <div class="mb-3">
              <label for="lotName" class="form-label">Location Name</label>
              <input type="text" class="form-control" id="lotName" v-model="lotData.prime_location_name" required>
            </div>
            <div class="mb-3">
              <label for="lotPrice" class="form-label">Price per Hour</label>
              <input type="number" class="form-control" id="lotPrice" v-model="lotData.price" step="0.01" required>
            </div>
            <div class="mb-3">
              <label for="lotAddress" class="form-label">Address</label>
              <input type="text" class="form-control" id="lotAddress" v-model="lotData.address" required>
            </div>
            <div class="modal-footer pb-0">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAdminStore } from '@/stores/admin';
import { onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Modal } from 'bootstrap';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ConfirmModal from '@/components/ConfirmModal.vue';

export default {
    name: 'AdminLotDetailView',
    components: { LoadingSpinner, ConfirmModal },
    setup() {
        const adminStore = useAdminStore();
        const route = useRoute();
        const router = useRouter();
        const lotData = ref({});

        watch(() => adminStore.currentLotDetails, (newDetails) => {
            if (newDetails) {
                lotData.value = JSON.parse(JSON.stringify(newDetails));
            }
        }, { deep: true, immediate: true });

        onMounted(() => {
            adminStore.fetchLotDetails(route.params.id);
        });

        onUnmounted(() => {
          adminStore.currentLotDetails = null;
        });

        const handleUpdateLot = async () => {
            await adminStore.updateLot(route.params.id, lotData.value);
            const modalEl = document.getElementById('editLotModal');
            if (modalEl) Modal.getInstance(modalEl)?.hide();
        };
        
        const handleDeleteLot = async () => {
            const success = await adminStore.deleteLot(route.params.id);
            const modalEl = document.getElementById('deleteLotModal');
            if (modalEl) Modal.getInstance(modalEl)?.hide();
            if (success) {
                router.push('/admin/dashboard');
            }
        };

        return { adminStore, lotData, handleUpdateLot, handleDeleteLot };
    }
}
</script>
