# QR Code Generator App

A full-stack web application that allows users to generate, view, and manage QR codes. The app also includes an admin panel to monitor system activity and manage users. Built with Python, Streamlit, and MongoDB.

## Features

### User Features
- Login / Signup
  - Secure registration and login
  - Passwords hashed for security
- QR Code Generation
  - Generate QR codes from text, URLs, or custom data
  - Preview QR codes before downloading
  - Download QR codes in PNG or SVG format
- QR Code History
  - View a list of previously generated QR codes
  - Reuse or download old QR codes
- Dashboard
  - Overview of recent QR codes
  - Quick access to generate new QR codes
  - Profile management (update info, password)

### Admin Features
- Admin Dashboard
  - View all registered users
  - Monitor system activity (logins, QR generation)
- User Management
  - CRUD operations for user accounts
  - Activate/deactivate user accounts
- Activity Logging
  - Tracks user activity for auditing and security

### Backend Features
- Authentication Service for login/signup
- QR Code Processor for dynamic QR code generation
- User Management Service for handling user operations
- Activity Logging Service for monitoring actions
- MongoDB integration for storing users, QR codes, and logs
- Utility functions for handling repetitive tasks

## Technology Stack

| Layer        | Technology                   |
|-------------|------------------------------|
| Frontend    | Streamlit                    |
| Backend     | Python                       |
| Database    | MongoDB                      |
| QR Code     | `qrcode` Python library      |
| Authentication | bcrypt, session management |


