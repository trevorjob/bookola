# BOOKOLA

Welcome to Bookola, your go-to destination for discovering and exploring a world of literature. This README provides an overview of the features, setup instructions, and guidelines for contributing to the Book Haven website.

## Table of Contents
- [BOOKOLA](#bookola)
  - [Table of Contents](#table-of-contents)
  - [Introduction {introduction}](#introduction-introduction)
  - [Features {#features}](#features-features)
  - [Getting Started {#getting-started}](#getting-started-getting-started)
    - [Prerequisites {#prerequisites}](#prerequisites-prerequisites)
    - [Installation {#installation}](#installation-installation)

## Introduction {introduction}
Bookola is a web platform dedicated to connecting readers with their next favorite books. It aims to create a space where users can explore, review, and discuss a wide range of literary works. Whether you're a bibliophile searching for your next read or an author looking to share your work, Bookola has something for everyone.

## Features {#features}
- **Book Discovery:** Browse through an extensive collection of books, filter by genres, authors, and more.
- **User Reviews:** Read and write reviews to share your thoughts on books, helping others make informed decisions.
- **Author Profiles:** Explore profiles of your favorite authors, discover their works, and connect with the literary community.
- **Personal Library:** Create and manage your virtual bookshelf, keeping track of books you've read, want to read, or are currently reading.
- **Chat-Room Discussions:** Engage in discussions with fellow readers through forums and comment sections.
- **Book Recommendations:** Receive personalized book recommendations based on your reading history and preferences.

## Getting Started {#getting-started}
### Prerequisites {#prerequisites}
Before you begin, ensure you have the following:
- **Node.js installed**
- **Flask_SQLAchemyDB installed and running**

### Installation {#installation}
1. Clone the repository
git clone https://github.com/redeks12/bookola.git
2. cd bookola
3. npm install
4. set up environment variables:
   Create a .env file in the root directory and configure the following variables:
   PORT=3000
   MONGODB_URI=mongodb://localhost:27017/bookhaven
   SECRET_KEY=your_secret_key
5. Start the application:
   npm start
6. Open your browser and visit http://localhost:3000 to view Bookola.

