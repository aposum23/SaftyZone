<script setup lang="ts">
import {ref, toRefs, watch} from "vue";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import {getApiUrl} from "../../utils/getEnvData.ts";

const props = defineProps<{
  currentVideo: string,
}>();

const emit = defineEmits<{
  "closeDialog": []
}>();

const { currentVideo } = toRefs(props);
const visible = ref(true);

watch(
    () => visible.value,
    () => emit('closeDialog')
);
</script>

<template>
  <Dialog v-model:visible="visible" modal closable header="Реакция на инцидент" draggable closeOnEscape class="text-center">
    <img :src="`${getApiUrl()}/video_feed/${currentVideo}`"/>
    <audio autoplay src="../../src/assets/audio/alert.mp3"/>
    <template #closeicon>
      <span class="material-icons-round">close</span>
    </template>
    <template #footer>
      <Button @click="visible = false" label="Отключить питание" style="background: transparent; border: 1px solid white" rounded outlined plain class="w-18rem"></Button>
      <Button @click="visible = false" label="Включить пожаротушение" style="background: transparent; border: 1px solid white" rounded outlined plain class="w-18rem"></Button>
      <Button @click="visible = false" label="Включить предупреждение" style="background: transparent; border: 1px solid white" rounded outlined plain class="w-18rem"></Button>
    </template>
  </Dialog>
</template>

<style scoped lang="scss">
  img {
    width: 30rem;
    height: 17.6rem;
    border-radius: 10px;
  }
</style>