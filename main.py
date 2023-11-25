from typing import Union, Annotated
from fastapi import FastAPI, Form, Request
from model import predict_legendaryStatus
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates
    
def generate_html_response(prediction):
    html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prediction</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    background: linear-gradient(to right, #3498db, #6C63FF); /* Updated gradient colors */
                }

                header {
                    text-align: center;
                    color: #fff; /* White text color */
                    font-family: 'Press Start 2P', cursive;
                    margin-bottom: 20px;
                    padding: 20px;
                    background: linear-gradient(to right, #e74c3c, #ff9c2b); /* Header gradient colors */
                }

                header a {
                    text-decoration: none;
                    color: #fff; /* White text color */
                }

                h1 {
                    text-align: center;
                    color: #e74c3c; /* Pokemon Red Color */
                    font-family: 'Press Start 2P', cursive;
                    margin: 0;
                }
            </style>
        </head>
        <body>
            <header>
                <a href="/">Pokemon Legendary Status Predictor</a>
            </header>
            <h1>{Prediction}</h1>
        </body>
        </html>

    """
    if(prediction == 0):
        prediction = "Not Legendary"
    else:
        prediction = "Legendary"
    html_content = html_content.replace("{Prediction}", str(prediction))
    return HTMLResponse(content=html_content, status_code=200)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("newPage.html", {"request": request})

@app.post("/predict/", response_class=HTMLResponse)
async def pokemon(Type_1: Annotated[str, Form()], Type_2: Annotated[str, Form()],
                    Total: Annotated[int, Form()], hp: Annotated[int, Form()], 
                    attack: Annotated[int, Form()], defense: Annotated[int, Form()],
                    Sp_Atk: Annotated[int, Form()], Sp_Def: Annotated[int, Form()],
                    Speed: Annotated[int, Form()], Generation: Annotated[int, Form()],
                    Color: Annotated[str, Form()], Pr_Male: Annotated[float, Form()],
                    Egg_Group_1: Annotated[str, Form()], 
                    # Egg_Group_2: Annotated[str, Form()],
                    hasMegaEvolution: Annotated[bool, Form()], Height_m: Annotated[float, Form()],
                    Weight_kg: Annotated[float, Form()], 
                    # Catch_Rate: Annotated[int, Form()],
                    Body_Style: Annotated[str, Form()]):
    
    pokemon_data = [[Type_1, Type_2, Total, hp, attack, defense, Sp_Atk, Sp_Def, Speed, 
    Generation, Color, Pr_Male, Egg_Group_1, hasMegaEvolution, Height_m, Weight_kg, Body_Style]]
    
    df = pd.DataFrame(pokemon_data, columns=['Type_1', 'Type_2', 'Total', 'HP', 'Attack', 'Defense', 'Sp_Atk',
     'Sp_Def', 'Speed', 'Generation', 'Color', 'Pr_Male', 'Egg_Group_1', 'hasMegaEvolution', 'Height_m', 'Weight_kg', 'Body_Style'])

    data_dict = {'Type_1': Type_1, 'Type_2': Type_2, 'Total': Total, 'HP': hp, 'Attack': attack, 'Defense': defense, 'Sp_Atk': Sp_Atk,
                    'Sp_Def': Sp_Def, 'Speed': Speed, 'Generation': Generation, 'Color': Color, 'Pr_Male': Pr_Male, 'Egg_Group_1': Egg_Group_1,
                    'hasMegaEvolution': hasMegaEvolution, 'Height_m': Height_m, 'Weight_kg': Weight_kg, 'Body_Style': Body_Style }

    input_df = pd.DataFrame(data_dict, index=[0])
    
    prediction = predict_legendaryStatus(input_df)
    
    htmlResponsePage = generate_html_response(prediction)
    return htmlResponsePage

@app.get("/preset")
def preset():
    input={
    'Type_1':'Grass',
    'Type_2':'Poison',
    'Total':318,
    'HP':45,
    'Attack':49,
    'Defense':49,
    'Sp_Atk':65,
    'Sp_Def':65,
    'Speed':45,
    'Generation':1,
    'Color':'Green',
    'Pr_Male':0.875,
    'Egg_Group_1':'Monster',
    'hasMegaEvolution':False,
    'Height_m':0.71,
    'Weight_kg':6.9,
    'Body_Style':'quadruped'}

    input = pd.DataFrame(input,index=[0])
    prediction = predict_legendaryStatus(input)
    return {"prediction": prediction}