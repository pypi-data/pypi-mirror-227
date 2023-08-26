from typing import TypeAlias, Literal, Set

class MauiOscilloscope:
    """
    Class used for communicating with and controlling a Teledyne-Lecroy oscilloscope
    using the MAUI interface.
    """


    class SetupSubsystem:
        """
        Class used to control panel setups for the oscilloscope.
        """

        def save_panel_setup(self, filepath: str):
            """
            Save the panel setup to the specified filepath on the controller.

            :param filepath: path to save the setup file to
            :return: returns nothing
            """

        def load_panel_setup(self, filepath: str):
            """
            Load a panel setup to the device from a specified filepath on the controller.

            :param filepath: path of the setup file
            :return: returns nothing
            """

    class AcquisitionSubsystem:
        """
        Class used to control the acquisition system for the oscilloscope.
        """

        def arm_acquisition(self):
            """
            Arms the scope and forces a single acquisition if it is already armed.
            """

        def force_trigger(self):
            """
            Causes the device to make one acquisition if it is in an active trigger mode.

            If the intrument is in STOP trigger mode, there is no action.
            """

        def stop(self):
            """
            Immediatly stops the acquisition of a signal. If the trigger mode is AUTO or NORMAL,
            this command places the oscilloscope in STOP trigger mode to prevent further acquisitions.
            """

        def wait(self, duration_milliseconds: int|None):
            """
            Prevents the device from analyzing new commands until the current acquisition has beem completed.
            The optional `timeout_duration` argument specifies the timeout after which the scope stops
            waiting for new acquisitions. If the timeout duration is not given or zero, the scope waits
            indefinitely.

            :param duration_milliseconds: optional time to wait in milliseconds
            """

        def get_sample_clock_state(self) -> Literal["INTERNAL", "EXTERNAL"]:
            """
            Get the state of the sample clock, either INTERNAL of EXTERNAL.

            :return: returns a string for INTERNAL or EXTERNAL
            """

        def get_reference_clock_state(self) -> Literal["INTERNAL", "EXTERNAL"]:
            """
            Get the state of the reference clock, either INTERNAL of EXTERNAL.

            :return: returns a string for INTERNAL or EXTERNAL
            """

        def set_internal_sample_clock(self):
            """
            Sets the sample clock to be INTERNAL.
            """
        
        def set_external_sample_clock(self):
            """
            Sets the sample clock to be EXTERNAL.
            """

        def set_internal_reference_clock(self):
            """
            Sets the reference clock to be INTERNAL.
            """

        def set_external_reference_clock(self):
            """
            Sets the reference clock to be EXTERNAL.
            """

        def auto_setup(self, channel: int, find: bool):
            """
            The AUTO_SETUP command attempts to display the input signal(s) by adjusting the vertical, timebase
            and trigger parameters. AUTO_SETUP operates only on the channels whose traces are currently turned
            on. If no traces are turned on, AUTO_SETUP operates on all channels.

            If signals are detected on several channels, the lowest numbered channel with a signal determines the
            selection of the timebase and trigger source.

            If only one input channel is turned on, the timebase will be adjusted for that channel.
            The AUTO_SETUP FIND command adjusts gain and offset only for the specified channel.

            If the FIND keyword is present, gain and offset adjustments are performed only on the specified channel.

            If no <channel> prefix is added, an auto-setup is performed on the channel used on the last ASET FIND
            remote command.

            In the absence of the FIND keyword, the normal auto-setup is performed, regardless of the <channel>
            prefix.

            :param channel: the channel to auto setup on
            :param find: adjust gain and offset only for the specified channel
            """

        def set_attenuation(self, channel: int, attenuation: int):
            """
            The ATTENUATION command selects the vertical attenuation factor of the probe. Values up to 10000 can
            be specified.

            :param channel: the channel to set attenuation on
            :param attenuation: value between 
            """

        def get_attenuation(self, channel: int) -> int:
            """
            Get the attenuation factor of the specified channel.

            :param channel: the channel to get attenuation from
            """

        def set_bandwidth_limit(self, channel: int, bandwidth_limit: int|None):
            """
            The BANDWIDTH_LIMIT command enables or disables the bandwidth-limiting low-pass filter on a per-
            channel basis. When the <channel> argument is omitted, the BWL command applies to all channels.

            :param channel: the channel to set bandwidth limit on
            :param bandwidth_limit: value of the limit to set
            """

        def get_bandwidth_limit(self, channel: int) -> int:
            """
            The response to the BANDWIDTH_LIMIT? query shows the bandwidth filter setting for each channel.

            :param channel: the channel to get the bandwidth limit from
            :return: returns the bandwidth limit value
            """

        def get_vertical_offset(self, channel: int) -> float:
            """
            The OFFSET? query returns the DC offset value of the specified channel at the probe tip.

            :param channel: the channel to get the vertical offset from
            """

        def set_vertical_offset(self, channel: int, offset: float):
            """
            The OFFSET command allows adjustment of the vertical offset of the specified input channel at the probe
            tip.

            The maximum ranges depend on the fixed sensitivity setting. Refer to the product datasheet at
            teledynelecroy.com for maximum offset specifications.

            If an out-of-range value is entered, the oscilloscope is set to the closest possible value and the VAB bit (bit
            2) in the STB register is set.

            :param channel: the channel to set the vertical offset for
            :param offset: the vertical offset value in volts
            """

        def set_time_div(self, time_div: float):
            """
            Set the timebase value per division. Values will be adjusted
            to the nearest value possible on the device.
            """

        def get_time_div(self) -> float:
            """
            Get the timebase value per division
            """

        def set_volt_div(self, channel: int, volt_div: float):
            """
            Set the volt value per division for the selected channel. 
            Values will be adjusted to the nearest value possible 
            on the device.

            :param channel: the channel on which the volt div is set
            :param volt_div: the volt div value
            """

        def get_volt_div(self, channel: int) -> float:
            """
            Get the volt value per division.
            """

        def set_trigger_mode_auto(self):
            """
            Set the trigger mode to AUTO.
            """

        def set_trigger_mode_normal(self):
            """
            Set the trigger mode to NORM.
            """

        def set_trigger_mode_single(self):
            """
            Set the trigger mode to SINGLE.
            """

        def set_trigger_mode_stop(self):
            """
            Set the trigger mode to STOP.
            """

    class CommunicationSubsystem:
        """
        Class used to control the communication parameters and log for the oscilloscope.
        """

        def read_remote_log(self, clear_log: bool) -> str:
            """
            
            Returns the remote log as a string. if `clear_log` is set to `True`,
            the remote log is cleared after being sent.

            :param clear_log: clear the log after reading it
            :return: a string with the contents of the log
            """

        def get_log_level(self) -> str:
            """
            Get the log level currently in use.

            :return: a string identifying the log level
            """

        def set_log_level_off(self):
            """
            Set the log level to OFF. Nothing is logged.

            :return: returns nothing
            """

        def set_log_level_errors_only(self):
            """
            Set the log level to EO. Only errors are logged.

            :return: returns nothing
            """

        def set_log_level_full_dialog(self):
            """
            Set the log level to FD. All remote interactions are logged.

            :return: returns nothing
            """

    class StorageSubsystem:
        """
        Class used to control the filesystem on the oscilloscope.
        """

        def delete_file_on_device(self, filepath: str):
            """
            Delete a specified file on the device.

            :param filepath: path to the file on the device
            :return: returns nothing
            """

        # def transfer_file_to_device(self, device_filepath: str, controller_filepath: str):
        #     """
        #     Transfer a file from the controller to the device.

        #     :param device_filepath: destination path on the device
        #     :param controller_filepath: source path on the controller
        #     :return: returns nothing 
        #     """

        def transfer_file_from_device(self, device_filepath: str, controller_filepath: str):
            """
            Transfer a file from the device to the controller.

            :param device_filepath: source path on the device
            :param controller_filepath: destination path on the controller
            :return: returns nothing
            """

        def create_directory_on_device(self, directory: str):
            """
            Create a directory on the device.

            :param directory: the target directory to create
            :return: returns nothing
            """

        def delete_all_files_in_directory_on_device(self, directory: str):
            """
            Deletes all the files inside a directory on the device.

            :param directory: target directory in which all files will be deleted
            :return: returns nothing
            """

        def get_screen_capture(self, filepath: str):
            """
            Get a screen shot of the current screen and save it on the controller.

            :param filepath: destination filepath of the image on the controller
            :return: returns nothing
            """

    class VbsSubsystem:
        """
        Class used to command and query the oscilloscope using VBS.
        """

        def vbs_command(self, vbs_cmd: str):
            """
            Send a VBS command to the oscilloscope.

            :param vbs_cmd: the VBS command
            :return: returns nothing
            """

        def vbs_query(self, vbs_cmd: str) -> str:
            """
            Send a VBS query and return the response as a string.

            The 'Return=' part of a VBS query MUST BE OMITTED when using this method.

            :param vbs_cmd: the VBS command
            :return: returns the response as a string
            """

        def vbs_query_raw(self, vbs_cmd: str) -> bytes:
            """
            Send a VBS query and return the response as bytes.

            The 'Return=' part of a VBS query MUST BE OMITTED when using this method.

            :param vbs_cmd: the VBS command
            :return: returns the response as bytes
            """

    class WaveformSubsystem:
        """
        Class used to setup saving and transfering waveforms from the scope to the controller.
        """

        def set_autosave_mode_fill(self):
            """
            Set the autosave mode to fill. Acquisitions begin as soon as it is set.
            """

        def set_autosave_mode_wrap(self):
            """
            Set the autosave mode to wrap. Acquisitions begin as soon as it is set.
            """

        def set_autosave_mode_off(self):
            """
            Set the autosave mode to off. Acquisitions end once the last one is completed.
            """

        def set_autosave_format_ascii(self):
            """
            Set ASCII formatting for saved waveform files.
            """

        def set_autosave_format_binary(self):
            """
            Set binary formatting for saved waveform files.
            """

        Trace: TypeAlias = Literal["C1", "C2", "C3", "C4", "F1", "F2", "F3", "F4", "ALL_DISPLAYED"]
        def set_autosave_trace(self, trace: Trace):
            """
            Select a trace to save data from.

            :param trace: the selected trace
            """

        def set_autosave_path(self, directory: str, title_prefix: str):
            """
            Set the directory and the file title prefix on the device.

            :param directory: directory on the device
            :title_prefix: prefix to the title name
            """

        # def wait_fill_complete(self):
        #     """
        #     Blocks new commands from being sent until the FILL autosave mode is switched to OFF or the
        #     scope cannot save more files to the directory.
        #     """

    setup: SetupSubsystem
    acquisition: AcquisitionSubsystem
    communication: CommunicationSubsystem
    storage: StorageSubsystem
    vbs: VbsSubsystem
    waveform: WaveformSubsystem

    def __init__(self, visa_address: str) -> None:
        """## Connect
        
        Connect to the oscilloscope using a VISA address.

        NOTE: only USBTMC is supported at the moment.
        """

    def command(self, cmd: str):
        """## Command
        
        Send a command to the oscilloscope.
        """

    def query(self, cmd: str) -> str:
        """## Query
        
        Send a query to the oscilloscope and return the response as a string.
        """
    
    def query_raw(self, cmd: str) -> bytes:
        """## Query Raw

        Send a query to the oscilloscope and return the response as bytes.
        """

    def set_timeout(self, milliseconds: int):
        """## Set Timeout
        
        Set the oscilloscope timeout duration using milliseconds.
        """
