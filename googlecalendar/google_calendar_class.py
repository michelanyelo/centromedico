import os.path
import datetime as dt
from datetime import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "primary"


class GoogleCalendarManager:
    """
    Class to manage events in Google Calendar.
    """

    def __init__(self):
        """
        Initializes the Google Calendar service.
        """
        self.service = self._authenticate()

    def _authenticate(self):

        # Obtén la ruta al directorio actual (donde se encuentra este script)
        """
        Authenticates the application and returns the Google Calendar service.
        """
        creds = None
        current_directory = os.path.dirname(os.path.abspath(__file__))
        token_path = os.path.join(current_directory, 'token.json')
        credentials_path = os.path.join(current_directory, 'credentials.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    def _handle_http_error(self, error):
        """
        Handles HTTP errors.
        """
        print(f"An HTTP error occurred: {error}")
        # Properly handle the HTTP error

    def _print_event_details(self, event):
        """
        Prints the details of an event.
        """
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

    # def list_upcoming_events(self):
    #     """
    #     Lists the upcoming 10 events.
    #     """
    #     now = dt.datetime.now(timezone.utc).isoformat()
    #     print(f"Getting the upcoming 10 events from: {now}")
    #     try:
    #         events_result = (
    #             self.service.events()
    #             .list(
    #                 calendarId=CALENDAR_ID,
    #                 timeMin=now,
    #                 maxResults=10,
    #                 singleEvents=True,
    #                 orderBy="startTime",
    #             )
    #             .execute()
    #         )
    #         events = events_result.get("items", [])
    #         if not events:
    #             print("No upcoming events found.")
    #         else:
    #             print(f"Found {len(events)} events.")
    #             for event in events:
    #                 self._print_event_details(event)
    #         return events
    #     except HttpError as error:
    #         self._handle_http_error(error)
    #         return []

    def list_all_events(self):
        """
        Lists all events.
        """
        print("Getting all events.")
        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId=CALENDAR_ID,
                    maxResults=2500,  # Adjust maxResults as needed
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            if not events:
                print("No events found.")
            else:
                print(f"Found {len(events)} events.")
                for event in events:
                    self._print_event_details(event)
            return events
        except HttpError as error:
            self._handle_http_error(error)
            return []

    def list_events_in_date_range(self, start_date, end_date):
        """
        Lists events in a specific date range.
        """
        print(f"Getting events from {start_date} to {end_date}")
        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId=CALENDAR_ID,
                    timeMin=start_date.isoformat(),
                    timeMax=end_date.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            if not events:
                print("No events found.")
            else:
                print(f"Found {len(events)} events.")
                for event in events:
                    self._print_event_details(event)
            return events
        except HttpError as error:
            self._handle_http_error(error)
            return []

    def create_event(self, summary, start_time, end_time, timezone, attendees=None):
        """
        Creates a new event in the calendar.
        """
        event = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        }
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]
        try:
            event = self.service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except HttpError as error:
            self._handle_http_error(error)

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        """
        Updates an existing event in the calendar.
        """
        try:
            event = self.service.events().get(
                calendarId=CALENDAR_ID, eventId=event_id).execute()
            if summary:
                event["summary"] = summary
            if start_time:
                event["start"]["dateTime"] = start_time.isoformat()
            if end_time:
                event["end"]["dateTime"] = end_time.isoformat()
            updated_event = self.service.events().update(
                calendarId=CALENDAR_ID, eventId=event_id, body=event
            ).execute()
            return updated_event
        except HttpError as error:
            self._handle_http_error(error)

    def delete_event(self, event_id):
        """
        Deletes an event from the calendar.
        """
        try:
            self.service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
            return True
        except HttpError as error:
            self._handle_http_error(error)


if __name__ == "__main__":
    calendar = GoogleCalendarManager()

    # calendar.list_upcoming_events()

    # calendar.create_event(
    #     "Camila: Psicología I.J",
    #     "2024-04-09T09:00:00",  # Start time: 09:00 am in Santiago
    #     "2024-04-09T10:00:00",  # End time: 10:00 am in Santiago
    #     "America/Santiago",
    #     ["camila@correo.cl", "paciente@quillota.cl"]
    # )
