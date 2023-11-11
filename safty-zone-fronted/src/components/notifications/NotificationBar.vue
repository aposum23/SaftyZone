<script setup lang="ts">
const props = defineProps<{
  sourceName: string
}>();

const emit = defineEmits<{
  "closeNotificationBar": []
}>();
</script>

<template>
  <div class="grid notification-bar fadeindown">
    <audio autoplay href=""/>
    <div class="col-11">
      <p>{{`${sourceName}: человек находится в опасной зоне`}}</p>
    </div>
    <div class="col-1">
      <span class="material-icons-round notification-bar__close" @click="emit('closeNotificationBar')">close</span>
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