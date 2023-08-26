//! Acquisition Subsystem Module
//!

use pyo3::prelude::*;

use anyhow::{anyhow, Result};
use instrument_ctl::Instrument;
use std::{sync::Arc, time::Duration};

/// ## Acquisition Subsystem
/// 
/// Object for controlling the acquisition functions of the oscilloscope.
/// 
#[pyclass(subclass)]
pub struct AcquisitionSubsystem {
    client: Arc<Instrument>,
}

impl AcquisitionSubsystem {
    /// ## Init
    /// 
    /// Initialize an Acquisition Subsystem object.
    /// 
    pub fn init(client: &Arc<Instrument>) -> AcquisitionSubsystem {
        AcquisitionSubsystem {
            client: client.clone(),
        }
    }
}

#[pymethods]
impl AcquisitionSubsystem {
    // TRIGGER EXECUTION METHODS
    // ==========


    /// ## Arm Acquisition
    ///
    /// Arms the scope and forces a single acquisition if it is already armed.
    ///
    pub fn arm_acquisition(&self) -> Result<()> {
        self.client.command("ARM;*OPC")?;
        Ok(())
    }

    /// ## Force Trigger
    ///
    /// Causes the device to make one acquisition if it is in an active trigger mode.
    /// If the instrument is in Stop trigger mode, there is no action.
    ///
    pub fn force_trigger(&self) -> Result<()> {
        self.client.command("FRTR;*OPC")?;
        Ok(())
    }

    /// ## Stop
    ///
    /// Immediatly stops the acquisition of a signal. If the trigger mode is AUTO or NORMAL,
    /// this command places the oscilloscope in Stopped trigger mode to prevent further acquisition.
    ///
    pub fn stop(&self) -> Result<()> {
        self.client.command("STOP;*OPC")?;
        Ok(())
    }

    /// ## Wait
    ///
    /// Prevents the device from analyzing new commands until the current acquisition has beem completed.
    ///
    /// The optional `timeout_duration` argument specifies the timeout after which the scope stops
    /// waiting for new acquisitions. If the timeout duration is not given or zero, the scope waits
    /// indefinitely.
    ///
    pub fn wait(&self, duration_milliseconds: Option<u64>) -> Result<()> {
        let cmd = match duration_milliseconds {
            Some(milliseconds) => format!("WAIT {};*OPC", Duration::from_millis(milliseconds).as_secs()),
            None => format!("WAIT;*OPC"),
        };
        self.client.command(&cmd)?;
        Ok(())
    }

    // CLOCKS METHODS
    // ==========

    /// ## Get Sample Clock State
    ///
    /// Returns whether the sample clock is INTERNAL or EXTERNAL.
    ///
    pub fn get_sample_clock_state(&self) -> Result<String> {
        let resp = self.client.query("SAMPLE_CLOCK?")?;
        Ok(resp)
    }

    /// ## Get Reference Clock State
    ///
    /// Returns whether the reference clock is INTERNAL or EXTERNAL.
    ///
    pub fn get_reference_clock_state(&self) -> Result<String> {
        let resp = self.client.query("REFERENCE_CLOCK?")?;
        Ok(resp)
    }

    /// ## Set Internal Sample Clock
    ///
    /// Sets the sample clock to be INTERNAL.
    ///
    pub fn set_internal_sample_clock(&self) -> Result<()> {
        self.client.command("SAMPLE_CLOCK INTERNAL;*OPC")?;
        Ok(())
    }

    /// ## Set External Sample Clock
    ///
    /// Sets the sample clock to be EXTERNAL.
    ///
    pub fn set_external_sample_clock(&self) -> Result<()> {
        self.client.command("SAMPLE_CLOCK EXTERNAL;*OPC")?;
        Ok(())
    }

    /// ## Set Internal Reference Clock
    ///
    /// Sets the reference clock to be INTERNAL.
    ///
    pub fn set_interal_reference_clock(&self) -> Result<()> {
        self.client.command("REFERENCE_CLOCK INTERNAL;*OPC")?;
        Ok(())
    }

    /// ## Set External Reference Clock
    ///
    /// Sets the reference clock to be EXTERNAL.
    ///
    pub fn set_external_reference_clock(&self) -> Result<()> {
        self.client.command("REFERENCE_CLOCK EXTERNAL;*OPC")?;
        Ok(())
    }

