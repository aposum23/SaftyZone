<script setup lang="ts">
import {useIndicatorsStatusStore} from "../stores/indicatorsStatus.ts";
import {storeToRefs} from "pinia";

const indicatorsStatusStore = useIndicatorsStatusStore();
const { incidentData } = storeToRefs(indicatorsStatusStore);
</script>

<template>
  <div class="sidebar">
    <template v-for="incident in incidentData">
      <div class="grid sidebar__source">
        <div :class="`marker marker-${incident.incidentLevel}`"></div>
        <p><a :href="`#${incident.name}`">{{incident.name}}</a></p>
      </div>
    </template>
    <div>
      <p class="text-left sidebar__source-add">Добавить источник</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .sidebar {
    margin-top: .5rem;
    height: 100%;
    padding-left: 4rem;
    padding-right: 3rem;
    background: var(--mid-gray);
    overflow: scroll;
  }

  .sidebar::-webkit-scrollbar {
    background: transparent;
    width: .5rem;
  }

  .sidebar::-webkit-scrollbar-thumb {
    background: var(--light-grey);
    border-radius: 10px;
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

  .sidebar__source-add {
    width: fit-content;
  }

  .sidebar__source-add:hover {
    color: var(--border-color-hover);
    cursor: pointer;
  }

  a {
    color: white;
  }
</style>