from framework.reporting.metadata_builder import (
    MetadataBuilder,
)



def test_metadata_builder(tmp_path):

    path = MetadataBuilder().build(

        tmp_path,

        "long_call_butterfly",

        "Long Call Butterfly",

    )


    assert path.exists()

    assert path.name == "metadata.json"