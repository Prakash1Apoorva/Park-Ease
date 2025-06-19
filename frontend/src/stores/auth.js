import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import router from '@/router';
import { useToast } from 'vue-toastification';

const toast = useToast();

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isAdmin: (state) => state.user?.role === 'admin',
    },
    actions: {
        async login(credentials) {
            try {
                const response = await apiClient.post('/auth/login', credentials);
                const token = response.data.access_token;
                this.token = token;
                localStorage.setItem('token', token);
                
                await this.fetchProfile();

                toast.success(`Welcome, ${this.user.username}!`);
                if (this.isAdmin) {
                    router.push('/admin/dashboard');
                } else {
                    router.push('/dashboard');
                }
            } catch (error) {
                toast.error('Login failed: Invalid username or password.');
                console.error('Login failed:', error);
            }
        },
        async fetchProfile() {
            if (this.token) {
                try {
                    console.log("Attempting to fetch user profile with existing token...");
                    const response = await apiClient.get('/auth/profile');
                    this.user = response.data.logged_in_as;
                    localStorage.setItem('user', JSON.stringify(this.user));
                    console.log("Profile fetched successfully:", this.user);
                } catch (error) {
                    console.error('Failed to fetch profile with stored token. It is likely invalid or expired.', error);
                    toast.info('Your session has expired. Please log in again.');
                    // This logout will trigger the redirect to login, which is the correct behavior.
                    this.logout();
                }
            }
        },
        logout() {
            console.log("Logging out and clearing session data.");
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            router.push('/login');
        },
        async register(credentials) {
             try {
                await apiClient.post('/auth/register', credentials);
                toast.success("Registration successful! Logging you in...");
                await this.login({ username: credentials.username, password: credentials.password });
            } catch (error) {
                toast.error('Registration failed: ' + (error.response?.data?.msg || 'Please try again.'));
                console.error('Registration failed:', error);
            }
        }
    },
});
