<script setup lang="ts">
import { NuxtPage } from '#components';

</script>

<template>
  <div>
    <!-- Main Content -->
    <main>
      <NuxtPage /> <!-- This renders the page content (e.g., index.vue) -->
    </main>
  </div>
</template>

  
  <style scoped>
  .header {
    background-color: #007bff;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  
  .header nav ul {
    display: flex;
    justify-content: center;
    list-style: none;
    padding: 0;
  }
  
  .header nav ul li {
    margin: 0 1rem;
  }
  
  .header nav ul li a {
    color: white;
    text-decoration: none;
  }
  
  .footer {
    background-color: #f1f1f1;
    padding: 1rem;
    text-align: center;
    margin-top: 2rem;
  }
  </style>
  