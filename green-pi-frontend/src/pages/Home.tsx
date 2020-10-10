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
  IonToolbar,
  useIonViewWillEnter
} from '@ionic/react';
import './Home.css';

const Home: React.FC = () => {

  const [schedules, setSchedules] = useState<Schedule[]>([]);

  useIonViewWillEnter(() => {
    getSchedules().then((scheds) => setSchedules(scheds));
  });

  const refresh = (e: CustomEvent) => {
    setTimeout(() => {
      e.detail.complete();
    }, 3000);
  };

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
          {schedules.map(m => <ScheduleListItem key={m.id} schedule={m} />)}
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default Home;
