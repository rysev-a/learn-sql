async def create_auth_tables(execute):
    await execute("""
        create table if not exists users (
            id uuid DEFAULT gen_random_uuid() primary key,
            email varchar(255) unique,
            password varchar(1024),
            first_name varchar(1024),
            last_name varchar(1024),
            birthdate date
        );
    """)

    await execute("""
        create table if not exists roles (
            id uuid DEFAULT gen_random_uuid() primary key,
            name varchar(255) unique
        );
    """)

    await execute("""
        create table if not exists users_roles (
            user_id uuid,
            role_id uuid,
            unique (role_id, user_id),
            foreign key(user_id) references users(id),
            foreign key(role_id) references roles(id)
        );
    """)


async def drop_auth_tables(execute):
    await execute("drop table users_roles cascade")
    await execute("drop table roles cascade")
    await execute("drop table users cascade")
