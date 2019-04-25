interface StateInfo {
  title: string;
  description: string;
  sources: string[];
  color: string;
  onlyStaff?: boolean;
}

export function getNextStateInfos(status: string): StateInfo[] {
  return stateInfos.filter((s) => s.sources.includes(status));
}

export function getNextStates(status: string): string[] {
  return getNextStateInfos(status).map((si) => si.title);
}

export function getStateInfo(status: string): StateInfo | undefined {
  return stateInfos.find((s) => s.title === status);
}

export const stateInfos: StateInfo[] = [
  {
    title: 'angemeldet',
    description: 'Das Seminar wurde angemeldet.',
    sources: ['zurückgezogen', 'abgesagt'],
    color: 'yellow'
  },
  {
    title: 'zurückgezogen',
    description: 'Der Antrag auf Förderung wurde zurückgezogen.',
    color: 'red',
    sources: ['angemeldet', 'zugesagt']
  },
  {
    title: 'zugesagt',
    description: 'Die Förderung wurde von JANUN zugesagt.',
    color: 'green',
    sources: ['angemeldet', 'abgelehnt', 'abgesagt', 'zurückgezogen'],
    onlyStaff: true
  },
  {
    title: 'abgesagt',
    description: 'Das Seminar findet nicht statt.',
    color: 'red',
    sources: ['zugesagt', 'angemeldet']
  },
  {
    title: 'abgelehnt',
    description: 'Die Förderung wurde von JANUN abgelehnt.',
    color: 'red',
    sources: ['angemeldet', 'zugesagt'],
    onlyStaff: true
  },
  {
    title: 'stattgefunden',
    description: 'Das Seminar hat tatsächlich stattgefunden.',
    color: 'green',
    // disabled: new Date(this.seminar.start_date) > new Date(),
    sources: ['zugesagt']
  },
  {
    title: 'ohne Abrechnung',
    description: '',
    color: 'red',
    sources: ['stattgefunden'],
    onlyStaff: true
  },
  {
    title: 'Abrechnung abgeschickt',
    description: 'Die Abrechnung wurde per Post abgeschickt.',
    color: 'green',
    sources: ['stattgefunden']
  },
  {
    title: 'Abrechnung angekommen',
    description: 'Die Abrechnung ist bei JANUN angekommen.',
    color: 'green',
    onlyStaff: true,
    sources: ['Abrechnung abgeschickt', 'stattgefunden']
  },
  {
    title: 'Abrechnung unmöglich',
    description: '',
    color: 'red',
    onlyStaff: true,
    sources: ['Abrechnung angekommen', 'Nachprüfung', 'inhaltliche Prüfung']
  },
  {
    title: 'rechnerische Prüfung',
    description: '',
    color: 'green',
    onlyStaff: true,
    sources: ['Abrechnung angekommen']
  },
  {
    title: 'inhaltliche Prüfung',
    description: '',
    color: 'green',
    onlyStaff: true,
    sources: ['rechnerische Prüfung']
  },
  {
    title: 'Nachprüfung',
    description: '',
    color: 'green',
    onlyStaff: true,
    sources: ['inhaltliche Prüfung']
  },
  {
    title: 'fertig geprüft',
    description: '',
    color: 'green',
    onlyStaff: true,
    sources: ['Nachprüfung']
  },
  {
    title: 'überwiesen',
    description: '',
    color: 'green',
    onlyStaff: true,
    sources: ['fertig geprüft']
  }
];

export const states = stateInfos.map((si) => si.title);
