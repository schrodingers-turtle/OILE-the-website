from django.shortcuts import render

DEFAULT_FORM_VALUES = {
    'tf': 100,
    'dt': 0.01,
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


def index(request):
    return render(request, 'multinu/index.html', context={'form_values': DEFAULT_FORM_VALUES})


def simulate(request):
    context = {
        'form_values': request.POST
    }
    return render(request, 'multinu/index.html', context=context)
