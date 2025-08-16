# HealthCheckr
A simple web page monitoring tool using Python, Docker, and Jenkins.
# HealthCheckr 🩺 

HealthCheckr is a simple, containerized web application that monitors the health and response time of websites. It features a background worker to perform checks, a PostgreSQL database for storage, and a Flask-based web dashboard to display real-time status. The entire application is orchestrated with Docker Compose and includes a complete CI/CD pipeline configured with Jenkins.

![HealthCheckr Dashboard Screenshot](https://i.imgur.com/L7E1WfK.png) 
*(Suggestion: Take a nice screenshot of your final dashboard and replace this link!)*

---

### ## ✨  Features

* **Real-time Monitoring:**  View the live status (UP/DOWN), HTTP status code, and response time of all monitored websites.
* **Dynamic Configuration:** Add or delete websites to monitor directly from the web interface.
* **Email Alerts:** Configure email addresses to receive instant alerts when a website's status changes from UP to DOWN (or vice-versa).
* **CI/CD Automation:** The project is integrated with a Jenkins pipeline that automatically builds and deploys the application whenever new code is pushed to the `main` branch.
* **Containerized:** All services (webapp, checker, database) are fully containerized with Docker for consistency and ease of deployment.

---

### ## 🏛️ Architecture

The application runs as a multi-container setup managed by Docker Compose. A custom Jenkins server (also running in Docker) is used for CI/CD.



---

### ## 🛠️ Technology Stack

* **Backend:** Python 🐍, Flask
* **Database:** PostgreSQL 🐘
* **Containerization:** Docker 🐳, Docker Compose
* **CI/CD:** Jenkins 🤖

---

### ## 🚀 How to Run Locally

To run this project on your local machine, you'll need Docker and Docker Compose installed.

**1. Clone the repository:**
```bash
git clone [https://github.com/Sadhu2005/HealthCheckr.git](https://github.com/Sadhu2005/HealthCheckr.git)
cd HealthCheckr