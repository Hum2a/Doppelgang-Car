<template>
    <div>
      <!-- Header -->
      <header class="header">
        <h1>CarClone</h1>
        <nav>
          <ul>
            <li><nuxt-link to="/">Home</nuxt-link></li>
            <li><nuxt-link to="/about">About</nuxt-link></li>
          </ul>
        </nav>
      </header>
  
      <!-- Main Content -->
      <main>
        <nuxt /> <!-- This renders the page content (e.g., index.vue) -->
      </main>
  
      <!-- Footer -->
      <footer class="footer">
        <p>&copy; 2025 CarClone</p>
      </footer>
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
  