# from .ai import edit_params

from django.shortcuts import render

import subprocess

DEFAULT_FORM_VALUES = {
    'tf': 500,
    'dt': 0.001,
    'prob': 0.1,
    'N_A': 60,
    'N_B': 40,
    'P_A01': 0.001,
    'P_A02': 0,
    'P_A03': 0.9999995,
    'P_B01': -0.001,
    'P_B02': 0,
    'P_B03': -0.9999995,
    'omega_A': 0.1,
    'omega_B': 0.2
}
DEFAULT_GRAPH_PATH = 'multinu/default_graph.png'

SIMULATION_PARAM_KEYS = (
    'tf',
    'dt',
    'prob',
    'N_A',
    'N_B',
    'P_A01',
    'P_A02',
    'P_A03',
    'P_B01',
    'P_B02',
    'P_B03',
    'omega_A',
    'omega_B'
)


def index(request):
    if request.method == 'GET':
        form_values = DEFAULT_FORM_VALUES
        graph_path = DEFAULT_GRAPH_PATH
    
    elif request.method == 'POST':
        form_values = request.POST.dict()

        # Separate simulation parameters from form data.
        simulation_parameters = [form_values.get(key) for key in SIMULATION_PARAM_KEYS]

        if form_values.get('prompt'):
            # AI logic here. E.g.:
            # simulation_parameters = edit_params(form_values.get('prompt'), *simulation_parameters)

            # Update form values to reflect new simulation parameters.
            for param, key in zip(simulation_parameters, SIMULATION_PARAM_KEYS):
                form_values[key] = param

        graph_path = _run_simulation(*simulation_parameters)

    context = {
        'form_values': form_values,
        'graph_path': graph_path
    }

    return render(request, 'multinu/index.html', context=context)


def _run_simulation(*args):
    call = subprocess.run(['julia', 'multinu/simulate.jl', *args], capture_output=True, text=True)

    if call.stderr:
        raise RuntimeError(call.stderr)

    graph_path = call.stdout

    return graph_path
