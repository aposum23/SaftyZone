<script setup lang="ts">
import Button from "primevue/button";
import Dropdown from 'primevue/dropdown';
import Dialog from "primevue/dialog";
import {onMounted, ref, watch} from "vue";
import axios from "axios";
import {getApiUrl} from "../../utils/getEnvData.ts";

const emit = defineEmits<{
  "closeDialog": []
}>();

const visible = ref(true);
const availableSelects = ref([]);
const selectedValue = ref();

watch(
    () => visible.value,
    () => emit('closeDialog')
);

const downloadReport = () => {
  axios.post(`${getApiUrl()}/report`,
      {cameras: [selectedValue.value.code]
  }).then(
      (response:any) => {
        let a = document.createElement("a");
        let file = new Blob([response.data], {type: 'application/json'});
        a.href = URL.createObjectURL(file);
        a.download = "report.pdf";
        a.click();
      }
  ).catch(
      (error) => console.error(error)
  )
  visible.value = false;
}

onMounted(() => {
  axios.get(`${getApiUrl()}/get_all_cameras_info`).then(
      (response: any) => {
        availableSelects.value = response.data
      }
  ).catch(
      (error) => console.error(error)
  );
})
</script>

<template>
  <Dialog v-model:visible="visible" modal closable header="Скачать отчет за месяц" draggable closeOnEscape>
    <div class="grid spource-dialog p-2">
      <Dropdown v-model="selectedValue" :options="availableSelects" optionLabel="name" placeholder="Выберете источник" class="w-full" />
    </div>
    <template #closeicon>
      <span class="material-icons-round">close</span>
    </template>
    <template #footer>
      <Button @click="downloadReport()" label="Скачать" style="background: white" rounded plain></Button>
    </template>
  </Dialog>
</template>

<style scoped lang="scss">

</style>