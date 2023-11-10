<script setup lang="ts">

const props = defineProps<{
  sourceName: string,
}>()
</script>

<template>
  <div class="grid card m-2">
    <div class="card__video col-12 p-0">
      <img src="@/assets/vue.svg" class="w-full h-full"/>
    </div>
    <div class="col-12 grid">
      <div class="col-6">
        <p>{{sourceName}}</p>
      </div>
      <div class="col-6">
        <p :class="`card__status px-4 ml-auto card__status-${0}`">{{'Подключено'}}</p>
      </div>
      <div class="col-5 card__button ml-3">
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

  .card__video {
    height: 17.6rem;
    & img {
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
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
</style>