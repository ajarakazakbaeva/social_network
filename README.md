# social_network
social network REST API service

The following URLs could be used for testing:

http://127.0.0.1:8000/api/register/ - for sign up

http://127.0.0.1:8000/api/token/ - for login

http://127.0.0.1:8000/api/token/refresh - for token refresh

http://127.0.0.1:8000/api/posts - for viewing the list of posts and creating a new post

http://127.0.0.1:8000/api/posts/1/vote - for voting and unvoting on post (in this example for post with id = 1)

http://127.0.0.1:8000/api/votes_analytics/?start=07-08-2022&end=01-09-2022 - for vote analytics between start and end date aggregated by day

http://127.0.0.1:8000/api/user_analytics/ - for viewing last login and last request time of a user


Postman collection is also provided in the repository
