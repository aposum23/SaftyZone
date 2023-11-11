<script setup lang="ts">
import VideoCard from "../components/videoCard/VideoCard.vue";
import AddSource from "../components/videoCard/AddSource.vue";
import NotificationBar from "../components/notifications/NotificationBar.vue";
import {onMounted, ref} from "vue";
import {getApiUrl} from "../utils/getEnvData.ts";
import {useIndicatorsStatusStore} from "../stores/indicatorsStatus.ts";
import {storeToRefs} from "pinia";
import MaskSettings from "../components/videoCard/MaskSettings.vue";

const sources = ref<{[k: string]: any}>([]);
const indicatorsStatusStore = useIndicatorsStatusStore();
const { incidentData, generateAlarm, alarmSource } = storeToRefs(indicatorsStatusStore);
const showNotifBar = ref(false);
const currentContent = ref('cards');
const currentVideo = ref('');

const openMaskSettings = (fileName: string) => {
  currentVideo.value = fileName
  currentContent.value = 'maskSettings';
}

onMounted(() => {
  let eventSource;
  eventSource = new EventSource(`${getApiUrl()}/sse`);
  eventSource.onmessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);
    let result = [];
    for (const key of Object.keys(data)) {
      result.push({name: key, file: key, incidentLevel: data[key].is_intersection})
    }
    generateAlarm.value = false;
    for (const value of result) {
      if (value.incidentLevel === 1) {
        generateAlarm.value = true;
        showNotifBar.value = true;
        alarmSource.value = value.name;
        break;
      }
    }
    sources.value = result;
    if (showNotifBar.value) incidentData.value = result;
  }
})
</script>

<template>
  <div class="content grid justify-content-center">
    <NotificationBar v-if="generateAlarm && showNotifBar" :source-name="alarmSource" class="col-11 mt-1" @closeNotificationBar="showNotifBar = false"/>
    <template v-if="currentContent === 'cards'">
      <template v-for="source in sources">
        <VideoCard :id="source.name" :sourceName="source.name" :fileName="source.file" :incidentLevel="source.incidentLevel" class="col-6 mx-5 my-3" @openMaskSettings="openMaskSettings(source.file)"/>
      </template>
      <AddSource class="col-6 mx-5 my-3"/>
    </template>
    <template v-else-if="currentContent === 'maskSettings'">
      <MaskSettings :current-video="currentVideo" class="col-12"/>
    </template>
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