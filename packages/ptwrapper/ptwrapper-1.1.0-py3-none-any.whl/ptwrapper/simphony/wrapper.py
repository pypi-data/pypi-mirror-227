import ctypes
import os

from .utils import (
    get_platform,
    load_c_lib,
    unload_c_lib,
)


class SimphonyWrapper:
    """Utility class exposing the access to the simphony library"""

    def __init__(self, library_root_path=None):
        if not library_root_path:
            self.library_root_path = os.path.join(
                os.path.dirname(__file__), "..", "c-lib"
            )
        else:
            self.library_root_path = library_root_path

    def load_library(self):
        """Loads the library appropriate for each platform and
        returns the handler reference

        Returns:
            any: handler of the simphony library
        """
        platform = get_platform()

        if platform == "mac_os_intel":
            mac_library = os.path.join(
                self.library_root_path, "mac/x86_64/libosve-sim-if-pt.dylib"
            )
            lib = load_c_lib(mac_library)
        elif platform == "mac_os_m1":
            mac_library = os.path.join(
                self.library_root_path, "mac/arm64/libosve-sim-if-pt.dylib"
            )
            lib = load_c_lib(mac_library)
        else:
            linux_library = os.path.join(self.library_root_path, "lin/libosve-sim-if-pt.so")
            cspice_library = os.path.join(
                self.library_root_path, "lin/cspice_n67_linux_64.so"
            )
            lib = load_c_lib(linux_library, cspice_library)
        return lib

    def get_attitude(self, root_scenario_path, session_file_path):
        """Process the session folder passed as input, parsing it, calculating the attitude represented
        (including the slew estimation, if required) and checking the violation of constraints.

        Args:
            root_scenario_path (str): Absolute path of the scenario folder
            session_file_path (str): Absolute path of the session file

        Returns:
            int: termination flag (0: success, -1: failure)
        """
        lib = self.load_library()
        root_scenario_path_bytes = root_scenario_path.encode()
        session_file_path_bytes = session_file_path.encode()
        get_attitude_func = lib.pti_getAttitude
        try:
            result = get_attitude_func(
                root_scenario_path_bytes, session_file_path_bytes
            )
        except Exception:
            return -1
        finally:
            unload_c_lib(lib)
        return result

    def get_app_version(self):
        """Returns the version of the simphony library

        Returns:
            str: version
        """
        lib = self.load_library()
        version_func = lib.pti_getAppVersion
        version_func.restype = ctypes.c_char_p
        version = version_func()
        unload_c_lib(lib)
        return version

    def get_interface_version(self):
        """Returns the version of the ICD used by
        Returns:
            str: version
        """
        lib = self.load_library()
        version_func = lib.pti_getInterfaceVersion
        version_func.restype = ctypes.c_char_p
        version = version_func()
        unload_c_lib(lib)
        return version

    def get_agm_version(self):
        """Returns the version of the underlying AGM module

        Returns:
            str: version
        """
        lib = self.load_library()
        version_func = lib.pti_getAgmVersion
        version_func.restype = ctypes.c_char_p
        version = version_func()
        unload_c_lib(lib)
        return version

    def get_eps_version(self):
        """Returns the version of the underlying EPS module

        Returns:
            str: version
        """
        lib = self.load_library()
        version_func = lib.pti_getEpsVersion
        version_func.restype = ctypes.c_char_p
        version = version_func()
        unload_c_lib(lib)
        return version
