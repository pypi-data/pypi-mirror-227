//! # Rust MAUI
//!
//! A pure Rust driver for Teledyne-Lecroy MAUI oscilloscopes.
//!

use pyo3::prelude::*;

use anyhow::Result;
use instrument_ctl::Instrument;
use std::{sync::Arc, time::Duration};

mod subsystems {
    pub mod acquisition;
    pub mod communication;
    pub mod setup;
    pub mod storage;
    pub mod waveform;
    pub mod vbs;
}

mod utils;

use subsystems::{
    acquisition::AcquisitionSubsystem, communication::CommunicationSubsystem,
    setup::SetupSubsystem, storage::StorageSubsystem, vbs::VbsSubsystem,
    waveform::WaveformSubsystem,
};

/// ## MAUI Oscilloscope
///
/// Object through which communication with the oscilloscope is done.
///
#[pyclass]
pub struct MauiOscilloscope {
    client: Arc<Instrument>,
    #[pyo3(get)]
    pub communication: Py<CommunicationSubsystem>,
    #[pyo3(get)]
    pub vbs: Py<VbsSubsystem>,
    #[pyo3(get)]
    pub acquisition: Py<AcquisitionSubsystem>,
    #[pyo3(get)]
    pub setup: Py<SetupSubsystem>,
    #[pyo3(get)]
    pub storage: Py<StorageSubsystem>,
    #[pyo3(get)]
    pub waveform: Py<WaveformSubsystem>,
}

#[pymethods]
impl MauiOscilloscope {
    /// ## Connect
    ///
    /// Connect and initialize the device.
    ///
    #[new]
    #[pyo3(text_signature = "(visa_address: str)")]
    pub fn connect(py: Python, visa_address: &str) -> Result<MauiOscilloscope> {
        // Connect
        let client = Arc::new(Instrument::connect(visa_address)?);

        // Set the COMM HEADERS off
        client.command("CHDR OFF")?;

        // Enable standard events to be reflected in the status byte
        let mask: u8 = 0b1111_1111;
        let cmd = format!("*ESE {}", mask);
        client.command(&cmd)?;

        // Enable internal state changes to be reflected in the status byte
        let mask: u16 = 0b0111_1111_1101_1111;
        let cmd = format!("INE {}", mask);
        client.command(&cmd)?;

        // Setup the subsystems
        let communication = Py::new(py, CommunicationSubsystem::init(&client))?;
        let vbs = Py::new(py, VbsSubsystem::init(&client))?;
        let acquisition = Py::new(py, AcquisitionSubsystem::init(&client))?;
        let setup = Py::new(py, SetupSubsystem::init(&client))?;
        let storage = Py::new(py, StorageSubsystem::init(&client))?;
        let waveform = Py::new(py, WaveformSubsystem::init(&client))?;

        Ok(MauiOscilloscope {
            client,
            communication,
            vbs,
            acquisition,
            setup,
            storage,
            waveform,
        })
    }

    /// ## Set Timeout
    ///
    /// Set a new timeout duration for the oscilloscope connection.
    ///
    pub fn set_timeout(&self, duration_milliseconds: u64) {
        self.client.set_timeout(Duration::from_millis(duration_milliseconds));
    }

    /// ## Command
    ///
    /// Send a command to the oscilloscope.
    ///
    pub fn command(&self, cmd: &str) -> Result<()> {
        self.client.command(cmd)?;
        Ok(())
    }

    /// ## Query
    ///
    /// Send a command to the oscilloscope and return the response as a string.
    ///
    pub fn query(&self, cmd: &str) -> Result<String> {
        let resp = self.client.query(cmd)?;
        Ok(resp)
    }

    /// ## Query Raw
    ///
    /// Send a command to the oscilloscope and return the response as a vector of bytes.
    ///
    pub fn query_raw(&self, cmd: &str) -> Result<Vec<u8>> {
        let resp = self.client.query_raw(cmd)?;
        Ok(resp)
    }
}

#[pymodule]
fn py_maui(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<MauiOscilloscope>()?;
    m.add_class::<AcquisitionSubsystem>()?;
    m.add_class::<CommunicationSubsystem>()?;
    m.add_class::<SetupSubsystem>()?;
    m.add_class::<StorageSubsystem>()?;
    m.add_class::<VbsSubsystem>()?;
    m.add_class::<WaveformSubsystem>()?;
    Ok(())
}