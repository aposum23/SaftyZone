<script setup lang="ts">
import HeaderComponent from "./HeaderComponent.vue";
import SidebarComponent from "./SidebarComponent.vue";
import MainContent from "./MainContent.vue";
</script>

<template>
  <div class="container">
    <HeaderComponent />
    <div class="grid mx-0 content-container">
      <SidebarComponent class="col-3"/>
      <MainContent class="col-9"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .container {
    height: 100vh;
    background: var(--grey);
  }

  .content-container {
    height: calc(100% - 5rem);
  }
</style>