<script setup lang="ts">
import {useIndicatorsStatusStore} from "../stores/indicatorsStatus.ts";
import {storeToRefs} from "pinia";
import EmptyNotif from '../assets/images/empty-notification.svg';
import FullNotif from '../assets/images/full-notification.svg';

const emit = defineEmits<{
  "changePage": [string]
}>();

const indicatorsStatusStore = useIndicatorsStatusStore();
const { generateAlarm } = storeToRefs(indicatorsStatusStore);
</script>

<template>
  <div class="grid w-full h-5rem m-0 header">
    <div class="col-2">
      <h3 @click="emit('changePage', 'cards')" class="cursor-pointer">Источники</h3>
    </div>
    <div class="col-2 text-left">
      <h3 @click="emit('changePage', 'data-base')" class="cursor-pointer">База данных</h3>
    </div>
    <div class="col-6"></div>
    <div class="col-2 header__notification">
      <img :src="generateAlarm ? FullNotif : EmptyNotif"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
.header {
  background: var(--light-grey);
}

.header__notification {
  line-height: 4.7rem;
  & img {
    width: 1.5rem;
    height: 1.5rem;
  }
}
</style>