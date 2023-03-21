# Yumble - a dating app for foodies

## Capstone project #1

This is a dating app where users match each other based on their top 3 favorite foods.  

It is a project I designed for the purpose of learning web development. The back end is served with Flask, the database uses PostgreSQL, and the front end uses HTML5, CSS and Javascript. 
### Basic app functions
  1. user authentication. Passwords are encrypted and verified using the bcrypt hashing function.
      - Users are not able to access private information. A user, when logged in, can only see their own favorite foods, matches, and recipes. 
      - When a user evaluates potential matches, they can only see their top 3 favorite foods.  
  3. API integration. The app gathers data from TheMealDB.com which represents users' favorite foods. They can search for recipes by ingredient and save them to their favorites. Users select their top 3 favorite foods as the matching criteria for finding other users to match with and send messages to. Users are able to see their matches' profile pictures and bios only after mutually matching each other.
  4. Data persistence via database storage. All data relating to users, their matches/messages, and favorite foods are stored in a postgres database. Passwords are stored in their encrypted form.