    // SIGNAL SETUP
    // ==========

    /// ## Auto Setup
    ///
    /// The AUTO_SETUP command attempts to display the input signal(s) by adjusting the vertical, timebase
    /// and trigger parameters. AUTO_SETUP operates only on the channels whose traces are currently turned
    /// on. If no traces are turned on, AUTO_SETUP operates on all channels.
    ///
    /// If signals are detected on several channels, the lowest numbered channel with a signal determines the
    /// selection of the timebase and trigger source.
    ///
    /// If only one input channel is turned on, the timebase will be adjusted for that channel.
    /// The AUTO_SETUP FIND command adjusts gain and offset only for the specified channel.
    ///
    /// If the FIND keyword is present, gain and offset adjustments are performed only on the specified channel.
    ///
    /// If no <channel> prefix is added, an auto-setup is performed on the channel used on the last ASET FIND
    /// remote command.
    ///
    /// In the absence of the FIND keyword, the normal auto-setup is performed, regardless of the <channel>
    /// prefix.
    ///
    pub fn auto_setup(&self, channel: u8, find: bool) -> Result<()> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = if find {
            format!("C{}:ASET FIND;*OPC", channel)
        } else {
            format!("C{}:ASET;*OPC", channel)
        };

        self.client.command(&cmd)?;

