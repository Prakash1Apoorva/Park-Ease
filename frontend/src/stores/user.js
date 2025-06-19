import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { useToast } from 'vue-toastification';
import router from '@/router';

const toast = useToast();

export const useUserStore = defineStore('user', {
    state: () => ({
        availableLots: [],
        reservations: [],
        analytics: null // Add user analytics state
    }),
    actions: {
        async fetchAvailableLots() {
            try {
                const response = await apiClient.get('/api/user/lots');
                this.availableLots = response.data;
            } catch (error) {
                console.error('Failed to fetch available lots:', error);
            }
        },
        async fetchReservations() {
            try {
                const response = await apiClient.get('/api/user/reservations');
                this.reservations = response.data;
            } catch (error) {
                console.error('Failed to fetch reservations:', error);
            }
        },
        async reserveSpot(lotId) {
            try {
                await apiClient.post(`/api/user/lots/${lotId}/reserve`);
                toast.success("Spot reserved!");
                await this.fetchAvailableLots();
                await this.fetchReservations();
            } catch (error) {
                toast.error("Failed to reserve spot. " + (error.response?.data?.msg || ''));
            }
        },
        async releaseSpot(reservationId) {
        try {
            // The API call returns the calculated cost
            const response = await apiClient.post(`/api/user/reservations/${reservationId}/release`);
            const cost = response.data.total_cost;
            
            // Instead of just showing a toast, we redirect to the payment page
            router.push({ 
            name: 'payment', 
            params: { 
                reservationId: reservationId, 
                cost: cost.toFixed(2) 
            } 
            });

            // We can still update the state in the background
            this.fetchAvailableLots();
            this.fetchReservations();
        } catch (error) {
            toast.error("Failed to release spot.");
        }
        },

        // NEW ACTIONS
        async fetchAnalytics() {
            try {
                const response = await apiClient.get('/api/user/analytics/summary');
                this.analytics = response.data;
            } catch (error) {
                console.error('Failed to fetch user analytics:', error);
            }
        },
        async triggerCsvExport() {
            try {
                await apiClient.post('/api/user/export/csv');
                toast.info("CSV export started! You will be notified when it's ready.");
            } catch (error) {
                toast.error("Failed to start CSV export.");
            }
        }
    }
});