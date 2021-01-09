import React, { useState, useContext, FormEvent } from 'react';
import { Schedule, getSchedule, updateSchedule, createSchedule } from '../data/schedules';

import {
  IonBackButton,
  IonButton,
  IonInput,
  IonIcon,
  IonNote,
  IonButtons,
  IonContent,
  IonHeader,
  IonItem,
  IonLabel,
  IonPage,
  IonToolbar,
  IonList,
  IonToggle,
  IonRange,
  IonSelect,
  IonSelectOption,
  IonDatetime,
  useIonViewWillEnter
} from '@ionic/react';
import { thermometer } from 'ionicons/icons';
import { RouteComponentProps, Router } from 'react-router';
import {NavContext} from '@ionic/react'
import './UpdateSchedule.css';
import ScheduleListItem from '../components/ScheduleListItem';

interface UpdateScheduleProps extends RouteComponentProps<{ id: string; }> { }

const UpdateSchedule: React.FC<UpdateScheduleProps> = ({ match }) => {

  const [schedule, setSchedule] = useState<Schedule>();
  const {goBack} = useContext(NavContext);
  
  useIonViewWillEnter(() => {
    let scheduleId = parseInt(match.params.id, 10)
    if (isNaN(scheduleId)) {
      setSchedule({
        startSchedule: '08:00:00',
        endSchedule: '18:00:00',
        enableSchedule: true,
        manualSchedule: true,
        lastState: 0,
        deviceId: 1,
        id: -1,
        sensor: "",
      });
    }
    else {
      getSchedule(parseInt(match.params.id, 10)).then((schd) => {
        setSchedule(schd);
      });
    }
  });

  const handleSubmit = (e: FormEvent<HTMLFormElement>, schedule: Schedule) => {
    e.preventDefault();
    let scheduleId = parseInt(match.params.id, 10);
    if (isNaN(scheduleId)) {
      createSchedule(schedule);
    } else {
      updateSchedule(scheduleId, schedule);
    }
    goBack("/home");
  }

  const handleSensorChange = (e: CustomEvent, schedule: Schedule) => {
    setSchedule({...schedule, sensor: e.detail.value || ""});
  }

  return (

    <IonPage id="view-schedule-page">
      <IonHeader translucent>
        <IonToolbar>
          <IonButtons>
            <IonBackButton text="Schedules" defaultHref="/home"></IonBackButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen>
        {schedule ? (
          <form className="ion-padding" onSubmit={e => handleSubmit(e, schedule)}>
          <IonList>
            <IonItem>
              <IonLabel>Schedule From</IonLabel>
              <IonDatetime displayFormat="HH:mm" value={schedule.startSchedule} onIonChange={e => setSchedule({...schedule, startSchedule:e.detail.value!})}></IonDatetime>
            </IonItem>
            <IonItem>
              <IonLabel>Schedule To</IonLabel>
              <IonDatetime displayFormat="HH:mm" value={schedule.endSchedule} onIonChange={e => setSchedule({...schedule, endSchedule:e.detail.value!})}></IonDatetime>
            </IonItem>
            <IonItem>
              <IonLabel>Enabled {JSON.stringify(schedule.deviceId)}</IonLabel>
              <IonToggle checked={schedule.enableSchedule} onIonChange={e => setSchedule({...schedule, enableSchedule:e.detail.checked})} />
            </IonItem>
            <IonItem>
              <IonLabel>Device ID</IonLabel>
              <IonSelect value={String(schedule.deviceId)} placeholder="Select Device ID" onIonChange={e => setSchedule({...schedule, deviceId: e.detail.value})}>
                <IonSelectOption value="0">0</IonSelectOption>
                <IonSelectOption value="1">1</IonSelectOption>
                <IonSelectOption value="2">2</IonSelectOption>
                <IonSelectOption value="3">3</IonSelectOption>
                <IonSelectOption value="4">4</IonSelectOption>
                <IonSelectOption value="5">5</IonSelectOption>
                <IonSelectOption value="6">6</IonSelectOption>
                <IonSelectOption value="7">7</IonSelectOption>
              </IonSelect>
            </IonItem>
            <IonItem>
              <IonLabel>Sensor</IonLabel>
              <IonSelect value={String(schedule.sensor? schedule.sensor : "")} placeholder="Select Sensor" onIonChange={e => handleSensorChange(e, schedule)}>
                <IonSelectOption value="">No Sensor</IonSelectOption>
                <IonSelectOption value="temperature">Temperature</IonSelectOption>
                <IonSelectOption value="humidity">Humidity</IonSelectOption>
              </IonSelect>
            </IonItem>
            <IonItem>
            <IonLabel>Sensor Min {schedule.sensorMin}</IonLabel>
              <IonRange disabled={!schedule.sensor} min={-20} max={50} step={0.5} pin value={schedule.sensorMin} onIonChange={e => setSchedule({...schedule, sensorMin: Number(e.detail.value)})}>
                <IonIcon size="small" slot="start" icon={thermometer} color="danger" />
                <IonIcon slot="end" color="danger" icon={thermometer} />
              </IonRange>
            </IonItem>
            <IonItem>
              <IonLabel>Sensor Max {schedule.sensorMax}</IonLabel>
              <IonRange disabled={!schedule.sensor} min={-20} max={50} step={0.5} pin value={schedule.sensorMax} onIonChange={e => setSchedule({...schedule, sensorMax: Number(e.detail.value)})}>
                <IonIcon size="small" slot="start" icon={thermometer} color="danger" />
                <IonIcon slot="end" color="danger" icon={thermometer} />
              </IonRange>
            </IonItem>
            <IonButton type="submit" className="ion-margin-top" expand="block">Save</IonButton>
          </IonList>
          </form>
        ) : <IonNote id="error-message" className="ion-padding" color="danger"><h3>Schedule not found</h3></IonNote>}
      </IonContent>
    </IonPage>
  );
};

export default UpdateSchedule;
