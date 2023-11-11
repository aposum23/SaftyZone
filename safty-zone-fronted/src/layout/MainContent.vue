<script setup lang="ts">
import VideoCard from "../components/videoCard/VideoCard.vue";
import AddSource from "../components/videoCard/AddSource.vue";
import NotificationBar from "../components/notifications/NotificationBar.vue";
import {onMounted, ref} from "vue";
import {getApiUrl} from "../utils/getEnvData.ts";
import {useIndicatorsStatusStore} from "../stores/indicatorsStatus.ts";
import {storeToRefs} from "pinia";
import ZoneSelection from "../components/Dialogs/ZoneSelection.vue";
import IncidentReaction from "../components/Dialogs/IncidentReaction.vue";
import AddSourceDialog from "../components/Dialogs/AddSourceDialog.vue";

const sources = ref<{[k: string]: any}>([]);
const indicatorsStatusStore = useIndicatorsStatusStore();
const { incidentData, generateAlarm, alarmSource } = storeToRefs(indicatorsStatusStore);
const showNotifBar = ref(false);
const currentContent = ref('cards');
const currentVideo = ref('');
let counter = 0;

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
        // if (counter < 1) {
          currentVideo.value = value.file;
          currentContent.value = 'incident';
        // }
        alarmSource.value = value.name;
        counter++;
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
  <NotificationBar v-if="generateAlarm && showNotifBar" :source-name="alarmSource" class="notif-bar mt-1" @closeNotificationBar="showNotifBar = false"/>
    <template v-for="source in sources">
      <VideoCard :id="source.name" :sourceName="source.name" :fileName="source.file" :incidentLevel="source.incidentLevel" class="col-6 mx-5 my-3" @openMaskSettings="openMaskSettings(source.file)"/>
    </template>
    <div @click="currentContent = 'add-source'">
      <AddSource class="col-6 mx-5 my-3"/>
    </div>
    <ZoneSelection
        v-if="currentContent === 'maskSettings'"
        :current-video="currentVideo"
        @closeDialog="currentContent = ''"
    />
    <IncidentReaction
        v-else-if="currentContent === 'incident'"
        :current-video="currentVideo"
        @closeDialog="currentContent = ''"
    />
    <AddSourceDialog
        v-else-if="currentContent === 'add-source'"
        @closeDialog="currentContent = ''"
    />
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

 .notif-bar {
   width: 87%;
 }
</style>