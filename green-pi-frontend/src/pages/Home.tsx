import ScheduleListItem from '../components/ScheduleListItem';
import React, { useState } from 'react';
import { Schedule, getSchedules } from '../data/schedules';
import {
  IonContent,
  IonHeader,
  IonList,
  IonPage,
  IonRefresher,
  IonRefresherContent,
  IonTitle,
  IonFab, 
  IonFabButton, 
  IonIcon,
  IonToolbar,
  useIonViewWillEnter
} from '@ionic/react';
import { add } from 'ionicons/icons';
import './Home.css';

const Home: React.FC = () => {

  const [schedules, setSchedules] = useState<Schedule[]>([]);

  useIonViewWillEnter(() => {
    getSchedules().then((scheds) => setSchedules(scheds));
  });

  const refresh = (e: CustomEvent) => {
    getSchedules().then((scheds) => {
      setSchedules(scheds);
      e.detail.complete();
    });    
  };

  const handleDelete = (e: CustomEvent, id: number) => {
    setSchedules(schedules.filter(elem => elem.id !== id));
  }

  return (
    <IonPage id="home-page">
      <IonHeader>
        <IonToolbar>
          <IonTitle>Green PI</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonRefresher slot="fixed" onIonRefresh={refresh}>
          <IonRefresherContent></IonRefresherContent>
        </IonRefresher>

        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">
              Green PI
            </IonTitle>
          </IonToolbar>
        </IonHeader>

        <IonList>
          {schedules.map(m => <ScheduleListItem onItemDelete={(e: CustomEvent) => {handleDelete(e, m.id)}} key={m.id} schedule={m} />)}
        </IonList>
        <IonFab vertical="bottom" horizontal="end" slot="fixed">
          <IonFabButton href={"/schedule/new"}>
            <IonIcon icon={add} />
          </IonFabButton>
        </IonFab>
      </IonContent>
    </IonPage>
  );
};

export default Home;
