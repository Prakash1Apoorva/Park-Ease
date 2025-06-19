<template>
  <div class="landing-page">
    <!-- 1. Hero Section -->
    <section class="hero-section text-white text-center d-flex align-items-center">
      <div class="container">
        <h1 class="display-3 fw-bolder animate-on-scroll" ref="heroTitle">Park Smarter, Not Harder with Park Easy</h1>
        <p class="lead my-4 mx-auto animate-on-scroll" ref="heroSubtitle" style="max-width: 40rem;">
          The all-in-one solution for drivers to find spots and for administrators to manage lots. Simple, fast, and reliable.
        </p>
        <div class="animate-on-scroll" ref="heroButtons">
          <router-link to="/register" class="btn btn-light btn-lg me-2 px-4">Get Started Now</router-link>
          <router-link to="/login" class="btn btn-outline-light btn-lg px-4">Login</router-link>
        </div>
      </div>
    </section>

    <!-- 2. Features Section -->
    <section class="features-section py-5" ref="featuresSection">
      <div class="container">
        <div class="text-center mb-5 animate-on-scroll">
          <h2 class="fw-bold">Key Features</h2>
          <p class="text-muted">A powerful platform designed for both drivers and administrators.</p>
        </div>
        <div class="row text-center">
          <div class="col-md-4 mb-4 animate-on-scroll">
            <div class="feature-card p-4 h-100">
              <div class="feature-icon bg-primary bg-opacity-10 text-primary mb-3">
                <i class="fas fa-search-location fa-2x"></i>
              </div>
              <h4 class="fw-bold">Real-Time Availability</h4>
              <p class="text-muted">Find parking spots in real-time with up-to-the-minute availability updates across all our lots.</p>
            </div>
          </div>
          <div class="col-md-4 mb-4 animate-on-scroll">
            <div class="feature-card p-4 h-100">
              <div class="feature-icon bg-primary bg-opacity-10 text-primary mb-3">
                 <i class="fas fa-calendar-check fa-2x"></i>
              </div>
              <h4 class="fw-bold">Seamless Reservations</h4>
              <p class="text-muted">Reserve your parking spot in advance with just a few clicks, ensuring a space is waiting for you.</p>
            </div>
          </div>
          <div class="col-md-4 mb-4 animate-on-scroll">
            <div class="feature-card p-4 h-100">
              <div class="feature-icon bg-primary bg-opacity-10 text-primary mb-3">
                <i class="fas fa-credit-card fa-2x"></i>
              </div>
              <h4 class="fw-bold">Secure Payments</h4>
              <p class="text-muted">Pay for your parking securely and transparently through the app after you release your spot.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. How It Works Section -->
    <section class="how-it-works-section bg-light py-5" ref="howItWorksSection">
        <div class="container">
            <div class="text-center mb-5 animate-on-scroll">
                <h2 class="fw-bold">Get Parking in 3 Simple Steps</h2>
            </div>
            <div class="row">
                <div class="col-md-4 text-center mb-4 animate-on-scroll">
                    <div class="step-card">
                        <div class="step-number">1</div>
                        <h5 class="fw-bold mt-3">Search for Parking</h5>
                        <p class="text-muted">Enter your destination or browse the map to find available parking spaces.</p>
                    </div>
                </div>
                <div class="col-md-4 text-center mb-4 animate-on-scroll">
                    <div class="step-card">
                        <div class="step-number">2</div>
                        <h5 class="fw-bold mt-3">Reserve Your Spot</h5>
                        <p class="text-muted">Select your desired parking lot and reserve your spot instantly.</p>
                    </div>
                </div>
                <div class="col-md-4 text-center mb-4 animate-on-scroll">
                    <div class="step-card">
                        <div class="step-number">3</div>
                        <h5 class="fw-bold mt-3">Park and Pay</h5>
                        <p class="text-muted">Park in your reserved spot and pay seamlessly when you leave.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. Final Call to Action Section -->
    <section class="cta-section text-center py-5 text-white">
      <div class="container animate-on-scroll" ref="ctaSection">
        <h2 class="fw-bolder display-5">Ready to Experience Smarter Parking?</h2>
        <p class="lead my-4">Join today and enjoy the convenience of stress-free parking.</p>
        <router-link to="/register" class="btn btn-light btn-lg fw-bold px-5 py-3">Sign Up Today</router-link>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted, onUnmounted, ref } from 'vue';

export default {
  name: 'LandingView',
  setup() {
    const heroTitle = ref(null);
    const heroSubtitle = ref(null);
    const heroButtons = ref(null);
    const featuresSection = ref(null);
    const howItWorksSection = ref(null);
    const ctaSection = ref(null);
    
    let observer;

    onMounted(() => {
      observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });

      const elementsToAnimate = [
        heroTitle.value, heroSubtitle.value, heroButtons.value, ctaSection.value,
        ...featuresSection.value.querySelectorAll('.animate-on-scroll'),
        ...howItWorksSection.value.querySelectorAll('.animate-on-scroll'),
      ];
      
      elementsToAnimate.forEach(el => {
        if (el) observer.observe(el);
      });
    });

    onUnmounted(() => {
      if (observer) {
        observer.disconnect();
      }
    });

    return { heroTitle, heroSubtitle, heroButtons, featuresSection, howItWorksSection, ctaSection };
  }
}
</script>

<style scoped>
.landing-page {
  /* This removes the container padding from App.vue for this page specifically */
  margin-top: -3.5rem; 
}

.hero-section {
  background: linear-gradient(rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.7) 100%), url("https://images.unsplash.com/photo-1543357485-380927171d82?q=80&w=2070&auto=format&fit=crop");
  background-size: cover;
  background-position: center;
  min-height: 85vh;
  padding: 6rem 0;
}

.features-section .feature-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background-color: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.features-section .feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 1rem 1.5rem rgba(0,0,0,0.1);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.how-it-works-section .step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--bs-primary);
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem auto;
  border: 4px solid var(--bs-light);
  box-shadow: 0 0 0 4px var(--bs-primary);
}

.cta-section {
    background-color: var(--bs-primary);
}

/* --- Animation Styles --- */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

/* Staggered animation delays */
.features-section .animate-on-scroll:nth-child(2) { transition-delay: 0.15s; }
.features-section .animate-on-scroll:nth-child(3) { transition-delay: 0.3s; }
.how-it-works-section .animate-on-scroll:nth-child(2) { transition-delay: 0.15s; }
.how-it-works-section .animate-on-scroll:nth-child(3) { transition-delay: 0.3s; }

/* Different delays for the hero section for a more dramatic entrance */
.hero-section .animate-on-scroll:nth-child(1) { transition-delay: 0s; }
.hero-section .animate-on-scroll:nth-child(2) { transition-delay: 0.2s; }
.hero-section .animate-on-scroll:nth-child(3) { transition-delay: 0.4s; }

.animate-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
