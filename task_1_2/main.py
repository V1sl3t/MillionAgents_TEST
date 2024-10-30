import sys
from pathlib import Path
import base64


sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, responses

from task_1_2.db import get_db, ShortLink


app = FastAPI()


@app.post("/create")
async def create_short_link(request: Request, url: str, db=Depends(get_db)):

    short_code = base64.urlsafe_b64encode(url.encode()).decode()[:10] # Генерация короткого кода

    # Проверяем, существует ли уже такой короткий код
    existing_link = db.query(ShortLink).filter_by(short_code=short_code).first()
    if existing_link:
        return {
            "message": f"Short link already exists: {request.url_for('redirect_to_original', short_code=existing_link.short_code)}"
        }

    # Сохраненяем новую ссылку
    new_link = ShortLink(original_url=url, short_code=short_code)
    db.add(new_link)
    db.commit()

    return {
        "original_url": url,
        "short_link": request.url_for('redirect_to_original', short_code=short_code),
    }


@app.get("/{short_code}")
async def redirect_to_original(request: Request, short_code: str, db=Depends(get_db)):
    # Поиск оригинальной ссылки по короткому коду
    link = db.query(ShortLink).filter_by(short_code=short_code).first()

    if link is None:
        raise HTTPException(status_code=404, detail="Short link not found")

    return responses.RedirectResponse(url=link.original_url)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)