# EduTrack Web Frontend 🎓

Interactive web frontend for the **EduTrack Smart Student Academic Performance Monitoring System**.

---

## 🌟 Architecture & Features

- **Multi-Role Dashboards**:
  - **Teacher Portal** (`teacher.html`): View and update student marks across 5 subjects, log attendance, review behavioral remarks, bulk-import students via CSV/Excel (`student_record.csv`, `student_record.xlsx`).
  - **Principal Portal** (`principal.html`): Macro-level performance distributions, inter-class comparisons, and academic health indicators.
  - **Coordinator Portal** (`coordinator.html`): Issue pedagogical directives, track curriculum gaps, and monitor implementation.
  - **Parent Portal** (`parent.html`): Track student marks and topic-level mastery; submit questions/doubts directly to teachers.
  - **Admin Control Portal** (`admin.html`): User provisioning, role assignments, system thresholds, audit logging, and seed controls.
- **Backend Integration**:
  - Directly connects to the **EduTrack Node.js & Express REST API** running on `http://localhost:5000` (or cloud-hosted URL configured in `config.js`).
  - Authenticates users with JWT tokens via `POST /api/v1/auth/login`.
  - Automatically synchronizes students, directives, parent inquiries, and mastery thresholds.
  - Graceful fallback to local simulated session if the backend is offline.

---

## 🚀 Quick Start

### 1. Start the Backend API
From the root workspace:
```bash
cd backend
npm install
npm start
```
The backend server runs on `http://localhost:5000` (auto-seeding initial demo data on first start).

### 2. Launch the Web Frontend
Open `index.html` or `login.html` directly in any web browser, or serve via any static HTTP server:
```bash
# Using VS Code Live Server, or Python:
python -m http.server 3000
```
Then navigate to: `http://localhost:3000`

---

## 🌐 Configuring Backend API URL (`config.js`)

Edit `config.js` to change the backend API endpoint:
```javascript
// In production, set your cloud API URL:
const PRODUCTION_BACKEND_URL = 'https://your-backend-service.onrender.com';
```

---

## 👥 Demo Credentials

| Role | Email | Password | Portal |
| :--- | :--- | :--- | :--- |
| **Teacher** | `teacher@edutrack.edu` | `teach123` | `teacher.html` |
| **Principal** | `principal@edutrack.edu` | `admin123` | `principal.html` |
| **Coordinator (BRC)** | `brc@edutrack.edu` | `brc123` | `coordinator.html` |
| **Parent** | `parent@edutrack.edu` | `parent123` | `parent.html` |
| **System Admin** | `admin@edutrack.edu` | `AdminSecurePass@2026` | `admin.html` |
