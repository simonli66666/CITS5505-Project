# Food Forum Web Application

## Description

### Purpose of the Application

Our group has developed a food forum web application where users can share and discover recipes. After registering and logging in, users can engage with the community by sharing their favorite recipes, liking posts, and leaving comments.

### Design and Use

#### User Registration and Login
- Users need to register and log in to access the full features of the forum.

#### Sharing Recipes
- On the homepage, users can share their recipes by clicking the "Share a Recipe" button.
- They can fill out a form with details such as ingredients, preparation time, calories, cooking process, and a URL for an image of the finished dish.
- This information is used to create a new post.

#### Viewing Recipes
- Users can view all posted recipes in the "Recipe" section on the left side of the homepage.

#### Liking and Commenting
- Users can like and comment on other users' posts.
- Recipes with high numbers of likes appear in the "Popular" section on the right side of the homepage.

#### Points System
- The forum features a points system where users can earn points by registering, posting recipes, and receiving likes on their posts.
- Users start with 20 points upon registration.
- Additional points can be earned by posting recipes and getting likes on their posts.
- As users accumulate points, they can achieve different ranks or titles.

#### User Profile
- Users can view their liked posts and comments in the "User Profile" section on the left side.
- Users can also edit their personal information in this section.

This food forum aims to create an engaging community where users can share their culinary creations, discover new recipes, and interact with fellow food enthusiasts.

## Group Members

| UWA ID     | Name               | GitHub Username  |
|------------|--------------------|------------------|
| 22853272   | Xiheng Li          | simonli66666     |
| 23892376   | Kexin Jiang        | kjiang001        |
| 23930318   | Wenxin Li.         | Chiaraliz.       |
| 23945949   | Yisong Zhang       | markzhhang.       |

## Instructions for Launching the Application

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/simonli66666/CITS5505-Project.git
    cd CITS5505-Project
    ```

2. **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Set the configuration file to initialize the Flask application with the following command:**
    ```bash
    export FLASK_APP=app
    ```
    ```bash
    set FLASK_APP=app (windows)
    ```
5. **Run the Application:**
    run run.py


