import pytest
import h5py as h5


def pytest_addoption(parser):
    parser.addoption(
        "--augfile", action="store", default="meraxes_augmented_stats.h5", help="the augemented stats file"
    )


@pytest.fixture(scope='session')
def augfile(request):
    fname = request.config.getoption("--augfile")
    with h5.File(fname, 'r') as fp:
        yield fp
