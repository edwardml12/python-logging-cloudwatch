from fastapi import FastAPI, HTTPException
from services.item import Item
from services.logger import logger

app = FastAPI(title="FastAPI on Lambda")

@app.get("/health")
def health_check():
    logger.debug("Health check endpoint called.")
    return {"status": "ok"}

@app.get("/items")
def create_item():
    try:
        item = Item(name="Sample", description="This is a sample item")
        return item.get_item()
    except Exception as e:
        return {"error": str(e)}

@app.get("/function_with_raise")
def function_with_raise():
    try:
        raise ValueError("An intentional error occurred.")
    except Exception as e:
        logger.error(f"Error inaa all_items: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
@app.get("/function_with_error")
def function_with_error():
    try:
        call_function_not_implemented()
    except Exception as e:
        logger.error(f"Error inaa all_items: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )