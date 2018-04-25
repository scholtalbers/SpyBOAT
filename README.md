## Small pipeline to Wavelet transform Image Intensity Stacks

### local_scripts - The Fiji UI scripts 

- to be executed at a local machine
- entry point into the pipeline: copies the data/scripts onto /scratch
- creates a slurm script in /g/aulehla/vLab/WaveletMovieBatch

### cluster_scripts - scripts for the computation on the HPC cluster

- slurm template
- python Wavelet analysis template