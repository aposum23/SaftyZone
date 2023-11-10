<script setup lang="ts">

import HeaderComponent from "./HeaderComponent.vue";
import SidebarComponent from "./SidebarComponent.vue";
</script>

<template>
  <div class="container">
    <HeaderComponent />
    <SidebarComponent />
  </div>
</template>

<style scoped lang="scss">
  .container {
    height: 100vh;
    background: var(--grey);
  }
</style>