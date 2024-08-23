# Philosophy



# Application Structure

1. Externally developed resources
 
    - Distribution Services
        IPFS
    - Local Database
        SQLite/aiosql 
    - HTTP Host
        uvicorn
    - GUI framework
        FastAPI

2. Locally developed components

    - GUI
        Console Interface
        Browser Interface

    - Daemon
        Periodically examine Distribution Services for new network peers and reflect additions in DB
        Periodically examine Distribution Services and reflect changes in DB
        Periodically examine the DB and reflect changes in Distribution Services

    - One time
         DB build and initialization
         Application configuration
