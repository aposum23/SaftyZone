<script setup lang="ts">
import {ref, watch} from 'vue';
import {getApiUrl} from "../../utils/getEnvData.ts";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import axios from "axios";

const props = defineProps<{
  currentVideo: string,
}>();

const emit = defineEmits<{
  "closeDialog": []
}>();

const visible = ref(true);
let canvasFigurePoints = []

watch(
    () => visible.value,
    () => emit('closeDialog')
);

const canvasClickHandler = (evt: any) => {
  canvasFigurePoints.push({x: evt.offsetX, y: evt.offsetY});
  if (canvasFigurePoints.length > 1) {
    const canvas:any = document.getElementById('video-canvas');
    if (canvas.getContext){
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0,0, canvas.width, canvas.height);
      ctx.lineWidth = 2;
      ctx.strokeStyle = '#ff0000';
      ctx.beginPath();
      ctx.moveTo(canvasFigurePoints[0].x, canvasFigurePoints[0].y);
      for (let i = 1; i < canvasFigurePoints.length; i++){
        ctx.lineTo(canvasFigurePoints[i].x, canvasFigurePoints[i].y);
      }
      if (canvasFigurePoints.length > 2) {
        ctx.lineTo(canvasFigurePoints[0].x, canvasFigurePoints[0].y);
      }
      ctx.stroke();
    }
  }
}

const dropChanges =() => {
  const canvas:any = document.getElementById('video-canvas');
  if (canvas.getContext) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvasFigurePoints.length = 0;
  }
  axios.post(`${getApiUrl()}/mask/${props.currentVideo}`, {userSelection: canvasFigurePoints})
}

const saveChanges = () => {
  const requestData = []
  const canvas:any = document.getElementById('video-canvas');
  for (let point of canvasFigurePoints) {
    requestData.push({x: point.x / canvas.width, y: point.y / canvas.height})
  }
  if (requestData.length > 3) {
    axios.post(`${getApiUrl()}/mask/${props.currentVideo}`, {userSelection: requestData})
    visible.value = false;
  }
  else {
    canvasFigurePoints.length = 0;
    const canvas:any = document.getElementById('video-canvas');
    if (canvas.getContext) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      canvasFigurePoints.length = 0;
    }
  }
}
</script>

<template>
  <Dialog v-model:visible="visible" modal closable header="Выбор опасной области" draggable closeOnEscape>
    <div class="justify-content-center">
      <div class="">
        <canvas
            width="700"
            height="411.6"
            id="video-canvas"
            class="video"
            :style="`
           background: url(${getApiUrl()}/video_feed/${currentVideo});
           background-size: cover;
           background-repeat: no-repeat;
           background-position-x: center;`"
            @click="canvasClickHandler"
        >
        </canvas>
      </div>
    </div>
    <template #closeicon>
      <span class="material-icons-round">close</span>
    </template>
    <template #footer>
      <Button @click="saveChanges()" label="Сохранить" style="background: white" rounded plain></Button>
      <Button @click="dropChanges()" label="Сбросить" style="background: transparent; border: 1px solid white" rounded outlined plain></Button>
    </template>
  </Dialog>
</template>

<style scoped lang="scss">
</style>