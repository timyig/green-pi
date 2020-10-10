export interface Schedule {
  startSchedule: string;
  endSchedule: string;
  enableSchedule: boolean;
  manualSchedule: boolean;
  lastState: number;
  deviceId: number;
  id: number;
}

export const getSchedules = () => {
  return fetch('http://localhost:8000/schedules')
  .then((response) => response.json())
  .then((data) => {
    Object.keys(data).map((key) => {
      let schd = data[key];
      schd.startSchedule = schd.start_schedule;
      schd.endSchedule = schd.end_schedule;
      schd.enableSchedule = schd.enable_schedule;
      schd.manualSchedule = schd.manual_schedule;
      schd.lastState = schd.last_state;
      schd.deviceId = schd.device_id;
      return schd;
    });
    console.log(data);
    return data;
  })
  .catch((error) => {
    console.error(error);
  });
};

export const getSchedule = (id: number) => {
  return fetch(`http://localhost:8000/schedules/${id}`)
  .then((response) => response.json())
  .then((data) => {
    data.startSchedule = data.start_schedule;
    data.endSchedule = data.end_schedule;
    data.enableSchedule = data.enable_schedule;
    data.manualSchedule = data.manual_schedule;
    data.lastState = data.last_state;
    data.deviceId = data.device_id;
    return data;
  })
  .catch((error) => {
    console.error(error);
  });
};
