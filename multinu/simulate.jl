using NuGasesQP
using Random
using PyPlot


"""Turn group quantities into quantities for individual neutrinos."""
function individual(Q)
    vcat((stack(repeat([Q], N), dims=1) for (Q, N) in zip(Q, N))...)
end


# Parse arguments.
tf, dt, prob, N_A, N_B, P_A01, P_A02, P_A03, P_B01, P_B02, P_B03, ωA, ωB = (
    parse(Float64, s) for s in ARGS
)
tf, N_A, N_B = (Int(f) for f in (tf, N_A, N_B))

# Neutrino setup

P0 = [
    [P_A01, P_A02, P_A03],
    [P_B01, P_B02, P_B03]
]

N = [N_A, N_B]
ω = [ωA, ωB]

N_total = sum(N)
N_groups = length(N)

v = randvec3(N_total, rng=Xoshiro(1000))

# Simulation setup
every = Int(1 / dt)

# Run the simulation.
gas = NuGasNQP(individual(P0), ωs=individual(ω), tf=tf, vs=v, Δt=dt, prob=prob, every=every, rng=Xoshiro(1234));

# Make the graph.

plt.style.use("dark_background")

fig, ax = plt.subplots(3, figsize=(4, 6), sharex=true)

for (P, ax) in zip(eachslice(gas.Ps, dims=2), ax)
    for P in eachslice(P, dims=1)
        ax.plot(gas.ts, P, lw=0.75, alpha=0.15)
    end
end

for ax in ax
    ax.grid(true, ls=":")
    ax.minorticks_on()
    ax.tick_params(which="both", direction="in", top=true, right=true)
end

ax[end].set_xlabel(L"time ($1/\mu$)")
for (ylabel, ax) in zip([L"$P_1$", L"$P_2$", L"$P_3$"], ax)
    ax.set_ylabel(ylabel)
end

fig.suptitle("Neutrino polarizations")

fig.tight_layout()

# Save the graph and return the filename.
path = "multinu/" * randstring(3) * ".png"
fig.savefig("static/" * path)
print(path)
