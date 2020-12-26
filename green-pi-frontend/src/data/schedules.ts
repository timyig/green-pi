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
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules`)
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
      delete schd.start_schedule;
      delete schd.end_schedule;
      delete schd.enable_schedule;
      delete schd.manual_schedule;
      delete schd.last_state;
      delete schd.device_id;
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
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules/${id}`)
  .then((response) => response.json())
  .then((data) => {
    data.startSchedule = data.start_schedule;
    data.endSchedule = data.end_schedule;
    data.enableSchedule = data.enable_schedule;
    data.manualSchedule = data.manual_schedule;
    data.lastState = data.last_state;
    data.deviceId = data.device_id;
    delete data.start_schedule;
    delete data.end_schedule;
    delete data.enable_schedule;
    delete data.manual_schedule;
    delete data.last_state;
    delete data.device_id;
    return data;
  })
  .catch((error) => {
    console.error(error);
  });
};

export const deleteSchedule = (id: number) => {
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules/${id}`, {
    method: 'DELETE'
  }).then(response => response.json())
  .catch((error) => {
    console.error(error);
  });
}

export const enableSchedule = (id: number) => {
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "enable_schedule": true
    }),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .catch((error) => {
    console.error(error);
  });
}

export const disableSchedule = (id: number) => {
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "enable_schedule": false
    }),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .catch((error) => {
    console.error(error);
  });
}

export const updateSchedule = (id: number, data: Schedule) => {
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      "start_schedule": data.startSchedule,
      "end_schedule": data.endSchedule,
      "enable_schedule": data.enableSchedule,
      "device_id": data.deviceId
    }),
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .catch((error) => {
    console.error(error);
  });
}

export const createSchedule = (data: Schedule) => {
  return fetch(`${process.env.GREEN_PI_BACKEND_HOST}/schedules`, {
    method: 'POST',
    body: JSON.stringify({
      "start_schedule": data.startSchedule,
      "end_schedule": data.endSchedule,
      "enable_schedule": data.enableSchedule,
      "device_id": data.deviceId
    }),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .catch((error) => {
    console.error(error);
  });
}