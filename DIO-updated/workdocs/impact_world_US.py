import lciafmt
from lciafmt.util import store_method, collapse_indicators

method = lciafmt.Method.ImpactWorld


def main():

    import lciafmt.iw as iw
    data = iw.get(region='USA')

    # map the flows to the Fed.LCA commons flows
    mapping = method.get_metadata()['mapping']
    mapped_data = lciafmt.map_flows(data, system=mapping)

    mapped_data = collapse_indicators(mapped_data)

    # write the result to parquet
    store_method(mapped_data, method, name='ImpactWorld+_US')

if __name__ == "__main__":
    main()
