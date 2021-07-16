import subprocess
import pytest

@pytest.mark.skip("This test will fail, and execute the command in terminal will not works too")
def test_main(datadir):

    process = subprocess.run(["MicroTokenizer", "train", "./model", "./data.txt"], cwd=datadir)
    assert process.returncode == 0
