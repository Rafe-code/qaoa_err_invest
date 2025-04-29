"""
script contains functions to fetch data from the IBM server so it can be processed
Can do this for batch and single runs due to both methods being used to run the circuits
"""

import numpy as np
import pandas as pd
from qiskit_ibm_runtime import QiskitRuntimeService
import TOKEN_DOC

# should move this to a constants file eventually
poss_outcomes = ["00", "01", "10", "11"]
single_job_ids_fname = "data/1_interim/rzz_job_ids_1.csv"
batch_ids_fname = "data/1_interim/rzz_batch_ids.csv"


#### Start with single batch #######
# have to use that this was the order the rotations were done in
# not great practice, future work has this embedded
gamma_values = np.pi * np.linspace(0, 1, 20)


def split_results_by_outcome(results, results_dict, gamma_val, repeats):
    """splits results by each possible outcome bitstring"""

    # all equally likely, so just divide shots by 4
    expected_num = results[0].data.meas.num_shots / 4

    # loop thru 00, 01, 10, 11
    for outcome in poss_outcomes:
        # get results for this outcome
        outcome_num = results[0].data.meas.get_counts().get(outcome, 0)
        # find change from expected
        outcome_diff = (outcome_num - expected_num) / expected_num
        # small conversions so things line up later
        gamma_rounded = float(gamma_val)
        # add to a dict containing info
        # this gets turned into a df later
        # dict is weird format - legacy of how earlier code was written
        results_dict[outcome]["gamma"].append(gamma_rounded)
        results_dict[outcome][f"rep{repeats}"].append(outcome_diff)

    return results_dict


# some strange formatting which gets undone later - legacy of path here
# details to allow it to run later
# replace token string with yours
service = QiskitRuntimeService(channel="ibm_quantum", token=TOKEN_DOC.TOKEN_STRING)
repeat_num = 1
name_per_outc = ["gamma"] + [f"rep{rep_num}" for rep_num in range(repeat_num)]


def process_batch_results(ids: list[str], repeat_num=1):
    """from list of job id strings get the results from ibm
    server and put them into a dict to be plotted
    has to load in each job single - very inefficient"""
    count = 0
    results_dict = {
        outcome: {name: [] for name in name_per_outc} for outcome in poss_outcomes
    }
    for repeats in range(repeat_num):
        for gamma_val in gamma_values:
            # expect them all with equal probability
            # produce error plots for each possibility
            results = service.job(job_id=ids[count]).result()
            count += 1
            results_dict = split_results_by_outcome(
                results, results_dict, gamma_val, repeats
            )

    return results_dict


# now we can actually turn it into dataframe
def single_runs_dict2df(results_dict):
    """dataframe more useful than dict, transform dict to df
    also does conversion of rotation angle = 2*gamma"""
    data = []
    for result_type, values in results_dict.items():
        for gamma, value in zip(values["gamma"], values["rep0"]):
            data.append(
                {
                    "result_type": result_type,
                    "rotation_angle": 2 * gamma,  # angle is 2*gamma
                    "error_rate": value,
                    "repeat": 0,
                }
            )

    # Create the dataframe
    df_0 = pd.DataFrame(data)
    return df_0


def load_single_jobs():
    # load in single job ids
    single_job_ids_df = pd.read_csv(single_job_ids_fname, header=None)
    single_job_ids = single_job_ids_df.iloc[:, 0].values
    # make a results dictionary based on this
    results_dict = process_batch_results(ids=single_job_ids, repeat_num=repeat_num)
    # turn this into a dataframe
    results_df = single_runs_dict2df(results_dict)
    return results_df


###### Now loading in batch ######
batch_job_ids_fname = "data/1_interim/rzz_batch_ids.csv"


def extract_dataframe_from_results(batch_id, repeat_num):
    """
    Extracts a DataFrame with columns: result_type, gamma, value
    from the fetched batch results object.
    """
    data = []
    # load in from ibm
    raw_results = service.job(job_id=batch_id).result()

    # Iterate through the results in raw_results
    for result in raw_results:
        gamma = result.metadata["circuit_metadata"]["gamma"]
        for result_type, value in result.data.meas.get_counts().items():
            expected_result = raw_results[0].data.meas.num_shots / 4
            frac_off = (value - expected_result) / expected_result
            data.append(
                {
                    "result_type": result_type,
                    "rotation_angle": 2 * gamma,  # angle is 2*gamma
                    "error_rate": frac_off,
                    "repeat": repeat_num,
                }
            )

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)
    return df


def load_batch_jobs():
    # load in batch job ids
    batch_job_ids_df = pd.read_csv(batch_job_ids_fname)
    # know this is the order
    repeat_nums = [1, 2, 2]
    # loop thru and get data in df format for all, then concat
    for i, id in enumerate(batch_job_ids_df["id"].values):
        results_df = extract_dataframe_from_results(
            batch_id=id, repeat_num=repeat_nums[i]
        )
        if i == 0:
            result_df_all = results_df.copy()
        else:
            result_df_all = pd.concat([result_df_all, results_df], axis=0)
    return result_df_all
