# 🎬 Movie Rating System 

## 📌 Overview

The Movie Rating System is a backend service for managing movies and user ratings.

This phase focuses on:
- REST API implementation for movies and ratings
- Adding structured logging using Python logging module
- Dockerizing the application
- Basic observability (logs for debugging and monitoring)

---

## 🚀 Features

### 🎥 Movies
- Get all movies
- Get movie details

### ⭐ Ratings
- Submit rating for a movie
- Validate rating (1 to 10)
- Handle invalid inputs and errors

---

## 📊 Logging

This project uses Python’s built-in `logging` module instead of `print`.

### Why logging?
- Structured and searchable logs
- Different severity levels
- Better debugging in production
- Standard practice in real systems

---

## 🧠 Log Levels

- DEBUG → Development details
- INFO → Normal application events
- WARNING → Unexpected but handled cases
- ERROR → Failures in operations
- CRITICAL → System-level failures

---

## 📦 Example Logs

### Success
INFO - movie_rating - Rating saved (movie_id=42, rating=8)

### Invalid rating
WARNING - movie_rating - Invalid rating (movie_id=42, rating=12)

### Database error
ERROR - movie_rating - Failed to save rating (movie_id=42)

---

## 🐳 Docker

The project is fully containerized using Docker.

### Build image
```bash
docker build -t movie-rating-system .
