from typing import List


STATE_INFO = {
    "angemeldet": {
        "description": "Das Seminar wurde angemeldet.",
        "sources": ["zurückgezogen", "abgesagt"],
        "color": "yellow",
        "staff_only": False,
    },
    "zugesagt": {
        "description": "Die Förderung wurde von JANUN zugesagt.",
        "color": "green",
        "sources": ["angemeldet", "abgelehnt", "abgesagt", "zurückgezogen"],
        "staff_only": True,
    },
    "abgesagt": {
        "description": "Das Seminar findet nicht statt oder der Antrag wurde zurückgezogen",
        "color": "red",
        "sources": ["zugesagt", "angemeldet"],
        "staff_only": False,
    },
    "abgelehnt": {
        "description": "Die Förderung wurde von JANUN abgelehnt.",
        "color": "red",
        "sources": ["angemeldet", "zugesagt"],
        "staff_only": True,
    },
    "stattgefunden": {
        "description": "Das Seminar hat tatsächlich stattgefunden.",
        "color": "green",
        # disabled: new Date(this.seminar.start_date) > new Date(),
        "sources": [
            "zugesagt",
            "ohne Abrechnung",
            "Abrechnung abgeschickt",
            "Abrechnung angekommen",
        ],
        "staff_only": False,
    },
    "ohne Abrechnung": {
        "description": "",
        "color": "red",
        "sources": ["stattgefunden"],
        "staff_only": True,
    },
    "Abrechnung abgeschickt": {
        "description": "Die Abrechnung wurde per Post abgeschickt.",
        "color": "green",
        "sources": ["stattgefunden", "Abrechnung angekommen"],
        "staff_only": False,
    },
    "Abrechnung angekommen": {
        "description": "Die Abrechnung ist bei JANUN angekommen.",
        "color": "green",
        "sources": [
            "Abrechnung abgeschickt",
            "stattgefunden",
            "Abrechnung unmöglich",
            "rechnerische Prüfung",
        ],
        "staff_only": True,
    },
    "Abrechnung unmöglich": {
        "description": "",
        "color": "red",
        "sources": ["Abrechnung angekommen", "Zweitprüfung", "inhaltliche Prüfung"],
        "staff_only": True,
    },
    "rechnerische Prüfung": {
        "description": "",
        "color": "green",
        "sources": ["Abrechnung angekommen", "inhaltliche Prüfung"],
        "staff_only": True,
    },
    "inhaltliche Prüfung": {
        "description": "",
        "color": "green",
        "sources": ["rechnerische Prüfung", "Abrechnung unmöglich", "Zweitprüfung"],
        "staff_only": True,
    },
    "Zweitprüfung": {
        "description": "",
        "color": "green",
        "sources": ["inhaltliche Prüfung", "Abrechnung unmöglich", "fertig geprüft"],
        "staff_only": True,
    },
    "fertig geprüft": {
        "description": "",
        "color": "green",
        "sources": ["Zweitprüfung", "überwiesen"],
        "staff_only": True,
    },
    "überwiesen": {
        "description": "Die Förderung wurde überwiesen.",
        "color": "green",
        "sources": ["fertig geprüft"],
        "staff_only": True,
    },
}


STATES_APPLIED = ("angemeldet",)

STATES_CONFIRMED = (
    "zugesagt",
    "stattgefunden",
    "Abrechnung abgeschickt",
    "Abrechnung angekommen",
    "rechnerische Prüfung",
    "inhaltliche Prüfung",
    "Zweitprüfung",
    "fertig geprüft",
    "überwiesen",
)


STATES_REJECTED = ("abgelehnt", "abgesagt", "ohne Abrechnung", "Abrechnung unmöglich")

STATES = STATES_APPLIED + STATES_CONFIRMED + STATES_REJECTED


def get_next_states(status: str, is_staff: bool = False) -> List[str]:
    return [
        state
        for state, info in STATE_INFO.items()
        if status in info["sources"] and (is_staff or not info["staff_only"])
    ]
