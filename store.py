"""
store.py - In-memory Store for HackHub Hackathon Management App.
Contains zero tkinter code. All data is stored in plain Python objects and resets on app exit.
Preloads realistic sample data with 2 events, 4 judges, 2 volunteers, 12 participants in 6 teams,
2 rounds (Round 1 with 2 panels, Final Round with 1 panel), criteria totaling weight 100,
saved scores, one disqualified team with reason, and demo logins.
"""

from __future__ import annotations
import copy
from dataclasses import dataclass, field
from datetime import datetime
import time
from typing import Dict, List, Optional, Tuple

# Event status constants
STATUS_DRAFT = "DRAFT"
STATUS_REG_OPEN = "REGISTRATION_OPEN"
STATUS_JUDGING = "JUDGING"
STATUS_COMPLETED = "COMPLETED"

EVENT_STATUSES = [STATUS_DRAFT, STATUS_REG_OPEN, STATUS_JUDGING, STATUS_COMPLETED]

# Team round progression status
STATUS_ACTIVE = "ACTIVE"
STATUS_QUALIFIED = "QUALIFIED"
STATUS_ELIMINATED = "ELIMINATED"
STATUS_DISQUALIFIED = "DISQUALIFIED"


@dataclass
class User:
    id: str
    email: str
    password: str
    name: str
    role: str  # "ORGANIZER", "JUDGE", "VOLUNTEER", "PARTICIPANT"


@dataclass
class Criterion:
    id: str
    name: str
    max_score: float = 10.0
    weight: float = 25.0


@dataclass
class Round:
    id: str
    event_id: str
    round_number: int
    name: str
    is_closed: bool = False
    criteria: List[Criterion] = field(default_factory=list)


@dataclass
class Panel:
    id: str
    event_id: str
    round_id: str
    name: str
    judge_ids: List[str] = field(default_factory=list)
    team_ids: List[str] = field(default_factory=list)


@dataclass
class Team:
    id: str
    event_id: str
    name: str
    members: List[str]
    project_title: str
    description: str
    repo_url: str
    checked_in: bool = False
    is_disqualified: bool = False
    disqualification_reason: str = ""
    registered_at: float = field(default_factory=time.time)
    creator_user_id: Optional[str] = None
    # Progression state per round: round_id -> "ACTIVE" | "QUALIFIED" | "ELIMINATED"
    round_status: Dict[str, str] = field(default_factory=dict)


@dataclass
class ScoreRecord:
    id: str
    event_id: str
    round_id: str
    panel_id: str
    judge_id: str
    team_id: str
    criterion_id: str
    value: float
    comment: str
    updated_at: str


