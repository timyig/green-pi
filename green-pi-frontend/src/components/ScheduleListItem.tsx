import React from 'react';
import {
  IonItem,
  IonLabel,
  IonToggle,
  IonButton,
  IonIcon
  } from '@ionic/react';
import { createOutline, trashOutline } from 'ionicons/icons';
import { Schedule, deleteSchedule, enableSchedule, disableSchedule } from '../data/schedules';
import './ScheduleListItem.css';

interface ScheduleListItemProps {
  schedule: Schedule;
  onItemDelete: CallableFunction;
}

const ScheduleListItem: React.FC<ScheduleListItemProps> = ({ schedule, onItemDelete }) => {
  const handleDelete = () => {
    deleteSchedule(schedule.id);
    onItemDelete();
  }

  const handleToggle = (e: CustomEvent, id: number) => {
    if (e.detail.checked) {
      enableSchedule(id);
    } else {
      disableSchedule(id);
    }
  }

  return (
    <IonItem detail={false}>
      <IonToggle value="pepperoni" checked={schedule.enableSchedule} onIonChange={(e) => {handleToggle(e, schedule.id)}}/>
      <IonLabel className="ion-text-wrap">
        <h2> <span>Schedule From</span> <b>{schedule.startSchedule}</b> <span> To </span> <b>{schedule.endSchedule}</b></h2>
        <p>Device ID: <b>{schedule.deviceId}</b></p>
        <p>Manual Schedule: <b>{String(schedule.manualSchedule)}</b></p>
        <p>Last State: <b>{schedule.lastState}</b></p>
        <p>
          Sensor: <b>{schedule.sensor || "No Sensor"}</b>
          <span> </span>
          Between <b>{schedule.sensorMin}</b>
          <span> </span>
          and <b>{schedule.sensorMax}</b>
        </p>
      </IonLabel>
      <IonButton href={"/schedule/" + schedule.id} slot="end" size="default" color="secondary">
        <IonIcon icon={createOutline} />
      </IonButton>
      <IonButton slot="end" size="default" color="danger" onClick={handleDelete}>
        <IonIcon icon={trashOutline} />
      </IonButton>
    </IonItem>
  );
};

export default ScheduleListItem;
