import React, { useState, useContext, FormEvent } from 'react';
import { Schedule, getSchedule, updateSchedule, createSchedule } from '../data/schedules';

import {
  IonBackButton,
  IonButton,
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
  IonSelect,
  IonSelectOption,
  IonDatetime,
  useIonViewWillEnter
} from '@ionic/react';
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
        id: -1
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
                <IonSelectOption value="1">1</IonSelectOption>
                <IonSelectOption value="2">2</IonSelectOption>
                <IonSelectOption value="3">3</IonSelectOption>
                <IonSelectOption value="4">4</IonSelectOption>
                <IonSelectOption value="5">5</IonSelectOption>
                <IonSelectOption value="6">6</IonSelectOption>
                <IonSelectOption value="7">7</IonSelectOption>
                <IonSelectOption value="8">8</IonSelectOption>
                <IonSelectOption value="9">9</IonSelectOption>
                <IonSelectOption value="10">10</IonSelectOption>
                <IonSelectOption value="11">11</IonSelectOption>
                <IonSelectOption value="12">12</IonSelectOption>
                <IonSelectOption value="13">13</IonSelectOption>
                <IonSelectOption value="14">14</IonSelectOption>
                <IonSelectOption value="15">15</IonSelectOption>
                <IonSelectOption value="16">16</IonSelectOption>
              </IonSelect>
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
