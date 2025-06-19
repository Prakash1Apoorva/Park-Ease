<template>
  <div>
    <h1 class="mb-4">Registered Users</h1>
    <div v-if="adminStore.users.length" class="card">
      <div class="table-responsive">
        <table class="table table-striped table-hover mb-0">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Username</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in adminStore.users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td class="text-end">
                <!-- MODIFIED LINE: Changed from <a> to <button> -->
                <button @click="handlePreviewReport(user.id)" class="btn btn-sm btn-outline-primary">
                  <i class="fas fa-file-pdf"></i> Preview Report
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <LoadingSpinner v-else-if="loading" />
    <p v-else class="text-muted">No users found.</p>
  </div>
</template>



<script>
import { useAdminStore } from '@/stores/admin';
import { onMounted, ref } from 'vue';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import apiClient from '@/services/api'; // Import our apiClient
import { useToast } from 'vue-toastification'; // Import toast for feedback

export default {
    name: 'AdminUserListView',
    components: { LoadingSpinner },
    setup() {
        const adminStore = useAdminStore();
        const loading = ref(true);
        const toast = useToast(); // Initialize toast

        onMounted(async () => {
            await adminStore.fetchUsers();
            loading.value = false;
        });
        const handlePreviewReport = async (userId) => {
          try {
            toast.info("Generating report, please wait...", { timeout: 2000 });
            
            const response = await apiClient.get(`/api/admin/reports/preview/${userId}`, {
              responseType: 'blob', // This tells axios to expect binary data
            });

            // Create a Blob from the PDF stream
            const file = new Blob([response.data], { type: 'application/pdf' });
            
            // Build a URL from the file
            const fileURL = URL.createObjectURL(file);
            
            // Open the URL on a new tab
            window.open(fileURL, '_blank');
            
          } catch (error) {
            toast.error("Failed to generate report.");
            console.error(error);
          }
        };
        return { adminStore, loading,handlePreviewReport };
    }
}
</script>
