export interface Schedule {
  startSchedule: string;
  endSchedule: string;
  enableSchedule: boolean;
  manualSchedule: boolean;
  lastState: number;
  deviceId: number;
  id: number;
}

const schedules: Schedule[] = [
  {
    startSchedule: '08:00:00',
    endSchedule: '18:00:00',
    enableSchedule: true,
    manualSchedule: true,
    lastState: 1,
    deviceId: 1,
    id: 1
  },
  {
    startSchedule: '09:00:00',
    endSchedule: '19:00:00',
    enableSchedule: false,
    manualSchedule: true,
    deviceId: 2,
    lastState: 1,
    id: 2
  }
];

export const getSchedules = () => schedules;

export const getSchedule = (id: number) => schedules.find(m => m.id === id);
