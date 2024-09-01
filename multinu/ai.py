import os
import google.generativeai as genai
import json

# Configure API
genai.configure(api_key='AIzaSyAOZYO8FSVr95OnPEMynxjbMEOiTAxRnQc')

# Create the model configuration
generation_config = genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro-exp-0827")


def edit_params(prompt, *simulation_parameters):
    # User input
    user_input = prompt

    # Construct the full prompt with system instructions and user input
    full_prompt = (
        "You are to come up with values to simulate a neutrino physics simulation based on what the user says they want the simulation to contain. "
        "The default values are:\n\n"
        "Simulation time (1/μ): 500\n"
        "Time step (1/μ): 0.001\n"
        "Probability of interaction per neutrino per step: 0.1\n"
        "Number of neutrinos Group 1: 60\n"
        "Number of neutrinos Group 2: 40\n"
        "Initial polarization components Group 1 X Vector: 0.001\n"
        "Initial polarization components Group 1 Y Vector: 0\n"
        "Initial polarization components Group 1 Z Vector: 0.9999995\n"
        "Initial polarization components Group 2 X Vector: -0.001\n"
        "Initial polarization components Group 2 Y Vector: 0\n"
        "Initial polarization components Group 2 Z Vector: -0.9999995\n"
        "Oscillation frequencies (μ) Group 1: 0.1\n"
        "Oscillation frequencies (μ) Group 2: 0.2\n\n"
        "!OUTPUT YOUR ANSWER AS A JSON KEY WITH ALL OF THESE FIELDS AND YOUR CHOSEN NUMBER\n"
        "Your goal is to pick numbers that won't break the simulation but adhere to the user's request.\n\n"
        f"User input: {user_input}"
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
