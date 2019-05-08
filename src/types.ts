export enum UserRole {
  Verwalter_in = 'Verwalter_in',
  Teamer_in = 'Teamer_in',
  Prüfer_in = 'Prüfer_in'
}

export interface User {
  pk: number;
  password?: string;
  address: string;
  created_at: string;
  email: string;
  group_hats: Group[];
  janun_groups: Group[];
  name: string;
  role: UserRole;
  telephone?: string;
  updated_at: string;
  username: string;
  is_reviewed: boolean;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface Group {
  pk: number;
  name: string;
}

// export enum SeminarStatus {
//   angemeldet = 'angemeldet',
//   zurückgezogen = 'zurückgezogen',
//   zugesagt = 'zugesagt',
//   abgelehnt = 'abgelehnt',
//   abgesagt = 'abgesagt',
//   stattgefunden = 'stattgefunden',
//   ohne_Abrechnung = 'ohne Abrechnung',
//   Abrechnung_abgeschickt = 'Abrechnung abgeschickt',
//   Abrechnung_angekommen = 'Abrechnung angekommen',
//   Abrechnung_unmöglich = 'Abrechnung unmöglich',
//   rechnerische_Prüfung = 'rechnerische Prüfung',
//   inhaltliche_Prüfung = 'inhaltliche Prüfung',
//   Zweitprüfung = 'Zweitprüfung',
//   fertig_geprüft = 'fertig geprüft',
//   überwiesen = 'überwiesen'
// }

export interface Seminar {
  pk: number;
  status: string;
  title: string;
  description: string;
  start_date: string;
  start_time?: string;
  end_date: string;
  end_time?: string;
  location: string;
  created_at: string;
  updated_at: string;
  group?: Group;
  group_pk?: string;
  owner: User;
  owner_pk?: string;
  planned_training_days: number;
  planned_attendees_min: number;
  planned_attendees_max: number;
  requested_funding: number;
  tnt: number;
  tnt_cost: number;
  deadline: string;
  deadline_expired: boolean;
  deadline_in_two_weeks: boolean;
}

export interface Alert {
  id: number;
  text: string;
  variant: string;
}

export interface Toast {
  id?: number;
  duration?: number;
  type?: 'error';
  text?: string;
}
