from fastapi import FastAPI
from app.core.settings import get_settings

app = FastAPI()

@app.get('/info')
async def info():
    settings = get_settings()
    return {
        'app_name': settings.app_name
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)