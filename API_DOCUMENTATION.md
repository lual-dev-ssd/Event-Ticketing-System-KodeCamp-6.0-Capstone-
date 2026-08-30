# Event Ticketing API Documentation 

**Base URL:** `http://localhost:8080/api/v1`
**Authentication:** Bearer Token (`Authorization: Bearer <access_token>`)

---
## 1. Authentication (`/auth`)

### Register User
* **Method:** `POST`
* **Endpoint:** `api/v1/auth/reqister`
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
* **Endpoint:** `api/v1/auth/verify-email`
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
* **Endpoint:** `api/v1/auth/token`
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
* **Endpoint:** `api/v1/auth/refresh_token`
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
* **Endpoint:** `api/v1/users/me`
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
* **Endpoint:** `api/v1/users/me`
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
* **Endpoint:** `api/v1/events/`
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
* **Endpoint:** `api/v1/events/{event_id}`
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
* **Endpoint:** `api/v1/events/{event_id}`
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
* **Endpoint:** `api/v1/events/{event_id}/attendees`
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
* **Endpoint:** `api/v1/tickets/`
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
* **Endpoint:** `api/v1/tickets/me`
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
* **Endpoint:** `api/v1/tickets/event/{event_id}`
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
* **Endpoint:** `api/v1/tickets/{ticket_id}/cancel`
* **Auth Required:** Yes(Bearer)

### Response
* **200 Ok**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "string",
  
}
```
### Initiate MoMo Payment
Initiate a ticket purchase via MTN Mobile Money. The backend dynamically retrieves the event ticket price from PostgreSQL to prevent requestion tampering
* **Method:** `POST`
* **Endpoint:** `api/v1/payments/momo/initiate`
* **Auth Required:** Yes(Bearer)

### Request Body
```json
 {
    "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "phone_number": "46733123453",
  }
```

### Response
* **202 Accepted**

```json
{
  "Message": "Payment prompt sent to mobile device",
  "ticket_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "pending_payment"
}
```
### Error Response:
* **404 NOT FOUND**: Event ID does not exist
* **400 BAD REQUEST**: Event Is sout out or payment initiation failed
* **403 SERVICE UNAVAILABLE**: MoMo payment gateway circuit breaker tripped


### MoMo Webhook Callback
Asynchronous webhook endpoint called by MYN MoMo to notify the Backend of transaction completion
* **Method:** `POST`
* **Endpoint:** `api/v1/payments/momo/callback`
* **Auth Required:** `No` called by Provider

### Request Body
```json
{
  "externalId": "25c2de8a-bce1-4018-9da1-454d0db2865b",
  "status": "SUCCESSFUL",
  "financialTransactionId": "123456789",
  "amount": "10.00",
  "currency": "EUR",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "46733123453"
  }
}
```

### Response
* **202 Accepted**

```json
{
  "status": "SUCCESSFUL",
  "message": "Payment confirmed and PDF ticket sent."
}
```

### Check In Ticket
* **Method:** `PATCH`
* **Endpoint:** `api/v1/tickets/{ticket_id}/check-in`
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