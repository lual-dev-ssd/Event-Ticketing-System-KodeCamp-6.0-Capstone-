# Event Ticketing API Documentation 

**Base URL:** `http://localhost:8080/api/v1`
**Authentication:** Bearer Token (`Authorization: Bearer <access_token>`)

---
## 1. Authentication (`/auth`)

### Register User
* **Method:** `POST`
* **Endpoint:** `/auth/reqister`
* **Auth Required:** No
### Request Body

#### Request body
```json
{
  "email": "user@example.com",
  "name": "string",
  "password": "string"
}
```

### Responses
 * **201 Created**

```json
{
    "message": "User registered successfully. Please check your email to verify your account."
}
```

### Verify Email
* **Medthod:** `GET`
* **Endpoint:** `/auth/verify-email`
* **Auth Required:** No
* **Query Parameter:** `token` (string, required)

### Response
* **200 Ok**

```json
{
    "message": "Email verified successfully. You can now purchase tickets."
}
```

### User Login (Obtain Tokens)
* **Method:** `POST`
* **Endpoint:** `/auth/token`
* **Auth Required:** No
* **Content-Type:** application/x-www-form-urlencoded

### Request Body (Form Data)
* **username:** **user@example.com**
* **password:** **SecurePassword123!**

### Response
* **200 Ok**

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "string"
}
```

### Refresh Access Token
* **Method:** `POST`
* **Endpoint:** `/auth/refresh_token`
* **Auth Required:** No


### Request Body (Form Data)
```json
{
  "refresh_token": "eyjhGcioJIUzI1Ni..."
}
```

### Response
* **200 Ok**

```json
{
  "access_token": "eyjhGcioJIUzI1Ni...",
  "refresh_token": "eyjhGcioJIUzI1Ni...",
  "token_type": "bearer"
}
```

---

## 2. Users(/users)

### Read Users Me
* **Method:**: `GET`
* **Endpoint:** `/users/me
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
  "email": "user@example.com",
  "name": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_verified": true,
  "is_admin": true,
  "is_active": true,
  "created_at": "2026-08-27T14:52:35.115Z",
  "updated_at": "2026-08-27T14:52:35.115Z"
}
```

### Update My Profile
* **Method:**: `PATCH`
* **Endpoint:** `/users/me
* **Auth Required:** Yes(Bearer)


### Request Body (Form Data)
```json
{
  "name": "example user"
}
```

### Response
* **200 Ok**

```json
{
  "email": "user@example.com",
  "name": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "is_verified": true,
  "is_admin": true,
  "is_active": true,
}
```

---

## 3. Events(/users)

### Create Event
* **Method:** `POST`
* **Endpoint:** `/events/`
* **Auth Required:** Yes(Bearer)

### Request Body
```json
 {
    "title": "string",
    "description": "string",
    "date": "2026-08-27T15:05:00.006Z",
    "location": "string",
    "ticket_price": 0,
    "capacity": 0,
  }
```

### Response
* **200 Ok**

```json

 {
    "title": "string",
    "description": "string",
    "date": "2026-08-27T15:05:00.006Z",
    "location": "string",
    "ticket_price": 0,
    "capacity": 0,
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "organizer_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2026-08-27T15:05:00.006Z",
    "updated_at": "2026-08-27T15:05:00.006Z"
  }

```

### Update Event
* **Method:** `PATCH`
* **Endpoint:** `/events/{event_id}`
* **Auth Required:** Yes(Bearer)


### Request Body
```json
 {
    "title": "string",
    "ticket_price": 0,
  }
```

### Response
* **200 Ok**

```json
{
  "title": "string",
  "ticket_price": 0
}
```

### Delete Event
* **Method:** `DELETE`
* **Endpoint:** `/events/{event_id}`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
 {
    "message": "Event Deleted Successfully",
  }
```


### List Event Attendees
* **Method:** `GET`
* **Endpoint:** `/events/{event_id}/attendees`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "ticket_status": "string",
    "purchase_price": 0,
    "checked_in_at": "2026-08-27T15:24:21.645Z",
    "user": {
      "email": "user@example.com",
      "name": "string",
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "is_verified": true,
      "is_admin": true,
      "is_active": true,
      "created_at": "2026-08-27T15:24:21.645Z",
      "updated_at": "2026-08-27T15:24:21.645Z"
    }
  }
```

---
## 4. Tickets(/users)

### Puchase Ticket
* **Method:** `POST`
* **Endpoint:** `/tickets/`
* **Auth Required:** Yes(Bearer)

### Request Body
```json
{
  "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}
```

### Response
* **200 Ok**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "purchase_price": 0,
  "status": "string",
  "created_at": "2026-08-27T15:27:46.384Z",
  "updated_at": "2026-08-27T15:27:46.384Z"
}
```

### Get My Tickets
* **Method:** `GET`
* **Endpoint:** `/tickets/me`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "purchase_price": 0,
    "status": "string",
    "created_at": "2026-08-27T15:31:59.888Z",
    "updated_at": "2026-08-27T15:31:59.888Z"
  }
```


### Get Events Tickets
* **Method:** `GET`
* **Endpoint:** `/tickets/event/{event_id}`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "purchase_price": 0,
    "status": "string",
    "created_at": "2026-08-27T15:31:59.888Z",
    "updated_at": "2026-08-27T15:31:59.888Z"
  }
```

### Cancel Ticket
* **Method:** `PATCH`
* **Endpoint:** `/tickets/{ticket_id}/cancel`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "string",
  
}
```

### Check In Ticket
* **Method:** `PATCH`
* **Endpoint:** `/tickets/{ticket_id}/check-in`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "checked_in": true,
  "checked_in_at": "2026-11-15T08:45:00Z"
}
```