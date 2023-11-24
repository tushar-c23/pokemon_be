from typing import Union, Annotated
from fastapi import FastAPI, Form
from model import predict_legendaryStatus
from fastapi.responses import HTMLResponse
import pandas as pd
    
def generate_html_response():
    html_content = """
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pokemon Legendary or not</title>
    </head>
    <body>
        <h1>Pokemon Legendary Status Predictor</h1>
        <form action="/predict" method="post">
            <label for="Type_1">Pokemon Type 1</label>
            <input type="text" name="Type_1" placeholder="Pokemon Type 1">
            <label for="Type_2">Pokemon Type 2</label>
            <input type="text" name="Type_2" placeholder="Pokemon Type 2">
            <label for="Total">Total</label>
            <input type="number" name="Total" placeholder="Total">
            <label for="hp">HP</label>
            <input type="number" name="hp" placeholder="HP">
            <label for="attack">Attack</label>
            <input type="number" name="attack" placeholder="Attack">
            <label for="defense">Defense</label>
            <input type="number" name="defense" placeholder="Defense">
            <label for="Sp_Atk">Sp. Attack</label>
            <input type="number" name="Sp_Atk" placeholder="Sp. Attack">
            <label for="Sp_Def">Sp. Defense</label>
            <input type="number" name="Sp_Def" placeholder="Sp. Defense">
            <label for="Speed">Speed</label>
            <input type="number" name="Speed" placeholder="Speed">
            <label for="Generation">Generation</label>
            <input type="number" name="Generation" placeholder="Generation">
            <label for="Color">Color</label>
            <input type="text" name="Color" placeholder="Color">
            <label for="Pr_Male">Pr_Male</label>
            <input type="text" name="Pr_Male" placeholder="Pr_Male">
            <label for="Egg_Group_1">Egg Group 1</label>
            <input type="text" name="Egg_Group_1" placeholder="Egg Group 1">
            <label for="hasMegaEvolution">hasMegaEvolution</label>
            <input type="boolean" name="hasMegaEvolution" placeholder="hasMegaEvolution">
            <label for="Height_m">Height_m</label>
            <input type="text" name="Height_m" placeholder="Height_m">
            <label for="Weight_kg">Weight_kg</label>
            <input type="text" name="Weight_kg" placeholder="Weight_kg">
            <label for="Body_Style">Body Style</label>
            <input type="text" name="Body_Style" placeholder="Body Style">
            <button>Submit</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

app = FastAPI()

@app.get("/")
def read_root():
    return generate_html_response()

@app.post("/predict/")
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
    
    return {"prediction": prediction}

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