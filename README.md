# ChatWithLocalAI

## How to use
1. Install and run OLLAMA
2. Run a redis docker container.
* sudo docker run -d --rm -p 6378:6379 redis:8
3. Run a Django Application
* source DjangoChannel/.venv/bin/activate
* cd ./DjangoChannel
* python manage.py runserver
4. Run npm dev server
* cd Djangochannel/React/FrondEnd
* npm run dev
5. Access to the page
* Open a browser and type "localhost:5173"

## features I want to add
### React
* websocket connection indicator

## How to set a CSRF token in FrontEnd
### 1. Retrieve CSRF cookie
Before accessing the server with a method like POST, you need to reach the dedicated endpoint /api/csrf for CSRF cookie, and then a csrf token is set in cookie.

### Case Study (React)
## 1. Retrive a csrf cookie 
const API_URL = "https://api.example.com";

let csrfToken = null;

async function initializeCSRF() {
    const response = await fetch(`${API_URL}/api/csrf/`, {
        credentials: "include",
    });

    if (!response.ok) {
        throw new Error("Failed to initialize CSRF");
    }

    const data = await response.json();
    csrfToken = data.csrfToken;
}
## 2. Access the server
async function updateProfile() {
    if (!csrfToken) {
        await initializeCSRF();
    }

    const response = await fetch(`${API_URL}/api/profile/`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            username: "new_username"
        }),
    });

    return response.json();
}