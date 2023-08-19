# Database

## How to setup the database.

1. Install mongodb on the system. On Ubuntu 22.04 I used the [official install guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/).

2. Setup a admin user on the database (if one doesn't already exist).

```
$ mongosh

> use admin
> db.createUser(
    {
        user: "admin",
        pwd: "somepass",
        roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
    }
)
> quit
```

3. Setup a user for the DAT database.

```
$ mongosh

> use DAT
> db.createUser(
    {
        user: "DAT",
        pwd: "somepass",
        roles: [ { role: "readWrite", db: "DAT" }]
    }
)
> quit
```

4. Enable authentication on the Mongo database by editing /etc/mongodb.conf as root. Make sure the security section isn't commented out, and looks like.

```yaml
security
  authorization: "enabled"
```

5. Restart mongodb. On my Ubuntu 22.04 system, this was `sudo systemctl restart mongod`