        Ok(())
    }

    /// ## Set Attenuation
    ///
    /// The ATTENUATION command selects the vertical attenuation factor of the probe. Values up to 10000 can
    /// be specified.
    ///
    pub fn set_attenuation(&self, channel: u8, attenuation: u16) -> Result<()> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }
        if !(attenuation >= 1 && attenuation <= 10000) {
            return Err(anyhow!(
                "attenuation factor {} is out of range (1 to 10000)",
                attenuation
            ));
        }

        let cmd = format!("C{}:ATTENUATION {};*OPC", channel, attenuation);
        self.client.command(&cmd)?;

        Ok(())
    }

    /// ## Get Attenuation
    ///
    /// The ATTENUATION? query returns the attenuation factor of the specified channel.
    ///
    pub fn get_attenuation(&self, channel: u8) -> Result<u16> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = format!("C{}:ATTENUATION?", channel);
        let attentuation = self.client.query(&cmd)?.parse::<u16>()?;
        Ok(attentuation)
    }

    /// ## Set Bandwidth Limit
    ///
    /// The BANDWIDTH_LIMIT command enables or disables the bandwidth-limiting low-pass filter on a per-
    /// channel basis. When the <channel> argument is omitted, the BWL command applies to all channels.
    ///
    pub fn set_bandwidth_limit(&self, channel: u8, bandwidth_limit: Option<usize>) -> Result<()> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        // validate bandwidth limit
        let bandwidth_limit: &str = match bandwidth_limit {
            Some(bw) => match bw {
                2_000_000 => "20MHZ",
                200_000_000 => "200MHZ",
                500_000_000 => "500MHZ",
                1_000_000_000 => "1GHZ",
                2_000_000_000 => "2GHZ",
                3_000_000_000 => "3GHZ",
                4_000_000_000 => "4GHZ",
                6_000_000_000 => "6GHZ",
                _ => return Err(anyhow!("{} is not a valid bandwidth limit value", bw)),
            },
            None => "OFF",
        };

        let cmd = format!("BWL C{},{};*OPC", channel, bandwidth_limit);
        self.client.command(&cmd)?;

        Ok(())
    }

    /// ## Get Bandwidth Limit
    ///
    /// The response to the BANDWIDTH_LIMIT? query shows the bandwidth filter setting for each channel.
    ///
    pub fn get_bandwidth_limit(&self, channel: u8) -> Result<Option<usize>> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let resp = self.client.query("BANDWIDTH_LIMIT?;*OPC")?;
        let resp = resp.split(",").collect::<Vec<&str>>();

        let bwl = match channel {
            1 => resp[1],
            2 => resp[3],
            3 => resp[5],
            4 => resp[7],
            _ => panic!("this is not supposed to happen"),
        };

        let bwl: Option<usize> = match bwl {
            "OFF" => None,
            "20MHZ" => Some(2_000_000),
            "200MHZ" => Some(200_000_000),
            "500MHZ" => Some(500_000_000),
            "1GHZ" => Some(1_000_000_000),
            "2GHZ" => Some(2_000_000_000),
            "3GHZ" => Some(3_000_000_000),
            "4GHZ" => Some(4_000_000_000),
            "6GHZ" => Some(6_000_000_000),
            _ => panic!("device returned invalid bandwidth limit value: {}", bwl),
        };

        Ok(bwl)
    }

    /// ## Get Vertical Offset
    ///
    /// The OFFSET? query returns the DC offset value of the specified channel at the probe tip.
    ///
    pub fn get_vertical_offset(&self, channel: u8) -> Result<f32> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = format!("C{}:OFFSET?;*OPC", channel);
        let offset = self.client.query(&cmd)?.parse::<f32>()?;

        Ok(offset)
    }

    /// ## Set Vertical Offset
    ///
    /// The OFFSET command allows adjustment of the vertical offset of the specified input channel at the probe
    /// tip.
    ///
    /// The maximum ranges depend on the fixed sensitivity setting. Refer to the product datasheet at
    /// teledynelecroy.com for maximum offset specifications.
    ///
    /// If an out-of-range value is entered, the oscilloscope is set to the closest possible value and the VAB bit (bit
    /// 2) in the STB register is set.
    ///
    pub fn set_vertical_offset(&self, channel: u8, offset: f32) -> Result<()> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = format!("C{}:OFFSET {}V;*OPC", channel, offset);
        self.client.command(&cmd)?;

        Ok(())
    }

    /// ## Set Time Div
    /// 
    /// Set the timebase value per division. Values will be adjusted
    /// to the nearest value possible on the device.
    /// 
    pub fn set_time_div(&self, time_div: f32) -> Result<()> {
        let cmd = format!("TDIV {};*OPC", time_div);
        self.client.command(&cmd)?;
        Ok(())
    }

    /// ## Get Time Div
    /// 
    /// Get the timebase value per division.
    /// 
    pub fn get_time_div(&self) -> Result<f32> {
        let time_div = self.client.query("TDIV?;*OPC")?.parse::<f32>()?;
        Ok(time_div)
    }

    /// ## Set Vold Div
    /// 
    /// Set the volt value per division for the selected channel. 
    /// Values will be adjusted to the nearest value possible 
    /// on the device.
    /// 
    pub fn set_volt_div(&self, channel: u8, volt_div: f32) -> Result<()> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = format!("C{}:VDIV {};*OPC", channel, volt_div);
        self.client.command(&cmd)?;
        Ok(())
    }

    /// ## Get Volt Div
    /// 
    /// Get the volt value per division.
    /// 
    pub fn get_volt_div(&self, channel: u8) -> Result<f32> {
        if !(channel >= 1 && channel <= 4) {
            return Err(anyhow!("channel {} does not exist", channel));
        }

        let cmd = format!("C{}:VDIV?;*OPC", channel);
        let vdiv = self.client.query(&cmd)?.parse::<f32>()?;
        Ok(vdiv)
    }


    // ACQUISITION MODE METHODS
    // ==========


    // TRIGGER METHODS
    // ==========

    /// ## Set Trigger Mode Auto
    /// 
    /// Set the trigger mode to AUTO.
    /// 
    pub fn set_trigger_mode_auto(&self) -> Result<()> {
        self.client.command("TRMD AUTO;*OPC")?;
        Ok(())
    }

    /// ## Set Trigger Mode Normal
    /// 
    /// Set the trigger mode to NORM.
    /// 
    pub fn set_trigger_mode_normal(&self) -> Result<()> {
        self.client.command("TRMD NORM;*OPC")?;
        Ok(())
    }

    /// ## Set Trigger Mode Single
    /// 
    /// Set the trigger mode to SINGLE.
    /// 
    pub fn set_trigger_mode_single(&self) -> Result<()> {
        self.client.command("TRMD SINGLE;*OPC")?;
        Ok(())
    }

    /// ## Set Trigger Mode Stop
    /// 
    /// Set the trigger mode to STOP.
    /// 
    pub fn set_trigger_mode_stop(&self) -> Result<()> {
        self.client.command("TRMD STOP;*OPC")?;
        Ok(())
    }


}
