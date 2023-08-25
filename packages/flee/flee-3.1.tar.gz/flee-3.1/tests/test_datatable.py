from flee.datamanager import handle_refugee_data

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""


def test_datatable():
    print("Testing basic data handling kernel.")

    d = handle_refugee_data.RefugeeTable(
        csvformat="generic",
        data_directory="test_data",
        start_date="2010-06-01",
        data_layout="data_layout.csv",
    )

    # print(d.header)
    # print(d.data_table)

    assert d.get_field(name="Total", day=0) == 2775
    assert d.get_field(name="Total", day=300) == 21079
    assert d.get_field(name="Total", day=700) == 311338

    print("Testing getMaxFromData.")
    assert d.getMaxFromData(name="camp1", days=1200) == 800000

    print("Testing correction for level 1 registrations.")
    d.correctLevel1Registrations(name="Total", date="2014-01-01")

    # print(d.header)
    # print(d.data_table)

    print(d.get_field(name="Total", day=0))
    print(d.get_field(name="Total", day=10))
    print(d.get_field(name="Total", day=100))
    print(d.get_field(name="Total", day=300))
    print(d.get_field(name="Total", day=500))
    print(d.get_field(name="Total", day=700))
    print(d.get_field(name="Total", day=1000000))

    assert d.get_field(name="Total", day=0) == int(2775 / 2)
    assert d.get_field(name="Total", day=300) == int(21079 / 2)
    assert d.get_field(name="Total", day=700) == int(311338 / 2)

    print("SUCCESS")


if __name__ == "__main__":
    test_datatable()
