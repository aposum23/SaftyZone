<script setup lang="ts">
import {getApiUrl} from "../../utils/getEnvData.ts";

const props = defineProps<{
  sourceName: string,
  fileName: string,
  incidentLevel: number
}>();

const emit = defineEmits<{
  "openMaskSettings": []
}>()

const messageVariants = [
    'Подключено',
    'Замечено движение',
    'Посторонний рядом',
    'В опасной зоне'
]
</script>

<template>
  <div class="grid card m-2 fadeindown animation-duration-300" :class="{'card__incident': incidentLevel === 1}">
    <div class="card__video col-12 p-0">
      <img :src="`${getApiUrl()}/video_feed/${fileName}`" class="w-full h-full"/>
      <div :class="`card__indicator card__indicator-${incidentLevel}`"></div>
    </div>
    <div class="col-12 grid">
      <div class="col-6">
        <p>{{sourceName}}</p>
      </div>
      <div class="col-6">
        <p :class="`card__status px-4 ml-auto card__status-${incidentLevel}`">{{messageVariants[incidentLevel]}}</p>
      </div>
      <div class="col-5 card__button ml-3" @click="emit('openMaskSettings')">
        <p>Настройка маски</p>
      </div>
      <div class="col-6 card__button ml-auto">
        <p>Включить индексацию</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .card {
    width: 30rem;
    background: var(--light-grey);
    border-radius: 10px;
    padding: 0 0 .5rem 0;
  }

  .card__incident {
    box-shadow: 5px 2px 5px rgb(158, 46, 46);
    border: 1px solid rgb(230, 22, 22)
  }

  .card__video {
    height: 17.6rem;
    & img {
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      z-index: 9;
    }
  }

  .card__status {
    width: fit-content;
  }

  .card__status-0 {
    border: 2px solid green;
    border-radius: 10px;
    color: green;
  }

  .card__status-1 {
    border: 2px solid #ae0000;
    background: red;
    border-radius: 10px;
    color: white;
  }

  .card__button {
    border: 2px solid var(--border-color);
    border-radius: 10px;
    & p {
      margin: 0;
    }
  }

  .card__button:hover {
    border: 2px solid var(--border-color-hover);
    color: var(--border-color-hover);
    cursor: pointer;
  }

  .card__indicator {
    z-index: 999;
    position: sticky;
    margin-top: -17rem;
    margin-left: auto;
    margin-right: 1rem;
    width: 1rem;
    height: 1rem;
    border-radius: 90px;
    background: blue;
  }

  .card__indicator-0 {
    background: green;
  }

  .card__indicator-1 {
    background: red;
  }
</style>