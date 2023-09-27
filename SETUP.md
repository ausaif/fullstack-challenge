## Pre requisite ##
Python version: 3.10+
Node Version: v16.14.2+

## Backend ##

### Running the server ###

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Once the server is running API documentation can be viewed at
http://localhost:8000/docs

### Loading Data ###

```bash
cd script
pip install -r requirements.txt
python db_load.py
```

## Frontend ##

```bash
cd frontend/app
npm install
npm run build
npm run preview
```

## UI ##
Once all the above setups are completed and the backend and frontend servers are running, click [web app](http://localhost:4173/).

```
url: http://localhost:4173/
```

## Bonus ##
- **Optimization**: Propose at least one optimization that can help the application perform better under increased data loads.
  
    I have added pagination to enhance performance by reducing the payload size on every call. To improve performance we could use enterprise-grade DBMS that supports multiple replicas and run several instances of both backend and frontend servers behind load balancers.

- **Additional Feature**: Propose a feature you believe would enhance the user's experience while managing their property list.

    I would love to add features that can enhance user experience and one could be, instead of showing just a list of properties we can offer properties in a geographical map. This will allow users to visualize the clusters of properties and provide insights into the properties in the region.
