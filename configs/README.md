Example configs for reference:
* wideband_pipeline.yml

Wideband processing steps:
* create caracal config with pipeline workers
* run on calibrators with standard flagging and calibration
* inspect data and update config with additional flagging / refined calibration strategy
* re-run with calibration and include application of calibration solutions and standard flagging to target
* inspect target data and update target flagging workers to include additional manual flags
* re-run workers applying calibration solution and flagging to target and include selfcal imaging runs
* imaging of calibrated target dataset 

Refined calibration strategies:
* Using setjy to fill in model column externally before running caracal pipeline

Processing strategy:
* Caracal pipelines function well to flag and calibrate large MS datasets.
  * Flagging and calculating antenna based calibration results for calibrator sources    
Currently, these are CASA processes and can be tracked through the log files
  * Standard flags and relevant flags identified during calibration solution calculation worker
  processes can easily be applied to the target sources
  * Calibration solutions are applied on the fly during the extraction of the target sources from the MS
  * Other flags identified when viewing target data can also easily be applied on the target
* Selfcal and imaging needs to be done by external tools
  * masks ...
  * Imaging and selfcal using wsclean

Benefits using Caracal for calibration and flagging:
* The original MS remains RO, which means that the MS cannot be corrupted, keeping the data safe
* Undoing flags and redoing select workers with caracal is easy
* Optimal approach if you have to rerun processing a couple of times on the large MKAT datasets.

**Important**
RFI flagging for wideband data processing is more aggressive to get a good clean image.
For narrow band, first inspect the impact of the flags, as well as check that your standard flags do
not flag out broad regions that include your line data

-fin-
