<script setup lang="ts">
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import FileUpload from 'primevue/fileupload';
import {ref, watch} from "vue";

const emit = defineEmits<{
  "closeDialog": []
}>();

const visible = ref(true);
const tabType = ref('camera')
const sourceName = ref('');
const address = ref('');
const password = ref('');
const validation = ref(false);

watch(
    () => visible.value,
    () => emit('closeDialog')
);

const saveChanges = () => {
  if (!!sourceName.value) {
    console.log('Видео отправлено');
    emit('closeDialog');
  }
  else {
    validation.value = true;
  }
}
</script>

<template>
  <Dialog v-model:visible="visible" modal closable header="Добавить источник" draggable closeOnEscape>
    <div class="grid spource-dialog">
      <div class="col-12">
        <Button @click="tabType = 'camera'" class="mx-2 w-10rem" label="IP Камеру" :style="`${tabType !== 'camera' ? 'border: 1px solid white; background: transparent' : 'background: white'}`" rounded :outlined="tabType !== 'camera'" plain></Button>
        <Button @click="tabType = 'video'" class="mx-2 w-10rem" label="Видео" :style="`${tabType !== 'video' ? 'border: 1px solid white; background: transparent' : 'background: white'}`" rounded :outlined="tabType !== 'video'" plain></Button>
      </div>
      <div class="col-12" style="width: 30rem">
        <InputText type="text"  placeholder="Имя источника" v-model="sourceName" class="w-full my-2" :style="`${validation ? 'border-color: red' : ''}`"></InputText>
        <InputText type="text" placeholder="Адресс" v-model="address" class="w-14rem" v-if="tabType === 'camera'"></InputText>
        <InputText type="text" placeholder="Пароль" v-model="password" class="w-14rem ml-3" v-if="tabType === 'camera'"></InputText>
        <FileUpload choose-label="Выбрать" mode="basic" name="demo[]" url="/api/upload" accept="image/*" v-if="tabType === 'video'"/>
      </div>
    </div>
    <template #closeicon>
      <span class="material-icons-round">close</span>
    </template>
    <template #footer>
      <Button @click="saveChanges()" label="Сохранить" style="background: white" rounded plain></Button>
    </template>
  </Dialog>
</template>

<style scoped lang="scss">
  .spource-dialog {
    width: 30rem;
  }
</style>