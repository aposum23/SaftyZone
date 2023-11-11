<script setup lang="ts">
import HeaderComponent from "./HeaderComponent.vue";
import SidebarComponent from "./SidebarComponent.vue";
import MainContent from "./MainContent.vue";
import DataBase from "./DataBase.vue";
import { ref } from 'vue';

const currentPage = ref('cards');

const changePage = (page: string) => {
  currentPage.value = page;
}
</script>

<template>
  <div class="container">
    <HeaderComponent @changePage="changePage"/>
    <div class="grid mx-0 content-container">
      <SidebarComponent class="col-3" v-if="currentPage === 'cards'"/>
      <MainContent class="col-9" v-if="currentPage === 'cards'"/>
      <DataBase class="col-12" v-else-if="currentPage === 'data-base'"/>
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