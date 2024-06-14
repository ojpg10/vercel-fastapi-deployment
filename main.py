    from time import time
    from fastapi import FastAPI, __version__
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import HTMLResponse
    from fastapi.requests import Request

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI on Vercel</title>
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
            <style>
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f0f0f0;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                button {{
                    padding: 10px 20px;
                    margin-right: 10px;
                    border: none;
                    cursor: pointer;
                    background-color: #007bff;
                    color: white;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hello from FastAPI@{__version__}</h1>
                <p>Current time: {time()}</p>
                <form action="/change_message" method="post">
                    <button type="submit" name="action" value="change">Change Message</button>
                </form>
                <form action="/change_message" method="post">
                    <button type="submit" name="action" value="reset">Reset Message</button>
                </form>
                <ul>
                    <li><a href="/docs">/docs</a></li>
                    <li><a href="/redoc">/redoc</a></li>
                </ul>
                <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
            </div>
        </body>
    </html>
    """

    @app.get("/")
    async def root():
        return HTMLResponse(html)

    @app.post("/change_message")
    async def change_message(request: Request):
        form = await request.form()
        action = form.get("action")

        if action == "change":
            global html
            html = html.replace("Hello from FastAPI", "Message Changed!")

        elif action == "reset":
            global html
            html = html.replace("Message Changed!", "Hello from FastAPI")

        return HTMLResponse(html)