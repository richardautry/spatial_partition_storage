import uvicorn

import app.main

if __name__ == "__main__":
    uvicorn.main(app.main.app)
