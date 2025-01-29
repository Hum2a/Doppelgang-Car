<template>
  <div class="container">
    <!-- Hero Section -->
    <div class="hero fade-in">
      <h1 class="title">CarClone 🚗</h1>
      <p class="subtitle">Find out which car best matches your personality!</p>
    </div>

    <!-- Upload Card -->
    <div class="upload-card slide-up">
      <transition name="fade">
        <div v-if="!imagePreview" class="upload-placeholder">
          <label for="file-upload" class="upload-label">
            <div class="upload-icon">
              <svg class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V12M17 16V12M5 20h14a2 2 0 002-2V9a2 2 0 00-2-2h-4l-2-3h-4l-2 3H5a2 2 0 00-2 2v9a2 2 0 002 2z" />
              </svg>
            </div>
            <span class="upload-text">Click to upload an image</span>
          </label>
          <input type="file" id="file-upload" @change="handleFileInput" accept="image/*" class="hidden" />
        </div>
      </transition>

      <transition name="slide">
        <div v-if="imagePreview" class="preview-container">
          <img :src="imagePreview" alt="Uploaded Image" class="preview-image" />
          <button @click="clearImage" class="remove-btn">Remove Image</button>
        </div>
      </transition>

      <button @click="uploadImage" :disabled="!selectedFile" class="upload-btn">Find My Car 🚗</button>
    </div>

    <!-- Loading Spinner -->
    <transition name="bounce">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">Analyzing your face...</p>
      </div>
    </transition>

    <!-- Results Section -->
    <transition name="fade">
      <div v-if="result" class="result-card">
        <h2 class="result-title">Your Car Match 🚗</h2>
        <p class="result-text">{{ result.make }} - {{ result.model }} ({{ result.year }})</p>
        <img v-if="result.image_url" :src="result.image_url" class="car-image" alt="Matched Car Image" />
      </div>
    </transition>

    <transition name="fade">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      imagePreview: null,
      result: null,
      error: null,
      loading: false
    };
  },
  methods: {
    handleFileInput(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.selectedFile = file;
      this.imagePreview = URL.createObjectURL(file);
    },
    clearImage() {
      this.selectedFile = null;
      this.imagePreview = null;
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.result = null;
      this.error = null;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await fetch("http://127.0.0.1:5000/process-photo", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) throw new Error("Something went wrong. Try again.");

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        this.result = data.car;
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.slide-enter-active, .slide-leave-active {
  transition: transform 0.4s ease-in-out, opacity 0.4s;
}
.slide-enter {
  transform: translateY(10px);
  opacity: 0;
}
.slide-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce 0.8s infinite;
}

/* Layout */
.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #0f172a;
  color: white;
  padding: 1rem;
}

/* Hero Section */
.hero {
  text-align: center;
  margin-bottom: 2rem;
  animation: fadeIn 1s ease-in-out;
}
.title {
  font-size: 2.5rem;
  font-weight: bold;
}
.subtitle {
  font-size: 1.2rem;
  color: #94a3b8;
}

/* Upload Card */
.upload-card {
  background-color: #1e293b;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

/* Upload Placeholder */
.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.upload-icon {
  width: 80px;
  height: 80px;
  background-color: #334155;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon {
  width: 40px;
  height: 40px;
  color: #94a3b8;
}
.upload-text {
  margin-top: 8px;
  font-size: 0.9rem;
  color: #cbd5e1;
}

/* Preview Image */
.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.preview-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
  border: 2px solid #475569;
}
.remove-btn {
  margin-top: 10px;
  font-size: 0.8rem;
  color: #f87171;
  cursor: pointer;
}
.remove-btn:hover {
  color: #ef4444;
}

/* Upload Button */
.upload-btn {
  margin-top: 1rem;
  width: 100%;
  background-color: #2563eb;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}
.upload-btn:active {
  transform: scale(0.95);
}

/* Loading */
.loading-container {
  margin-top: 1.5rem;
  text-align: center;
}
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.car-image {
  width: 100%;
  max-width: 400px;
  border-radius: 10px;
  margin-top: 1rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}
</style>
