import React from 'react';
import {
  IonItem,
  IonLabel,
  IonNote,
  IonToggle,
  IonButton,
  IonIcon
  } from '@ionic/react';
import { createOutline, trashOutline } from 'ionicons/icons';
import { Schedule } from '../data/schedules';
import './ScheduleListItem.css';

interface ScheduleListItemProps {
  schedule: Schedule;
}

const ScheduleListItem: React.FC<ScheduleListItemProps> = ({ schedule }) => {
  return (
    <IonItem detail={false}>
      <IonToggle value="pepperoni" checked={schedule.enableSchedule} />
      <IonLabel className="ion-text-wrap">
        <h2> <span>Schedule From</span> <b>{schedule.startSchedule}</b> <span> To </span> <b>{schedule.endSchedule}</b></h2>
        <p>Device ID: <b>{schedule.deviceId}</b></p>
        <p>Manual Schedule: <b>{schedule.manualSchedule.toString()}</b></p>
        <p>Last State: <b>{schedule.lastState}</b></p>
      </IonLabel>
      <IonButton href={"/schedule/" + schedule.id} slot="end" size="default" color="secondary">
        <IonIcon icon={createOutline} />
      </IonButton>
      <IonButton slot="end" size="default" color="danger">
        <IonIcon icon={trashOutline} />
      </IonButton>
    </IonItem>
  );
};

export default ScheduleListItem;
