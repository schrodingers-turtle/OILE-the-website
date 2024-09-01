import os
import google.generativeai as genai
import json

# Configure API
genai.configure(api_key=os.environ["API_KEY"])

# Create the model configuration
generation_config = genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro-exp-0827")


def edit_params(prompt, *simulation_parameters):# Construct the full prompt with system instructions and user input
    full_prompt = (
        "You are to come up with values to simulate a neutrino physics simulation based on what the user says they want the simulation to contain. "
        "The current values are:\n\n"
        f"Simulation time (1/μ): {simulation_parameters[0]}\n"
        f"Time step (1/μ): {simulation_parameters[1]}\n"
        f"Probability of interaction per neutrino per step: {simulation_parameters[2]}\n"
        f"Number of neutrinos Group 1: {simulation_parameters[3]}\n"
        f"Number of neutrinos Group 2: {simulation_parameters[4]}\n"
        f"Initial polarization components Group 1 X Vector: {simulation_parameters[5]}\n"
        f"Initial polarization components Group 1 Y Vector: {simulation_parameters[6]}\n"
        f"Initial polarization components Group 1 Z Vector: {simulation_parameters[7]}\n"
        f"Initial polarization components Group 2 X Vector: {simulation_parameters[8]}\n"
        f"Initial polarization components Group 2 Y Vector: {simulation_parameters[9]}\n"
        f"Initial polarization components Group 2 Z Vector: {simulation_parameters[10]}\n"
        f"Oscillation frequencies (μ) Group 1: {simulation_parameters[11]}\n"
        f"Oscillation frequencies (μ) Group 2: {simulation_parameters[12]}\n\n"
        "!OUTPUT YOUR ANSWER AS A JSON KEY WITH ALL OF THESE FIELDS AND YOUR CHOSEN NUMBER\n"
        "Your goal is to pick numbers that won't break the simulation but adhere to the user's request.\n\n"
        f"User input: {prompt}"
    )

    # Generate the model's response
    response = model.generate_content(
        full_prompt,
        generation_config=generation_config
    )

    # Extract the model's response text
    model_response = response.text

    # Remove code block markers if present
    json_str = model_response.replace("```json\n", "").replace("\n```", "")

    # Parse JSON
    simulation_data = json.loads(json_str)

    # Split JSON into different variables
    simulation_time = simulation_data.get("Simulation time (1/μ)")
    time_step = simulation_data.get("Time step (1/μ)")
    probability_of_interaction = simulation_data.get("Probability of interaction per neutrino per step")
    num_neutrinos_group1 = simulation_data.get("Number of neutrinos Group 1")
    num_neutrinos_group2 = simulation_data.get("Number of neutrinos Group 2")
    initial_polarization_group1_x = simulation_data.get("Initial polarization components Group 1 X Vector")
    initial_polarization_group1_y = simulation_data.get("Initial polarization components Group 1 Y Vector")
    initial_polarization_group1_z = simulation_data.get("Initial polarization components Group 1 Z Vector")
    initial_polarization_group2_x = simulation_data.get("Initial polarization components Group 2 X Vector")
    initial_polarization_group2_y = simulation_data.get("Initial polarization components Group 2 Y Vector")
    initial_polarization_group2_z = simulation_data.get("Initial polarization components Group 2 Z Vector")
    oscillation_frequencies_group1 = simulation_data.get("Oscillation frequencies (μ) Group 1")
    oscillation_frequencies_group2 = simulation_data.get("Oscillation frequencies (μ) Group 2")

    simulation_parameters = [
        simulation_time,
        time_step,
        probability_of_interaction,
        num_neutrinos_group1,
        num_neutrinos_group2,
        initial_polarization_group1_x,
        initial_polarization_group1_y,
        initial_polarization_group1_z,
        initial_polarization_group2_x,
        initial_polarization_group2_y,
        initial_polarization_group2_z,
        oscillation_frequencies_group1,
        oscillation_frequencies_group2
    ]

    simulation_parameters = [str(param) for param in simulation_parameters]

    return simulation_parameters
