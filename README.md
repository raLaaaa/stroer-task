## Ströer SE & Co. KGaA - Job Coding Task

###  Task Description

Create a simple REST API to interact with the Fake API in JSONPlaceholder - Free Fake REST API
1. Create a Django command to import the data for the first time (posts and comments only) from JsonPlaceholder Free Fake Rest API to the local Postgres.
2. You cannot modify the external provider data structure
3. You can define whatever you want in your local database
4. Create a Rest API to manage that data in those models.
5. Implement all CRUD operations.
6. The user_id for the new posts created is always 99999942 since we don’t implement the user model.
7. Provide users authentication and request authorization through Bearer Token.
8. Synchronize both systems. The system you are implementing is the MASTER. You can decide how and when this synchronization will be done. Please write a README to specify how it can be 
9.	We prefer a tested and well documented task than a quick one.

**Technical Requirements**
- Use Python 3
- Use Django with Django REST framework
- Use PostgreSQL
- Deliver the task using Docker and docker-compose.

Notes You can resort to use any library that you need but specify the purpose of including it.

## Implementation & Documentation

###  Additional Libraries & Frameworks
- `psycopg2-binary ^2.9.3`

Used as PostgreSQL database adapter.
- `requests ^2.31.0`

Used as HTTP client to fetch / post to the fake rest API.
- `black ^23.3.0`

Used for formatting.

- `poetry`

Used as a dependency and package manager. A personal choice for me to boost productivity.


### Available Commands

- `python .\manage.py setup_testing_user`

This will create a base user and print out a basic token for authorization.
Alternatively, you can obtain this token by authenticating with a POST containing the credentials to `auth/`.
The credentials are `user` with password `1234`.

- `python .\manage.py import_data_from_api`

This will populate the database with the default data from the fake rest API (Posts and Comments only).
This solves task 1.

- `python .\manage.py sync_with_fake_system`

If you trigger this command both systems will synchronize. This means our local database state will be pushed towards the fake rest API with a single request.
You can navigate into the docker container and run this command at any time. This solves task 8.

### Usage

Simply run `docker-compose up` in the project root folder. This will run a PostgreSQL instance as well as the Django server. Before starting the web service it will perform automatic migrations, create a base user and print out the API token as well as populating the database with the `import_data_from_api` command. After that the server is available at `0.0.0.0:8000`. Please see the system logs for detailed information.

Note that restarting the container will delete all User, Post and Comment objects. How ever the general database state is persistent via a Docker volume.

### Structure & Thoughts

The API specified below is REST oriented and aims at providing a similiar interface the fake API does. When creating objects you do not have to provide any `ids` when posting since the server takes care of it. There are two serializers for each model. One of each takes care of our own API requests the others are responsible for serializing objects from the fake API. This is neccessary since the fake API specifies the id of the object and for instance a user id. In case of our API these details can be ignored and are taken care of by our system as mentioned above. That means we distinguish between input from our API by requests and imprting from the fake API.

It is important to note that the models contain two `id` fields. The basic Django `id` fields and `server_id`. We store both since we can not ensure that the fake rest API provides a consistent `id` schema even though thats probably the case. Towards our API we only use the `server_id` and basically the internal Django `id` and the `server_id` should always be equal.

We use DRFs generic views to provide the CRUD operations. Please note that there a limitations for the PUT requests for posts and comments. You can not change the id of an object or change the parent of an comment. For cases of deletion we are cascading the call. That means if you delete a `Post` all `Comments` will subsequently be deleted. 

### Routes

The application has the following routes:

```
    POST - auth/
    GET - fakeapi/v1/posts/
    POST - fakeapi/v1/posts/create/
    PUT - fakeapi/v1/posts/update/<int:server_id>/
    DELETE - fakeapi/v1/posts/delete/<int:server_id>/

    GET - fakeapi/v1/posts/<int:post_server_id>/comments/
    POST - fakeapi/v1/posts/<int:post_server_id>/comments/create/
    PUT - fakeapi/v1/posts/<int:post_server_id>/comments/update/<int:comment_server_id>/
    DELETE - fakeapi/v1/posts/<int:post_server_id>/comments/delete/<int:comment_server_id>/
```
