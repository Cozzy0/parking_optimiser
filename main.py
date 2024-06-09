import tkinter
import customtkinter
import numpy as np
import matplotlib.pyplot as plt


# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

############# UI ################

# App frame
app = customtkinter.CTk()
app.geometry("730x330")
app.title("Parking Optimiser")

# AreaParking UI elements
areaParkingLabel = customtkinter.CTkLabel(app, text="Parking Area in use (SqM)")
areaParkingLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
areaParkingField = customtkinter.CTkEntry(app, width=300, height=40)
areaParkingField.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Aisle width
widthLabel = customtkinter.CTkLabel(app, text="Width of each parking aisle (M)")
widthLabel.grid(row=0, column=2, padx=10, pady=10)
widthField = customtkinter.CTkEntry(app, width=150, height=40)
widthField.grid(row=1, column=2, padx=10, pady=10)

# Aisle length
lengthLabel = customtkinter.CTkLabel(app, text="Length of each parking aisle (M)")
lengthLabel.grid(row=0, column=3, padx=10, pady=10)
lengthField = customtkinter.CTkEntry(app, width=150, height=40)
lengthField.grid(row=1, column=3, padx=10, pady=10)

# Objective Combo Field
objectiveLabel = customtkinter.CTkLabel(app, text="Objective of Algorithm")
objectiveLabel.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
objectiveCombo = customtkinter.CTkComboBox(master=app, values=["Increase Parking Spaces", "Improve Traffic Flow"], width=250, state="readonly")
objectiveCombo.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Error Label
errorLabel = customtkinter.CTkLabel(app, text="", text_color="red")
errorLabel.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Result Label
resultLabel = None

############### Optimisation functions ##################

#Get Inputs of Fields
def get_inputs():
    try:
        area_parking = float(areaParkingField.get())
        aisle_width = float(widthField.get())
        aisle_length = float(lengthField.get())
        objective = objectiveCombo.get()

        if area_parking <= 0 or aisle_width <= 0 or aisle_length <= 0:
            raise ValueError("All input values must be positive.")
        
        return area_parking, aisle_width, aisle_length, objective
    except ValueError as e:
        errorLabel.configure(text=f"Invalid input: {e}") #Display error so user can debug
        return None

# Objective selection
def optimise_parking(area_parking, aisle_width, aisle_length, objective):
    if objective == "Increase Parking Spaces":
        return increase_parking_spaces(area_parking, aisle_width, aisle_length)
    elif objective == "Improve Traffic Flow":
        return improve_traffic_flow(area_parking, aisle_width, aisle_length)
    else:
        raise ValueError("Invalid optimization objective.")

#Algorithm 1
def logistic_growth(x, L, k, x0):
    return (L*0.7) / (1 + np.exp(-k * (x - x0)))

# Objective 1
def increase_parking_spaces(area_parking, aisle_width, aisle_length): 
    # Logistic growth curve parameters
    L = area_parking
    k = 0.0025  # Growth rate
    x0 = 200  # Midpoint

    #How many possible parking spaces can fit
    total_possible_spaces = area_parking // (aisle_width * aisle_length)
    
    # The parking ratio
    parking_ratio = logistic_growth(L, 1, k, x0)
    
    # Return integer of car spaces
    actual_spaces = int(total_possible_spaces * parking_ratio)

    return actual_spaces, parking_ratio

#Algorithm 2
def logistic_growth2(x, L, k, x0):
    return (L*0.7) / (1 + np.exp(-k * (x - x0)))


# Objective 2
def improve_traffic_flow(area_parking, aisle_width, aisle_length):
    # Logistic growth parameters
    L = area_parking
    k = 0.0010  # Growth rate adjusted
    x0 = 200 # Midpoint adjusted

    #How many possible parking spaces can fit
    total_possible_spaces = area_parking // (aisle_width * aisle_length)
    
    # The parking ratio from logistic growth curve
    parking_ratio = logistic_growth2(L, 1, k, x0)
    
    # Return whole number of car spaces
    actual_spaces = int(total_possible_spaces * parking_ratio)
    
    return actual_spaces, parking_ratio

#Display result
def show_result(result, ratio):
    global resultLabel
    if resultLabel:
            resultLabel.destroy() # Need to destroy label or text overlaps
    resultLabel = customtkinter.CTkLabel(app, text=f"Optimised result: At a Parking Ratio of {round(ratio, 2)}, {result} parking space(s) can efficiently fit\nThis result should only be used as assistance in assessing and restructuring parking areas.")
    resultLabel.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

def on_optimise_button_click():
    inputs = get_inputs()
    if inputs:
        area_parking, aisle_width, aisle_length, objective = inputs
        try:
            result, ratio = optimise_parking(area_parking, aisle_width, aisle_length, objective)
            show_result(result, ratio)
            errorLabel.configure(text="")  # Clear error message on successful optimization
        except ValueError as e:
            errorLabel.configure(text=f"Error: {e}") #Display error so user can debug

# Optimise Button
optimise_button = customtkinter.CTkButton(app, text="Optimise", command=on_optimise_button_click)
optimise_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Run app
app.mainloop()
