from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

# ---------------- LOGIN PAGE ----------------
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return "PAGE LOGIN"


# ---------------- LOGIN ACTION ----------------
@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if username == "admin" and password == "juris123":
        request.session["admin"] = True
        return RedirectResponse("/admin", status_code=303)

    return RedirectResponse("/login", status_code=303)


# ---------------- LOGOUT ----------------
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)