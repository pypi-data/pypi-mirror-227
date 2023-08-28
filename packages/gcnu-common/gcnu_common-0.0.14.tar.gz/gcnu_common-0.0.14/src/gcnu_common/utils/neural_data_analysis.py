import numpy as np


def checkAtLeastOneSpikePerNeuron(spikes_times):
    n_trials = len(spikes_times)
    n_neurons = len(spikes_times[0])
    for n in range(n_neurons):
        n_spikes = 0
        r = 0
        while n_spikes == 0 and r < n_trials:
            n_spikes = len(spikes_times[r][n])
            r += 1
        if n_spikes == 0:
            raise ValueError(f"neuron {n} has no spike across trials")


def checkSpikesTimesWithinBounds(spikes_times, trials_start_times,
                                 trials_end_times):
    n_trials = len(spikes_times)
    n_neurons = len(spikes_times[0])
    for r in range(n_trials):
        for n in range(n_neurons):
            if len(spikes_times[r][n]) > 0:
                min_spike_time_rn = min(spikes_times[r][n]) 
                if min_spike_time_rn < trials_start_times[r]:
                    raise ValueError(f"spike time at {min_spike_time_rn} found "
                                     f"before trial start time at "
                                     f"{trials_start_times[r]} for trials {r} "
                                     f"and neuron {n}")
                max_spike_time_rn = max(spikes_times[r][n]) 
                if max_spike_time_rn > trials_end_times[r]:
                    raise ValueError(f"spike time at {max_spike_time_rn} found "
                                     f"after trial start time at "
                                     f"{trials_start_times[r]} for trials {r} "
                                     f"and neuron {n}")


def checkEpochedSpikesTimes(spikes_times, trials_start_times, trials_end_times):
    checkAtLeastOneSpikePerNeuron(spikes_times=spikes_times)
    checkSpikesTimesWithinBounds(spikes_times=spikes_times,
                                 trials_start_times=trials_start_times,
                                 trials_end_times=trials_end_times)


def getSpikesRatesAllTrialsAllNeurons(spikes_times, trials_durations):
    n_trials = len(spikes_times)
    n_neurons = len(spikes_times[0])

    spikes_rates = np.empty((n_trials, n_neurons), dtype=np.double)
    for r in range(n_trials):
        for n in range(n_neurons):
            spikes_rates[r][n] = len(spikes_times[r][n])/trials_durations[r]
    return spikes_rates


# def binSpikes(spikes, bins_edges):
#     bin_counts, bins_edges_output = np.histogram(input=spikes, bins=bins_edges)
#     bin_centers = (bins_edges_output[:-1]+bins_edges_output[1:])/2.0
#     return bin_counts, bin_centers


def clipSpikesTimes(spikes_times, from_time, to_time):
    nTrials = len(spikes_times)
    clipped_spikes_times = [[]] * nTrials
    for r in range(nTrials):
        clipped_spikes_times[r] = clipTrialSpikesTimes(
            trial_spikes_times=spikes_times[r],
            from_time=from_time, to_time=to_time)
    return clipped_spikes_times


def clipTrialSpikesTimes(trial_spikes_times, from_time, to_time):
    nNeurons = len(trial_spikes_times)
    clipped_trial_spikes_times = [[]] * nNeurons
    for n in range(nNeurons):
        clipped_trial_spikes_times[n] = clipNeuronSpikesTimes(
            neuron_spikes_times=trial_spikes_times[n],
            from_time=from_time, to_time=to_time)
    return clipped_trial_spikes_times


def clipNeuronSpikesTimes(neuron_spikes_times, from_time, to_time):
    clipped_neuron_spikes_times = neuron_spikes_times[
        np.logical_and(from_time <= neuron_spikes_times,
                          neuron_spikes_times < to_time)]
    return clipped_neuron_spikes_times


def offsetSpikeTimes(spikes_times, offset):
    nTrials = len(spikes_times)
    offsetted_spikes_times = [[]] * nTrials
    for r in range(nTrials):
        offsetted_spikes_times[r] = offsetTrialSpikesTimes(
            trial_spikes_times=spikes_times[r], offset=offset)
    return offsetted_spikes_times


