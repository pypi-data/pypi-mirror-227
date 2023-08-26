from pathlib import Path
import zipfile
from io import BytesIO
import numpy as np

def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()

def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)

class ResultsStore:
    # FIXME Ideally I'd like to use HDF5 but for some
    # reasons, its DLL conflicts with wolfhece's ones :-(

    def __init__(self, sim_path: Path, mode:str = "a"):
        """
        * `sim_path` must include the beacon file name like `d:\alpha\bravo\simul`
        * `mode` is `r` read, `w` (over)write or `a` append.
        """

        self._zip = None
        self._path = sim_path.with_suffix(".zip")
        self._mode = mode

        if mode in ('r','a'):
            assert self._path.exists() and self._path.is_file()
            self._zip = zipfile.ZipFile(self._path, mode=mode)
            self._result_number = int(self._zip.read(f"nb_results.txt"))
        elif mode == 'w':
            if self._path.exists():
                assert self._path.is_file()
                self._path.unlink()
            self._zip = zipfile.ZipFile(self._path, mode="x")
            self._result_number = 1
        else:
            raise Exception(f"Unrecognized mode : {mode}")

    @property
    def nb_results(self):
        return self._result_number

    @property
    def path(self) -> Path:
        return self._path

    def close(self):
        # Call this early if you need to read the zip while
        # some computations is still running.
        if self._zip is not None:
            if self._mode in ("w","a"):
                self._zip.writestr(f"nb_results.txt", str(self._result_number))
            self._zip.close()
            self._zip = None

    def __del__(self):
        # Important for write operations (see zipfile documentation)
        self.close()
        if self._zip is not None:
            self._zip.close()

    def append_result(self, h:np.ndarray, qx:np.ndarray, qy:np.ndarray):
        assert self._mode in ('w','a')

        n = f"{self._result_number:07}"
        self._zip.writestr(f"h_{n}", array_to_bytes(h))
        self._zip.writestr(f"qx_{n}", array_to_bytes(qx))
        self._zip.writestr(f"qy_{n}", array_to_bytes(qy))
        self._result_number += 1

    def get_last_result(self, ndx=0) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
        """ returns [h,qx,qy]
        """
        assert ndx <= 0, "-0 == last, -1=one before last, -2=..."
        assert self._mode == "r", "Only makes sens in read mode"
        return self.get_result(self._result_number-1+ndx)


    def get_result(self, ndx: int) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
        """ returns [h,qx,qy]
        """
        assert ndx >= 1, "We're one based"
        assert self._mode == "r", "Only makes sens in read mode"

        n = f"{ndx:07}"

        # Built this way so that one can look at results
        # without preventing write operations
        try:
            with zipfile.ZipFile(self._path, mode="r") as zip:
                arrays = []
                for name in ("h","qx","qy"):
                    with zip.open(f"{name}_{n}",mode="r") as fin:
                        arrays.append(bytes_to_array(fin.read()))
        except Exception as ex:
            raise Exception(f"Unable to load result '{n}' from {self._path}")

        return tuple(arrays)