@dataclass
class Event:
    id: str
    title: str
    description: str
    status: str = STATUS_DRAFT
    organizer_id: str = ""
    judge_ids: List[str] = field(default_factory=list)
    volunteer_ids: List[str] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)
    panels: List[Panel] = field(default_factory=list)
    teams: List[Team] = field(default_factory=list)
    scores: List[ScoreRecord] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class Store:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.events: Dict[str, Event] = {}
        self._current_user: Optional[User] = None
        self._seed_data()

    # ---------------------------------------------------------
    # Authentication & Session
    # ---------------------------------------------------------
    @property
    def current_user(self) -> Optional[User]:
        return self._current_user

    def authenticate(self, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        email_clean = email.strip().lower()
        for user in self.users.values():
            if user.email.lower() == email_clean:
                if user.password == password:
                    self._current_user = user
                    return True, "Login successful", user
                return False, "Incorrect password", None
        return False, "No account found with this email", None

    def register(self, email: str, password: str, name: str, role: str) -> Tuple[bool, str, Optional[User]]:
        email_clean = email.strip().lower()
        if not email_clean or "@" not in email_clean or "." not in email_clean:
            return False, "Please enter a valid email address.", None
        if not password or len(password) < 4:
            return False, "Password must be at least 4 characters.", None
        if not name.strip():
            return False, "Name cannot be empty.", None

        for user in self.users.values():
            if user.email.lower() == email_clean:
                return False, "An account with this email already exists.", None

        valid_roles = ["ORGANIZER", "JUDGE", "VOLUNTEER", "PARTICIPANT"]
        norm_role = role.upper() if role.upper() in valid_roles else "PARTICIPANT"
        new_id = f"usr_{len(self.users) + 1}_{int(time.time())}"
        new_user = User(
            id=new_id,
            email=email_clean,
            password=password,
            name=name.strip(),
            role=norm_role
        )
        self.users[new_id] = new_user
        self._current_user = new_user
        return True, "Registration successful!", new_user

    def logout(self) -> None:
        self._current_user = None

    def get_demo_users(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "Organizer",
                "email": "alice@hackhub.io",
                "password": "password123",
                "name": "Alice Organizer"
            },
            {
                "role": "Judge",
                "email": "bob@hackhub.io",
                "password": "password123",
                "name": "Dr. Bob Judge"
            },
            {
                "role": "Participant",
                "email": "charlie@hackhub.io",
                "password": "password123",
                "name": "Charlie Coder"
            },
            {
                "role": "Volunteer",
                "email": "victor@hackhub.io",
                "password": "password123",
                "name": "Victor Volunteer"
            }
        ]

    # ---------------------------------------------------------
    # Event Management
    # ---------------------------------------------------------
    def get_events_for_user(self, user_id: str) -> List[Tuple[Event, str]]:
        """Returns list of (Event, role_in_event). If user has no specific role in an event,
        it still shows with their global role or 'PARTICIPANT'."""
        result = []
        user = self.users.get(user_id)
        if not user:
            return result

        for event in self.events.values():
            role = self.get_user_role_in_event(event.id, user_id)
            result.append((event, role))
        return result

    def get_user_role_in_event(self, event_id: str, user_id: str) -> str:
        event = self.events.get(event_id)
        if not event:
            return "PARTICIPANT"
        if event.organizer_id == user_id:
            return "ORGANIZER"
        if user_id in event.judge_ids:
            return "JUDGE"
        if user_id in event.volunteer_ids:
            return "VOLUNTEER"
        # Check if participant on a team
        user = self.users.get(user_id)
        user_email = user.email.lower() if user else ""
        for team in event.teams:
            if team.creator_user_id == user_id:
                return "PARTICIPANT"
            for member in team.members:
                if user_email in member.lower() or (user and user.name.lower() in member.lower()):
                    return "PARTICIPANT"
        # Default to user's assigned primary role if valid for event
        return user.role if user else "PARTICIPANT"

    def get_event(self, event_id: str) -> Optional[Event]:
        return self.events.get(event_id)

    def create_event(self, title: str, description: str, organizer_id: str) -> Tuple[bool, str, Optional[Event]]:
        if not title.strip():
            return False, "Event title cannot be empty.", None
        new_id = f"evt_{len(self.events) + 1}_{int(time.time())}"
        
        # Default 2 rounds
        r1 = Round(
            id=f"rnd_{new_id}_1",
            event_id=new_id,
            round_number=1,
            name="Round 1 - Preliminary",
            criteria=[
                Criterion(id=f"crit_{new_id}_1_1", name="Innovation & Creativity", max_score=10.0, weight=40.0),
                Criterion(id=f"crit_{new_id}_1_2", name="Technical Execution", max_score=10.0, weight=35.0),
                Criterion(id=f"crit_{new_id}_1_3", name="Presentation & Demo", max_score=10.0, weight=25.0),
            ]
        )
        r2 = Round(
            id=f"rnd_{new_id}_2",
            event_id=new_id,
            round_number=2,
            name="Round 2 - Grand Finale",
            criteria=[
                Criterion(id=f"crit_{new_id}_2_1", name="Feasibility & Impact", max_score=10.0, weight=50.0),
                Criterion(id=f"crit_{new_id}_2_2", name="Polish & Completeness", max_score=10.0, weight=50.0),
            ]
        )

        # Final round panel
        final_panel = Panel(
            id=f"pnl_{new_id}_final",
            event_id=new_id,
            round_id=r2.id,
            name="Finalists Showcase Panel"
        )

        event = Event(
            id=new_id,
            title=title.strip(),
            description=description.strip(),
            status=STATUS_DRAFT,
            organizer_id=organizer_id,
            rounds=[r1, r2],
            panels=[final_panel]
        )
        self.events[new_id] = event
        return True, "Event created successfully!", event

    def advance_event_status(self, event_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        curr_idx = EVENT_STATUSES.index(event.status)
        if curr_idx >= len(EVENT_STATUSES) - 1:
            return False, "Event has reached the final status (COMPLETED)."

        next_status = EVENT_STATUSES[curr_idx + 1]
        
        # Validation checks
        if next_status == STATUS_JUDGING:
            if not event.teams:
                return False, "Cannot advance to JUDGING without any registered teams."
            if not event.rounds:
                return False, "Cannot advance to JUDGING without at least one round configured."

        event.status = next_status
        return True, f"Event status successfully moved to {next_status}."

    # ---------------------------------------------------------
    # Staff Management (Judges and Volunteers)
    # ---------------------------------------------------------
    def get_judges(self, event_id: str) -> List[User]:
        event = self.events.get(event_id)
        if not event:
            return []
        return [self.users[uid] for uid in event.judge_ids if uid in self.users]

    def get_volunteers(self, event_id: str) -> List[User]:
        event = self.events.get(event_id)
        if not event:
            return []
        return [self.users[uid] for uid in event.volunteer_ids if uid in self.users]

    def add_judge_by_email(self, event_id: str, email: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        clean = email.strip().lower()
        if not clean:
            return False, "Email cannot be empty"

        user = next((u for u in self.users.values() if u.email.lower() == clean), None)
        if not user:
            # Create a placeholder user account for this judge
            name_guess = clean.split("@")[0].replace(".", " ").title()
            new_id = f"usr_judge_{len(self.users)+1}"
            user = User(id=new_id, email=clean, password="password123", name=f"Judge {name_guess}", role="JUDGE")
            self.users[new_id] = user

        if user.id in event.judge_ids:
            return False, f"{user.name} ({user.email}) is already assigned as a judge."
        if user.id in event.volunteer_ids:
            event.volunteer_ids.remove(user.id)

        event.judge_ids.append(user.id)
        return True, f"Successfully added {user.name} as a judge."

    def remove_judge(self, event_id: str, user_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        if user_id in event.judge_ids:
            event.judge_ids.remove(user_id)
            # Remove from panels
            for panel in event.panels:
                if user_id in panel.judge_ids:
                    panel.judge_ids.remove(user_id)
            return True, "Judge removed from event."
        return False, "Judge not found in this event."

    def add_volunteer_by_email(self, event_id: str, email: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        clean = email.strip().lower()
        if not clean:
            return False, "Email cannot be empty"

        user = next((u for u in self.users.values() if u.email.lower() == clean), None)
        if not user:
            name_guess = clean.split("@")[0].replace(".", " ").title()
            new_id = f"usr_vol_{len(self.users)+1}"
            user = User(id=new_id, email=clean, password="password123", name=f"Volunteer {name_guess}", role="VOLUNTEER")
            self.users[new_id] = user

        if user.id in event.volunteer_ids:
            return False, f"{user.name} ({user.email}) is already a volunteer."
        if user.id in event.judge_ids:
            event.judge_ids.remove(user.id)

        event.volunteer_ids.append(user.id)
        return True, f"Successfully added {user.name} as a volunteer."

    def remove_volunteer(self, event_id: str, user_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        if user_id in event.volunteer_ids:
            event.volunteer_ids.remove(user_id)
            return True, "Volunteer removed from event."
        return False, "Volunteer not found in this event."

    # ---------------------------------------------------------
    # Team Management
    # ---------------------------------------------------------
    def get_teams(self, event_id: str) -> List[Team]:
        event = self.events.get(event_id)
        return event.teams if event else []

    def get_team(self, event_id: str, team_id: str) -> Optional[Team]:
        event = self.events.get(event_id)
        if not event:
            return None
        return next((t for t in event.teams if t.id == team_id), None)

    def get_team_for_user(self, event_id: str, user_id: str) -> Optional[Team]:
        event = self.events.get(event_id)
        if not event:
            return None
        user = self.users.get(user_id)
        user_email = user.email.lower() if user else ""
        user_name = user.name.lower() if user else ""

        for team in event.teams:
            if team.creator_user_id == user_id:
                return team
            for m in team.members:
                if user_email in m.lower() or (user_name and user_name in m.lower()):
                    return team
        return None

    def register_team(
        self,
        event_id: str,
        creator_user_id: str,
        name: str,
        members: List[str],
        project_title: str,
        description: str,
        repo_url: str
    ) -> Tuple[bool, str, Optional[Team]]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found", None

        if event.status != STATUS_REG_OPEN and event.status != STATUS_DRAFT:
            return False, f"Registration is closed. Current status is {event.status}.", None

        if not name.strip():
            return False, "Team name cannot be empty.", None
        if not project_title.strip():
            return False, "Project title cannot be empty.", None

        # Clean repo url check
        repo_url_clean = repo_url.strip()
        if not (repo_url_clean.startswith("http://") or repo_url_clean.startswith("https://")):
            return False, "Repo URL must begin with http:// or https://", None

        clean_members = [m.strip() for m in members if m.strip()]
        if not clean_members:
            # If user has a name, default to user
            user = self.users.get(creator_user_id)
            clean_members = [user.name if user else "Lead Hacker"]

        new_team_id = f"tm_{event_id}_{len(event.teams)+1}_{int(time.time())}"
        team = Team(
            id=new_team_id,
            event_id=event_id,
            name=name.strip(),
            members=clean_members,
            project_title=project_title.strip(),
            description=description.strip(),
            repo_url=repo_url_clean,
            checked_in=False,
            is_disqualified=False,
            disqualification_reason="",
            registered_at=time.time(),
            creator_user_id=creator_user_id
        )

        # Set default active status for first round
        if event.rounds:
            team.round_status[event.rounds[0].id] = STATUS_ACTIVE

        event.teams.append(team)
        return True, "Team registered successfully!", team

    def update_team(
        self,
        event_id: str,
        team_id: str,
        name: str,
        members: List[str],
        project_title: str,
        description: str,
        repo_url: str
    ) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        if event.status in [STATUS_JUDGING, STATUS_COMPLETED]:
            return False, "Team details are locked once judging has started."

        team = next((t for t in event.teams if t.id == team_id), None)
        if not team:
            return False, "Team not found"

        if not name.strip():
            return False, "Team name cannot be empty."
        if not project_title.strip():
            return False, "Project title cannot be empty."

        repo_url_clean = repo_url.strip()
        if not (repo_url_clean.startswith("http://") or repo_url_clean.startswith("https://")):
            return False, "Repo URL must begin with http:// or https://"

        clean_members = [m.strip() for m in members if m.strip()]
        team.name = name.strip()
        team.project_title = project_title.strip()
        team.description = description.strip()
        team.repo_url = repo_url_clean
        if clean_members:
            team.members = clean_members

        return True, "Team details updated successfully."

    def set_team_checked_in(self, event_id: str, team_id: str, checked_in: bool) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        team = next((t for t in event.teams if t.id == team_id), None)
        if not team:
            return False, "Team not found"
        team.checked_in = checked_in
        state_str = "Checked In" if checked_in else "Not Checked In"
        return True, f"Team '{team.name}' status set to {state_str}."

    def disqualify_team(self, event_id: str, team_id: str, reason: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        reason_clean = reason.strip()
        if not reason_clean:
            return False, "A clear disqualification reason is required."

        team = next((t for t in event.teams if t.id == team_id), None)
        if not team:
            return False, "Team not found"

        team.is_disqualified = True
        team.disqualification_reason = reason_clean
        return True, f"Team '{team.name}' has been DISQUALIFIED."

    def reinstate_team(self, event_id: str, team_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        team = next((t for t in event.teams if t.id == team_id), None)
        if not team:
            return False, "Team not found"

        team.is_disqualified = False
        team.disqualification_reason = ""
        return True, f"Team '{team.name}' has been reinstated."

    # ---------------------------------------------------------
    # Rounds and Criteria Management
    # ---------------------------------------------------------
    def get_rounds(self, event_id: str) -> List[Round]:
        event = self.events.get(event_id)
        return event.rounds if event else []

    def get_round(self, event_id: str, round_id: str) -> Optional[Round]:
        event = self.events.get(event_id)
        if not event:
            return None
        return next((r for r in event.rounds if r.id == round_id), None)

    def add_round(self, event_id: str, name: str) -> Tuple[bool, str, Optional[Round]]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found", None

        if len(event.rounds) >= 5:
            return False, "Maximum 5 rounds allowed per event.", None

        round_num = len(event.rounds) + 1
        new_round_id = f"rnd_{event_id}_{round_num}_{int(time.time())}"
        round_name = name.strip() if name.strip() else f"Round {round_num}"

        new_round = Round(
            id=new_round_id,
            event_id=event_id,
            round_number=round_num,
            name=round_name,
            criteria=[
                Criterion(id=f"crit_{new_round_id}_1", name="Overall Impact", max_score=10.0, weight=50.0),
                Criterion(id=f"crit_{new_round_id}_2", name="Technical Depth", max_score=10.0, weight=50.0),
            ]
        )
        event.rounds.append(new_round)

        # If it is the last round, ensure it has a panel
        if len(event.rounds) > 1:
            # check if previous round was final, re-balance or create panel for new final
            pass

        return True, f"Added {round_name}.", new_round

    def delete_round(self, event_id: str, round_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"
        if len(event.rounds) <= 1:
            return False, "Events must have at least one round."

        target = next((r for r in event.rounds if r.id == round_id), None)
        if not target:
            return False, "Round not found."

        event.rounds.remove(target)
        # Remove panels belonging to this round
        event.panels = [p for p in event.panels if p.round_id != round_id]

        # Re-number rounds
        for idx, r in enumerate(event.rounds, start=1):
            r.round_number = idx

        return True, "Round deleted."

    def save_round_criteria(
        self,
        event_id: str,
        round_id: str,
        criteria_data: List[Dict[str, any]]
    ) -> Tuple[bool, str]:
        """criteria_data is list of dicts: {'id': Optional[str], 'name': str, 'max_score': float, 'weight': float}"""
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return False, "Round not found"

        if not criteria_data:
            return False, "Round must have at least one criterion."

        total_weight = sum(float(c.get("weight", 0)) for c in criteria_data)
        if abs(total_weight - 100.0) > 0.001:
            return False, f"Total weight must equal 100% (currently {total_weight:.1f}%)."

        new_criteria: List[Criterion] = []
        for idx, c in enumerate(criteria_data, start=1):
            name = str(c.get("name", "")).strip()
            if not name:
                return False, f"Criterion #{idx} name cannot be empty."
            try:
                max_score = float(c.get("max_score", 10.0))
                weight = float(c.get("weight", 0.0))
            except (ValueError, TypeError):
                return False, f"Criterion #{idx} has invalid numeric values."

            if max_score <= 0:
                return False, f"Max score for '{name}' must be greater than 0."
            if weight < 0:
                return False, f"Weight for '{name}' cannot be negative."

            crit_id = c.get("id") or f"crit_{round_id}_{idx}_{int(time.time())}"
            new_criteria.append(Criterion(
                id=crit_id,
                name=name,
                max_score=max_score,
                weight=weight
            ))

        round_obj.criteria = new_criteria
        return True, "Criteria saved successfully!"

    # ---------------------------------------------------------
    # Panels Management
    # ---------------------------------------------------------
    def get_panels(self, event_id: str, round_id: Optional[str] = None) -> List[Panel]:
        event = self.events.get(event_id)
        if not event:
            return []
        if round_id:
            return [p for p in event.panels if p.round_id == round_id]
        return event.panels

    def create_panel(self, event_id: str, round_id: str, name: str) -> Tuple[bool, str, Optional[Panel]]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found", None

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return False, "Round not found", None

        # Check final round constraint: "The final round must have exactly one panel."
        is_final_round = (event.rounds and round_obj.id == event.rounds[-1].id)
        existing_panels = [p for p in event.panels if p.round_id == round_id]
        if is_final_round and len(existing_panels) >= 1:
            return False, "The final round must have exactly one panel.", None

        panel_name = name.strip() if name.strip() else f"Panel {chr(65 + len(existing_panels))}"
        panel_id = f"pnl_{round_id}_{len(existing_panels)+1}_{int(time.time())}"
        panel = Panel(
            id=panel_id,
            event_id=event_id,
            round_id=round_id,
            name=panel_name
        )
        event.panels.append(panel)
        return True, f"Created {panel_name}.", panel

    def delete_panel(self, event_id: str, panel_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return False, "Panel not found"

        event.panels.remove(panel)
        return True, f"Panel '{panel.name}' deleted."

    def assign_judge_to_panel(self, event_id: str, panel_id: str, judge_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return False, "Panel not found"

        if judge_id not in event.judge_ids:
            return False, "User is not a judge in this event."

        # Judges can be assigned to panels; remove from other panels in this round to avoid duplicate judging
        for other_p in event.panels:
            if other_p.round_id == panel.round_id and judge_id in other_p.judge_ids:
                other_p.judge_ids.remove(judge_id)

        panel.judge_ids.append(judge_id)
        judge = self.users.get(judge_id)
        return True, f"Assigned Judge {judge.name if judge else judge_id} to {panel.name}."

    def remove_judge_from_panel(self, event_id: str, panel_id: str, judge_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return False, "Panel not found"

        if judge_id in panel.judge_ids:
            panel.judge_ids.remove(judge_id)
            return True, "Judge removed from panel."
        return False, "Judge not found in this panel."

    def assign_team_to_panel(self, event_id: str, panel_id: str, team_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return False, "Panel not found"

        # Remove team from any other panel in the same round
        for p in event.panels:
            if p.round_id == panel.round_id and team_id in p.team_ids:
                p.team_ids.remove(team_id)

        panel.team_ids.append(team_id)
        team = self.get_team(event_id, team_id)
        return True, f"Assigned Team '{team.name if team else team_id}' to {panel.name}."

    def remove_team_from_panel(self, event_id: str, panel_id: str, team_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return False, "Panel not found"

        if team_id in panel.team_ids:
            panel.team_ids.remove(team_id)
            return True, "Team removed from panel."
        return False, "Team not found in panel."

    def auto_balance_teams(self, event_id: str, round_id: str) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panels = [p for p in event.panels if p.round_id == round_id]
        if not panels:
            return False, "No panels exist for this round. Create at least one panel first."

        # Clear teams from these panels
        for p in panels:
            p.team_ids.clear()

        # Gather eligible active teams for this round
        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        is_first_round = (event.rounds and round_obj and event.rounds[0].id == round_id)

        eligible_teams = []
        for t in event.teams:
            if t.is_disqualified:
                continue
            if is_first_round:
                eligible_teams.append(t)
            else:
                # If qualified in previous round or explicitly marked ACTIVE/QUALIFIED
                prev_round_idx = [r.id for r in event.rounds].index(round_id) - 1
                prev_round = event.rounds[prev_round_idx]
                prev_status = t.round_status.get(prev_round.id, STATUS_ACTIVE)
                if prev_status in [STATUS_QUALIFIED, STATUS_ACTIVE]:
                    eligible_teams.append(t)

        if not eligible_teams:
            # Fall back to all non-disqualified teams if none explicitly marked
            eligible_teams = [t for t in event.teams if not t.is_disqualified]

        # Distribute evenly
        for idx, team in enumerate(eligible_teams):
            target_panel = panels[idx % len(panels)]
            target_panel.team_ids.append(team.id)

        return True, f"Distributed {len(eligible_teams)} teams across {len(panels)} panel(s)."

    # ---------------------------------------------------------
    # Scoring & Judging
    # ---------------------------------------------------------
    def get_judge_panel_and_teams(
        self,
        event_id: str,
        round_id: str,
        judge_id: str
    ) -> Tuple[Optional[Panel], List[Team]]:
        event = self.events.get(event_id)
        if not event:
            return None, []

        panel = next((p for p in event.panels if p.round_id == round_id and judge_id in p.judge_ids), None)
        if not panel:
            return None, []

        teams = [t for t in event.teams if t.id in panel.team_ids and not t.is_disqualified]
        return panel, teams

    def get_team_scores_by_judge(
        self,
        event_id: str,
        round_id: str,
        judge_id: str,
        team_id: str
    ) -> Dict[str, Dict[str, any]]:
        """Returns map: criterion_id -> {'value': float, 'comment': str, 'updated_at': str}"""
        event = self.events.get(event_id)
        if not event:
            return {}

        results = {}
        for s in event.scores:
            if s.round_id == round_id and s.judge_id == judge_id and s.team_id == team_id:
                results[s.criterion_id] = {
                    "value": s.value,
                    "comment": s.comment,
                    "updated_at": s.updated_at
                }
        return results

    def save_score(
        self,
        event_id: str,
        round_id: str,
        panel_id: str,
        judge_id: str,
        team_id: str,
        criterion_id: str,
        value: float,
        comment: str
    ) -> Tuple[bool, str, str]:
        """Save a single criterion score. Returns (success, message, timestamp_str)."""
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found", ""

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return False, "Round not found", ""

        if round_obj.is_closed:
            return False, "This round has been closed. Scores are read-only.", ""

        crit = next((c for c in round_obj.criteria if c.id == criterion_id), None)
        if not crit:
            return False, "Criterion not found in this round", ""

        if value < 0 or value > crit.max_score:
            return False, f"Score must be between 0 and {crit.max_score}", ""

        now_str = datetime.now().strftime("%H:%M:%S")

        # Find existing record or add
        existing = next(
            (s for s in event.scores if s.round_id == round_id and s.judge_id == judge_id
             and s.team_id == team_id and s.criterion_id == criterion_id),
            None
        )

        if existing:
            existing.value = float(value)
            existing.comment = comment.strip()
            existing.updated_at = now_str
        else:
            rec_id = f"scr_{round_id}_{judge_id}_{team_id}_{criterion_id}"
            new_rec = ScoreRecord(
                id=rec_id,
                event_id=event_id,
                round_id=round_id,
                panel_id=panel_id,
                judge_id=judge_id,
                team_id=team_id,
                criterion_id=criterion_id,
                value=float(value),
                comment=comment.strip(),
                updated_at=now_str
            )
            event.scores.append(new_rec)

        return True, "Score saved.", now_str

    def calculate_weighted_total_for_judge(
        self,
        event_id: str,
        round_id: str,
        judge_id: str,
        team_id: str
    ) -> float:
        """Formula: sum( (value / max_score) * weight )"""
        event = self.events.get(event_id)
        if not event:
            return 0.0

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return 0.0

        scores = self.get_team_scores_by_judge(event_id, round_id, judge_id, team_id)
        total = 0.0
        for crit in round_obj.criteria:
            if crit.id in scores:
                val = scores[crit.id]["value"]
                if crit.max_score > 0:
                    total += (val / crit.max_score) * crit.weight
        return round(total, 2)

    # ---------------------------------------------------------
    # Results & Round Closing
    # ---------------------------------------------------------
    def get_panel_ranked_teams(
        self,
        event_id: str,
        round_id: str,
        panel_id: str
    ) -> List[Dict[str, any]]:
        event = self.events.get(event_id)
        if not event:
            return []

        panel = next((p for p in event.panels if p.id == panel_id), None)
        if not panel:
            return []

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return []

        ranked_list = []
        for tid in panel.team_ids:
            team = self.get_team(event_id, tid)
            if not team:
                continue

            # Average score across all panel judges
            judge_totals = []
            for jid in panel.judge_ids:
                total_for_j = self.calculate_weighted_total_for_judge(event_id, round_id, jid, tid)
                judge_totals.append(total_for_j)

            avg_score = round(sum(judge_totals) / len(judge_totals), 2) if judge_totals else 0.0
            round_status = team.round_status.get(round_id, STATUS_ACTIVE)

            ranked_list.append({
                "team": team,
                "average_score": avg_score,
                "judge_scores": judge_totals,
                "round_status": round_status,
                "is_disqualified": team.is_disqualified,
                "registered_at": team.registered_at
            })

        # Rank: Disqualified at bottom, then higher average score, tie-break: earlier registered_at wins
        def sort_key(item):
            disq = 1 if item["is_disqualified"] else 0
            score = item["average_score"]
            reg_time = item["registered_at"]
            return (disq, -score, reg_time)

        ranked_list.sort(key=sort_key)
        for idx, item in enumerate(ranked_list, start=1):
            item["rank"] = idx

        return ranked_list

    def check_missing_scores(self, event_id: str, round_id: str) -> List[str]:
        event = self.events.get(event_id)
        if not event:
            return ["Event not found"]

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return ["Round not found"]

        panels = [p for p in event.panels if p.round_id == round_id]
        if not panels:
            return ["No panels defined for this round."]

        missing = []
        for panel in panels:
            if not panel.judge_ids:
                missing.append(f"{panel.name}: No judges assigned")
                continue
            if not panel.team_ids:
                continue

            for tid in panel.team_ids:
                team = self.get_team(event_id, tid)
                if not team or team.is_disqualified:
                    continue

                for jid in panel.judge_ids:
                    judge = self.users.get(jid)
                    j_name = judge.name if judge else jid
                    team_scores = self.get_team_scores_by_judge(event_id, round_id, jid, tid)

                    for crit in round_obj.criteria:
                        if crit.id not in team_scores:
                            missing.append(f"{panel.name}: Judge {j_name} has not scored '{team.name}' on '{crit.name}'")

        return missing

    def close_round(self, event_id: str, round_id: str, allow_partial: bool = False) -> Tuple[bool, str, List[str]]:
        """Closes a round. Blocked if missing scores unless explicitly allowed."""
        missing = self.check_missing_scores(event_id, round_id)
        if missing and not allow_partial:
            return False, f"Cannot close round: {len(missing)} score(s) are missing.", missing

        event = self.events.get(event_id)
        if not event:
            return False, "Event not found", []

        round_obj = next((r for r in event.rounds if r.id == round_id), None)
        if not round_obj:
            return False, "Round not found", []

        round_obj.is_closed = True
        return True, f"'{round_obj.name}' has been successfully closed! Scores are now locked.", []

    def advance_top_n_per_panel(self, event_id: str, round_id: str, n: int) -> Tuple[bool, str]:
        event = self.events.get(event_id)
        if not event:
            return False, "Event not found"

        panels = [p for p in event.panels if p.round_id == round_id]
        if not panels:
            return False, "No panels found for this round."

        total_advanced = 0
        for panel in panels:
            ranked = self.get_panel_ranked_teams(event_id, round_id, panel.id)
            active_teams = [item for item in ranked if not item["is_disqualified"]]

            for idx, item in enumerate(active_teams):
                team = item["team"]
                if idx < n:
                    team.round_status[round_id] = STATUS_QUALIFIED
                    total_advanced += 1
                else:
                    team.round_status[round_id] = STATUS_ELIMINATED

        return True, f"Advanced top {n} team(s) from each panel (total {total_advanced} teams advanced)."

    def set_team_round_status(
        self,
        event_id: str,
        round_id: str,
        team_id: str,
        status: str
    ) -> Tuple[bool, str]:
        team = self.get_team(event_id, team_id)
        if not team:
            return False, "Team not found"

        team.round_status[round_id] = status
        return True, f"Team '{team.name}' status set to {status}."

    # ---------------------------------------------------------
    # Leaderboard & Statistics
    # ---------------------------------------------------------
    def get_leaderboard_data(self, event_id: str) -> Dict[str, any]:
        event = self.events.get(event_id)
        if not event:
            return {
                "ranked_teams": [],
                "podium": [],
                "stats": {
                    "total_teams": 0,
                    "total_rounds": 0,
                    "disqualified_count": 0,
                    "winner": "N/A",
                    "highest_score": 0.0,
                    "avg_score": 0.0
                },
                "chart_data": []
            }

        # Calculate overall score per team across all closed or active rounds
        ranked = []
        for team in event.teams:
            round_scores = {}
            total_sum = 0.0
            rounds_counted = 0

            for r in event.rounds:
                # Find panels team was in
                panel = next((p for p in event.panels if p.round_id == r.id and team.id in p.team_ids), None)
                if panel and panel.judge_ids:
                    judge_scores = [
                        self.calculate_weighted_total_for_judge(event_id, r.id, jid, team.id)
                        for jid in panel.judge_ids
                    ]
                    avg_r = sum(judge_scores) / len(judge_scores) if judge_scores else 0.0
                    round_scores[r.name] = round(avg_r, 2)
                    total_sum += avg_r
                    rounds_counted += 1
                else:
                    round_scores[r.name] = 0.0

            overall_score = round(total_sum / rounds_counted, 2) if rounds_counted > 0 else 0.0

            ranked.append({
                "team": team,
                "overall_score": overall_score,
                "round_scores": round_scores,
                "is_disqualified": team.is_disqualified,
                "reason": team.disqualification_reason,
                "registered_at": team.registered_at
            })

        # Sort: Disqualified at bottom, then overall_score DESC, tie-break: earlier registered_at wins
        def sort_lb(item):
            disq = 1 if item["is_disqualified"] else 0
            score = item["overall_score"]
            reg = item["registered_at"]
            return (disq, -score, reg)

        ranked.sort(key=sort_lb)
        for idx, item in enumerate(ranked, start=1):
            item["rank"] = idx

        # Podium: top 3 non-disqualified teams
        active_teams = [t for t in ranked if not t["is_disqualified"]]
        podium = active_teams[:3]

        # Stats
        disqualified_count = sum(1 for t in event.teams if t.is_disqualified)
        active_scores = [t["overall_score"] for t in active_teams]
        highest = max(active_scores) if active_scores else 0.0
        avg = round(sum(active_scores) / len(active_scores), 2) if active_scores else 0.0
        winner = active_teams[0]["team"].name if active_teams else "None"

        # Chart data: top 8 teams (name, score)
        chart_data = [
            {"name": item["team"].name, "score": item["overall_score"], "disqualified": item["is_disqualified"]}
            for item in ranked[:8]
        ]

        return {
            "ranked_teams": ranked,
            "podium": podium,
            "stats": {
                "total_teams": len(event.teams),
                "total_rounds": len(event.rounds),
                "disqualified_count": disqualified_count,
                "winner": winner,
                "highest_score": highest,
                "avg_score": avg
            },
            "chart_data": chart_data
        }

    # ---------------------------------------------------------
    # Realistic Seed Data
    # ---------------------------------------------------------
    def _seed_data(self):
        # 1. Demo & Staff Users
        alice = User(id="usr_alice", email="alice@hackhub.io", password="password123", name="Alice Organizer", role="ORGANIZER")
        bob = User(id="usr_bob", email="bob@hackhub.io", password="password123", name="Dr. Bob Judge", role="JUDGE")
        dana = User(id="usr_dana", email="dana@hackhub.io", password="password123", name="Dana AI Lead", role="JUDGE")
        edward = User(id="usr_edward", email="edward@hackhub.io", password="password123", name="Edward Architect", role="JUDGE")
        fiona = User(id="usr_fiona", email="fiona@hackhub.io", password="password123", name="Fiona VP Tech", role="JUDGE")

        victor = User(id="usr_victor", email="victor@hackhub.io", password="password123", name="Victor Volunteer", role="VOLUNTEER")
        valerie = User(id="usr_valerie", email="valerie@hackhub.io", password="password123", name="Valerie Volunteer", role="VOLUNTEER")

        # 12 Participants
        charlie = User(id="usr_charlie", email="charlie@hackhub.io", password="password123", name="Charlie Coder", role="PARTICIPANT")
        david = User(id="usr_david", email="david@hackhub.io", password="password123", name="David Data", role="PARTICIPANT")
        emma = User(id="usr_emma", email="emma@hackhub.io", password="password123", name="Emma Engineer", role="PARTICIPANT")
        frank = User(id="usr_frank", email="frank@hackhub.io", password="password123", name="Frank Frontend", role="PARTICIPANT")
        grace = User(id="usr_grace", email="grace@hackhub.io", password="password123", name="Grace Guard", role="PARTICIPANT")
        heidi = User(id="usr_heidi", email="heidi@hackhub.io", password="password123", name="Heidi Hacker", role="PARTICIPANT")
        ivan = User(id="usr_ivan", email="ivan@hackhub.io", password="password123", name="Ivan Innovator", role="PARTICIPANT")
        judy = User(id="usr_judy", email="judy@hackhub.io", password="password123", name="Judy Java", role="PARTICIPANT")
        kevin = User(id="usr_kevin", email="kevin@hackhub.io", password="password123", name="Kevin Cloud", role="PARTICIPANT")
        liam = User(id="usr_liam", email="liam@hackhub.io", password="password123", name="Liam Logic", role="PARTICIPANT")
        mona = User(id="usr_mona", email="mona@hackhub.io", password="password123", name="Mona Motion", role="PARTICIPANT")
        noah = User(id="usr_noah", email="noah@hackhub.io", password="password123", name="Noah Network", role="PARTICIPANT")

        all_seed_users = [
            alice, bob, dana, edward, fiona, victor, valerie,
            charlie, david, emma, frank, grace, heidi, ivan, judy, kevin, liam, mona, noah
        ]
        for u in all_seed_users:
            self.users[u.id] = u

        # -----------------------------------------------------
        # Event 2: "Nexus Spring Hackathon" (STATUS_JUDGING)
        # 4 judges, 2 volunteers, 12 participants in 6 teams,
        # 2 rounds (R1 with 2 panels, final with 1 panel),
        # weights total 100, saved scores, 1 disqualified team.
        # -----------------------------------------------------
        e2_id = "evt_nexus_2026"

        # Criteria for Round 1 (weights total 100)
        c1_1 = Criterion(id="crit_r1_1", name="Technical Innovation", max_score=10.0, weight=35.0)
        c1_2 = Criterion(id="crit_r1_2", name="Execution & Design", max_score=10.0, weight=30.0)
        c1_3 = Criterion(id="crit_r1_3", name="Practical Utility", max_score=10.0, weight=20.0)
        c1_4 = Criterion(id="crit_r1_4", name="Pitch & Presentation", max_score=10.0, weight=15.0)

        r1 = Round(
            id="rnd_nexus_1",
            event_id=e2_id,
            round_number=1,
            name="Preliminary Round",
            is_closed=False,
            criteria=[c1_1, c1_2, c1_3, c1_4]
        )

        # Criteria for Round 2 (Final Round - weights total 100)
        c2_1 = Criterion(id="crit_r2_1", name="Market Feasibility", max_score=10.0, weight=40.0)
        c2_2 = Criterion(id="crit_r2_2", name="Scalability & Security", max_score=10.0, weight=30.0)
        c2_3 = Criterion(id="crit_r2_3", name="Final Stage Polish", max_score=10.0, weight=30.0)

        r2 = Round(
            id="rnd_nexus_2",
            event_id=e2_id,
            round_number=2,
            name="Grand Finale",
            is_closed=False,
            criteria=[c2_1, c2_2, c2_3]
        )

        base_time = time.time() - 86400  # 1 day ago

        # 6 Teams
        t1 = Team(
            id="tm_nexus_1",
            event_id=e2_id,
            name="NeuralCraft",
            members=["Charlie Coder", "David Data"],
            project_title="AI Code Review Copilot",
            description="Autonomous AST analyzer that predicts runtime memory bugs and race conditions.",
            repo_url="https://github.com/neuralcraft/copilot-ai",
            checked_in=True,
            is_disqualified=False,
            registered_at=base_time + 100,
            creator_user_id=charlie.id,
            round_status={r1.id: STATUS_ACTIVE}
        )

        t2 = Team(
            id="tm_nexus_2",
            event_id=e2_id,
            name="QuantumLeap",
            members=["Emma Engineer", "Frank Frontend"],
            project_title="Visual Qubit Simulator",
            description="Browser-based quantum computing visualizer for high school educators.",
            repo_url="https://github.com/quantumleap/qubit-sim",
            checked_in=True,
            is_disqualified=False,
            registered_at=base_time + 200,
            creator_user_id=emma.id,
            round_status={r1.id: STATUS_ACTIVE}
        )

        t3 = Team(
            id="tm_nexus_3",
            event_id=e2_id,
            name="CyberShield",
            members=["Grace Guard", "Heidi Hacker"],
            project_title="Zero-Trust API Gateway",
            description="eBPF-powered real-time anomaly detection and rate limiter.",
            repo_url="https://github.com/cybershield/ebpf-gateway",
            checked_in=True,
            is_disqualified=False,
            registered_at=base_time + 300,
            creator_user_id=grace.id,
            round_status={r1.id: STATUS_ACTIVE}
        )

        t4 = Team(
            id="tm_nexus_4",
            event_id=e2_id,
            name="BioPulse",
            members=["Ivan Innovator", "Judy Java"],
            project_title="Wearable Arrhythmia Alert",
            description="Low-power firmware for BLE medical sensors with edge ML classification.",
            repo_url="https://github.com/biopulse/arrhythmia-firmware",
            checked_in=True,
            is_disqualified=False,
            registered_at=base_time + 400,
            creator_user_id=ivan.id,
            round_status={r1.id: STATUS_ACTIVE}
        )

        t5 = Team(
            id="tm_nexus_5",
            event_id=e2_id,
            name="EcoTrack",
            members=["Kevin Cloud", "Liam Logic"],
            project_title="Serverless Carbon Counter",
            description="FinOps dashboard calculating real-time CO2 emissions from Kubernetes pods.",
            repo_url="https://github.com/ecotrack/k8s-carbon-telemetry",
            checked_in=False,
            is_disqualified=False,
            registered_at=base_time + 500,
            creator_user_id=kevin.id,
            round_status={r1.id: STATUS_ACTIVE}
        )

        # One Disqualified team with reason
        t6 = Team(
            id="tm_nexus_6",
            event_id=e2_id,
            name="PixelPioneers",
            members=["Mona Motion", "Noah Network"],
            project_title="Generative Pixel Game Engine",
            description="Procedural sprite generator for 2D retro indie games.",
            repo_url="https://github.com/pixelpioneers/sprite-forge",
            checked_in=True,
            is_disqualified=True,
            disqualification_reason="Violated open-source licensing: submitted an existing unmodified third-party library.",
            registered_at=base_time + 600,
            creator_user_id=mona.id,
            round_status={r1.id: STATUS_DISQUALIFIED}
        )

        # Panels: Round 1 has 2 panels, Round 2 has 1 panel
        p1 = Panel(
            id="pnl_r1_alpha",
            event_id=e2_id,
            round_id=r1.id,
            name="Panel Alpha (Software & AI)",
            judge_ids=[bob.id, dana.id],
            team_ids=[t1.id, t2.id, t3.id]
        )

        p2 = Panel(
            id="pnl_r1_beta",
            event_id=e2_id,
            round_id=r1.id,
            name="Panel Beta (Systems & Hardware)",
            judge_ids=[edward.id, fiona.id],
            team_ids=[t4.id, t5.id, t6.id]
        )

        p_final = Panel(
            id="pnl_r2_grand",
            event_id=e2_id,
            round_id=r2.id,
            name="Finalists Grand Stage",
            judge_ids=[bob.id, dana.id, edward.id, fiona.id],
            team_ids=[]  # Teams advance here after Round 1
        )

        # Saved scores by Bob (for Team 1 & Team 2) and Dana (for Team 1)
        scores_list = [
            # Bob judging Team 1 (NeuralCraft)
            ScoreRecord("s1", e2_id, r1.id, p1.id, bob.id, t1.id, c1_1.id, 9.5, "Superb AST heuristics!", "14:12:05"),
            ScoreRecord("s2", e2_id, r1.id, p1.id, bob.id, t1.id, c1_2.id, 8.5, "Clean UI and smooth latency.", "14:14:22"),
            ScoreRecord("s3", e2_id, r1.id, p1.id, bob.id, t1.id, c1_3.id, 9.0, "High commercial demand.", "14:15:30"),
            ScoreRecord("s4", e2_id, r1.id, p1.id, bob.id, t1.id, c1_4.id, 8.0, "Great live demonstration.", "14:16:10"),
            # Bob judging Team 2 (QuantumLeap)
            ScoreRecord("s5", e2_id, r1.id, p1.id, bob.id, t2.id, c1_1.id, 8.0, "Creative teaching approach.", "14:22:15"),
            ScoreRecord("s6", e2_id, r1.id, p1.id, bob.id, t2.id, c1_2.id, 7.5, "Canvas graphics are intuitive.", "14:23:40"),
            ScoreRecord("s7", e2_id, r1.id, p1.id, bob.id, t2.id, c1_3.id, 8.0, "Helpful for physics curricula.", "14:25:01"),
            ScoreRecord("s8", e2_id, r1.id, p1.id, bob.id, t2.id, c1_4.id, 9.0, "Crisp slides and delivery.", "14:26:12"),
            # Dana judging Team 1 (NeuralCraft)
            ScoreRecord("s9", e2_id, r1.id, p1.id, dana.id, t1.id, c1_1.id, 9.0, "Very sound architecture.", "14:30:11"),
            ScoreRecord("s10", e2_id, r1.id, p1.id, dana.id, t1.id, c1_2.id, 9.0, "Impressive CLI + GUI duo.", "14:31:00"),
            ScoreRecord("s11", e2_id, r1.id, p1.id, dana.id, t1.id, c1_3.id, 8.5, "Scales well on large codebases.", "14:32:15"),
            ScoreRecord("s12", e2_id, r1.id, p1.id, dana.id, t1.id, c1_4.id, 8.5, "Handled Q&A with deep knowledge.", "14:33:45"),
        ]

        event_nexus = Event(
            id=e2_id,
            title="Nexus Spring Hackathon 2026",
            description="The premier collegiate engineering challenge focusing on AI, DevTools, and Cloud Infrastructure.",
            status=STATUS_JUDGING,
            organizer_id=alice.id,
            judge_ids=[bob.id, dana.id, edward.id, fiona.id],
            volunteer_ids=[victor.id, valerie.id],
            rounds=[r1, r2],
            panels=[p1, p2, p_final],
            teams=[t1, t2, t3, t4, t5, t6],
            scores=scores_list,
            created_at=base_time
        )
        self.events[e2_id] = event_nexus

        # -----------------------------------------------------
        # Event 1: "HackAI Global Summit" (STATUS_REGISTRATION_OPEN)
        # -----------------------------------------------------
        e1_id = "evt_hackai_2026"

        r1_e1 = Round(
            id="rnd_hackai_1",
            event_id=e1_id,
            round_number=1,
            name="Qualifying Round",
            criteria=[
                Criterion(id="crit_hai_1", name="Originality", max_score=10.0, weight=40.0),
                Criterion(id="crit_hai_2", name="Technical Difficulty", max_score=10.0, weight=30.0),
                Criterion(id="crit_hai_3", name="Design & Polish", max_score=10.0, weight=30.0),
            ]
        )

        r2_e1 = Round(
            id="rnd_hackai_2",
            event_id=e1_id,
            round_number=2,
            name="Final Presentations",
            criteria=[
                Criterion(id="crit_hai_4", name="Impact & Execution", max_score=10.0, weight=60.0),
                Criterion(id="crit_hai_5", name="Audience Pitch", max_score=10.0, weight=40.0),
            ]
        )

        p_hai_final = Panel(
            id="pnl_hai_final",
            event_id=e1_id,
            round_id=r2_e1.id,
            name="Championship Panel"
        )

        event_hackai = Event(
            id=e1_id,
            title="HackAI Global Summit 2026",
            description="Worldwide open hackathon exploring generative interfaces, autonomous agents, and ambient computing.",
            status=STATUS_REG_OPEN,
            organizer_id=alice.id,
            judge_ids=[bob.id, dana.id],
            volunteer_ids=[victor.id],
            rounds=[r1_e1, r2_e1],
            panels=[p_hai_final],
            teams=[],
            scores=[],
            created_at=base_time - 86400 * 3
        )
        self.events[e1_id] = event_hackai
