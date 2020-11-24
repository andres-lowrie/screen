# Docker_Project
Get gihub datasets and store in docker image




cd Desktop\DockerFiles


1.Run docker 

    docker build -t interview .

2.Enter Image

    docker run -it interview /bin/bash

3. Some prerequest need to run in docker image
    
    Install Libmariadb

        apt-get install libmariadb-dev

	    press Y and enter

    Install mysqlclient python packages

       pip3 install mysqlclient

4. Update mysql's root password

        service mysql start
        mysql

        use mysql;

        update user set password=PASSWORD("1234") where User='root';
        update user set plugin='mysql_native_password' where User='root';

        flush privileges;

        CREATE DATABASE TEST;

        exit;

	(mysql -u root -p1234)

5. Run the python file to load

        python3 Load_CSV_to_DB.py

6. Run the python file to get the answer

       python3 exercise_answer.py
