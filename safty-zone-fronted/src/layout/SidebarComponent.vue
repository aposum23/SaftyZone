<script setup lang="ts">
const incidents = [
  {
    level: 0,
    sourceName: 'Название источника'
  },
  {
    level: 1,
    sourceName: 'Название источника'
  },
  {
    level: 3,
    sourceName: 'Название источника'
  },
  {
    level: 2,
    sourceName: 'Название источника'
  },
  {
    level: 1,
    sourceName: 'Название источника'
  },
];
</script>

<template>
  <div class="sidebar">
    <template v-for="incident in incidents">
      <div class="grid sidebar__source">
        <div :class="`marker marker-${incident.level}`"></div>
        <p>{{incident.sourceName}}</p>
      </div>
    </template>
    <div>
      <p class="text-left ">Добавить источник</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .sidebar {
    margin-top: .5rem;
    width: 15vw;
    height: 100%;
    padding-left: 4rem;
    padding-right: 3rem;
    background: var(--mid-gray);
  }

  .sidebar__source {
    padding: .5rem 0;
    border-bottom: 2px solid var(--border-color);
  }

  .marker {
    width: 1.3rem;
    height: 1.3rem;
    border-radius: 90px;
    margin-top: 1.1rem;
    margin-right: .5rem;
  }

  .marker-0 {
    background:green;
  }

  .marker-1 {
    background:yellow;
  }

  .marker-2 {
    background:orange;
  }

  .marker-3 {
    background:red;
  }
</style>