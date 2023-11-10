<script setup lang="ts">
import VideoCard from "../components/videoCard/VideoCard.vue";
import AddSource from "../components/videoCard/AddSource.vue";
import NotificationBar from "../components/notifications/NotificationBar.vue";

const sources = [
  'Источник 1',
  'Источник 2',
  'Источник 3',
  'Источник 4',
  'Источник 5',
  'Источник 6',
  'Источник 7',
  'Источник 8',
  'Источник 9',
]
</script>

<template>
  <div class="content grid justify-content-center">
    <NotificationBar source-name="Источник 1" class="col-11 mt-1"/>
    <template v-for="source in sources">
      <VideoCard :sourceName="source" class="col-6 mx-5 my-3"/>
    </template>
    <AddSource class="col-6 mx-5 my-3"/>
  </div>
</template>

<style scoped lang="scss">
 .content {
   margin-top: .5rem;
   height: 100%;
   overflow-y: scroll;
 }

 .content::-webkit-scrollbar {
   background: transparent;
   width: .5rem;
 }

 .content::-webkit-scrollbar-thumb {
   background: var(--light-grey);
   border-radius: 10px;
 }
</style>