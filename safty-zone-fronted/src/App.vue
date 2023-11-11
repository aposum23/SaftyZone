<script setup lang="ts">
import AppContainer from "./layout/AppContainer.vue";
</script>

<template>
  <div>
    <AppContainer />
  </div>
</template>

<style lang="scss">
  #app {
    margin: 0;
    padding: 0;
    width: 100vw;
    max-width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  .p-dialog-header-icon {
    background-color: transparent !important;
    border-radius: 90px;
    width: 1rem;
    height: 2.5rem;
  }
</style>
