# Goal Description
Develop a clean, modern, mobile-first frontend for "Shakti Shield," a women safety web application. The frontend will be built in React and structured to connect seamlessly to the existing backend APIs (Authentication, SOS alerts, Location sharing, Emergency contacts, and Incident reporting). The design language will utilize Purple, White, and Saffron to signify safety and empowerment.

## User Review Required
Please review the proposed UI/UX Wireframes, Page Structure, Component Hierarchy, and styling constraints below before I proceed with the actual implementation (code generation).

## UI/UX Wireframes & Conceptual Design

### Global Layout
- **Mobile-First App Shell**: A fixed bottom navigation bar on mobile for easy reachability.
- **Header**: Branding (Shakti Shield logo), current user profile icon, and dynamic safety status indicator.
- **Colors**:
  - Primary: Purple (`#6B21A8` to `#9333EA`)
  - Accent: Saffron (`#F97316`)
  - Background: Off-white (`#F8FAFC`)

### Home Dashboard Wireframe
```text
+------------------------------------------+
|  [Logo] Shakti Shield        [Profile]   |
|------------------------------------------|
|                                          |
|        +------------------------+        |
|        |                        |        |
|        |                        |        |
|        |       [ S O S ]        |        |
|        |                        |        |
|        | (Tap to Send Alert)    |        |
|        +------------------------+        |
|                                          |
|  [ Quick Actions ]                       |
|  - Report Incident                       |
|  - Share Live Location                   |
|  - Emergency Contacts                    |
|                                          |
|------------------------------------------|
| [Home]  [Map]  [Contacts]  [History]     |
+------------------------------------------+
```

### Emergency Contacts Wireframe
```text
+------------------------------------------+
|  < Back        Trusted Contacts      [+] |
|------------------------------------------|
|                                          |
|  [Icon] Mom                              |
|         +91 9876543210             [Edit]|
|                                          |
|  [Icon] Brother                          |
|         +91 8765432109             [Edit]|
|                                          |
|  [ Add New Contact Button ]              |
|                                          |
|------------------------------------------|
| [Home]  [Map]  [Contacts]  [History]     |
+------------------------------------------+
```

## Page Structure
1. `/login` - Phone/Email login & authentication
2. `/profile` - User profile
3. `/` (Dashboard) - Giant SOS button, safety stats, quick links
4. `/contacts` - Trusted contacts list & management
5. `/location` - Map interface showing live location
6. `/report` - Incident reporting form (Location, description)
7. `/history` - Log of past SOS alerts and incidents

## Component Hierarchy
- `App`
  - `AuthProvider` (Manages user session context)
    - `Router`
      - `Layout` (Contains Header & BottomNav)
        - `Header` (Logo, SafetyStatus)
        - `BottomNavigation` (Home, Map, Contacts, History links)
      - `Pages`
        - `LoginPage`
          - `AuthForm`
        - `DashboardPage`
          - `SOSButton` (Large pulsing button)
          - `ActionCardsGrid` (Tile links to features)
        - `ContactsPage`
          - `ContactList` -> `ContactCard`
          - `ContactFormModal`
        - `LocationPage`
          - `MapViewer`
        - `ReportPage`
          - `IncidentForm`
        - `HistoryPage`
          - `AlertTimeline`

## Proposed Changes

### Frontend Project Setup
I will initialize a Vite React application in a new `C:/Users/User/OneDrive/Desktop/FRONTEND` directory (adjacent to your `BACKEND` folder).

#### [NEW] `frontend/src/App.jsx`
Main layout, AuthProvider wrapping, and React Router configuration.
#### [NEW] `frontend/src/api/client.js`
Pre-configured Axios/Fetch instance pointing to your Python Flask backend URL.
#### [NEW] `frontend/src/api/services.js`
Frontend service methods for all backend modules (e.g. `login()`, `triggerSOS()`, `getContacts()`, `addContact()`, `submitReport()`).
#### [NEW] `frontend/src/pages/*`
All React pages detailed in the Page Structure above.
#### [NEW] `frontend/src/components/*`
All reusable UI components (Buttons, Inputs, Modals, Navbar).
#### [NEW] `frontend/src/index.css`
Custom CSS styling using the Purple/White/Saffron aesthetic for extreme usability and highly visible SOS mechanisms.
#### [NEW] `frontend/README.md`
Instructions to configure and connect the React frontend with the Flask Python backend APIs.

## Verification Plan

### Manual Verification
1. **Local Dev Server Verification**: 
   - Start the Vite server locally using `npm run dev`.
   - The user can open the app in Chrome, toggle DevTools `Device Toolbar` (Mobile View, e.g., iPhone 14 Pro), and verify the "mobile-first responsive design".
2. **Component & Navigation**: 
   - Verify that clicking `[ S O S ]` triggers the confirmation screens.
   - Verify that adding a contact opens the modal, and the API service is correctly called.
3. **API Integration Readiness**: 
   - Provide explicit configuration details in the frontend console/documentation so when the backend is started natively via `flask run`, valid network requests successfully exchange data.
