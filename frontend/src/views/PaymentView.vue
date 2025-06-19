<template>
  <div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
      <div class="card shadow-sm">
        <div class="card-header bg-primary text-white text-center">
          <h4>Complete Your Payment</h4>
        </div>
        <div class="card-body p-4">
          <div class="text-center mb-4">
            <p class="lead">Total Amount Due</p>
            <h1 class="display-4 fw-bold">${{ cost }}</h1>
            <p class="text-muted">For parking reservation #{{ reservationId }}</p>
          </div>

          <hr>

          <h5 class="mb-3">Dummy Payment Information</h5>
          <form @submit.prevent="handlePayment">
            <div class="mb-3">
              <label for="cardNumber" class="form-label">Card Number</label>
              <input type="text" class="form-control" id="cardNumber" value="**** **** **** 4242" disabled>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="expiryDate" class="form-label">Expiry Date</label>
                <input type="text" class="form-control" id="expiryDate" value="12/26" disabled>
              </div>
              <div class="col-md-6 mb-3">
                <label for="cvv" class="form-label">CVV</label>
                <input type="text" class="form-control" id="cvv" value="***" disabled>
              </div>
            </div>
            <div class="d-grid">
              <button type="submit" class="btn btn-success btn-lg">
                <i class="fas fa-lock"></i> Pay Now
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

export default {
  name: 'PaymentView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const toast = useToast();

    const reservationId = route.params.reservationId;
    const cost = parseFloat(route.params.cost).toFixed(2);

    const handlePayment = () => {
      // Simulate payment success
      toast.success(`Payment of $${cost} was successful!`);
      
      // Redirect back to the dashboard after a short delay
      setTimeout(() => {
        router.push('/dashboard');
      }, 1500);
    };

    return {
      reservationId,
      cost,
      handlePayment
    };
  }
};
</script>