def offsetTrialSpikesTimes(trial_spikes_times, offset):
    nNeurons = len(trial_spikes_times)
    offsetted_trial_spikes_times = [[]] * nNeurons
    for n in range(nNeurons):
        offsetted_trial_spikes_times[n] = trial_spikes_times[n]+offset
    return offsetted_trial_spikes_times


def removeUnits(spikes_times, units_to_remove):
    nTrials = len(spikes_times)
    spikes_times_woUnits = [[]] * nTrials
    for r in range(nTrials):
        spikes_times_woUnits[r] = \
                removeUnitsFromTrial(trial_spikes_times=spikes_times[r],
                                     units_to_remove=units_to_remove)
    return spikes_times_woUnits


def removeUnitsFromTrial(trial_spikes_times, units_to_remove):
    nNeurons = len(trial_spikes_times)
    spikes_times_woUnits = []
    for n in range(nNeurons):
        if n not in units_to_remove:
            spikes_times_woUnits.append(trial_spikes_times[n])
    return spikes_times_woUnits


def selectUnitsWithLessSpikesThanThrInAllTrials(spikes_times, thr):
    nTrials = len(spikes_times)
    nNeurons = len(spikes_times[0])
    selected_units = set([i for i in range(nNeurons)])
    for r in range(nTrials):
        selected_trial_units = selectUnitsWithLessSpikesThanThrInTrial(
            spikes_times=spikes_times[r], thr=thr)
        selected_units = selected_units.intersection(selected_trial_units)
    answer = list(selected_units)
    return answer


def selectUnitsWithLessSpikesThanThrInAnyTrial(spikes_times, thr):
    nTrials = len(spikes_times)
    selected_units = set([])
    for r in range(nTrials):
        selected_trial_units = selectUnitsWithLessSpikesThanThrInTrial(
            spikes_times=spikes_times[r], thr=thr)
        selected_units = selected_units.union(selected_trial_units)
    answer = list(selected_units)
    return answer
    return selected_units


def selectUnitsWithLessSpikesThanThrInTrial(spikes_times, thr):
    nNeurons = len(spikes_times)
    selected_units = set([])
    for n in range(nNeurons):
        if len(spikes_times[n]) < thr:
            selected_units.add(n)
    return selected_units


def removeUnitsWithLessSpikesThanThrInAnyTrial(
        spikes_times, min_nSpikes_perNeuron_perTrial):
    nNeurons = len(spikes_times[0])
    neurons_indices = [n for n in range(nNeurons)]
    units_to_remove = \
        selectUnitsWithLessSpikesThanThrInAllTrials(
            spikes_times=spikes_times,
            thr=min_nSpikes_perNeuron_perTrial)
    spikes_times = removeUnits(spikes_times=spikes_times,
                               units_to_remove=units_to_remove)
    neurons_indices = [n for n in neurons_indices
                       if n not in units_to_remove]
    return spikes_times, neurons_indices


def removeTrialsLongerThanThr(spikes_times, trials_indices,
                              trials_durations, max_trial_duration):
    trials_to_keep = np.where(trials_durations<=max_trial_duration)[0]
    spikes_times = [spikes_times[trial_to_keep]
                    for trial_to_keep in trials_to_keep]
    trials_indices = trials_indices[trials_to_keep]
    return spikes_times, trials_indices

def removeUnitsWithLessTrialAveragedFiringRateThanThr(
        spikes_times, neurons_indices, trials_durations,
        min_neuron_trials_avg_firing_rate):
    n_neurons = len(spikes_times[0])
    n_trials = len(spikes_times)

    neurons_indices_to_keep = []
    for n in range(n_neurons):
        trials_firing_rates = np.array([np.nan for r in range(n_trials)])
        for r in range(n_trials):
            spikes_times_rn = spikes_times[r][n]
            trials_firing_rates[r] = len(spikes_times_rn)/trials_durations[r]
        trial_avg_firing_rate = trials_firing_rates.mean()
        if trial_avg_firing_rate > min_neuron_trials_avg_firing_rate:
            neurons_indices_to_keep.append(n)
    filtered_spikes_times = [[spikes_times[r][n]
                              for n in neurons_indices_to_keep]
                             for r in range(n_trials)]
    filtered_neurons_indices = [neurons_indices[n]
                                for n in neurons_indices_to_keep]
    return filtered_spikes_times, filtered_neurons_indices


