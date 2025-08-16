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


Of course. A professional `README.md` is the most important part of a public project. It serves as both a manual and a showcase of your skills.

Here is a complete, professionally written `README.md` file for your project. It is written from the perspective of a developer documenting their work. You can copy and paste this directly into the `README.md` file in your GitHub repository.

-----

````markdown
# HealthCheckr 🩺

[![Build Status](https://img.shields.io/badge/CI/CD-Jenkins-blue.svg)](http://localhost:8080)
[![Technology](https://img.shields.io/badge/Technology-Docker-blue.svg)](https://www.docker.com/)
[![Language](https://img.shields.io/badge/Language-Python-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

HealthCheckr is a full-stack, containerized web application for monitoring website uptime and performance. It features a persistent PostgreSQL database, a background Python worker for performing checks, a Flask web dashboard for visualization, and a complete CI/CD pipeline for automated builds and deployments using a custom-built Jenkins server.

---

### ## ✨ Features

-   **Live Status Dashboard:** A clean web interface to view the current status (UP/DOWN), HTTP code, and response time of multiple websites.
-   **Dynamic Website Management:** Add or delete websites to be monitored directly through the UI.
-   **Email Alerting:** Configure email notifications to be sent instantly when a monitored site's status changes.
-   **Fully Containerized:** All services (webapp, background worker, database) are containerized with Docker for a consistent and portable environment.
-   **Automated CI/CD Pipeline:** Integrated with a Jenkins pipeline that automatically builds and deploys the application on every push to the `main` branch.

---

### ## 🏛️ Architecture

#### Application Architecture
The application is orchestrated via Docker Compose, with three core services communicating over a shared Docker network.
```
  Browser
    |
    v
[ Webapp (Flask UI) ] <-----> [ PostgreSQL Database ]
                                     ^
                                     |
                                     | (Reads URLs, Writes Status)
                                     |
                             [ Checker (Python Worker) ]
                                     |
                                     v
                           (Checks External Websites)
```

#### CI/CD Workflow
A custom Jenkins server, also running in a Docker container, automates the deployment lifecycle.
```
[ Developer ] --(git push)--> [ GitHub ] --(triggers)--> [ Jenkins Server ] --(runs pipeline)--> [ Builds & Deploys Application Containers ]
```

---

### ## 🛠️ Technology Stack

-   **Backend:** Python 3.9, Flask
-   **Database:** PostgreSQL
-   **Containerization:** Docker, Docker Compose
-   **CI/CD:** Jenkins (via a custom Docker image)

---

### ##  Prerequisites

Before you begin, ensure you have the following installed on your local machine:
-   [Git](https://git-scm.com/downloads)
-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/) (Included with Docker Desktop)

---

### ## 🚀 Local Setup and Deployment Guide

This guide covers setting up the application and the Jenkins CI/CD pipeline locally.

### ### Part 1: Running the HealthCheckr Application

**1. Clone the Repository**
```bash
git clone [https://github.com/Sadhu2005/HealthCheckr.git](https://github.com/Sadhu2005/HealthCheckr.git)
cd HealthCheckr
```

**2. Configure Environment Variables**
This project uses a `.env` file to manage secrets and local configuration.

-   Make a copy of the example file:
    ```bash
    cp .env.example .env
    ```
-   Edit the `.env` file and add your credentials for email alerts. The `POSTGRES` credentials can be left as is for local development.

**3. Build and Run the Application**
This command will build the `webapp` and `checker` images and start all three application containers in the background.
```bash
docker-compose up --build -d
```

**4. Verify**
-   Check that the containers are running: `docker-compose ps`
-   Open your browser and navigate to `http://localhost:5000` to see the dashboard.

To stop the application, run `docker-compose down`.

---

### ### Part 2: Setting up the Jenkins CI/CD Pipeline

This project includes a custom Jenkins server with all necessary tools pre-installed.

**1. Build the Custom Jenkins Image**
Navigate to the `jenkins-setup` directory and run the build command. This only needs to be done once.
```bash
cd ../jenkins-setup
docker build -t my-jenkins-lts .
```

**2. Run the Custom Jenkins Container**
This command will start your Jenkins server, persist its data in a volume, and give it access to your computer's Docker engine.
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins-lts my-jenkins-lts
```

**3. Initial Jenkins Setup**
-   Navigate to `http://localhost:8080` in your browser.
-   Get the initial admin password by running:
    ```bash
    docker exec jenkins-lts cat /var/jenkins_home/secrets/initialAdminPassword
    ```
-   Paste the password, click "Install suggested plugins," and create your admin user.

**4. Create the Pipeline Job**
-   On the Jenkins dashboard, click **"New Item"**.
-   Enter a name (e.g., `HealthCheckr-Pipeline`), select **"Pipeline"**, and click OK.
-   Scroll down to the "Pipeline" section.
-   Change the **Definition** to **"Pipeline script from SCM"**.
-   Select **"Git"**.
-   **Repository URL**: `https://github.com/Sadhu2005/HealthCheckr.git`
-   **Branch Specifier**: `*/main`
-   Click **Save**.

Your CI/CD pipeline is now fully configured. To test it, make a code change in the `HealthCheckr` project, commit it, and push it to GitHub. Jenkins will automatically start a new build.

---

### ### Part 3: Configuring Gmail Alerts

To receive email alerts, you must use a Google **App Password**. You cannot use your regular account password.

1.  **Enable 2-Step Verification** on your Google Account. App Passwords are only available if this is enabled.
2.  Go to the **[Google App Passwords page](https://myaccount.google.com/apppasswords)**.
3.  Generate a new password for "Mail" on "Other (Custom name)".
4.  Copy the generated 16-digit password.
5.  Paste this password into the `SMTP_PASSWORD` field in your `.env` file and provide your email in `SENDER_EMAIL`.
6.  Restart your application (`docker-compose down && docker-compose up --build -d`) for the changes to take effect.

---

### ## ⚖️ License

This project is licensed under the MIT License. See the `LICENSE` file for details.

````