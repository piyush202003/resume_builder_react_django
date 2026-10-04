- temporary: 
    ```powershell 
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    ```

- to start venv
    ```powershell
        ..\.venv\Scripts\activate
    ```

- restart docker after making changes:
    ```powershell
    docker compose down
    ```
    ```powershell
    docker compose up --build
    ```

- to create superuse in docker container
    ```powershell
    docker compose exec backed python manage.py createsuperuser
    ```