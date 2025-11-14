🚀 Pet Service (Microservice)
This is a pet-service, a FastAPI microservice developed for the Software Architecture course. It manages pet mood.

This service uses MongoDB for data persistence and follows Clean Architecture principles, separating logic into Domain, Usecase, Adapters, and Infrastructure layers.

🛠 Tech Stack
Framework: FastAPI
Database: MongoDB (local) / MongoDB Atlas (cloud)
Containerization: Docker / Docker Compose
Deployment Platform: Render
Validation: Pydantic
Authentication: JWT (python-jose) & Passlib
☁️ Cloud Deployment (Render + MongoDB Atlas)
This is the primary production deployment required by the assignment.

Live Endpoints:

Live URL: https://pet-service-dztd.onrender.com
Swagger UI (Docs): https://pet-service-dztd.onrender.com/docs
DB Health Check: https://pet-service-dztd.onrender.com/health/db
Deployment Setup
The service is deployed on Render using Docker. It connects to a MongoDB Atlas M0 free-tier cluster.

Environment Variables configured in Render:

MONGO_URI: mongodb+srv://task_user:1234@cluster0.iq3k1vm.mongodb.net/?appName=Cluster0
DB_NAME: petdb
NOTIFICATION_SERVICE_URL: https://notification-service-huk0.onrender.com
👤 Authors
Name: Ellen Seitkassimova, Bauyrzhan Yerzhanov, Eduard Shilke
Course: Software Architecture
