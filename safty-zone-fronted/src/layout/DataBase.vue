<script setup lang="ts">
import DataTable from "primevue/datatable";
import Column from 'primevue/column';
import Button from "primevue/button";
import {onMounted, ref} from 'vue';
import axios from "axios";
import {getApiUrl} from "../utils/getEnvData.ts";
import ReportDialog from "../components/Dialogs/ReportDialog.vue";

const dt = ref();
const data = ref([]);
const downloadReport = ref(false);

const exportCSV = ($event) => {
  dt.value.exportCSV();
};

const getReport = () => {
  downloadReport.value = true;
};

onMounted(() => {
  axios.get(`${getApiUrl()}/get_report_data`).then(
      (response: any) => data.value = response.data
  ).catch(
      (error) => console.error(error)
  );
})
</script>

<template>
  <div>
    <ReportDialog v-if="downloadReport" @closeDialog="downloadReport = false"/>
    <DataTable
        :value="data"
        showGridlines
        stripedRows
        scrollable
        scrollHeight="75vh"
        sortable
        :reorderableColumns="true"
        ref="dt"
        class="mt-3"
    >
      <template #header>
        <div style="text-align: right">
          <Button
              icon="pi pi-external-link"
              label="Отчет за месяц"
              @click="getReport()"
              style="background:white"
              class="mr-3"
          />
          <Button
              icon="pi pi-external-link"
              label="Экспортировать в CSV"
              @click="exportCSV($event)"
              style="color: white; background:transparent; border: 1px solid white"
          />
        </div>
      </template>
      <Column field="place" header="Название источника" sortable></Column>
      <Column field="intersection_percent" header="Процент вхождения в опасную зону" sortable></Column>
      <Column field="date" header="Время вхождения" sortable></Column>
      <Column field="responsible" header="Ответственный" sortable></Column>
    </DataTable>
  </div>
</template>

<style scoped lang="scss">

</style>