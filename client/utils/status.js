// export interface StateInfo {
//   title: string;
//   description: string;
//   sources: string[];
//   color: string;
//   staffOnly?: boolean;
// }

export function getNextStateInfos(status, isStaff) {
  return stateInfos
    .filter(s => s.sources.includes(status))
    .filter(s => isStaff || !s.staffOnly)
}

export function getNextStates(status, isStaff) {
  return getNextStateInfos(status, isStaff).map(si => si.title)
}

export function getStateInfo(status) {
  return stateInfos.find(s => s.title === status)
}

export const stateInfos = [
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
    staffOnly: true
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
    staffOnly: true
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
    staffOnly: true
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
    staffOnly: true,
    sources: ['Abrechnung abgeschickt', 'stattgefunden']
  },
  {
    title: 'Abrechnung unmöglich',
    description: '',
    color: 'red',
    staffOnly: true,
    sources: ['Abrechnung angekommen', 'Zweitprüfung', 'inhaltliche Prüfung']
  },
  {
    title: 'rechnerische Prüfung',
    description: '',
    color: 'green',
    staffOnly: true,
    sources: ['Abrechnung angekommen']
  },
  {
    title: 'inhaltliche Prüfung',
    description: '',
    color: 'green',
    staffOnly: true,
    sources: ['rechnerische Prüfung']
  },
  {
    title: 'Zweitprüfung',
    description: '',
    color: 'green',
    staffOnly: true,
    sources: ['inhaltliche Prüfung']
  },
  {
    title: 'fertig geprüft',
    description: '',
    color: 'green',
    staffOnly: true,
    sources: ['Zweitprüfung']
  },
  {
    title: 'überwiesen',
    description: '',
    color: 'green',
    staffOnly: true,
    sources: ['fertig geprüft']
  }
]

export const states = stateInfos.map(si => si.title)
