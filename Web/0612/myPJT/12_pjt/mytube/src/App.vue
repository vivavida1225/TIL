<template>
  <div id="app">
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
        <router-link class="navbar-brand fw-bold fs-4" to="/">
          <i class="fa-brands fa-youtube me-1 text-danger"></i>MyTube
        </router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navContent"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navContent">
          <ul class="navbar-nav ms-3 gap-1">
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.name === 'home' }" to="/">
                <i class="fa-solid fa-house me-1"></i>Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.name === 'search' }" to="/search">
                <i class="fa-solid fa-magnifying-glass me-1"></i>Search
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.name === 'saved' }" to="/saved">
                <i class="fa-regular fa-clock me-1"></i>Later
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{ active: $route.name === 'channels' }" to="/channels">
                <i class="fa-solid fa-tv me-1"></i>Channel
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <main class="container py-4">
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.navbar .nav-link.active {
  color: #fff !important;
  font-weight: 600;
  border-bottom: 2px solid #dc3545;
  padding-bottom: 2px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #6c757d;
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  transition: color 0.2s;
}
.back-btn:hover {
  color: #212529;
}
</style>