def binNeuronsAndTrialsSpikesTimes(spikes_times, bins_edges, time_unit):
    n_trials = len(spikes_times)
    n_neurons = len(spikes_times[0])
    binned_spikes_times = [[[] for n in range(n_neurons)]
                           for r in range(n_trials)]
    for r in range(n_trials):
        for n in range(n_neurons):
            binned_spikes_times[r][n] = binSpikesTimes(
                spikes_times=spikes_times[r][n],
                bins_edges=bins_edges,
                time_unit=time_unit)
    return binned_spikes_times

def binSpikesTimes(spikes_times, bins_edges, time_unit):
    bin_width = bins_edges[1]-bins_edges[0]
    binned_spikes, _ = np.histogram(a=spikes_times, bins=bins_edges)
    binned_spikes = binned_spikes.astype(float)
    if time_unit == "sec":
        binned_spikes *= 1.0/bin_width
    elif time_unit == "msec":
        binned_spikes *= 1000.0/bin_width
    else:
        raise ValueError("time_unit should be sec or msec, but not {}".format(time_unit))
    return binned_spikes


def binMultiTrialSpikes(spikes_times, neuron_index, trials_indices,
                        bins_edges, time_unit):
    mt_binned_spikes = np.empty((len(trials_indices), len(bins_edges)-1),
                                dtype=np.double)
    for i, trial_index in enumerate(trials_indices):
        aligned_spikes_trial_neuron = spikes_times[trial_index][neuron_index]
        binned_spikes = binSpikesTimes(
            spikes=aligned_spikes_trial_neuron,
            bins_edges=bins_edges, time_unit=time_unit)
        mt_binned_spikes[i, :] = binned_spikes
    return mt_binned_spikes


def computeBinnedSpikesAndPSTH(spikes_times, neuron_index, trials_indices,
                               bins_edges, time_unit):
    binned_spikes = binMultiTrialSpikes(spikes_times=spikes_times,
                                        neuron_index=neuron_index,
                                        trials_indices=trials_indices,
                                        bins_edges=bins_edges,
                                        time_unit=time_unit)
    psth = np.empty(len(bins_edges)-1, dtype=np.double)
    for j in range(len(bins_edges)-1):
        psth[j] = binned_spikes[:, j].mean()
    return binned_spikes, psth


def computeBinnedSpikesAndPSTHwithCI(spikes_times, neuron_index,
                                     trials_indices, epoch_times,
                                     bins_edges, time_unit,
                                     nResamples, alpha):
    binned_spikes = binMultiTrialSpikes(spikes_times=spikes_times,
                                        neuron_index=neuron_index,
                                        trials_indices=trials_indices,
                                        epoch_times=epoch_times,
                                        bins_edges=bins_edges,
                                        time_unit=time_unit)
    psth = np.empty(len(bins_edges)-1, dtype=np.double)
    psth_ci = np.empty((len(bins_edges)-1, 2), dtype=np.double)
    for j in range(len(bins_edges)-1):
        psth[j] = binned_spikes[:, j].mean()
        bootstrapped_mean = stats.bootstrapTests.bootstrapMean(
            observations=binned_spikes[:, j], nResamples=nResamples)
        psth_ci[j, :] = stats.bootstrapTests.estimatePercentileCI(
            alpha=alpha, bootstrapped_stats=bootstrapped_mean
        )
    return binned_spikes, psth, psth_ci


def alignAndClipSpikeTimes(spike_times, align_times, clip_start_time,
                           clip_end_time):
    nTrials = len(spike_times)
    nNeurons = len(spike_times[0])
    aligned_clipped_spikes_times = []
    for r in range(nTrials):
        aligned_clipped_spikes_times_r = []
        for n in range(nNeurons):
            aligned_spikes_times_rn = spike_times[r][n]-align_times[r]
            aligned_clipped_spikes_times_rn = aligned_spikes_times_rn[
                np.logical_and(clip_start_time <= aligned_spikes_times_rn,
                               aligned_spikes_times_rn < clip_end_time)
            ].tolist()
            aligned_clipped_spikes_times_r.append(
                aligned_clipped_spikes_times_rn)
        aligned_clipped_spikes_times.append(
            aligned_clipped_spikes_times_r)
    return aligned_clipped_spikes_times
