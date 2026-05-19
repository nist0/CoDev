# mermaid skill — Examples

## Example 1: Flowchart (request lifecycle)

```mermaid
flowchart LR
    Client([User]) --> LB[Load Balancer]

    subgraph Backend
        LB --> API[ASP.NET Core API]
        API -- cache hit --> Cache[(Redis)]
        API -- cache miss --> DB[(PostgreSQL)]
    end

    API --> Client
```

## Example 2: Sequence diagram (OAuth 2.0 authorization code flow)

```mermaid
sequenceDiagram
    participant U as User
    participant App as Web App
    participant Auth as Auth Server
    participant API as Resource API

    U->>App: Click "Sign in"
    App->>Auth: GET /authorize?client_id=...&response_type=code
    Auth-->>U: Login page
    U->>Auth: Submit credentials
    Auth-->>App: 302 redirect + code
    App->>Auth: POST /token (code + client_secret)
    Auth-->>App: access_token + refresh_token
    App->>API: GET /resource (Bearer access_token)
    API-->>App: 200 OK + data
```

## Example 3: Entity-Relationship diagram

```mermaid
erDiagram
    ORDER {
        uuid id PK
        uuid customer_id FK
        string status
        timestamp created_at
    }
    CUSTOMER {
        uuid id PK
        string email
        string name
    }
    ORDER_LINE {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCT {
        uuid id PK
        string sku
        string name
        decimal price
    }

    CUSTOMER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_LINE : contains
    PRODUCT ||--o{ ORDER_LINE : referenced_in
```

## Example 4: State diagram (order lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Confirmed : payment_captured
    Pending --> Cancelled : payment_failed
    Confirmed --> Shipped : items_dispatched
    Shipped --> Delivered : delivery_confirmed
    Delivered --> [*]
    Cancelled --> [*]
```

## Example 5: Git graph

```mermaid
gitGraph
    commit id: "init"
    branch feat/login
    checkout feat/login
    commit id: "add login form"
    commit id: "add auth service"
    checkout main
    merge feat/login id: "Merge feat/login"
    branch fix/session
    checkout fix/session
    commit id: "fix session expiry"
    checkout main
    merge fix/session id: "Merge fix/session"
```

## Example 6: C4 Context diagram

```mermaid
C4Context
    title System Context — Order Platform
    Person(user, "Customer", "Places and tracks orders")
    System(app, "Order Platform", "Manages product catalog, orders, and payments")
    System_Ext(payment, "Payment Gateway", "Processes card payments (Stripe)")
    System_Ext(email, "Email Service", "Sends transactional emails (SendGrid)")

    Rel(user, app, "Uses", "HTTPS")
    Rel(app, payment, "Charges card", "HTTPS / REST")
    Rel(app, email, "Sends emails", "HTTPS / REST")
```

## Embedding guidance

Always add a prose description before or after complex diagrams:

````markdown
The following diagram shows the OAuth 2.0 authorization code flow used by the web application.

```mermaid

sequenceDiagram
    ...

```

_The app exchanges the authorization code for an access token server-side to avoid exposing secrets to the browser._
````
