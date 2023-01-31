Notes on pipeline: Generic pipeline script to run on MS datafiles in bath mode
Only apply standard flags for wideband: flagging edges of the band, as well as satellite bands
No manual flagging is perfomed on individual datasets
No masking or RFI flagging is perfomed on the source data since the threshold evaluation may flag out lines
RFI and mask flagging using the caracal software will cause the bandpass to be displayed incorrectly in plotms when applying baseline averaging, only use antenna, frequency and time averaging

Since the raw data will not be touched, a copy of the datafiles will be made and processed.
Make sure you have enough space for all the files to process

Structure of workdirectory:
mkdir <name>

Move the caracal YAML recipe into the top level of this folder

All raw data files in the "ms-orig" folder, they will be accessed as read-only
mkdir ms-orig
<copy all files here>

Run caracal pipeline in steps for debugging:
- Flagging: caracal -c run-james-caracal.yml -ew flag__calibrators
- Inspect data located in the `msdir` folder 
- Manually inspect data and add worker for manual flagging (example below)
- Calibration: caracal -c run-james-caracal.yml -sw crosscal -ew inspect
- Inspect calibration results using calibration tables located in the `output-H1-james-4k/caltables/` folder 
- Extract and calibrate target: caracal -c run-james-caracal.yml -sw transform__target -ew flag__conttarget
- Selfcal: caracal -c run-james-caracal.yml -sw selfcal -ew selfcal
- Extract line data: caracal -c run-james-caracal.yml -sw transform__linetarget

To run the full pipeline: caracal -c run-james-caracal.yml

Example config for manual flagging:
```
# Flag bad data identified manually
flag__cal_manual:
  enable: true
  label_in: cal
  field: calibrators
  # time and antenna flags from WB processing is carried over
  # freq/ channel based flagging are done independently after inspecting the NB data
  flag_spw:
    enable: true
    chans: '*:0.965290GHz~0.965930GHz,*:1.05161GHz~1.05245GHz,*:1.1026GHz~1.10344GHz,*:1.10887GHz~1.11598GHz,*:1.12768GHz~1.12831GHz,*:1.13583GHz~1.13834GHz,*:1.1421GHz~1.16595GHz,*:1.1862GHz~1.3045GHz,*:1.48964GHz~1.49298GHz,*:1.52057GHz~1.59195GHz,*:1.51827GHz,*:1.62632GHz'
    ensure_valid: false
  flag_time:
    enable: true
    timerange: '2021/07/05/16:17:30~2021/07/05/16:19:30,2021/07/05/16:27:00~2021/07/05/16:27:15'
    ensure_valid: false
  flag_antennas:
    enable: true
    antennas: 'm054'
    ensure_valid: false
```

-fin-
