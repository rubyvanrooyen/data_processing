Alternative caracal recipes to understand the data processing compared to CASA knowledge

Compare processing mimicing the casa processing strategy with caracal pipeline implementation
Investigate what happens when you add the caracal rfi mask, as well as tricolour flagging

For continuum imaging the rfi flagging options work well, but because there are NaNs in the data, the
plotms averaging over baseline will result in some interesting passband displays.
Rather average over scan than over baseline in order to view the output.

`/scratch/data_processing/test_with_g330`

Pipeline implementation folders:
```
cd casarep
caracal -c casa_mimic_pipelines.yml
```
```
cd rfimask
caracal -c with_rfimask_pipeline.yml
```
```
cd tricolour
caracal -c with_tricolour_pipeline.yml
```
-fin-
