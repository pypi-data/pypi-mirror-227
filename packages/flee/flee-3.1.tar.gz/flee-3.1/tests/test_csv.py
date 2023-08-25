import os
import sys

import flee.postprocessing.analysis as a
import numpy as np
from flee import InputGeography, flee, spawning
from flee.datamanager import DataTable  # DataTable.subtract_dates()
from flee.datamanager import handle_refugee_data


def AddInitialRefugees(e, d, loc):
    """
    Add the initial refugees to a location, using the location name
    """
    num_refugees = int(d.get_field(name=loc.name, day=0, FullInterpolation=True))
    for _ in range(0, num_refugees):
        e.addAgent(location=loc, attributes={})


def date_to_sim_days(date):
    return DataTable.subtract_dates(date1=date, date2="2010-01-01")



def test_attribute_csv():

    flee.SimulationSettings.ReadFromYML("empty.yml")

    e = flee.Ecosystem()

    ig = InputGeography.InputGeography()

    ig.ReadAttributeInputCSV("flood_level","int",os.path.join("test_data", "test_input_csv", "flood_level.csv"))

    print(ig.attributes)

    assert ig.attributes["flood_level"]["B"][3] == 3
    assert ig.attributes["flood_level"]["B"][0] == 1
    assert ig.attributes["flood_level"]["A"][0] == 0



def test_csv(end_time=30, last_physical_day=30):

    flee.SimulationSettings.ReadFromYML("empty.yml")

    e = flee.Ecosystem()

    ig = InputGeography.InputGeography()

    flee.SimulationSettings.ConflictInputFile = os.path.join(
        "test_data", "test_input_csv", "flare-out.csv"
    )
    ig.ReadConflictInputCSV(csv_name=flee.SimulationSettings.ConflictInputFile)

    print(ig.conflicts)

    assert ig.conflicts["C"][49] == 0
    assert ig.conflicts["C"][50] == 1

    assert ig.conflicts["A"][0] == 1
    assert ig.conflicts["C2"][94] == 0

    ig.ReadLocationsFromCSV(csv_name=os.path.join("test_data", "test_input_csv/locations.csv"))

    ig.ReadLinksFromCSV(csv_name=os.path.join("test_data", "test_input_csv/routes.csv"))

    ig.ReadClosuresFromCSV(csv_name=os.path.join("test_data", "test_input_csv/closures.csv"))

    e, lm = ig.StoreInputGeographyInEcosystem(e=e)

    d = handle_refugee_data.RefugeeTable(
        csvformat="generic",
        data_directory=os.path.join("test_data", "test_input_csv", "refugee_data"),
        start_date="2010-01-01",
        data_layout="data_layout.csv",
    )

    output_header_string = "Day,"

    camp_locations = ["D", "E", "F"]
    # TODO: Add Camps from CSV based on their location type.

    for camp_name in camp_locations:
        AddInitialRefugees(e, d, lm[camp_name])
        output_header_string += "{} sim,{} data,{} error,".format(
            lm[camp_name].name, lm[camp_name].name, lm[camp_name].name
        )

    output_header_string += "Total error,refugees in camps (UNHCR),"
    "total refugees (simulation),raw UNHCR refugee count,"
    "refugees in camps (simulation),refugee_debt"

    print(output_header_string)

    # Set up a mechanism to incorporate temporary decreases in refugees
    refugee_debt = 0
    # raw (interpolated) data from TOTAL UNHCR refugee count only.
    refugees_raw = 0

    for t in range(0, end_time):

        # if t>0:
        ig.AddNewConflictZones(e=e, time=t)

        # Insert refugee agents
        spawning.spawn_daily_displaced(e, t, d, SumFromCamps=True)

        spawning.refresh_spawn_weights(e)
        # t_data = t

        e.enact_border_closures(time=t)
        e.evolve()

        # Calculation of error terms
        errors = []
        abs_errors = []
        loc_data = []

        camps = []
        for camp_name in camp_locations:
            camps += [lm[camp_name]]
            loc_data += [d.get_field(name=camp_name, day=t)]

        refugees_in_camps_sim = 0
        for c in camps:
            refugees_in_camps_sim += c.numAgents

        # calculate errors
        j = 0
        for i in camp_locations:
            errors += [a.rel_error(val=lm[i].numAgents, correct_val=loc_data[j])]
            abs_errors += [a.abs_error(val=lm[i].numAgents, correct_val=loc_data[j])]

            j += 1

        output = "%s" % t

        for i in range(0, len(errors)):
            output += ",%s,%s,%s" % (lm[camp_locations[i]].numAgents, loc_data[i], errors[i])

        if refugees_raw > 0:
            output += ",%s,%s,%s,%s,%s,%s" % (
                float(np.sum(abs_errors)) / float(refugees_raw),
                int(sum(loc_data)),
                e.numAgents(),
                refugees_raw,
                refugees_in_camps_sim,
                refugee_debt,
            )
        else:
            output += ",0,0,0,0,0,0,0"

        print(output)

    print("Test successfully completed.")


if __name__ == "__main__":
    end_time = 50
    last_physical_day = 50

    if len(sys.argv) > 1:
        if (sys.argv[1]).isnumeric():
            end_time = int(sys.argv[1])
            last_physical_day = int(sys.argv[1])
        else:
            end_time = 100
            last_physical_day = 100
            duration = flee.SimulationSettings.ReadFromCSV(sys.argv[1])
            if duration > 0:
                end_time = duration
                last_physical_day = end_time

    test_csv(end_time, last_physical_day)
