import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { useToast } from 'vue-toastification';

const toast = useToast();

export const useAdminStore = defineStore('admin', {
    state: () => ({
        lots: [],
        users: [],
        reservations: [],
        analytics: null,
        currentLotDetails: null, // For the detail page
    }),
    actions: {
        async fetchLots() {
            try {
                const response = await apiClient.get('/api/admin/lots');
                this.lots = response.data;
            } catch (error) {
                console.error('Failed to fetch lots:', error);
            }
        },
        async createLot(lotData) {
            try {
                await apiClient.post('/api/admin/lots', lotData);
                toast.success(`Lot "${lotData.prime_location_name}" created successfully!`);
                await this.fetchLots();
            } catch (error) {
                toast.error('Failed to create lot. ' + (error.response?.data?.msg || ''));
            }
        },
        async fetchLotDetails(lotId) {
            try {
                const response = await apiClient.get(`/api/admin/lots/${lotId}`);
                this.currentLotDetails = response.data;
            } catch (error) {
                toast.error('Failed to fetch lot details.');
                this.currentLotDetails = null;
            }
        },
        async updateLot(lotId, lotData) {
             try {
                await apiClient.put(`/api/admin/lots/${lotId}`, lotData);
                toast.success('Lot updated successfully!');
                await this.fetchLotDetails(lotId); // Refresh details
            } catch (error) {
                toast.error('Failed to update lot.');
            }
        },
        async deleteLot(lotId) {
            try {
                await apiClient.delete(`/api/admin/lots/${lotId}`);
                toast.success('Lot deleted successfully!');
                return true; // Indicate success for routing
            } catch (error) {
                toast.error('Failed to delete lot. ' + (error.response?.data?.msg || 'Make sure it is empty.'));
                return false;
            }
        },
        async fetchAllReservations() {
            try {
                const response = await apiClient.get('/api/admin/reservations');
                this.reservations = response.data; // Add 'reservations: []' to state
            } catch (error) {                    
                toast.error("Failed to fetch reservations.");
            }
        },
        async fetchUsers() {
            try {
                const response = await apiClient.get('/api/admin/users');
                this.users = response.data;
            } catch (error) {
                console.error('Failed to fetch users:', error);
            }
        },
        async fetchAnalytics() {
            try {
                const response = await apiClient.get('/api/admin/analytics/summary');
                this.analytics = response.data;
            } catch (error) {
                console.error('Failed to fetch admin analytics:', error);
            }
        }
    }
});
