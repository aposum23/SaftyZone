import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useIndicatorsStatusStore = defineStore(
    'indicatorsStatus',
    () => {
        const incidentData = ref<{ [k: string]: any }[]>([]);
        const generateAlarm = ref<boolean>(false);
        const alarmSource = ref<string>('');

        return{
            incidentData,
            generateAlarm,
            alarmSource
        }
    })