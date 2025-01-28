<template>
    <div class="landing-page">
      <h1>Welcome to CarClone</h1>
      <p>Find out what car you resemble!</p>
  
      <form @submit.prevent="uploadImage">
        <label for="file-input" class="file-label">Choose a photo:</label>
        <input 
          type="file" 
          id="file-input" 
          @change="handleFileInput" 
          accept="image/*" 
          class="file-input"
        />
        <button type="submit" :disabled="!selectedFile" class="upload-btn">
          Upload and Match
        </button>
      </form>
  
      <div v-if="selectedFile" class="file-info">
        <h3>Uploaded File:</h3>
        <p>Name: {{ selectedFile.name }}</p>
      </div>
  
      <div v-if="result" class="result">
        <h2>Your Match:</h2>
        <p>{{ result }}</p>
      </div>
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedFile: null, // Store the uploaded file
        result: null, // Store the backend result
        error: null, // Add error state
      };
    },
    layout: 'default', // Explicitly set the layout
    methods: {
      handleFileInput(event) {
        this.selectedFile = event.target.files[0];
      },
      async uploadImage() {
        if (!this.selectedFile) return;
  
        const formData = new FormData();
        formData.append("file", this.selectedFile);
  
        try {
          const response = await fetch("http://127.0.0.1:5000/process-photo", {
            method: "POST",
            body: formData,
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
  
          const data = await response.json();
          this.result = data.car;
          this.error = null; // Reset error state
        } catch (error) {
          console.error("Error uploading image:", error);
          this.error = "Something went wrong. Please try again."; // Set error message
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Basic styles for the landing page */
  .landing-page {
    text-align: center;
    margin: 2rem auto;
    padding: 2rem;
    max-width: 600px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .file-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
  .file-input {
    margin-bottom: 1rem;
  }
  
  .upload-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .upload-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .result {
    margin-top: 2rem;
    font-size: 1.2rem;
    color: #333;
  }
  
  .error {
    margin-top: 2rem;
    font-size: 1.2rem;
    color: #dc3545;
  }
  
  .file-info {
    margin-top: 1rem;
    font-size: 1.2rem;
    color: #333;
  }
  </style>
  