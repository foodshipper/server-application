# Notifications
Foodship sends notifications to users, eg. when they have a new Group Invitation pending. Clients have to store their Firebase Notification Token on the Server, see [API Documentation](/ean/endpoints/Endpoints.md#put-userfirebase-token).

## Invitation Notification
User receive an invitation Notification when they have an invitation pending. The Notification has the following data:
```json
{
    "status": "invited",
    "group_id": 12,
    "date": "2016-12-04"
}
```