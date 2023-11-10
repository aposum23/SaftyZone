<script setup lang="ts">
const props = defineProps<{
  sourceName: string
}>()
</script>

<template>
  <div class="grid notification-bar">
    <div class="col-11">
      <p>{{`${sourceName}: человек находиться в опасной зоне`}}</p>
    </div>
    <div class="col-1">
      <span class="material-icons-round notification-bar__close">close</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.notification-bar {
  background: #ff8484;
  border-radius: 10px;
  height: fit-content;
  & div {
    & p {
      margin: .1rem;
    }
  }
}

.notification-bar__close:hover {
  color: var(--border-color-hover);
  cursor: pointer;
}
</style>